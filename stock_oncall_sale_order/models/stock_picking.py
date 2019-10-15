from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    oncall_stock_ids = fields.Many2many('stock.oncall.stock', string="OnCall Stocks")

    # TODO : create a method to see all oncall stocks for one picking
