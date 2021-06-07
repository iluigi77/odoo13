# -*- coding: utf-8 -*-
{
    'name': "account_demo",

    'summary': """ check account as old account""",

    'description': """
        check account as old account for demo data odoo (on account)
    """,

    'author': "Luis González",
    'maintainer': ["Luis González"],
    'category': 'accounting',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'account'],

    'data': [
        'views/account_view.xml',
    ],
}
