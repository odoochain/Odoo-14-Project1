# -*- coding: utf-8 -*-
{
    'name': "Vehicle Rental",

    'summary': """
        vehicle rental""",

    'description': """
        
    """,

    'author': "Sonu Soman",
    'website': "http://www.yourcompany.com",

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
        'views/templates.xml',
        'data/sequence.xml',
        'security/ir.model.access.csv'

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
'images': ['static/description/icon.png'],
}
