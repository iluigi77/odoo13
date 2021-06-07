# -*- coding: utf-8 -*-
{
    'name': "pos_fiscal_print",
    'summary': """ fiscal print from odoo""",
    'description': """
        Establece conexion con impresora fiscal mediante un API, manteniendo el flujo offline nativo de odoo
    """,
    'author': "Luis González",
    "maintainer": ["Luis González"],

    'category': 'tpv',
    'version': '0.1',
    'depends': ['point_of_sale', 'account_tax_type', 'pos_popups', 'pos_client'],
    'data': [
        'views/pos_config.xml',
        'views/assets.xml',
        'views/pos_config.xml',
    ],
}