# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import logging
_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit_id = 'product.template'

    sale_price_line_ids = fields.One2many('product.sale.price.line', 'product_id', string="BSD Sale Price")
