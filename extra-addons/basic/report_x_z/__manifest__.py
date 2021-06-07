# -*- coding: utf-8 -*-
{
    'name': "report_x_z",

    'summary': """ generate report x and z from odoo""",

    'description': """
        Reporte x, reporte z, desde odoo
    """,

    'author': "Luis González",
    'maintainer': ["Luis González"],
    'category': 'tpv',
    'version': '0.1',

    'depends': ['base', 'point_of_sale'],

    'data': [
        'views/pos_session.xml',
        'views/assets.xml',
    ],

    'qweb': [
        'static/src/xml/client_action_view.xml',
    ],
}