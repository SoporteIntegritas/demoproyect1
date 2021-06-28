# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCompany(models.TransientModel,):
    _inherit = 'res.company'

    token_cp = fields.Char(related='company_id.token_cp', readonly=False,string='Token C.P.')    