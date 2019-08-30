from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class Partner(models.Model):
    _inherit = 'res.partner'

    oncall_product_count = fields.Integer(compute='_compute_oncall_product_count', string='# Products On-Call')
    use_oncall = fields.Boolean(compute='_compute_oncall_user')

    @api.one
    def _compute_oncall_user(self):
        self.use_oncall = False
        if self.property_stock_customer != self.env.ref('stock.stock_location_customers'):
            self.use_oncall = True

    @api.one
    def _compute_oncall_product_count(self):
        quant_ids = self.env['stock.quant'].search([('location_id', '=', self.property_stock_customer.id)])
        total = 0
        for quant in quant_ids:
            total += quant.quantity
        self.oncall_product_count = total
