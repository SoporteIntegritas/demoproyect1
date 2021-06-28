#-*- coding: utf-8 -*-
from odoo import http
import json
import logging
import pprint

import requests
import werkzeug
from werkzeug import urls

from odoo import http
from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.http import request
from odoo.addons.mx_integritas_payment_baz.models.payment import *
from datetime import datetime



_logger = logging.getLogger(__name__)


class BazController(http.Controller):
    _notify_url = '/payment/baz/ipn/'
    _return_url = '/payment/baz/dpn/'
    _cancel_url = '/payment/baz/cancel/'

    def _parse_pdt_response(self, response):
        lines = [line for line in response.split('\n') if line]
        status = lines.pop(0)

        pdt_post = {}
        for line in lines:
            split = line.split('=', 1)
            if len(split) == 2:
                pdt_post[split[0]] = urls.url_unquote_plus(split[1])
            else:
                _logger.warning('Baz: error processing pdt response: %s', line)

        return status, pdt_post

    def baz_validate_data(self, **post):
        res = False
        post['cmd'] = '_notify-validate'
        self_request = http.request.env['payment.acquirer'].sudo()
        xml_encrypt = post.get('doc').replace(" ","+")
        #_logger.exception("BAZ_ERROR: " + str(xml_encrypt))
        if xml_encrypt:
            xml = None
            try:
                xml = PaymentAcquirerBaz.decrypt_with_AES(self_request, xml_encrypt)
            except:
                return False
            autorizacion = PaymentAcquirerBaz.getTag(self_request, "autorizacion", xml)
            
            codigo_operacion = PaymentAcquirerBaz.getTag(self_request, "codigo_operacion", xml)
            descripcion_codigo = PaymentAcquirerBaz.getTag(self_request, "descripcion_codigo", xml)
            errorFlujo = PaymentAcquirerBaz.getTag(self_request, "errorFlujo", xml)
            folio = PaymentAcquirerBaz.getTag(self_request, "folio", xml)
            idTransaccion = PaymentAcquirerBaz.getTag(self_request, "idTransaccion", xml)
            monto = PaymentAcquirerBaz.getTag(self_request, "monto", xml)
            referencia = PaymentAcquirerBaz.getTag(self_request, "referencia", xml)
            error_baz = str(codigo_operacion)+": "+str(descripcion_codigo)
            #validacion id_transaccion
            payment_validation = request.env['payment.transaction'].sudo().search([('reference', '=', idTransaccion)])
            if codigo_operacion == "00" and idTransaccion:
                tx = None
                tx = request.env['payment.transaction'].sudo().search([('reference', '=', idTransaccion)])
                if not tx:
                    _logger.warning('received notification for unknown payment reference')
                    payment_validation.write({"baz_txn_status": error_baz}) 
                    return False
                res = request.env['payment.transaction'].sudo().form_feedback(post, 'baz')
                payment_validation.write({"baz_txn_status": error_baz})   
                return True
            else :
                payment_validation._set_transaction_error(error_baz)   
                _logger.exception("BAZ_ERROR: "+ error_baz)
                payment_validation.write({"baz_txn_status": error_baz}) 
                return False



    @http.route('/payment/baz/ipn/', type='http', auth='public', methods=['POST'], csrf=False)
    def baz_ipn(self, **post):
        try:
            self.baz_validate_data(**post)
        except ValidationError:
            _logger.exception('Unable to validate the Baz payment')
        return ''
    
    @http.route('/process_baz', type='http', auth='public', methods=['POST'], csrf=False)
    def baz_process(self, **post):
        tipo_operacion = 'ecommerce3D'
        amount = str(post.get('amount'))
        email = post.get('email').lower()
        item_number = post.get('item_number')
        item_name = post.get('item_name')
        ip_address = request.httprequest.environ['REMOTE_ADDR']
        nav = request.httprequest.environ['HTTP_USER_AGENT']
        url_procedencia = str(request.httprequest.environ['HTTP_REFERER']) + '/baz'
        self_request = http.request.env['payment.acquirer'].sudo()
        data = request.httprequest.environ
        afiliacion = str(self_request.search(['|',('provider', '=', 'baz'),('provider', '=', 'Baz')]).baz_afiliacion)
        id_sesion, id_transaccion = PaymentAcquirerBaz.getSession(self_request,item_number)
        if amount and email and item_number and item_name and id_transaccion and ip_address and url_procedencia and data:
            size_amount = len(amount)
            num = ""
            _logger.warning('Amount = ' + str(amount)) 
            _logger.warning('item_name = ' + str(item_name))
            _logger.warning('item_number = ' + str(item_number))
            
            if '.' in amount:
                amountArr = amount.split(".")
                part1 = amountArr[0]
                part2 = amountArr[1]

                if len(part2) == 1:
                    part2 = part2 + "0"
                elif len(part2) == 0:
                    part2 = part2 + "00"
                elif len(part2) > 2:
                    part2 = part2[0:2]

                ceros = 15 - len(part1)
                
                for i in range(ceros):
                    num = num + "0"
                num = num + str(part1) + str(part2)

                url = PaymentAcquirerBaz.getUrl(self_request, "request")
                sku = "Venta en linea para el pedido " + str(item_number)
                params =  '<bancoazteca><tipoOperacion>'+tipo_operacion+'</tipoOperacion><correoComprador>'+str(email)+'</correoComprador><idSesion>'+str(id_sesion)+'</idSesion><idTransaccion>'+str(id_transaccion)+'</idTransaccion><afiliacion>'+str(afiliacion)+'</afiliacion><monto>'+str(num)+'</monto><ipComprador>'+str(ip_address)+'</ipComprador><navegador>'+str(nav)+'</navegador><sku>'+str(sku)+'</sku><url>'+str(url_procedencia)+'</url></bancoazteca>'
                url_final = url + PaymentAcquirerBaz.encrypt_with_AES(self_request,params)
                return werkzeug.utils.redirect(url_final)
            else:
                return None
        else:
            return None

    @http.route('/shop/payment/baz', type='http', auth="public", methods=['GET'], csrf=False)
    def baz_dpn(self, **post):
        try:
            res = self.baz_validate_data(**post)
        except ValidationError:
            _logger.exception('Unable to validate the BAZ payment')
        return werkzeug.utils.redirect('/payment/process')

    @http.route('/payment/baz/cancel', type='http', auth="public", csrf=False)
    def baz_cancel(self, **post):
        """ When the user cancels its Baz payment: GET on this route """
        _logger.warning('Beginning Baz cancel with post data %s', pprint.pformat(post))  # debug
        return werkzeug.utils.redirect('/payment/process')

   