# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import logging
_logger = logging.getLogger(__name__)


class ProductPurchasePriceLine(models.Model):
    _name = "product.sale.price.line"
