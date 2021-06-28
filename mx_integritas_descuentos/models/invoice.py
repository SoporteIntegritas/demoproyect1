# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def invoice_validate(self):
        super(AccountInvoice, self).invoice_validate()
        print("Extension Validate")
        for invoice in self:
            if invoice.type in ['out_refund']
                for line in invoice.invoice_line_ids:
                    for lineaped in line.sale_line_ids:
                        order=lineaped.order_id
                    
                    if order.amount_total<=invoice.amount_total:
                        
                        order.invoice_status='invoiced'
                #print(desc)
                #line.discount=desc
            #if invoice.amount_total!=invoice.residual:
                #invoice.residual=invoice.amount_total


        