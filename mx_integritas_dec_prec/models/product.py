# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import re

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
from odoo.osv import expression

from odoo.addons import decimal_precision as dp

from odoo.tools import float_compare, pycompat


class ProductProduct(models.Model):
    _inherit = 'product.template'

    volume = fields.Float('Volume', help="The volume in m3.",digits=dp.get_precision('Stock Volumen'))