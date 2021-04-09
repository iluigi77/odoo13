# -*- coding: utf-8 -*-
{
    'name': "product_clean_view",

    'summary': """ clean view for product template""",

    'description': """
    """,

    'author': "Luis González",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Product',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'product'],

    # always loaded
    'data': [
        'views/product_template.xml',
    ],

    # 'installable': True,
}
