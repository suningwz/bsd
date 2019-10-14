# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import logging
_logger = logging.getLogger(__name__)


class ProductSalePriceLine(models.Model):
    _name = "product.sale.price.line"
    _description = "line containing all prices for one product"
    _order = 'sequence desc'

    product_id = fields.Many2one('product.template', string="Product")

    sequence = fields.Integer()
    unit_price = fields.Float("Unit Price", compute="_compute_unit_price", help="The price of the Sell Unit / the quantity of item in a Sell Unit")
    price_uv = fields.Float("Price U.V.", help="The price of one Sell Unit")
    qty_uv = fields.Integer("Qty U.V.", default=1, help="The quantity of item in one Sell Unit.")
    price_box = fields.Float("Price Box", help="The price used for one sell unit if the client buy a complete box.")
    qty_box = fields.Integer("Qty Box", default=1, help="The quantity of sell unit contained in a box.")
    qty_pallet = fields.Integer("Qty Pallet", default=1, help="The number of sell unit that can be stored in one pallet.")
    price_indu = fields.Float("Price Indu")


    @api.depends('price_uv', 'qty_uv')
    def _compute_unit_price(self):
        for line in self:
            if line.qty_uv > 0:
                line.unit_price = line.price_uv / line.qty_uv
            else:
                raise exceptions.ValidationError(_("Qty must be greater than 0"))

