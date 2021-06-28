from odoo import _, api, fields, models, tools

class ResPartner(models.Model):
    _inherit = ['res.partner']

    l10n_mx_edi_usage_partner = fields.Selection ([
        ('G01', 'Adquisición de mercancías'),
        ('G02', 'Devoluciones, descuentos o bonificaciones'),
        ('G03', 'Gastos generales'),
        ('I01', 'Construcciones'),
        ('I02', 'Inversión en mobiliario y equipo de oficina'),
        ('I03', 'Equipo de transporte'),
        ('I04', 'Equipos y accesorios informáticos'),
        ('I05', 'Dados, matrices, moldes, matrices y utillaje'),
        ('I06', 'Comunicaciones telefónicas'),
        ('I07', 'Comunicaciones por satélite'),
        ('I08', 'Otra maquinaria y equipo'),
        ('D01', 'Gastos médicos, dentales y hospitalarios'),
        ('D02', 'Gastos médicos por discapacidad'),
        ('D03', 'Gastos funerarios'),
        ('D04', 'Donaciones'),
        ('D05', 'Intereses reales efectivamente pagados por préstamos hipotecarios (casa habitación)'),
        ('D06', 'Contribuciones voluntarias al SAR'),
        ('D07', 'Primas de seguro médico'),
        ('D08', 'Gastos obligatorios de transporte escolar'),
        ('D09', 'Depósitos en cuentas de ahorro, primas basadas en planes de pensiones'),
        ('D10', 'Pagos por servicios educativos (Colegiatura)'),
        ('P01', 'Por definir'),
    ], string = 'Uso',  default='P01',
        help='Usado en CFDI 3.3 para expresar la clave del uso que '
         'le da al destinatario esta factura. Este valor está definido por el '
         'cliente. \n Nota: No es motivo de cancelación si el conjunto de claves es '
         'no el uso que le dará al receptor del documento.')
