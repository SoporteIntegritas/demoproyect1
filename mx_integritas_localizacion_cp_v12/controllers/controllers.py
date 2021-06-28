from odoo.addons.portal.controllers.portal import CustomerPortal as CP
from odoo.addons.website_sale.controllers.main import WebsiteSale as WS
from odoo import http
from odoo.http import request
import requests
from datetime import datetime

class CustomerPortal(CP):

    def __init__(self, **args):
        self.MANDATORY_BILLING_FIELDS.extend((
            'street_name',
            'street_number'))
        self.OPTIONAL_BILLING_FIELDS.extend((
            'street_number2',
            'l10n_mx_edi_locality',
            'l10n_mx_edi_colony',
        ))
        if 'street' in self.MANDATORY_BILLING_FIELDS:
            self.MANDATORY_BILLING_FIELDS.remove('street')
        super(CustomerPortal, self).__init__(**args)


class WebsiteSale(WS):

    def _get_mandatory_billing_fields(self):
        flds = super(WebsiteSale, self)._get_mandatory_billing_fields()
        flds.extend(('street_number', 'street_name'))
        if 'street' in flds:
            flds.remove('street')
        return flds

    def _get_mandatory_shipping_fields(self):
        flds = super(WebsiteSale, self)._get_mandatory_shipping_fields()
        flds.extend(('street_number', 'street_name'))
        if 'street' in flds:
            flds.remove('street')
        return flds


class ControllerData(http.Controller):
    
    
    @http.route(['/getToken'], type='json', auth='public', methods=['POST'], website=True, csrf=False)
    def getToken(self, **kw):
        token = request.env.user.company_id.token_cp
        if not token:
            token = ''
        return token