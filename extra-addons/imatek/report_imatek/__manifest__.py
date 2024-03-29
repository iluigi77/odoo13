# -*- coding: utf-8 -*-
{
    'name': "report_imatek",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Luis Gonzalez",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'imatek',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'service_budget'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/report_sale_order.xml',
        'views/report_purchase_order.xml',
        'views/report_purchase_quotation.xml',
        'views/report_sale_picking_operation.xml',
        'views/report_sale_delivery_slip.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
}
