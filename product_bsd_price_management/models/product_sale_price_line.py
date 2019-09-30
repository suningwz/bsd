# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import logging
_logger = logging.getLogger(__name__)


class ProductSalePriceLine(models.Model):
    _name = "product.sale.price.line"
    _description = "line containing all prices for one product"

    product_id = fields.Many2one('product.template', string="Product")

    unit_price = fields.Float("Unit Price", compute="_compute_unit_price")
    price_uv = fields.Float("Price U.V.")
    qty_uv = fields.Integer("Qty U.V.", default=1)
    price_box = fields.Float("Price Box")
    qty_box = fields.Integer("Qty Box", default=1)
    price_pallet = fields.Float("Price Pallet")
    qty_pallet = fields.Integer("Qty Pallet", default=1)
    price_indu = fields.Float("Price Indu")
    qty_for_discount = fields.Integer("Qty Discount", default=1)
    price_discount = fields.Float("Price Discount")

    @api.multi
    @api.depends('price_uv', 'qty_uv')
    def _compute_unit_price(self):
        for line in self:
            if line.qty_uv > 0:
                line.unit_price = line.price_uv / line.qty_uv
            else:
                raise exceptions.ValidationError(_("Qty must be greater than 0"))

