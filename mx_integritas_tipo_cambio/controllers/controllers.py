# -*- coding: utf-8 -*-
from odoo import http

# class MxIntegritasTipoCambio(http.Controller):
#     @http.route('/mx_integritas_tipo_cambio/mx_integritas_tipo_cambio/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mx_integritas_tipo_cambio/mx_integritas_tipo_cambio/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mx_integritas_tipo_cambio.listing', {
#             'root': '/mx_integritas_tipo_cambio/mx_integritas_tipo_cambio',
#             'objects': http.request.env['mx_integritas_tipo_cambio.mx_integritas_tipo_cambio'].search([]),
#         })

#     @http.route('/mx_integritas_tipo_cambio/mx_integritas_tipo_cambio/objects/<model("mx_integritas_tipo_cambio.mx_integritas_tipo_cambio"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mx_integritas_tipo_cambio.object', {
#             'object': obj
#         })