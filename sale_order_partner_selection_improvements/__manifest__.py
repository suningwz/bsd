# -*- coding: utf-8 -*-
{
    'name': "Sale Order Partner Selection Improvements",

    'summary': """
    """,
    'description': """
        Sale Order Partner Selection Improvements


        -> This module adds a domain to partner field on a sale order. Users can only fill partner_id field with a partner that is a parent.
        
        -> This module also adds a method triggered when partner_id field is changed.
         
        This method change domain of partner_invoicing_id and partner_shipping_id to allow only partner that are children of partner_id field.


        This module has been developed by François WYAIME @ AbAKUS it-solutions.
    """,
    'author': "ABAKUS IT-SOLUTIONS",
    'website': "http://www.abakusitsolutions.eu",

    'category': 'Sale',
    'version': '13.0.1.0',

    'depends': [
        'contacts',
        'sale'
    ],

    'data': [
        'views/sale_order.xml'
    ],
}
