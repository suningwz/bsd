# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import logging
_logger = logging.getLogger(__name__)


class SaleOrderMethod(models.Model):
    _name = 'sale.order.method'

    name = fields.Char("Method Name")
    active = fields.Boolean(default=True)
