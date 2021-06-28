# -*- coding: utf-8 -*-

from odoo import api, fields, models
import os
import os.path

class mx_integritas_rfc_lista_negra(models.Model):
    _name = "mx_integritas_validacion_rfc.rfc"
    #_inherit = ['mail.thread']
    _description = "RFC Lista Negra"

    name = fields.Char(string='RFC',required=True)
    is_cancelado=fields.Boolean(string='Cancelado',default=False)
    is_condonado=fields.Boolean(string='Condonado',default=False)
    is_retorno_inversiones=fields.Boolean(string='Retorno de Inversiones',default=False)
    is_exigible=fields.Boolean(string='Exigible',default=False)
    is_firmes=fields.Boolean(string='Firmes',default=False)
    is_no_localizado=fields.Boolean(string='No Localizado',default=False)
    is_sentencia=fields.Boolean(string='Sentencia',default=False)
    is_valido=fields.Boolean(string='Valido',default=False)
    is_permitido=fields.Boolean(string='Permitir aun en Lista Negra',default=False)

    is_desvirtuado=fields.Boolean(string='Desvirtuado',default=False)
    is_definitivo=fields.Boolean(string='Definitivo',default=False)
    is_presuntos=fields.Boolean(string='Presuntos',default=False)
    is_sentenciasfavorables=fields.Boolean(string='Sentencias Favorables',default=False)

    @api.multi
    def mx_integritas_proceso_lista_negra_sat(self):
        print("Hola")
        #reset_status=self.env['mx_integritas_validacion_rfc.rfc']
        #reset_status.write({'is_cancelado':False,'is_condonado':False,'is_retorno_inversiones':False,'is_exigible':False,'is_firmes':False,
        #    'is_no_localizado':False,'is_sentencia':False,'is_valido':False})
        #/home/luis/Documentos/scraping/datos_procesados
        directorio="/home/luis/Documentos/scraping/datos_procesados/"
        #self.mx_integritas_send()
        for dirpath,dirnames,filenames in os.walk(directorio):
            cont=0
            for filename in filenames:
                archivo=os.path.join(dirpath,filename)
                f=filename.upper().replace(" ","")
                if(cont>0):
                    break
                if(".CSV" in f):
                    print(f)
                    self.mx_integritas_escribe_tabla(directorio+filename)
                    os.remove(directorio+filename)
                    #print(directorio+filename)
                cont=cont+1
                    

    @api.multi
    def mx_integritas_scraping_archivos(self):
        print("Hola")

    @api.multi
    def mx_integritas_escribe_tabla(self,liga):
        archivo=open(liga,"r",encoding='utf-8')
        for linea in archivo.readlines():
            try:
                cad=linea.split(',')
                print(cad[0])
                print(cad[1])
                rfc_existente=self.env['mx_integritas_validacion_rfc.rfc'].search([('name','=',cad[0])]).id
                print(rfc_existente)
                if(rfc_existente==False):
                    print("Crear")
                    rfc_existente=self.env['mx_integritas_validacion_rfc.rfc'].create({'name':cad[0]})
                f=liga
                print(f)
                if("CANCELADOS" in f and "CANCELADOS_" not in f):
                    rfc_existente.write({'is_cancelado':True})
                if("CONDONADOS" in f and "CONDONADOS_" not in f):
                    rfc_existente.write({'is_condonado':True})
                if("EXIGIBLES" in f):
                    rfc_existente.write({'is_exigible':True})
                if("FIRMES" in f):
                    rfc_existente.write({'is_firmes':True})
                if("NOLOCALIZADOS" in f):
                    rfc_existente.write({'is_no_localizado':True})
                if("RETORNOINVERSIONES" in f):
                    rfc_existente.write({'is_retorno_inversiones':True})
                if("SENTENCIAS" in f):
                    rfc_existente.write({'is_sentencia':True})
                if("CANCELADOS_" in f):
                    rfc_existente.write({'is_cancelado':True})
                if("CONDONADOS_" in f):
                    rfc_existente.write({'is_condonado':True})

                
            except(ConnectionError, Exception):
                print("Error")
        archivo.close()

    @api.multi
    def mx_integritas_send(self):
        template_id=self.env.ref('mx_integritas_validacion_rfc.demo').id
        template=self.env['mail.template'].browse(template_id)
        template.send_mail(self.id,force_send=True)
    
    

