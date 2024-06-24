# -*- coding: utf-8 -*-

{
    'name': 'hospital management',
    'version': '1.0.0',
    'category': 'hospital',
    'summary': 'hospital management system',
    'description': """hospital management system""",
    'depends': ['mail', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'data/patient_tag_Data.xml',
        'data/patient.tag.csv',
        'data/sequence_data.xml',
        'views/odoo_playground_view.xml',
        'wizard/cancel_appointment_view.xml',
        'views/patient_view.xml',
        'views/menu.xml',
        'views/female_patient_view.xml',
        'views/appointment_view.xml',
        'views/patient_tag_view.xml',
        'views/res_config_settings_view.xml',

    ],
    'demo': [],
    'application': True,
    'sequence': -100,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',

}
