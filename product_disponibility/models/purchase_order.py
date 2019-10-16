# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import datetime
from datetime import timedelta
from odoo.tools.float_utils import float_round

class PurchaseOrder( models.Model ) :
    _inherit = "purchase.order"

    reception_date = fields.Date( 
        string     = _( "Date de Réception Estimée" ),
        translate  = True,
        default    = lambda self: self._get_default_r_date(),
        track_visibility = "onchange" 
    )

    date_disponibility = fields.Date( 
        string     = _( "Date de Mise à Disposition Estimée" ),
        translate  = True,
        default    = lambda self: self._get_default_d_date(),
        track_visibility = "onchange" 
    )

    sales_count = fields.Float(
        compute = "_compute_sales_count",
        string  = "Vendu"
    )

    uom_name = fields.Char(
        related = "product_id.uom_name",
        string  = "UOM"
    )

    product_id = fields.Many2one( 
        "product.product", 
        related = "order_line.product_id",
        string  = "Product"
    )

    def _compute_sales_count(self):
        product_ids = set()
        r = {}
        if not self.user_has_groups('sales_team.group_sale_salesman'):
            return r

        for line in self.order_line:
            product_ids.add( line.product_id.id )

        product_ids = list( product_ids )

        date_from = fields.Datetime.to_string(fields.datetime.now() - timedelta(days=365))
        domain = [
            ('state', 'in', ['draft', 'sent', 'sale', 'done']),
            ('product_id', 'in', product_ids),
            ('date', '>', date_from)
        ]
        for group in self.env['sale.report'].read_group(domain, ['product_id', 'product_uom_qty'], ['product_id']):
            r[group['product_id'][0]] = group['product_uom_qty']
        for product in self.env[ "product.product" ].browse( product_ids ):
            self.sales_count = float_round(r.get(product.id, 0), precision_rounding=product.uom_id.rounding)
        return r

    @api.model
    def _get_default_r_date( self ):
        return str( datetime.datetime.now() + datetime.timedelta( weeks = 16 ) )

    @api.model
    def _get_default_d_date( self ):
        return str( datetime.datetime.now() + datetime.timedelta( weeks = 16 ) + datetime.timedelta( days = 8 ) )

    @api.onchange( "date_order" )
    def _onchange_date_order( self ):
        self.date_disponibility = str( self.date_order + datetime.timedelta( 
            weeks = 16 ) + datetime.timedelta( days = 8 ) )

        self.reception_date = str( self.date_order + datetime.timedelta( 
            weeks = 16 ) )

    @api.onchange( "reception_date" )
    def _onchange_reception_date( self ):
        self.date_disponibility = str( self.reception_date + datetime.timedelta( days = 8 ) )

    def update_related_documents( self ):
        SaleOrderLine = self.env[ 'sale.order.line' ]

        if not self.order_line:
            raise ValidationError( _( 'Veuillez tout d\'abord créer et enregistrer des lignes de commande.' ) )

        #product_ids = set()
        for line in self.order_line:
            line.date_disponibility = self.date_disponibility
            line.product_id.date_disponibility = self.date_disponibility
            #product_ids.add( line.product_id.id )

        """order_line_ids = SaleOrderLine.search( 
            [ ( 'product_id', 'in', list( product_ids ) ) ] )

        if order_line_ids:
            sale_order_ids = set()
            for line in order_line_ids:
                line.date_disponibility = self.date_disponibility
                sale_order_ids.add( line.order_id )
            
            for order in sale_order_ids:
                order.update_disponibility_date()"""

    def action_view_sales_po( self ):
        product_ids = set()
        sale_lines = []
        sales = []
        SaleOrderLine = self.env[ 'sale.order.line' ]
        SaleOrder = self.env[ 'sale.order' ]

        for line in self.order_line:
            product_ids.add( line.product_id.id )

        sale_order_line_ids = SaleOrderLine.search( 
            [ ( 'product_id', 'in', list( product_ids ) ) ] )

        for line in sale_order_line_ids:
            sale_lines.append( line.id )

        sale_order_ids = SaleOrder.search( 
            [ ( 'order_line', 'in', sale_lines ) ] )

        for sale in sale_order_ids:
            sales.append( sale.id )

        action = self.env.ref('product_disponibility.update_mad_date_action').read()[0]
        action['domain'] = [ '|', ('id', 'in', sales ), ('order_line.product_id', 'in', list( product_ids ) ) ]
        action['context'] = {
            'search_default_last_year': 1,
            'search_default_team_id': 1,
        }
        return action

class PurchaseOrderLine( models.Model ) :
    _inherit = "purchase.order.line"

    date_disponibility = fields.Date( 
        string     = _( "Date de MàD" ),
        translate  = True
    )

    @api.onchange( 'product_id' )
    def onchange_product( self ):
        if self.product_id.date_disponibility:
            self.date_disponibility = self.product_id.date_disponibility
