# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import logging
_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sale_price_line_ids = fields.One2many('product.sale.price.line', 'product_id', string="BSD Sale Price")
    list_price = fields.Float(compute="_compute_list_price")


    @api.depends('sale_price_line_ids')
    def _compute_list_price(self):
        for template in self:
            if template.sale_price_line_ids:
                template.list_price = template.sale_price_line_ids[0].price_uv
            else:
                template.list_price = 0.0