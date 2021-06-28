from odoo import _, api, fields, models, tools

class ResPartner(models.Model):
    _inherit = ['res.partner']
    mx_integritas_refprov=fields.Char(string="Referencia Prov",traslate=True)





