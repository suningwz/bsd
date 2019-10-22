from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    oncall_stock_ids = fields.One2many('stock.oncall.stock', 'sale_order_id', string="On-Call Stock")
    oncall_product_count = fields.Integer(compute='_compute_oncall_product_count', string='# Products On-Call')

    @api.one
    def _compute_oncall_product_count(self):
        total = 0
        for order in self.oncall_stock_ids:
            total += order.qty_to_deliver
        self.oncall_product_count = total

    @api.multi
    def _action_confirm(self):
        for order in self:
            # Check if on-call route is used
            for line in order.order_line:
                if line.route_id.is_oncall_route:
                    # Create On-Call Stock
                    oncall_stock_id = self.env['stock.oncall.stock'].create({
                        'partner_id': order.partner_id.id,
                        'sale_order_line_id': line.id,
                        'uom_id': line.product_uom,
                        'qty_to_deliver': line.product_uom_qty,
                        'qty_ordered': line.product_uom_qty,
                        'qty_to_deliver_now': 0,
                        'qty_done': 0,
                    })

        super(SaleOrder, self)._action_confirm()

    def view_pickings(self):
        return {
            'name': _("Stock Picking"),
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'views': [(self.env.ref('stock.vpicktree').id, 'tree'), (False, 'form')],
            'view_mode': "tree,form",
            'view_type': "form",
            'search_view_id': self.env.ref('stock.view_picking_internal_search').id,
            'domain': [('id', 'in', self.stock_picking_ids.ids)],
            'context': {}
        }
