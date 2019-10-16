# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import logging
_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    method_id = fields.Many2one('sale.order.method', string="Sale Method", help="The sale method define how the sale has been done (on the road, by phone, ...)")
