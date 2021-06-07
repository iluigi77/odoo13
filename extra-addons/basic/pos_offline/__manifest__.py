# -*- coding: utf-8 -*-
{
    'name': "pos_offline",
    'summary': """ fix for best UI/UX on mode offline""",
    'description': """
        Mejora la UI/UX en modo offline, mostrando una alerta que indica que no se posee conexion al momento
    """,
    'author': "Luis González",
    "maintainer": ["Luis González"],

    'category': 'tpv',
    'version': '1.0',
    'depends': [
        'base',
        'point_of_sale'
    ],
    'data': [
        'views/assets.xml',
    ],
    'qweb': ['static/src/xml/pos.xml'],

}