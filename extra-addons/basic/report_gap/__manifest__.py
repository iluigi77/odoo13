# -*- coding: utf-8 -*-
{
    'name': "report_gap",

    'summary': """ Report Gap """,

    'description': """
        Report Gap
    """,

    'author': "Luis González",
    'maintainer': ["Luis González"],
    'category': 'Reports',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': [
        'base', 
        'product', 
        'dollar_price'
    ],

    # always loaded
    'data': [
        'views/product_template_view.xml',
    ],
}
