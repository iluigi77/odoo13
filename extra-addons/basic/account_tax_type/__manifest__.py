# -*- coding: utf-8 -*-
{
    'name': "account_tax_type",
    'summary': """ tax type for fiscal print""",
    'description': """
        define un codigo para el tipo de impuesto que lee la impresora fiscal
    """,
    "maintainer": ["Luis González"],
    'author': "Luis González",
    'category': 'tpv',
    'version': '0.1',
    'depends': ['base', 'account'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_tax.xml',
    ],
}