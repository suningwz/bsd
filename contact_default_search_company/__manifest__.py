# -*- coding: utf-8 -*-
{
    'name': "Contact Default Search Company",

    'summary': """
    """,
    'description': """
        Contact Default Search Company


        This modules makes the filter Company used by default in contact module.


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
        'views/res_partner.xml',
    ],
}
