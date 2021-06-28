# -*- coding: utf-8 -*-

from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    token_cp = fields.Char(readonly=False,string='Token C.P.')    