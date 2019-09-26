from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class StockLocation(models.Model):
    _inherit = 'stock.location'

    oncall_origin_location_id = fields.Many2one('stock.location', string="On-Call origin location")
