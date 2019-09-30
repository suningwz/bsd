# -*- coding: utf-8 -*-
{
    'name': "Product BSD Price Management",

    'summary': """
    """,

    'author': "ABAKUS IT-SOLUTIONS",
    'website': "http://www.abakusitsolutions.eu",

    'category': 'Sale',
    'version': '12.0.1.0',

    'depends': [
        'product',
        'sale',
        'purchase'
    ],

    'data': [
        'data/uom_uom.xml',

        'security/ir.model.access.csv',

        'views/product_template.xml',
        'views/uom_uom.xml',
        'views/res_partner.xml',
    ],
}
