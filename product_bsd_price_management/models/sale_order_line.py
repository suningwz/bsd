# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import logging

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def compute_default(self):
        return self.env['ir.model.fields'].search([('model_id', '=', self.env.ref('product_bsd_price_management.model_product_sale_price_line').id), ('name', '=', "price_uv")])

    def compute_domain(self):
        return [('model_id', '=', self.env.ref('product_bsd_price_management.model_product_sale_price_line').id), ('name', 'like', 'price'), ('name', '!=', "unit_price")]

    price_line_ids = fields.One2many('product.sale.price.line', 'product_id',
                                     related="product_id.product_tmpl_id.sale_price_line_ids")
    sell_price_selector = fields.Many2one('ir.model.fields', string="Sell Price Selector",
                                          domain=compute_domain, default=compute_default)

    @api.onchange('sell_price_selector', 'product_id')
    def sell_price_selector_change(self):
        if self.sell_price_selector and self.product_id and self.product_id.product_tmpl_id and self.product_id.product_tmpl_id.sale_price_line_ids:
            self.price_unit = self.product_id.product_tmpl_id.sale_price_line_ids[0][self.sell_price_selector.name]
