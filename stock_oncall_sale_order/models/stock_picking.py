from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    oncall_stock_ids = fields.Many2many('stock.oncall.stock', string="OnCall Stocks")
    oncall_stock_count = fields.Integer(compute="_compute_oncall_stock_count", string="Products On-Call")
    is_from_oncall = fields.Boolean(compute="_compute_is_from_oncall", string="Is From OnCall", store=True)

    @api.depends('oncall_stock_ids')
    def _compute_is_from_oncall(self):
        for picking in self:
            picking.is_from_oncall = bool(picking.oncall_stock_ids)

    @api.depends('oncall_stock_ids')
    def _compute_oncall_stock_count(self):
        if self.oncall_stock_ids:
            self.oncall_stock_count = len(self.oncall_stock_ids)

    # TODO : create a method to see all oncall stocks for one picking
    def view_oncalls(self):
        action = self.env.ref('stock_oncall_sale_order.sale_order_oncall_stock').read()[0]
        action['domain'] = [('id', 'in', self.oncall_stock_ids.ids)]
        return action
