# -*- coding: utf-8 -*-
{
    'name': "pos_client",

    'summary': """restric for client on tpv""",

    'description': """
        Agrega restricciones y campos obligatorios a la ficha del cliente en el tpv
        e impide que se genere una factura sin un cliente seleccionado
    """,

    'author': "Luis González",
    "maintainer": ["Luis González"],
    'category': 'tpv',
    'version': '0.1',
    'depends': ['base', 'pos_offline' ,'point_of_sale', 'pos_popups'],
    'data': [
        'views/assets.xml',
    ],
    'qweb': ['static/src/xml/pos.xml'],

}