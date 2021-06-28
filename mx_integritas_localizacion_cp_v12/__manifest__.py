# -*- coding: utf-8 -*-
{
    'name': "mx_integritas_localizacion_cp_v12",
    'summary': """
        Automatización para obtener colonia, país y estado desde el código postal en el ecommerce""",

    'description': """
        Long description of module's purpose
    """,
    'author': "Integritas",
    'website': "http://www.integritas.mx",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','website_sale'],
    'data': [
        'views/templates.xml',
        'data/form_fields.xml',
        'views/res_config.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}
