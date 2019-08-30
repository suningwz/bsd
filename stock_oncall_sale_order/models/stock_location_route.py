from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class StockLocationRoute(models.Model):
    _inherit = 'stock.location.route'

    create_specific_location_for_customer = fields.Boolean(string="Create a specific stock location for customer when used in a Sales Order Line", default=False)
