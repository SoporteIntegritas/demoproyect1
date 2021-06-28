# -*- coding: utf-8 -*-
# from odoo import http


# class MxIntegritasWssProd(http.Controller):
#     @http.route('/mx_integritas_wss_prod/mx_integritas_wss_prod/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mx_integritas_wss_prod/mx_integritas_wss_prod/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mx_integritas_wss_prod.listing', {
#             'root': '/mx_integritas_wss_prod/mx_integritas_wss_prod',
#             'objects': http.request.env['mx_integritas_wss_prod.mx_integritas_wss_prod'].search([]),
#         })

#     @http.route('/mx_integritas_wss_prod/mx_integritas_wss_prod/objects/<model("mx_integritas_wss_prod.mx_integritas_wss_prod"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mx_integritas_wss_prod.object', {
#             'object': obj
#         })
