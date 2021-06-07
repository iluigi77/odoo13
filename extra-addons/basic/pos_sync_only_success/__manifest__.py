# -*- coding: utf-8 -*-
{
    'name': "pos_sync_only_success",

    'summary': """sync only success order on tpv""",

    'description': """
        Sincroniza solo los pedidos que ya han sido facturados desde el tpv
    """,
    'author': "Luis González",
    "maintainer": ["Luis González"],

    'category': 'tpv',
    'version': '0.1',
    'depends': ['base', 'point_of_sale', 'pos_fiscal_print'],
    'data': [
        'views/assets.xml',
    ],
}