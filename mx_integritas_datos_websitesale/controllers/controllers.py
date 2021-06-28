# -*- coding: utf-8 -*-
# from odoo import http


# class MxIntegritasDatosWebsitesale(http.Controller):
#     @http.route('/mx_integritas_datos_websitesale/mx_integritas_datos_websitesale/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mx_integritas_datos_websitesale/mx_integritas_datos_websitesale/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mx_integritas_datos_websitesale.listing', {
#             'root': '/mx_integritas_datos_websitesale/mx_integritas_datos_websitesale',
#             'objects': http.request.env['mx_integritas_datos_websitesale.mx_integritas_datos_websitesale'].search([]),
#         })

#     @http.route('/mx_integritas_datos_websitesale/mx_integritas_datos_websitesale/objects/<model("mx_integritas_datos_websitesale.mx_integritas_datos_websitesale"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mx_integritas_datos_websitesale.object', {
#             'object': obj
#         })
