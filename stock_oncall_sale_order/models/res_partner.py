from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class Partner(models.Model):
    _inherit = 'res.partner'

    oncall_location_id = fields.Many2one('stock.location', string="Oncall Main Stock Location")
    oncall_order_ids = fields.One2many('stock.oncall.order', 'partner_id', string="On-Call Orders")
    oncall_product_count = fields.Integer(compute='_compute_oncall_product_count', string='# Products On-Call')

    @api.one
    def _compute_oncall_product_count(self):
        total = 0
        for order in self.oncall_order_ids:
            total += order.qty_to_deliver
        self.oncall_product_count = total
