# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_applied_programs_with_rewards_on_current_order(self):
        # Need to add filter on current order. Indeed, it has always been calculating reward line even if on next order (which is useless and do calculation for nothing)
        # This problem could not be noticed since it would only update or delete existing lines related to that program, it would not find the line to update since not in the order
        # But now if we dont find the reward line in the order, we add it (since we can now have multiple line per  program in case of discount on different vat), thus the bug
        # mentionned ahead will be seen now
        print("_get_applied_programs_with_rewards_on_current_order")
        if self.code_promo_program_id.filtered(lambda p: p.promo_applicability == 'on_current_order'):
            for prom in self.code_promo_program_id.filtered(lambda p: p.promo_applicability == 'on_current_order'):
                self.elimina_lineasdesc(self,prom)
            print("1")
            return self.code_promo_program_id.filtered(lambda p: p.promo_applicability == 'on_current_order')
        a=self.no_code_promo_program_ids.filtered(lambda p: p.promo_applicability == 'on_current_order') + \
               self.applied_coupon_ids.mapped('program_id') + \
               self.code_promo_program_id.filtered(lambda p: p.promo_applicability == 'on_current_order')
        print(a)
        return a

    def _get_applied_programs_with_rewards_on_next_order(self):
        if self.code_promo_program_id.filtered(lambda p: p.promo_applicability == 'on_next_order'):
            for prom in self.code_promo_program_id.filtered(lambda p: p.promo_applicability == 'on_next_order'):
                self.elimina_lineasdesc(self,prom)
            return self.code_promo_program_id.filtered(lambda p: p.promo_applicability == 'on_next_order')
        return self.no_code_promo_program_ids.filtered(lambda p: p.promo_applicability == 'on_next_order') + \
            self.code_promo_program_id.filtered(lambda p: p.promo_applicability == 'on_next_order')
    
    
    def elimina_lineasdesc(self,order,prom):
        for line in order.order_line:
            if line.is_reward_line:
                print(line.product_id.name)
                if line.product_id!=prom.discount_line_product_id:
                    line.unlink()

    def _get_reward_values_discount(self, program):
        print("Extension Crea Descuento")
        context=self.env.context
        es_website=context.get('website_id')
        print(context)
        print(program)
        for order in self:
            if not es_website:
                self.elimina_lineasdesc(order,program)
                    
        return super(SaleOrder,self)._get_reward_values_discount(program)

    def _get_reward_values_product(self, program):
        print("Desc Producto")
        context=self.env.context
        es_website=context.get('website_id')
        for order in self:
            if not es_website:
                self.elimina_lineasdesc(order,program)
        return super(SaleOrder,self)._get_reward_values_product(program)

