# -*- coding: utf-8 -*-
{
    'name': "car_services",

    'summary': """ registro de vehículos para servicios """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Luis González",
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        
        'views/services_invoice.xml',
        'views/cars_model.xml',
        'views/services.xml',
        'views/reports.xml',
    ],
}
