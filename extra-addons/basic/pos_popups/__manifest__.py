# -*- coding: utf-8 -*-
{
    'name': "pos_popups",

    'summary': """popups for tpv""",

    'description': """
        popups de warning, error y success para el tpv
    """,

    'author': "Luis González",
    "maintainer": ["Luis González"],

    'category': 'tpv',
    'version': '0.1',

    'depends': ['point_of_sale'],
    'data': [
        'views/assets.xml',
    ],
    'qweb': ['static/src/xml/pos.xml'],

}