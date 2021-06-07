# -*- coding: utf-8 -*-
{
    'name': "invoice_fiscal_print",

    'summary': """ print for fiscal printer from invoice module""",

    'description': """
        Pemite imprimir por impresora fiscal desde el modulo de facturación
    """,

    'author': "Luis González",
    "maintainer": ["Luis González"],
    'category': 'Invoicing Management',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'sale',
        'account',
        'account_tax_type'
    ],

    # always loaded
    'data': [
        'views/assets.xml',
        'views/account_move.xml',
    ],

    'qweb': [
        'static/src/xml/action.xml',
    ],

}