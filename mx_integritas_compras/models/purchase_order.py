from odoo import _, api, fields, models, tools

class PurchaseOrder(models.Model):
    _inherit = ['purchase.order']
    
    
    requisition_id=fields.Many2one('purchase.requisition')

    def _set_requerimiento(self):
        for stock in self:
            for linea in stock.order_line:
                linea.requisition_id=stock.requisition_id

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'


    order_id = fields.Many2one('purchase.order')
    name = fields.Text(string='Description')
    partner_id = fields.Many2one('res.partner')
    product_id = fields.Many2one('product.product')
    price_unit = fields.Float(string='Unit Price')
    product_qty = fields.Float(string='Quantity')
    product_uom = fields.Many2one('uom.uom')
    price_subtotal = fields.Monetary(string='Subtotal')

    date_planned = fields.Datetime(string='Scheduled Date', required=True, index=True)
    #requi_id= fields.Many2one('purchase.requisition',string="Acuerdo de Compra",compute='_set_req')
    requisition_id= fields.Many2one(related="order_id.requisition_id",string="Acuerdo de Compra",store=True,readonly=True)
    #requisition_id=fields.related('order_id','requisition_id',string="Acuerdo de Compra",store=True,readonly=True)

    def _set_req(self):
        for stock in self:
            
            req=stock.order_id.requisition_id
            stock.update({'requi_id':req})
            stock.requisition_id=req
    
