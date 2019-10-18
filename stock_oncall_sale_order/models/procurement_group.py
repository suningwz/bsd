# (c) AbAKUS IT Solutions
import logging
from odoo import models, fields, api, _
_logger = logging.getLogger(__name__)


class ProcurementGroup(models.Model):
    _inherit = ['procurement.group']

    @api.model
    def run(self, product_id, product_qty, product_uom, location_id, name, origin, values):
        route = values['route_ids']
        if not route or route.id != self.env.ref('stock_oncall_sale_order.route_warehouse0_oncall').id:
            return super(ProcurementGroup, self).run(product_id, product_qty, product_uom, location_id, name, origin, values)
        else:
            return True
