# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import logging

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _get_categ_domain(self):
        return [('parent_id', '=', self.env.ref('sale_order_partner_selection_improvements.bsd_main_category').id)]

    categ_id = fields.Many2one('product.category', string="Category", domain=_get_categ_domain)
    qty_available = fields.Float("Quantity Available", related='product_id.product_tmpl_id.qty_available')

    @api.onchange('categ_id')
    def _onchange_categ_id(self):
        return {
            'domain': {
                'product_id': [('categ_id', '=', self.categ_id.id)] if self.categ_id else []
            }
        }
