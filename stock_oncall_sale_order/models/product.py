from odoo import models, fields, api
from odoo.addons import decimal_precision as dp
import logging

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    oncall_stock_ids = fields.One2many('stock.oncall.stock', 'product_tmpl_id', string="On-Call Stock")
    oncall_product_count = fields.Integer(compute='_compute_oncall_product_count', string='# Products On-Call')
    qty_owned_available = fields.Float('Owned Qty On Hand', compute='_compute_quantities', digits=dp.get_precision('Product Unit of Measure'))

    @api.one
    def _compute_oncall_product_count(self):
        total = 0
        for stock in self.oncall_stock_ids:
            total += stock.qty_to_deliver
        self.oncall_product_count = total

    def _compute_quantities(self):
        res = self._compute_quantities_dict()
        for template in self:
            template.qty_available = res[template.id]['qty_available']
            template.qty_owned_available = res[template.id]['qty_available'] - template.oncall_product_count
            template.virtual_available = res[template.id]['virtual_available']
            template.incoming_qty = res[template.id]['incoming_qty']
            template.outgoing_qty = res[template.id]['outgoing_qty']

    def _compute_quantities_dict(self):
        res = super(ProductTemplate, self)._compute_quantities_dict()
        for product in self:
            res[product.id]['qty_owned_available'] = product.qty_owned_available
        return res


class ProductProduct(models.Model):
    _inherit = 'product.product'

    oncall_stock_ids = fields.One2many('stock.oncall.stock', 'product_id', string="On-Call Stock")
    oncall_product_count = fields.Integer(compute='_compute_oncall_product_count', string='# Products On-Call')
    qty_owned_available = fields.Float('Owned Qty On Hand', compute='_compute_quantities', digits=dp.get_precision('Product Unit of Measure'))
    owned_stock_value = fields.Float('Owned Value', compute='_compute_owned_valuation')

    @api.one
    @api.depends('qty_owned_available', 'standard_price')
    def _compute_owned_valuation(self):
        self.owned_stock_value = self.qty_owned_available * self.standard_price

    @api.one
    def _compute_oncall_product_count(self):
        total = 0
        for stock in self.oncall_stock_ids:
            total += stock.qty_to_deliver
        self.oncall_product_count = total

    # Redefine this method as we will decrease the available quantity by the quantity in "OnCall stock"
    @api.depends('stock_move_ids.product_qty', 'stock_move_ids.state', 'oncall_stock_ids')
    def _compute_quantities(self):
        res = self._compute_quantities_dict(self._context.get('lot_id'), self._context.get('owner_id'), self._context.get('package_id'), self._context.get('from_date'), self._context.get('to_date'))
        for product in self:
            product.qty_available = res[product.id]['qty_available']
            product.qty_owned_available = res[product.id]['qty_available'] - product.oncall_product_count
            product.incoming_qty = res[product.id]['incoming_qty']
            product.outgoing_qty = res[product.id]['outgoing_qty']
            product.virtual_available = res[product.id]['virtual_available']

    def _compute_quantities_dict(self, lot_id, owner_id, package_id, from_date=False, to_date=False):
        res = super(ProductProduct, self)._compute_quantities_dict(lot_id, owner_id, package_id, from_date, to_date)
        for product in self:
            res[product.id]['qty_owned_available'] = product.qty_owned_available
        return res
