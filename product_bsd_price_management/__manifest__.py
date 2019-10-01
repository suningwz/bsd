# -*- coding: utf-8 -*-
{
    'name': "Product BSD Price Management",

    'summary': """
    """,
    'description': """
        Product BSD Price Management


        This module adds a page in notebook in product.template form. This page contains lines of model product.sale.price.line.
        
        This model is created by this module and contains a lot of price and quantity informations useful for sellers.
        
        The modules also adds a field in uom model to link uom to a specific price.
        
        This link allows users to select the price they want through unit of measure.


        This module has been developed by François WYAIME @ AbAKUS it-solutions.
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
