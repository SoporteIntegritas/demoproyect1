from odoo import _, api, fields, models, tools
from odoo.addons import decimal_precision as dp

class MrpProduction(models.Model):
    _inherit = ['mrp.production']

    mx_integritas_qtyprod = fields.Float('Cantidad Planificada',default="1.0",readonly=True, required=True)
    mx_integritas_qtyporc = fields.Float('Porcentaje de Produccion',default="1.0",readonly=True, required=True)