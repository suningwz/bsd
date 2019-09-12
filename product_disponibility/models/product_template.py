# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import datetime
from datetime import timedelta
from odoo.tools.float_utils import float_round

class ProductTemplate( models.Model ):
    _inherit = "product.template"

    date_disponibility = fields.Date( 
        string    = _('Date mise à disposition'),
        translate = True,
        default   = "2050-01-01",
        track_visibility = "onchange" 
    )

    @api.multi
    def update_order_lines( self ):
        SaleOrderLine = self.env[ 'sale.order.line' ]
        order_line_ids = SaleOrderLine.search( 
            [ ( 'product_id', '=', self.id ) ] )

        if not order_line_ids:
            raise ValidationError( _( 'Ce produit n\'a aucune ligne de vente associée.' ) )


        saleOrders = set()

        for line in order_line_ids:
            line.date_disponibility = self.date_disponibility
            saleOrders.add( line.order_id )
        
        for order in saleOrders:
            order.update_disponibility_date()

    @api.multi
    def action_view_sales( self ):
        action = self.env.ref('product_disponibility.update_mad_date_action').read()[0]
        action['domain'] = [('product_tmpl_id', 'in', self.ids)]
        action['context'] = {
            'search_default_last_year': 1,
            'search_default_team_id': 1
        }
        return action

class ProductProduct( models.Model ):
    _inherit = "product.product"

    sales_count = fields.Float(
        compute = "_compute_sales_count",
        string  = "Vendu"
    )

    @api.multi
    def _compute_sales_count( self ):
        r = {}
        if not self.user_has_groups('sales_team.group_sale_salesman'):
            return r

        date_from = fields.Datetime.to_string(fields.datetime.now() - timedelta(days=365))
        domain = [
            ('state', 'in', ['draft', 'sent', 'sale', 'done']),
            ('product_id', 'in', self.ids),
            ('date', '>', date_from)
        ]
        for group in self.env['sale.report'].read_group(domain, ['product_id', 'product_uom_qty'], ['product_id']):
            r[group['product_id'][0]] = group['product_uom_qty']
        for product in self:
            product.sales_count = float_round(r.get(product.id, 0), precision_rounding=product.uom_id.rounding)
        return r

    @api.multi
    def update_order_lines( self ):
        return self.product_tmpl_id.update_order_lines()

    @api.multi
    def action_view_sales(self):
        action = self.env.ref('product_disponibility.update_mad_date_action').read()[0]
        action['domain'] = [('product_id', 'in', self.ids)]
        action['context'] = {
            'search_default_last_year': 1,
            'search_default_team_id': 1,
        }
        return action
