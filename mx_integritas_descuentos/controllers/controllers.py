# -*- coding: utf-8 -*-
from odoo import http

# class MxIntegritasDescuentos(http.Controller):
#     @http.route('/mx_integritas_descuentos/mx_integritas_descuentos/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mx_integritas_descuentos/mx_integritas_descuentos/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mx_integritas_descuentos.listing', {
#             'root': '/mx_integritas_descuentos/mx_integritas_descuentos',
#             'objects': http.request.env['mx_integritas_descuentos.mx_integritas_descuentos'].search([]),
#         })

#     @http.route('/mx_integritas_descuentos/mx_integritas_descuentos/objects/<model("mx_integritas_descuentos.mx_integritas_descuentos"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mx_integritas_descuentos.object', {
#             'object': obj
#         })