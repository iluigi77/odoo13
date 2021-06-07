# -*- coding: utf-8 -*-
{
    'name': "services",

    'summary': """ services for ecommers""",

    'description': """
        [GET] product               -> Return all products
        [GET] product/<barcode>     -> Return product by barcode
    """,

    'author': "Luis González",
    'maintainer': ["Luis González"],
    'category': 'services',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product', 'stock'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
}
