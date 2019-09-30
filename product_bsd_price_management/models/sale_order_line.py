# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import logging

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_uom', 'product_uom_qty')
    def product_uom_change(self):
        # TODO: Dictionnary between UoM name and price field
        super(SaleOrderLine, self).product_uom_change()
        if self.product_uom and self.product_id and self.product_id.product_tmpl_id and self.product_id.product_tmpl_id.sale_price_line_ids and self.product_uom.sale_price_field:
            if self.order_id.partner_id and not self.order_id.partner_id.is_indu and self.product_uom.sale_price_field.name == 'price_indu':
                self.price_unit = self.product_id.product_tmpl_id.sale_price_line_ids[0][self.env.ref('product_bsd_price_management.uom_uv').sale_price_field.name]
            else:
                self.price_unit = self.product_id.product_tmpl_id.sale_price_line_ids[0][self.product_uom.sale_price_field.name]
