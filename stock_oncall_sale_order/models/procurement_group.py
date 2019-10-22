# (c) AbAKUS IT Solutions
import logging
from odoo import models, fields, api, _
_logger = logging.getLogger(__name__)


class ProcurementGroup(models.Model):
    _inherit = ['procurement.group']

    @api.model
    def run(self, product_id, product_qty, product_uom, location_id, name, origin, values):
        route = values['route_ids']
        if not route or not route.is_oncall_route:
            return super(ProcurementGroup, self).run(product_id, product_qty, product_uom, location_id, name, origin, values)
        else:
            return True
