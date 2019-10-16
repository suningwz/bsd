# -*- coding: utf-8 -*-
{
    'name': "Sale Order Product Selection Improvements",

    'summary': """
    """,
    'description': """
        Sale Order Product Selection Improvements

        
        This module adds a category in sale.order.line model. When the category is selected, users can only select products of this category.
        This module adds the category field in the pop-up when adding a sale.order.line.
        
        This module also adds a field with qty available in stock of the product selected in the pop-up.

        This module has been developed by François WYAIME @ AbAKUS it-solutions.
    """,
    'author': "ABAKUS IT-SOLUTIONS",
    'website': "http://www.abakusitsolutions.eu",

    'category': 'Sale',
    'version': '12.0.1.0',

    'depends': [
        'product',
        'sale',
    ],

    'data': [
        'data/product_category.xml',

        'views/sale_order.xml',
        'views/product_product.xml',
    ],
}
