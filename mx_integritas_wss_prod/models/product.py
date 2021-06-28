from odoo import _, api, fields, models, tools

class Product(models.Model):
    _inherit = ['product.template']
    description_sale1=fields.Text(string='Descripcion eCommerce')