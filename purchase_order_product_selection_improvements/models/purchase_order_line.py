# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import logging

_logger = logging.getLogger(__name__)


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    product_image = fields.Image("Image", related='product_id.image_1920')
    product_image_small = fields.Image("Image", related='product_id.image_128')
