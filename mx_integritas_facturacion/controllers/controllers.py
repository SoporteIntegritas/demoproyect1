# -*- coding: utf-8 -*-
from odoo import http

# class MxIntegritasFacturacion(http.Controller):
#     @http.route('/mx_integritas_facturacion/mx_integritas_facturacion/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mx_integritas_facturacion/mx_integritas_facturacion/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mx_integritas_facturacion.listing', {
#             'root': '/mx_integritas_facturacion/mx_integritas_facturacion',
#             'objects': http.request.env['mx_integritas_facturacion.mx_integritas_facturacion'].search([]),
#         })

#     @http.route('/mx_integritas_facturacion/mx_integritas_facturacion/objects/<model("mx_integritas_facturacion.mx_integritas_facturacion"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mx_integritas_facturacion.object', {
#             'object': obj
#         })