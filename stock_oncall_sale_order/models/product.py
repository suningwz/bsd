from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    oncall_stock_ids = fields.One2many('stock.oncall.stock', 'product_tmpl_id', string="On-Call Stock")
    oncall_product_count = fields.Integer(compute='_compute_oncall_product_count', string='# Products On-Call')

    @api.one
    def _compute_oncall_product_count(self):
        total = 0
        for stock in self.oncall_stock_ids:
            total += stock.qty_to_deliver
        self.oncall_product_count = total

