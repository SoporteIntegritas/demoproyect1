# -*- coding: utf-8 -*-
from odoo import http

# class MxIntegritasCamposExtra(http.Controller):
#     @http.route('/mx_integritas_campos_extra/mx_integritas_campos_extra/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mx_integritas_campos_extra/mx_integritas_campos_extra/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mx_integritas_campos_extra.listing', {
#             'root': '/mx_integritas_campos_extra/mx_integritas_campos_extra',
#             'objects': http.request.env['mx_integritas_campos_extra.mx_integritas_campos_extra'].search([]),
#         })

#     @http.route('/mx_integritas_campos_extra/mx_integritas_campos_extra/objects/<model("mx_integritas_campos_extra.mx_integritas_campos_extra"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mx_integritas_campos_extra.object', {
#             'object': obj
#         })