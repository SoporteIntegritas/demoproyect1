from odoo import _, api, fields, models, tools

class ResPartner(models.Model):
    _inherit = ['res.partner']

    error_scraping=fields.Boolean(string="Error Scrapping",traslate=True,defalt=False)

    