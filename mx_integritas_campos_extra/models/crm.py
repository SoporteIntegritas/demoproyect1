from odoo import _, api, fields, models, tools

class Lead(models.Model):
    _name = 'crm.lead'
    _inherit = ['crm.lead']

    mx_integritas_no_pedido=fields.Char(string="No Pedido",traslate=True)