from odoo import _, api, fields, models, tools

class AccountInvoice(models.Model):
    _name = 'purchase.order'
    _inherit = ['purchase.order']

    mx_integritas_prioridad=fields.Char(string="Prioridad Lista Negra",traslate=True,compute='_set_datos_atomaticos')

    def _set_datos_atomaticos(self):
        for record in self:
            rfc=record.partner_id.vat
            rfc_ln=self.env['mx_integritas_validacion_rfc.rfc'].search([('name','=',rfc),('is_condonado','=',False)])
            rfc_lnB=self.env['mx_integritas_validacion_rfc.rfc'].search([('name','=',rfc),('is_condonado','=',True)])
            print(rfc_ln)
            print(rfc_lnB)
            if rfc_ln:
                record.mx_integritas_prioridad='A'
            if rfc_lnB and not rfc_ln:
                record.mx_integritas_prioridad='B'
