# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime
from lxml import etree
from dateutil.relativedelta import relativedelta
import re
import logging
from pytz import timezone

import requests

from odoo import api, fields, models
from odoo.addons.web.controllers.main import xml2json_from_elementtree
from odoo.exceptions import UserError
from odoo.tools.translate import _
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT

BANXICO_DATE_FORMAT = '%d/%m/%Y'
DOF_DATE_FORMAT = '%d-%m-%Y'

_logger = logging.getLogger(__name__)
class mx_integritas_tipo_cambio(models.Model):
    #_name = 'mx_integritas_tipo_cambio.tipo_camb'
    _inherit = ['res.company']
    
    def _parse_banxico_data(self, available_currencies):
        if True:
            """Parse function for Banxico provider.
            * With basement in legal topics in Mexico the rate must be **one** per day and it is equal to the rate known the
            day immediate before the rate is gotten, it means the rate for 02/Feb is the one at 31/jan.
            * The base currency is always MXN but with the inverse 1/rate.
            * The official institution is Banxico.
            * The webservice returns the following currency rates:
                - SF46410 EUR
                - SF60632 CAD
                - SF43718 USD Fixed
                - SF46407 GBP
                - SF46406 JPY
                - SF60653 USD SAT - Officially used from SAT institution
            Source: http://www.banxico.org.mx/portal-mercado-cambiario/
            """
            icp = self.env['ir.config_parameter'].sudo()
            token = icp.get_param('banxico_token')

            if not token:
                # https://www.banxico.org.mx/SieAPIRest/service/v1/token
                token = 'd03cdee20272f1edc5009a79375f1d942d94acac8348a33245c866831019fef4'  # noqa
                icp.set_param('banxico_token', token)
            foreigns = {
                # position order of the rates from webservices
                'SF46410': 'EUR',
                'SF60632': 'CAD',
                'SF46406': 'JPY',
                'SF46407': 'GBP',
                'SF60653': 'USD',
            }
            url = 'https://www.banxico.org.mx/SieAPIRest/service/v1/series/%s/datos/%s/%s?token=%s' # noqa
            try:
                date_mx = datetime.datetime.now(timezone('America/Mexico_City'))
                today = date_mx.strftime(DEFAULT_SERVER_DATE_FORMAT)
                yesterday = (date_mx - datetime.timedelta(days=1)).strftime(DEFAULT_SERVER_DATE_FORMAT)
                res = requests.get(url % (','.join(foreigns), yesterday, today, token), verify=False)
                res.raise_for_status()
                #print("https://www.banxico.org.mx/SieAPIRest/service/v1/series/"+','.join(foreigns)+"/datos/"+yesterday+"/"+today+"?token="+token)
                series = res.json()['bmx']['series']
                series = {serie['idSerie']: {dato['fecha']: dato['dato'] for dato in serie['datos']} for serie in series if 'datos' in serie}
            except:
                return False
            
            url2 = 'https://sidofqa.segob.gob.mx/dof/sidof/indicadores/158/%s/%s' # noqa
            
            valor_dollar_dof = 0.0
            valor_dof_correct = False
            try:
                date_mx = datetime.datetime.now(timezone('America/Mexico_City'))  
                today = date_mx.strftime(DOF_DATE_FORMAT)
                #print('https://sidofqa.segob.gob.mx/dof/sidof/indicadores/158/'+today+'/'+today)
                res2 = requests.get(url2 % (today,today), verify=False)
                res2.raise_for_status()
                valor_dollar_dof = float(res2.json()['ListaIndicadores'][0]['valor'])
                fecha_dof_tipo_cambio = res2.json()['ListaIndicadores'][0]['fecha']
                valor_dof_correct = True
            except:
                valor_dof_correct = False
                print("----- > ERRORRRR")
                return False
            
            available_currency_names = available_currencies.mapped('name')

            rslt = {
                'MXN': (1.0, fields.Date.today().strftime(DEFAULT_SERVER_DATE_FORMAT)),
            }

            today = date_mx.strftime(BANXICO_DATE_FORMAT)
            yesterday = (date_mx - datetime.timedelta(days=1)).strftime(BANXICO_DATE_FORMAT)
            for index, currency in foreigns.items():
                if not series.get(index, False):
                    if valor_dof_correct:
                        #SOlo se agrega el tipo de cambio de la DOF por que no hay actualizacion en banxico para Algun elemento del array
                        foreign_rate_date_dof = datetime.datetime.strptime(fecha_dof_tipo_cambio, DOF_DATE_FORMAT).strftime(DEFAULT_SERVER_DATE_FORMAT)
                        rslt["USD"] = (1.0/valor_dollar_dof, foreign_rate_date_dof)
                        return rslt
                    else: 
                        return False
                if currency not in available_currency_names:
                    continue
                serie = series[index]

                for rate in serie:
                    try:
                        foreign_mxn_rate = float(serie[rate])
                    except (ValueError, TypeError):
                        return False
                    foreign_rate_date = datetime.datetime.strptime(rate, BANXICO_DATE_FORMAT).strftime(DEFAULT_SERVER_DATE_FORMAT)
                    if currency != 'USD':
                        rslt[currency] = (1.0/foreign_mxn_rate, foreign_rate_date)
                    else:
                        rslt[currency] = (1.0/valor_dollar_dof, foreign_rate_date)
                        print("-----> TIPO DE CAMBIO DIARIO DE LA FEDERACIÓN")
            return rslt 
