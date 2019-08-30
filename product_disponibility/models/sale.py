# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class SaleOrder( models.Model) :
    _inherit = "sale.order"

    date_diponibility = fields.Date( 
        string    = _( "Date de mise à disposition" ),
        translate = True
    )

class SaleOrderLine( models.Model ):
    _inherit = "sale.order.line"

    date_diponibility = fields.Date( 
        string    = _( "Date de mise à disposition" ),
        translate = True
    )