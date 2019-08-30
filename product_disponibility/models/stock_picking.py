# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import datetime

class Picking( models.Model ) :
    _inherit = "stock.picking"

    date_j_1 = fields.Datetime(
        string = _( "Jour J - 1" )
    )

    date_j = fields.Datetime( 
        string = _( "Jour J" )
    )

    date_disponibility = fields.Date( 
        string    = _( "Date de Mise à Disposition Estimée" ),
        translate = True,
        default   = "2050-01-01"
    )

    responsible_id = fields.Many2one(
        "hr.employee",
        string           = _( "Résponsable" ),
        translate        = True,
        track_visibility = "onchange" 
    )

    @api.model
    def create( self, vals ):
        if vals[ 'picking_type_id' ] == 5:
            SaleOrder  = self.env[ 'sale.order' ]
     
            order_id = SaleOrder.search( [ ( 'name', '=', vals[ 'origin' ] ) ] )

            vals[ 'date_disponibility' ] = order_id.date_disponibility

            vals[ 'date_j_1' ] = datetime.datetime.combine( 
                ( order_id.date_disponibility - datetime.timedelta( days = 2 ) ) , 
                datetime.time( 22, 59, 00 ) )

            vals[ 'date_j' ] = datetime.datetime.combine( 
                order_id.date_disponibility, datetime.time( 22, 59, 00 ) )

        return super( Picking, self ).create( vals )
