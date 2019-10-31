from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class Partner(models.Model):
    _inherit = 'res.partner'

    oncall_stock_ids = fields.One2many('stock.oncall.stock', 'partner_id', string="On-Call Stock")
    oncall_product_count = fields.Integer(compute='_compute_oncall_product_count', string='# Products On-Call')

    def _compute_oncall_product_count(self):
        for partner in self:
            total = 0
            for stock in partner.oncall_stock_ids:
                total += stock.qty_to_deliver
            partner.oncall_product_count = total
