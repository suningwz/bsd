# -*- coding: utf-8 -*-
{
    'name': "Stock On-Call Sales Order Management",
    'summary': """Manage On-Call from Sales Order  
    """,
    'author': "ABAKUS IT-SOLUTIONS",
    'website': "http://www.abakusitsolutions.eu",

    'category': 'Stock',
    'version': '13.0.1.0',

    'depends': [
        'stock',
        'sale',
        'sale_management',
    ],

    'data': [
        'views/stock_location_route_view.xml',
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
        'views/stock_oncall_stock.xml',
        'views/product_view.xml',
        'views/stock_picking.xml',

        'data/stock_location_route.xml',
        'security/ir.model.access.csv',
    ],

}
