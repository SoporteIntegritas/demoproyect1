# -*- coding: utf-8 -*-
from odoo import http

# class MxIntegritasDecPrec(http.Controller):
#     @http.route('/mx_integritas_dec_prec/mx_integritas_dec_prec/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mx_integritas_dec_prec/mx_integritas_dec_prec/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mx_integritas_dec_prec.listing', {
#             'root': '/mx_integritas_dec_prec/mx_integritas_dec_prec',
#             'objects': http.request.env['mx_integritas_dec_prec.mx_integritas_dec_prec'].search([]),
#         })

#     @http.route('/mx_integritas_dec_prec/mx_integritas_dec_prec/objects/<model("mx_integritas_dec_prec.mx_integritas_dec_prec"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mx_integritas_dec_prec.object', {
#             'object': obj
#         })