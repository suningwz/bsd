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
                    # Get to know where the product is
                    current_product_location = False
                    quant_ids = self.env['stock.quant'].search([('product_id', '=', line.product_id.id), ('location_id.usage', '=', 'internal'), ('quantity', '>', 0)])
                    quant_ids = quant_ids.sorted(key=lambda r: r.quantity, reverse=True)
                    if len(quant_ids) == 0:
                        _logger.debug("Error : no quant found")
                    for quant in quant_ids:
                        # We have enough quantity
                        if quant.quantity >= line.product_uom_qty:
                            _logger.debug('\n FOUND %s units in %s', quant.location_id, quant.quantity)
                            current_product_location = quant.location_id
                            break

                    # Duplicate the current location where the product is stored
                    if current_product_location == False:
                        _logger.debug("Error : no location found")
                    else:
                        new_location = False
                        # Check if this location does not already exists
                        loc_id = self.env['stock.location'].search([('location_id', '=', 'order.partner_id.oncall_location_id.id'), ('oncall_origin_location_id', '=', current_product_location.id)])
                        if len(loc_id) > 0:
                            if len(loc_id) > 1:
                                loc_id = loc_id[0]
                            new_location = loc_id

                        if new_location == False:
                            new_location = self.env['stock.location'].create({
                                'name': current_product_location.name,
                                'partner_id': order.partner_id.id,
                                'usage': 'internal',
                                'location_id': order.partner_id.oncall_location_id.id,
                                'posx': current_product_location.posx,
                                'posy': current_product_location.posy,
                                'posz': current_product_location.posz,
                                'oncall_origin_location_id': current_product_location.id,
                            })

                        # create a move
                        move_id = self.env['stock.move'].create({
                            'product_id': line.product_id.id,
                            'location_id': current_product_location.id,
                            'location_dest_id': new_location.id,
                            'name': order.name + " -> On-Call - " + line.product_id.name,
                            'product_uom_qty': line.product_uom_qty,
                            'product_uom': line.product_uom.id,
                            'procure_method': 'make_to_stock',
                            'picking_type_id': self.env.ref('stock.picking_type_internal').id,
                        })
                        _logger.debug("\n\n MOVE : %s", move_id)
                        move_id._assign_picking()
                        move_id._action_confirm()


                            # create auto rules for that move
                            # Create the auto push rule



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
                        })
                                push_rule_id = self.env['stock.rule'].create({
                                'name': current_product_location.name + ' => Customer',
                                'action': 'push',
                                'picking_type_id': self.env.ref('stock.picking_type_internal').id,
                                'location_src_id': current_product_location.id,
                                'location_id': new_location.id,
                                'route_id': line.route_id.id,
                                'auto': 'transparent',
                            })"""
