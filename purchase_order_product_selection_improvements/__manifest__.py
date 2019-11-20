# -*- coding: utf-8 -*-
{
    'name': "Purchase Order Product Selection Improvements",

    'summary': """
    """,
    'description': """
        Purchase Order Product Selection Improvements
        
        This module adds an image in purchase order lines.

        This module has been developed by François WYAIME @ AbAKUS it-solutions.
    """,
    'author': "ABAKUS IT-SOLUTIONS",
    'website': "http://www.abakusitsolutions.eu",

    'category': 'Purchase',
    'version': '13.0.1.0',

    'depends': [
        'product',
        'purchase',
    ],

    'data': [
        'views/purchase_order.xml',
    ],
}
