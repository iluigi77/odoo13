# -*- coding: utf-8 -*-
{
    'name': "sale_print_ticket",

    'summary': """ module for no fiscal printer""",

    'description': """
        generate pdf ticket for no fiscal printer, 
    """,

    "maintainer": ["Luis González"],
    'author': "Luis González",
    'category': 'Sales',
    'version': '0.1',

    'depends': [
        'base',
        'sale',
        'sale_payment_register',
    ],

    # always loaded
    'data': [
        'views/sale_view.xml',
        'reports/ticket_sale_order.xml'
    ],
}
