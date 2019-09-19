from odoo import models, fields, api
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
                # Create On-Call Stock
                oncall_stock_id = self.env['stock.oncall.stock'].create({
                    'partner_id': order.partner_id.id,
                    'sale_order_line_id': line.id,
                    'qty_to_deliver': line.product_uom_qty,
                })

        super(SaleOrder, self)._action_confirm()
