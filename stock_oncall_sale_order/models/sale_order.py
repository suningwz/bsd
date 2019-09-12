from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    oncall_order_ids = fields.One2many('stock.oncall.order', 'sale_order_id', string="On-Call Orders")
    oncall_product_count = fields.Integer(compute='_compute_oncall_product_count', string='# Products On-Call')

    @api.one
    def _compute_oncall_product_count(self):
        total = 0
        for order in self.oncall_order_ids:
            total += order.qty_to_deliver
        self.oncall_product_count = total

    @api.multi
    def _action_confirm(self):
        for order in self:
            # Check if on-call route is used and if customer has a specific stock location, if not, create it
            for line in order.order_line:
                if line.route_id and line.route_id.create_specific_location_for_customer:
                    if not order.partner_id.oncall_location_id:
                        # Create the Oncall Stock Location
                        order.partner_id.oncall_location_id = self.env['stock.location'].create({
                            'name': 'On-Call: ' + (order.partner_id.ref if order.partner_id.ref else order.partner_id.name),
                            'location_id': self.env.ref('stock.stock_location_locations_virtual').id,
                            'usage': 'internal',
                            'partner_id': order.partner_id.id
                        })
                    # Create On-Call Orders
                    oncall_order_id = self.env['stock.oncall.order'].create({
                        'partner_id': order.partner_id.id,
                        'sale_order_line_id': line.id,
                        'qty_to_deliver': line.product_uom_qty,
                    })
                    # Get to know
                    # Duplicate the current location where the product is stored

        super(SaleOrder, self)._action_confirm()


        """
                        # Create the pull rule
                        pull_rule_id = self.env['stock.rule'].create({
                            'name': self.env.ref('stock.stock_location_stock').name + ' => ' + customer_location_id.name,
                            'action': 'pull',
                            'picking_type_id': self.env.ref('stock.picking_type_internal').id,
                            'location_src_id': self.env.ref('stock.stock_location_stock').id,
                            'location_id': customer_location_id.id,
                            'procure_method': 'make_to_stock',
                            'route_id': line.route_id.id,
                        })

                        # Create the push rule
                        push_rule_id = self.env['stock.rule'].create({
                            'name': customer_location_id.name + ' => Customer',
                            'action': 'push',
                            'picking_type_id': self.env.ref('stock.picking_type_out').id,
                            'location_src_id': customer_location_id.id,
                            'location_id': self.env.ref('stock.stock_location_customers').id,
                            'procure_method': 'make_to_stock',
                            'route_id': line.route_id.id,
                        })"""
