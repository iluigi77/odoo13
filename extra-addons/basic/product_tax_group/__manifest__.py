# -*- coding: utf-8 -*-
{
    'name': "product_tax_group",
    'summary': """inherit tax group for product record""",

    'description': """
        Permite seleccionar un grupo de impuestos en la ficha de productos
        para asignar automaticamente estos impuestos al producto
    """,
    'author': "Luis González",
    'category': 'product',
    'version': '0.1',
    'depends': ['base', 'product', 'account'],

    'data': [
        'views/product_template.xml',
    ],
    # 'installable': True,
}