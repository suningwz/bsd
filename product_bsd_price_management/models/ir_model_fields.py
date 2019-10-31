# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import logging

_logger = logging.getLogger(__name__)


class IrModelFields(models.Model):
    _inherit = 'ir.model.fields'

    def name_get(self):
        result = []
        for field in self:
            if field.model_id.id == self.env.ref('product_bsd_price_management.model_product_sale_price_line').id:
                result.append((field.id, field.field_description))
        return result if result else super(IrModelFields, self).name_get()

