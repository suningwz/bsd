from odoo import models, fields, api, _
import logging

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _action_launch_stock_rule(self):
        list = [not line.route_id or (line.route_id and not line.route_id.is_oncall_route) for line in self]
        _logger.debug("\n\nlist: %s\n" % list)
        if all(list):
            return super(SaleOrderLine, self)._action_launch_stock_rule()
        return True