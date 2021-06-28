# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime, timedelta
from functools import partial
from itertools import groupby

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import formatLang
from odoo.osv import expression
from odoo.tools import float_is_zero, float_compare


from odoo.addons import decimal_precision as dp

from werkzeug.urls import url_encode


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def action_invoice_create(self, grouped=False, final=False):
        """
        Create the invoice associated to the SO.
        :param grouped: if True, invoices are grouped by SO id. If False, invoices are grouped by
                        (partner_invoice_id, currency)
        :param final: if True, refunds will be generated if necessary
        :returns: list of created invoices
        """
        inv_obj = self.env['account.invoice']
        precision = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        invoices = {}
        references = {}
        invoices_origin = {}
        invoices_name = {}

        # Keep track of the sequences of the lines
        # To keep lines under their section
        inv_line_sequence = 0
        for order in self:
            group_key = order.id if grouped else (order.partner_invoice_id.id, order.currency_id.id)

            # We only want to create sections that have at least one invoiceable line
            pending_section = None

            # Create lines in batch to avoid performance problems
            line_vals_list = []
            # sequence is the natural order of order_lines
            for line in order.order_line:
                if line.display_type == 'line_section':
                    pending_section = line
                    continue

                    
                if line.price_subtotal<=0:
                    line.qty_invoiced=line.product_uom_qty
                    continue
                    
                if float_is_zero(line.qty_to_invoice, precision_digits=precision):
                    continue
                if group_key not in invoices:
                    inv_data = order._prepare_invoice()
                    invoice = inv_obj.create(inv_data)
                    references[invoice] = order
                    invoices[group_key] = invoice
                    invoices_origin[group_key] = [invoice.origin]
                    invoices_name[group_key] = [invoice.name]
                elif group_key in invoices:
                    if order.name not in invoices_origin[group_key]:
                        invoices_origin[group_key].append(order.name)
                    if order.client_order_ref and order.client_order_ref not in invoices_name[group_key]:
                        invoices_name[group_key].append(order.client_order_ref)

                if line.qty_to_invoice > 0 or (line.qty_to_invoice < 0 and final):
                    if pending_section:
                        section_invoice = pending_section.invoice_line_create_vals(
                            invoices[group_key].id,
                            pending_section.qty_to_invoice
                        )
                        inv_line_sequence += 1
                        section_invoice[0]['sequence'] = inv_line_sequence
                        line_vals_list.extend(section_invoice)
                        pending_section = None

                    inv_line_sequence += 1
                    inv_line = line.invoice_line_create_vals(
                        invoices[group_key].id, line.qty_to_invoice
                    )
                    inv_line[0]['sequence'] = inv_line_sequence
                    line_vals_list.extend(inv_line)

            if references.get(invoices.get(group_key)):
                if order not in references[invoices[group_key]]:
                    references[invoices[group_key]] |= order

            lines=self.env['account.invoice.line'].create(line_vals_list)
            for l in lines:
                for lineaped in l.sale_line_ids:
                    l.discount=lineaped.calcula_porcentaje_desc()
                    #if l.quantity==0:
                    #    l.unlink()

        for group_key in invoices:
            invoices[group_key].write({'name': ', '.join(invoices_name[group_key]),
                                       'origin': ', '.join(invoices_origin[group_key])})
            sale_orders = references[invoices[group_key]]
            if len(sale_orders) == 1:
                invoices[group_key].reference = sale_orders.reference

        if not invoices:
            raise UserError(_('There is no invoiceable line. If a product has a Delivered quantities invoicing policy, please make sure that a quantity has been delivered.'))

        self._finalize_invoices(invoices, references)
        return [inv.id for inv in invoices.values()]

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def calcula_porcentaje_desc(self):
        for line in self:
            order=line.order_id
        
        
            lineasDescuento=self.env['sale.order.line'].search([('order_id','=',order.id),('price_unit','<',0)])
            
            for linea_desc in lineasDescuento:
                producto_descuento=linea_desc.product_id
                linea_desc

                descuento=self.env['sale.coupon.program'].search([('discount_line_product_id','=',producto_descuento.id)])
                #print(descuento)
                if descuento.reward_type=='discount':
                    if descuento.discount_type=='percentage' and descuento.discount_apply_on=='on_order':
                        #print(descuento.discount_percentage)
                    
                        envio=self.env['delivery.carrier'].search([('product_id','=',line.product_id.id)])
                        if line.price_unit>0 and not envio:
                            #l.write({'discount':l.discount+descuento.discount_percentage })
                            return line.discount+descuento.discount_percentage

                    #linea_desc.unlink()
                    if descuento.discount_type=='percentage':
                        if descuento.discount_apply_on=='specific_product':
                            pro=descuento.discount_specific_product_id
                        
                            if pro.id==line.product_id.id:
                                #l.write({'discount':l.discount+descuento.discount_percentage })
                                return line.discount+descuento.discount_percentage
                            #linea_desc.unlink()

                        if descuento.discount_apply_on=='cheapest_product':
                            #lineas=self.env['sale.order.line'].search([('order_id','=',order.id),('price_unit','>',0)], order="price_unit asc")
                        
                            envio=self.env['delivery.carrier'].search([('product_id','=',line.product_id.id)])
                            l=self.env['sale.order.line'].search([('order_id','=',order.id),('price_unit','>',0)],order='price_unit asc',limit=1)
                            #print()
                            if not envio and l.product_id==line.product_id:
                                #linea.write({'discount':linea.discount+descuento.discount_percentage })
                                return line.discount+descuento.discount_percentage
                                    #break
                        #linea_desc.unlink()

                    if descuento.discount_type=='fixed_amount':
                        base=order.amount_untaxed+descuento.discount_fixed_amount
                        base_desc=order.amount_untaxed
                        d=(1-(base_desc/base))*100
                        #print(d)
                    
                        envio=self.env['delivery.carrier'].search([('product_id','=',l.product_id.id)])
                        if line.price_unit>0 and not envio:
                            #print(base)
                            #print(l.price_subtotal)
                            
                            #l.write({'discount':l.discount+d })
                            return line.discount+d
                
                if descuento.reward_type=='product':
                    if descuento.reward_product_id==line.product_id:
                        #line.product_uom_qty=line.product_uom_qty-descuento.reward_product_quantity
                        qty_total=line.product_uom_qty
                        qty_desc=line.product_uom_qty-linea_desc.product_uom_qty
                        d=(qty_desc*100)/qty_total
                        if linea_desc.product_uom_qty>=line.product_uom_qty:
                            return 100
                        return d
                        

                    #linea_desc.unlink()
