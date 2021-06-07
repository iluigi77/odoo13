# -*- coding: utf-8 -*-
{
    'name': 'Customer Search Filter',
    'category': 'Sales',
    'version': '12.0.1.0.1',
    'author': "Luis González",
    'maintainer': ["Luis González"],
    'summary': '''
                This module helps in finding a customer with respect CI/RIF.
            ''',
    'description': '''
                This module helps in finding a customer with respect CI/RIF.
                ''',
    'depends': ['base'],

    'data': [
        'views/res_partner_views.xml',
    ],
    'images': [
        'static/description/banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': False
}
