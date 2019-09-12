from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class StockOnCallOrder(models.Model):
    _name = 'stock.oncall.order'

    partner_id = fields.Many2one('res.partner', string="Partner")
    sale_order_line_id = fields.Many2one('sale.order.line', string="Sale Order Line")
    sale_order_id = fields.Many2one('sale.order', related='sale_order_line_id.order_id')
    product_id = fields.Many2one('product.product', related='sale_order_line_id.product_id', string="Product")
    uom_id = fields.Many2one('uom.uom', related='sale_order_line_id.product_uom')
    qty_to_deliver = fields.Integer(string="Qty to deliver")


    def name_get(self):
        res = []
        for order in self:
            res.append((order.id, '{0} - {1} - {2} {3}'.format(order.sale_order_id.name, order.partner_id.name, order.qty_to_deliver, order.uom_id.name)))
        return res
