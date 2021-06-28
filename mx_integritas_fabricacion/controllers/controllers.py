# -*- coding: utf-8 -*-
from odoo import http

# class MxIntegritasFabricacion(http.Controller):
#     @http.route('/mx_integritas_fabricacion/mx_integritas_fabricacion/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mx_integritas_fabricacion/mx_integritas_fabricacion/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mx_integritas_fabricacion.listing', {
#             'root': '/mx_integritas_fabricacion/mx_integritas_fabricacion',
#             'objects': http.request.env['mx_integritas_fabricacion.mx_integritas_fabricacion'].search([]),
#         })

#     @http.route('/mx_integritas_fabricacion/mx_integritas_fabricacion/objects/<model("mx_integritas_fabricacion.mx_integritas_fabricacion"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mx_integritas_fabricacion.object', {
#             'object': obj
#         })