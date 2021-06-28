# -*- coding: utf-8 -*-
{
    'name': "mx_integritas_payment_baz",
    'summary': """
        Payment Acquirer: BAZ Implementation""",
    'description': """
        Modulo creado para implementar el metodo de pago con banco azteca v12
    """,
    'author': "Integritas",
    'website': "https://integritas.mx",
    'category': 'Accounting/Payment',
    'version': '0.1',
    'depends': ['payment'],
    'data': [
        'views/payment_views.xml',
        'views/payment_baz_templates.xml',
        'data/payment_acquirer_data.xml',
        'views/payment_transaction.xml',
    ],
    'installable': True,
    'post_init_hook': 'create_missing_journal_for_acquirers',
    
    
}
