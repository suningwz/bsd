# -*- coding: utf-8 -*-
{
    'name': "Product Disponibility",
    'summary': """
        Managing disponibility dates""",
    'author': "Psisoft, ABAKUS- IT-SOLUTIONS",
    'website': "",
    'category': 'Sale',
    'version': '0.2',
    'depends': [
        'sale',
        'website_sale',
        'purchase',
        'stock',
    ],
    'data': [
        # 'security/ir.model.access.csv',
        'views/product_template.xml',
        'views/sale_views.xml',
        'views/purchase_views.xml',
        'views/stock_picking_views.xml',
        'views/update_mad_date_action.xml'
        #'views/scheduler.xml',
    ],
}
