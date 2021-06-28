# -*- coding: utf-8 -*-
from odoo import http

# class MxIntegritasDescNoacum(http.Controller):
#     @http.route('/mx_integritas_desc_noacum/mx_integritas_desc_noacum/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mx_integritas_desc_noacum/mx_integritas_desc_noacum/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mx_integritas_desc_noacum.listing', {
#             'root': '/mx_integritas_desc_noacum/mx_integritas_desc_noacum',
#             'objects': http.request.env['mx_integritas_desc_noacum.mx_integritas_desc_noacum'].search([]),
#         })

#     @http.route('/mx_integritas_desc_noacum/mx_integritas_desc_noacum/objects/<model("mx_integritas_desc_noacum.mx_integritas_desc_noacum"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mx_integritas_desc_noacum.object', {
#             'object': obj
#         })