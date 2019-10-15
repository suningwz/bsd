from odoo import models, fields, api, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class StockOnCallStock(models.Model):
    _name = 'stock.oncall.stock'

    partner_id = fields.Many2one('res.partner', string="Partner")
    sale_order_line_id = fields.Many2one('sale.order.line', string="Sale Order Line")
    sale_order_id = fields.Many2one('sale.order', related='sale_order_line_id.order_id')
    product_id = fields.Many2one('product.product', related='sale_order_line_id.product_id', string="Product")
    product_tmpl_id = fields.Many2one('product.template', related='product_id.product_tmpl_id', string="Product Template")
    uom_id = fields.Many2one('uom.uom', related='sale_order_line_id.product_uom')
    qty_ordered = fields.Float('Qty Ordered', digits=dp.get_precision('Product Unit of Measure'))
    qty_available = fields.Float('Qty Available', digits=dp.get_precision('Product Unit of Measure'), compute='_compute_qty_available')
    qty_to_deliver = fields.Float('Qty to deliver', digits=dp.get_precision('Product Unit of Measure'))
    qty_to_deliver_now = fields.Float('Qty to deliver now', digits=dp.get_precision('Product Unit of Measure'))
    qty_done = fields.Float('Qty done', digits=dp.get_precision('Product Unit of Measure'))
    stock_picking_ids = fields.Many2many('stock.picking', string="Stock Pickings")

    def _compute_qty_available(self):
        for stock in self:
            stock.qty_available = stock.product_tmpl_id.qty_available

    def name_get(self):
        res = []
        for stock in self:
            res.append((stock.id, '{0} - {1} - {2} {3}'.format(stock.sale_order_id.name, stock.partner_id.name, stock.qty_to_deliver, stock.uom_id.name)))
        return res

    def deliver_products(self):
        # We will check if all selected onCall stock are for the same partner, if not, trigger an error
        if not all(oncall.partner_id == self[0].partner_id for oncall in self):
            raise UserError(_('Multiple partners in the selected lines, please select only one partner by batch.'))

        # Check Data
        transfer_something = False
        for oncall in self:
            # If nothing selected, skip to the next
            if oncall.qty_ordered == 0:
                continue
            if oncall.qty_to_deliver_now == 0:
                continue
            # If not enough qty available, only deliver what we have
            if oncall.qty_to_deliver_now > oncall.qty_available:
                oncall.qty_to_deliver_now = oncall.qty_available
            # If qty selected is greater that the total planned to deliver, only deliver the planned qty
            if oncall.qty_to_deliver_now > oncall.qty_to_deliver:
                _logger.debug("%s | Too much qty to order now related to what you have to deliver in all", oncall.id)
                oncall.qty_to_deliver_now = oncall.qty_to_deliver
            transfer_something = True

        if not transfer_something:
            raise UserError(_('Nothing to transfer as nothing is set.'))

        picking_id = self.env['stock.picking'].create({
            'company_id': self.env.user.company_id.id,
            'partner_id': self[0].partner_id.id,
            'picking_type_id': self.env.ref('stock.picking_type_out').id,
            'location_id': self.env.ref('stock.picking_type_out').default_location_src_id.id,
            'location_dest_id': self[0].partner_id.property_stock_customer.id,
        })
        origin_ref = ''

        # Compute origin ref and create moves
        for oncall in self:
            origin_ref += oncall.sale_order_id.name + ", "

            # Create stock move
            vals = {
                'name': oncall.product_id.name or '',
                'product_id': oncall.product_id.id,
                'product_uom': oncall.uom_id.id,
                'product_uom_qty': oncall.qty_to_deliver_now,
                'date': oncall.create_date,
                'date_expected': oncall.create_date,
                'location_id': picking_id.location_id.id,
                'location_dest_id': picking_id.location_dest_id.id,
                'picking_id': picking_id.id,
                'partner_id': picking_id.partner_id.id,
                'state': 'draft',
                'company_id': picking_id.company_id.id,
                'picking_type_id': picking_id.picking_type_id.id,
                'origin': _('OnCall: ') + oncall.sale_order_id.name,
                'route_ids': picking_id.picking_type_id.warehouse_id and [
                    (6, 0, [x.id for x in picking_id.picking_type_id.warehouse_id.route_ids])] or [],
                'warehouse_id': picking_id.picking_type_id.warehouse_id.id
            }
            move = self.env['stock.move'].create(vals)
            move._action_assign()

            oncall.stock_picking_ids = [(4, picking_id)]

            oncall.qty_done = oncall.qty_done + oncall.qty_to_deliver_now
            oncall.qty_to_deliver = oncall.qty_ordered - oncall.qty_done
            oncall.qty_to_deliver_now = 0

        # TODO manage the OUT in 3 steps
        picking_id.write({
            'origin': origin_ref,
        })
        picking_id.action_confirm()
        picking_id._action_assign()


        """result = {
            'name': _('View Picking List'),
            'type': 'ir.actions.act_window',
            'views': [[self.env.ref('stock.view_picking_form').id, 'form']],
            'target': 'current',
            'context': {},
            'res_model': 'stock.oncall.stock',
            'res_id': picking_id.id,
            }
        return result"""

    # TODO : create a method to see all pickings for one oncall
