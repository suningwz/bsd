# -*- coding: utf-8 -*-
{
    'name': "Stock On-Call Sales Order Management",
    'summary': """Manage On-Call from Sales Order  
    """,
    'author': "Valentin Thirion, AbAKUS it-solutions SARL",
    'website': "http://www.abakusitsolutions.eu",

    'category': 'Stock',
    'version': '12.0.1.1',

    'depends': [
        'stock',
        'sale'
    ],

    'data': [
        'views/stock_location_route_view.xml',
        'views/res_partner_view.xml',

        'data/stock_location_route.xml',
    ],

}
