# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import datetime

class SaleOrder( models.Model) :
    _inherit = "sale.order"

    date_disponibility = fields.Date( 
        string    = _( "Date de Mise à Disposition Estimée" ),
        translate = True,
        default   = "2050-01-01",
        track_visibility = "onchange" 
    )

    product_id = fields.Many2one( 
        "product.product", 
        related = "order_line.product_id",
        string  = "Product"
    )

    product_tmpl_id = fields.Many2one( 
        "product.template", 
        related = "product_id.product_tmpl_id",
        string  = "Product tmp"
    )

    @api.multi
    def update_disponibility_date( self ):
        dates_list = []

        if self.order_line:
            for line in self.order_line:
                if line.date_disponibility:
                    dates_list.append( line.date_disponibility )

            if dates_list:
                self.update( { 'date_disponibility': max( dates_list ) } )

    @api.onchange( 'order_line' )
    def onchange_order_line( self ):
        dates_list = []

        for line in self.order_line:
            if line.date_disponibility:
                dates_list.append( line.date_disponibility )

        if dates_list:
            self.date_disponibility = max( dates_list )

    @api.multi
    def write( self, vals ):
        dates_list = []
        orderLine  = self.env[ 'sale.order.line' ]

        print(vals)

        """if 'order_line' in vals.keys():
            if vals['order_line'][ 0 ][ 2 ]:
                if vals['order_line'][ 0 ][ 2 ]['date_disponibility']:
                    dates_list.append(datetime.datetime.strptime(vals['order_line'][ 0 ][ 2 ]['date_disponibility'], '%Y-%m-%d').date())
            
            if len(self.order_line) == 1:
                if dates_list:
                    vals[ 'date_disponibility' ] = max( dates_list )
                else:
                    vals[ 'date_disponibility' ] = self.order_line.date_disponibility

            else:
                for line in self.order_line:
                    dates_list.append( line.date_disponibility )

                if dates_list:
                    vals[ 'date_disponibility' ] = max( dates_list )"""

        return super( SaleOrder, self ).write( vals )

    @api.model
    def create( self, vals ):
        dates_list = []
        orderLine  = self.env[ 'sale.order.line' ]

        if 'order_line' in vals.keys():
            for line in vals[ 'order_line' ]:
                dates_list.append( line[ 2 ][ 'date_disponibility' ] )

            vals[ 'date_disponibility' ] = max( dates_list )

        return super( SaleOrder, self ).create( vals )

    @api.multi
    def update_documents( self, context ):
        orderLine  = self.env[ 'sale.order.line' ]
        picking    = self.env[ 'stock.picking' ]
        order_ids  = self.browse( context[ 'active_ids' ] )

        print(context)

        for order in order_ids:
            dates_list = []
            product_id = None
            product_ids = []

            if context[ 'active_domain' ][ 0 ][ 0 ] == "product_id":
                product_id = self.env['product.product'].browse( [ context[ 'active_domain' ][ 0 ][ 2 ][ 0 ] ] )
            elif context[ 'active_domain' ][ 0 ][ 0 ] == "product_tmpl_id":
                product_id = self.env['product.product'].search( [ context[ 'active_domain' ][ 0 ] ] )
            elif context[ 'active_domain' ][ 2 ][ 0 ] == "order_line.product_id":
                product_ids = self.env['product.product'].browse( context[ 'active_domain' ][ 2 ][ 2 ] )

            for line in order.order_line:
                if product_id is not None:
                    if line.product_id == product_id:
                        line.write( { 'date_disponibility': line.product_id.date_disponibility } )
                elif product_ids is not []:
                    if line.product_id in product_ids:
                        line.write( { 'date_disponibility': line.product_id.date_disponibility } )
                
                dates_list.append( line.date_disponibility )

            order.write( { 'date_disponibility': max( dates_list ) } )
            picking_ids =  picking.search( [ ( 'origin', '=', order.name ), ( 'picking_type_code', '=', 'outgoing' ) ] )

            if picking_ids:
                for picking in picking_ids:
                    picking.write( { 'date_disponibility': order.date_disponibility } )

class SaleOrderLine( models.Model ):
    _inherit = "sale.order.line"

    date_disponibility = fields.Date( 
        string    = _( "Date de MaD" ),
        translate = True,
        default   = "2050-01-01"
    )

    @api.onchange( 'product_id' )
    def onchange_product( self ):
        if self.product_id.date_disponibility:
            self.date_disponibility = self.product_id.date_disponibility
