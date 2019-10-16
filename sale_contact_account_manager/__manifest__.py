# -*- coding: utf-8 -*-
{
    'name': "Sale Contact Account Manager",

    'summary': """
    """,
    'description': """
        Sale Contact Account Manager

        This module adds a many2one field on the sale order to a new model sale.order.method. 
        This model contains only a name and is used to specify how the sale has been done (on the road, by phone, by email, ...)
        
        This module also shows the field create_uid on sale orders to specify who create the sale order.
        
        This module also renames the field 'user_id' in sale.order by 'Who'.
        

        This module has been developed by François WYAIME @ AbAKUS it-solutions.
    """,
    'author': "ABAKUS IT-SOLUTIONS",
    'website': "http://www.abakusitsolutions.eu",

    'category': 'Sale',
    'version': '12.0.1.0',

    'depends': [
        'contacts',
        'sale'
    ],

    'data': [
        'views/sale_order.xml',
        'views/sale_order_method.xml',

        'security/ir.model.access.csv'
    ],
}
