# -*- coding: utf-8 -*-
from odoo import http

# class MxIntegritasCompras(http.Controller):
#     @http.route('/mx_integritas_compras/mx_integritas_compras/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mx_integritas_compras/mx_integritas_compras/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mx_integritas_compras.listing', {
#             'root': '/mx_integritas_compras/mx_integritas_compras',
#             'objects': http.request.env['mx_integritas_compras.mx_integritas_compras'].search([]),
#         })

#     @http.route('/mx_integritas_compras/mx_integritas_compras/objects/<model("mx_integritas_compras.mx_integritas_compras"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mx_integritas_compras.object', {
#             'object': obj
#         })