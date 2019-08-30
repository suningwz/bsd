from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def _action_confirm(self):
        for order in self:
            # Check if on-call route is used and if customer has a specific stock location, if not, create it
            for line in order.order_line:
                if line.route_id and line.route_id.create_specific_location_for_customer:
                    if order.partner_id.property_stock_customer == self.env.ref('stock.stock_location_customers'):
                        # Create the location
                        customer_location_id = self.env['stock.location'].create({
                            'name': 'On-Call: ' + (order.partner_id.ref if order.partner_id.ref else order.partner_id.name),
                            'location_id': self.env.ref('stock.stock_location_locations_virtual').id,
                            'usage': 'internal',
                            'partner_id': order.partner_id.id
                        })
                        order.partner_id.property_stock_customer = customer_location_id

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
                        })

        super(SaleOrder, self)._action_confirm()

