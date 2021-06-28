# coding: utf-8

import logging
import requests
import pprint
import base64
import hashlib

from requests.exceptions import HTTPError
from werkzeug import urls
from collections import namedtuple

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_round

from odoo.addons.payment.models.payment_acquirer import ValidationError

from Crypto import Random
from Crypto.Cipher import AES
from datetime import datetime
_logger = logging.getLogger(__name__)
class PaymentAcquirerBaz(models.Model):
	_inherit = 'payment.acquirer'
	provider = fields.Selection(selection_add=[('baz', 'Baz')])
	baz_afiliacion = fields.Char('Afiliacion',  groups='base.group_user')#, required_if_provider='baz'
	baz_id_terminal = fields.Char('Id terminal',  groups='base.group_user')#, required_if_provider='baz'
	block_size = 16

 
	pad = lambda self, s: s + (self.block_size - len(s) % self.block_size) * chr(self.block_size - len(s) % self.block_size)
	unpad = lambda self, s: s[0:-ord(s[-1:])]
	iv = "cDRyNG0zN3IwMVY1cHJvZA=="

	secret_key = "QkFOQ09BWlRFQ0ExMjM0NTY3ODkwMTIzNDU2NzhQUjA="
	
	plain_text = "<bancoazteca><tipoOperacion>ecommerce3D</tipoOperacion><correoComprador>edgar.molina@integritas.mx</correoComprador><idSesion>11111111</idSesion><idTransaccion>1000000000001</idTransaccion><afiliacion>7952739</afiliacion><monto>000000000007000</monto><ipComprador>187.140.144.31</ipComprador><navegador>Mozilla/5.0(Windows_NT_10.0;_Win64;_x64;_rv:76.0)_Gecko/20100101_Firefox/76.0</navegador><sku>IMPPREDIAL</sku><url>http://187.217.66.205:99/api/infraccion</url></bancoazteca>"
	plain_text = "<bancoAzteca><eservices><request><canalEntrada>ecommerce</canalEntrada><idterminal>9562</idterminal><tipo_operacion>200</tipo_operacion><idTransaccion>APVV-7043220-2001760800767</idTransaccion></request></eservices></bancoAzteca>"

	def baz_form_generate_values(self, values):
		#base_url = base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
		baz_tx_values = dict(values)
		baz_tx_values.update({
			'cmd': '_xclick',
			'business': self.baz_afiliacion,
			'item_name': '%s: %s' % (self.company_id.name, values['reference']),
			'item_number': values['reference'],
			'amount': values['amount'],
			'currency_code': values['currency'] and values['currency'].name or '',
			'address1': values.get('partner_address'),
			'city': values.get('partner_city'),
			'country': values.get('partner_country') and values.get('partner_country').code or '',
			'state': values.get('partner_state') and (values.get('partner_state').code or values.get('partner_state').name) or '',
			'email': values.get('partner_email'),
			'zip_code': values.get('partner_zip'),
			'first_name': values.get('partner_first_name'),
			'last_name': values.get('partner_last_name'),
			'return_url': "/payment/baz/validate",
			'baz_return': '',
			'notify_url': '',
			'cancel_return': '',
		})
		return baz_tx_values

	def getSession(self,item_number):
		
		headers = {'Content-Type': 'application/xml'}
		canalEntrada = 'ecommerce'
		id_terminal =   str(self.search(['|',('provider', '=', 'baz'),('provider', '=', 'Baz')]).baz_id_terminal)
		tipo_operacion = '200'
		id_transaccion = item_number
		if id_terminal and id_terminal and tipo_operacion and id_transaccion:
			xml='''<?xml version='1.0' encoding='utf-8'?>
			<soapenv:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ser="http://service.btb.com">
			    <soapenv:Header/>
			        <soapenv:Body>
			            <ser:getToken soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
			            <xml xsi:type="xsd:string">
			                <![CDATA[
			                <bancoAzteca><eservices><request><canalEntrada>'''+canalEntrada+'''</canalEntrada><idterminal>'''+id_terminal+'''</idterminal><tipo_operacion>'''+tipo_operacion+'''</tipo_operacion><idTransaccion>'''+id_transaccion+'''</idTransaccion></request></eservices></bancoAzteca>
			                ]]>
			            </xml>
			        </ser:getToken>
			    </soapenv:Body>
			</soapenv:Envelope>'''
			headers = {'SOAPAction': 'add', 'Content-Type': 'text/xml; charset=utf-8'}
			r =requests.post('http://www.puntoazteca.com.mx/BusinessToBusinessWS/services/PB2B?wsdl',headers=headers,data=xml)
			xml=r.text
			xml=xml.replace('<?xml version="1.0" encoding="utf-8"?><soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"><soapenv:Body><ns1:getTokenResponse soapenv:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/" xmlns:ns1="http://service.btb.com"><getTokenReturn xsi:type="xsd:string">&lt;bancoazteca&gt;&lt;eservices&gt;&lt;response&gt;&lt;data_service&gt;&lt;token&gt;','')
			token=xml.replace('&lt;/token&gt;&lt;/data_service&gt;&lt;/response&gt;&lt;/eservices&gt;&lt;/bancoazteca&gt;</getTokenReturn></ns1:getTokenResponse></soapenv:Body></soapenv:Envelope>','')
			return token, id_transaccion
		else:
			return None, None

	def getUrl(self, typeLink):
		if typeLink == 'session':
			url = "https://www.puntoazteca.com.mx/BusinessPAYWeb/RealizaVenta?doc="
		elif typeLink == 'request':
			url = "https://www.puntoazteca.com.mx/BusinessPAYWeb/RealizaVenta?doc="
		return url
	def baz_get_form_action_url(self):
		self.ensure_one()
		url = self.getUrl('request')
		params = "<bancoazteca><tipoOperacion>ecommerce3D</tipoOperacion><correoComprador>correcomprador@gmail.com</correoComprador><idSesion>11111111</idSesion><idTransaccion>1000000000001</idTransaccion><afiliacion>"+self.baz_afiliacion+"</afiliacion><monto>000000000000010</monto><ipComprador>187.140.144.31</ipComprador><navegador>Mozilla/5.0(Windows_NT_10.0;_Win64;_x64;_rv:76.0)_Gecko/20100101_Firefox/76.0</navegador><sku>IMPPREDIAL</sku><url>http://187.217.66.205:99/api/infraccion</url></bancoazteca>"
		
		return "/process_baz/"
	def getAfiliacion(self):
		return self.baz_afiliacion


	def encrypt_with_AES(self, message):
		passs = base64.b64decode(self.secret_key.encode('utf-8'))
		iv_ = base64.b64decode(self.iv.encode('utf-8'))
		message = self.pad(message)
		cipher = AES.new(passs, AES.MODE_CBC, iv_)
		cipher_bytes = base64.b64encode(cipher.encrypt(message))
		return bytes.decode(cipher_bytes)


	def decrypt_with_AES(self, encoded):
		passs = base64.b64decode(self.secret_key.encode('utf-8'))
		iv_ = base64.b64decode(self.iv.encode('utf-8'))
		cipher_text = base64.b64decode(encoded.encode('utf-8'))
		cipher = AES.new(passs, AES.MODE_CBC, iv_)
		plain_bytes = cipher.decrypt(cipher_text[self.block_size:])
		xml = str(plain_bytes) 
		return xml

	def getTag(self, tag, xml):
		tag_apertura = "<"+tag+">"
		tag_cierre = "</"+tag+">"
		n1 = xml.index(tag_apertura)
		n2 = xml.index(tag_cierre)
		return xml[ int(n1) + len(tag_apertura)  : int(n2)]


class TxBaz(models.Model):
	_inherit = 'payment.transaction'

	baz_txn_type = fields.Char('Transaction type')
	baz_txn_status = fields.Char('Approval baz')
	
	@api.model
	def _baz_form_get_tx_from_data(self, data):
		_logger.warning("OOP1")
		xml_encrypt = data.get('doc').replace(" ","+")
		self_request = self.env['payment.acquirer'].sudo()
		if xml_encrypt:
			xml = PaymentAcquirerBaz.decrypt_with_AES(self_request, xml_encrypt)
			autorizacion = PaymentAcquirerBaz.getTag(self_request, "autorizacion", xml)
			codigo_operacion = PaymentAcquirerBaz.getTag(self_request, "codigo_operacion", xml)
			descripcion_codigo = PaymentAcquirerBaz.getTag(self_request, "descripcion_codigo", xml)
			errorFlujo = PaymentAcquirerBaz.getTag(self_request, "errorFlujo", xml)
			folio = PaymentAcquirerBaz.getTag(self_request, "folio", xml)
			idTransaccion = PaymentAcquirerBaz.getTag(self_request, "idTransaccion", xml)
			monto = PaymentAcquirerBaz.getTag(self_request, "monto", xml)
			reference = PaymentAcquirerBaz.getTag(self_request, "referencia", xml)


		_logger.warning("Reference "+str(data))
		if not idTransaccion:
		   error_msg = _('BAZ: received data with missing reference (%s)') % (idTransaccion)
		   _logger.info(error_msg)
		   raise ValidationError(error_msg)

		txs = self.env['payment.transaction'].search([('reference', '=', idTransaccion)])
		if not txs or len(txs) > 1:
		   error_msg = 'Baz: received data for reference %s' % (idTransaccion)
		   if not txs:
		       error_msg += '; no order found'
		   else:
		       error_msg += '; multiple order found'
		   _logger.info(error_msg)
		   raise ValidationError(error_msg)
		return txs[0]

	def _baz_form_get_invalid_parameters(self, data):
		_logger.warning("OOP2")   

	def _baz_form_validate(self, data):
		xml_encrypt = data.get('doc').replace(" ","+")
		self_request = self.env['payment.acquirer'].sudo()
		if xml_encrypt:
			xml = PaymentAcquirerBaz.decrypt_with_AES(self_request, xml_encrypt)
			autorizacion = PaymentAcquirerBaz.getTag(self_request, "autorizacion", xml)
			codigo_operacion = PaymentAcquirerBaz.getTag(self_request, "codigo_operacion", xml)
			descripcion_codigo = PaymentAcquirerBaz.getTag(self_request, "descripcion_codigo", xml)
			errorFlujo = PaymentAcquirerBaz.getTag(self_request, "errorFlujo", xml)
			folio = PaymentAcquirerBaz.getTag(self_request, "folio", xml)
			idTransaccion = PaymentAcquirerBaz.getTag(self_request, "idTransaccion", xml)
			monto = PaymentAcquirerBaz.getTag(self_request, "monto", xml)
			reference = PaymentAcquirerBaz.getTag(self_request, "referencia", xml)
		if codigo_operacion == '00':
			status = "Completed"
		else:
			status = "Failed"
		former_tx_state = self.state
		res = {
		    'acquirer_reference': reference,
		    'baz_txn_type': "Baz",
		    
		}
		

		if codigo_operacion == '00' and status in ['Completed', 'Processed', 'Pending']:
		    template = self.env.ref('payment_baz.mail_template_baz_invite_user_to_configure', False)
		    if template:
		        render_template = template.render({
		            'acquirer': self.acquirer_id,
		        }, engine='ir.qweb')
		        mail_body = self.env['mail.thread']._replace_local_links(render_template)
		        mail_values = {
		            'body_html': mail_body,
		            'subject': _('Add your baz account to Odoo'),
		            'email_to': self.acquirer_id.baz_email_account,
		            'email_from': self.acquirer_id.create_uid.email
		        }
		        self.env['mail.mail'].sudo().create(mail_values).send()

		if status in ['Completed', 'Processed']:
		    try:
		        tzinfos = {
		            'PST': -8 * 3600,
		            'PDT': -7 * 3600,
		        }
		        date = dateutil.parser.parse(data.get('payment_date'), tzinfos=tzinfos).astimezone(pytz.utc).replace(tzinfo=None)
		    except:
		        date = fields.Datetime.now()
		    res.update(date=date)
		    self._set_transaction_done()
		    if self.state == 'done' and self.state != former_tx_state:
		        _logger.info('Validated baz payment for tx %s: set as done' % (self.reference))
		        return self.write(res)
		    return True
		elif status in ['Pending', 'Expired','Failed']:
		    res.update(state_message=data.get('pending_reason', ''))
		    self._set_transaction_pending()
		    if self.state == 'pending' and self.state != former_tx_state:
		        _logger.info('Received notification for baz payment %s: set as pending' % (self.reference))
		        return self.write(res)
		    return True
		else:
		    error = 'Received unrecognized status for baz payment %s: %s, set as error' % (self.reference, status)
		    res.update(state_message=error)
		    self._set_transaction_cancel()
		    if self.state == 'cancel' and self.state != former_tx_state:
		        _logger.info(error)
		        return self.write(res)
		    return True