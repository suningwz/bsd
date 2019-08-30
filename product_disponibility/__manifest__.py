# -*- coding: utf-8 -*-
{
    'name': "Product Disponibility",

    'summary': """
        Managing disponibility dates""",

    'description': """
        Managing disponibility dates
    """,

    'author': "Psisoft",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'sale', 'stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/product_template.xml',
        'views/sale_views.xml',
        #'views/scheduler.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
