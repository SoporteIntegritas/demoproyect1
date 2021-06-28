# -*- coding: utf-8 -*-
from odoo import http

# class Extra-addons/mxIntegritasValidacionRfc(http.Controller):
#     @http.route('/extra-addons/mx_integritas_validacion_rfc/extra-addons/mx_integritas_validacion_rfc/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/extra-addons/mx_integritas_validacion_rfc/extra-addons/mx_integritas_validacion_rfc/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('extra-addons/mx_integritas_validacion_rfc.listing', {
#             'root': '/extra-addons/mx_integritas_validacion_rfc/extra-addons/mx_integritas_validacion_rfc',
#             'objects': http.request.env['extra-addons/mx_integritas_validacion_rfc.extra-addons/mx_integritas_validacion_rfc'].search([]),
#         })

#     @http.route('/extra-addons/mx_integritas_validacion_rfc/extra-addons/mx_integritas_validacion_rfc/objects/<model("extra-addons/mx_integritas_validacion_rfc.extra-addons/mx_integritas_validacion_rfc"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('extra-addons/mx_integritas_validacion_rfc.object', {
#             'object': obj
#         })