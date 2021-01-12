# -*- coding: utf-8 -*-
{
    'name': "Vehicle Rental",

    'summary': """
        vehicle rental""",

    'description': """
        The app used for renting the vehicle based on user request.
    """,

    'author': "Sonu Soman",
    'website': "http://www.cybrosys.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '14.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','fleet'],

    # always loaded
    'data': [

        'views/views.xml',
        'views/vehicle_rental.xml',
        'views/rental_request.xml',
        'data/sequence.xml',
        'security/security.xml',
        'security/ir.model.access.csv',


    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
'images': ['static/description/icon.png'],
}
