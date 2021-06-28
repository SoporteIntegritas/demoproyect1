from odoo import _, api, fields, models, tools

class StockPicking(models.Model):
    _inherit = 'sale.order'
    mx_integritas_refprov=fields.Char(string="Referencia",traslate=True)