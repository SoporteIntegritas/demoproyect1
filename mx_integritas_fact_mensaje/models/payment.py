# coding: utf-8

import datetime

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

class PaymentTransaction(models.Model):
    _inherit = "payment.transaction"
    @api.multi
    def _post_process_after_done(self):
        try:
            #self = self._check_context_lang()
            self._reconcile_after_transaction_done()
            self._log_payment_transaction_received()
            self.write({'is_processed': True})
            return True
        except Exception as e:
            _logger.exception(e)
            return False

