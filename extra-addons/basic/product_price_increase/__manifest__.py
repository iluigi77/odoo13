# -*- coding: utf-8 -*-
{
    'name': "product_price_increase",

    'summary': """ batch increment for products """,

    'description': """
        allows you to make fixed or percentage increases, 
        based on cost, sale and dollar rate criteria
    """,

    'author': "Luis González",
    'maintainer': ["Luis González"],
    'category': 'Product',
    'version': '1',

    # any module necessary for this one to work correctly
    'depends': [
        'base', 
        'product',
        'report_gap',
        'dollar_rate',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/assets.xml',
        'wizard/wizard_view.xml',
        'views/increase_line.xml',

    ],
}