# -*- coding: utf-8 -*-
{
    'name': "sale_clean_view",

    'summary': """
        fix flow for sale""",

    'description': """
        fix and validate required for sale flow
    """,

    'author': "Luis González",
    "maintainer": ["Luis González"],

    'category': 'Sales',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'sale_management', 'dollar_rate'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/sale_order_view.xml',
    ],
}