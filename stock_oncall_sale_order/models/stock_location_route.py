from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class StockLocationRoute(models.Model):
    _inherit = 'stock.location.route'

    is_oncall_route = fields.Boolean(string="Is Oncall Route", default=False)
