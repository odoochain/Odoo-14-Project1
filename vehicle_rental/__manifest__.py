# -*- coding: utf-8 -*-
{
    'name': "Vehicle Rental",

    'summary': """
        vehicle rental""",

    'description': """
        The app used for renting the vehicle based on user request.
    """,

    'author': "Sonu Soman KP",
    'website': "http://www.cybrosys.com",

    # Categories can be used to filter modules in modules listing
    'category': 'Uncategorized',
    'version': '14.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','fleet','account','mail'],

    # always loaded
    'data': [

        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/vehicle_rental.xml',
        'views/rental_request.xml',
        'data/sequence.xml',
        'data/product_new.xml',
        'reports/rent_report.xml',
    ],
    
    'images': ['static/description/icon.png'],
    'installable': True,
    'auto_install': False

}
