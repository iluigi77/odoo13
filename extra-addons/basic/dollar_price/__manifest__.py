# -*- coding: utf-8 -*-
{
    'name': "dollar_price",

    'summary': """ Precio en $ para colorados""",

    'description': """
        Establece precio en $ en la ficha de productos
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
        'views/product_product_variants.xml',
    ],
}