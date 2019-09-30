# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import logging

_logger = logging.getLogger(__name__)


class UomUom(models.Model):
    _inherit = 'uom.uom'

    @api.model
    def _get_domain_sale_price_field(self):
        return [('model_id', '=', self.env.ref('product_bsd_price_management.model_product_sale_price_line').id)]

    sale_price_field = fields.Many2one('ir.model.fields', string="Sale Price Field", domain=_get_domain_sale_price_field)
