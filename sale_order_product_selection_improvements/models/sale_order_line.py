# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import logging

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _get_categ_domain(self):
        return [('parent_id.name', '=', "BSD")]

    categ_id = fields.Many2one('product.category', string="Category", domain=_get_categ_domain)
    qty_available = fields.Float("Quantity Available", related='product_id.product_tmpl_id.qty_available')
    product_image = fields.Image("Image", related='product_id.image_1920')
    product_image_small = fields.Image("Image", related='product_id.image_128')

    @api.onchange('categ_id')
    def _onchange_categ_id(self):
        return {
            'domain': {
                'product_id': [('categ_id', 'child_of', self.categ_id.id)] if self.categ_id else []
            }
        }
