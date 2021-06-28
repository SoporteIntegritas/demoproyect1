# -*- coding: utf-8 -*-
{
    'name': "mx_integritas_localizacion_cp",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Este módulo integra una funcionalidad para porder obtener el país, delegación y estado por medio de un código postal.
    """,

    'author': "Integritas",
    'website': "http://integritas.mx",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Localización',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','website_sale','website_form'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
