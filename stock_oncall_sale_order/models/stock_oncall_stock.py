from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
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
    qty_to_deliver = fields.Float('Qty to deliver', digits=dp.get_precision('Product Unit of Measure'))
    qty_to_deliver_now = fields.Float('Qty to deliver now', digits=dp.get_precision('Product Unit of Measure'))
    qty_done = fields.Float('Qty done', digits=dp.get_precision('Product Unit of Measure'))

    # TODO : ajouter un champ avec la quantité en stock chez BSD

    def name_get(self):
        res = []
        for stock in self:
            res.append((stock.id, '{0} - {1} - {2} {3}'.format(stock.sale_order_id.name, stock.partner_id.name, stock.qty_to_deliver, stock.uom_id.name)))
        return res
