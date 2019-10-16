# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions, _
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        return {
            'domain': {
                'partner_invoice_id': [] if not self.partner_id else [('parent_id', '=', self.partner_id.id), ('type', '=', 'invoice')],
                'partner_shipping_id': [] if not self.partner_id else [('parent_id', '=', self.partner_id.id), ('type', '=', 'delivery')]
            }
        }
