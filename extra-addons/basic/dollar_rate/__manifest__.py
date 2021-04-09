# -*- coding: utf-8 -*-
{
    'name': "dollar_rate",

    'summary': """ Tasa actual de moneda""",

    'description': """
        Establece una tasa para los productos dolarizados y almacena el historico de las tasas
    """,

    'author': "Luis González",
    'category': 'purchases',
    'version': '0.1',
    'depends': [
        'base',
        'sale',
        'purchase',
        'product',
        'dollar_price',
        'product_variant_sale_price'
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/res_currency_line.xml',
        'views/product_template.xml',
        'views/product_product.xml'
    ],
}