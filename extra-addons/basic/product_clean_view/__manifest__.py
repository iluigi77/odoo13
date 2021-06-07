# -*- coding: utf-8 -*-
{
    'name': "product_clean_view",

    'summary': """ clean view for product template""",

    'description': """
    """,

    'author': "Luis González",
    'maintainer': ["Luis González"],

    'category': 'Product',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product'],

    # always loaded
    'data': [
        'views/product_template.xml',
    ],

    # 'installable': True,
}
