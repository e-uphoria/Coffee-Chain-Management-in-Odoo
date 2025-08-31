# -*- coding: utf-8 -*-
from odoo import api, fields, models


class PosPaymentMethod(models.Model):
    _inherit = "pos.payment.method"

    esewa_use_terminal = fields.Boolean(string="Use eSewa Terminal")
    esewa_provider_id = fields.Many2one("payment.provider", string="eSewa Provider",
                                        domain=[('code', '=', 'esewa')])

    @api.onchange("esewa_use_terminal")
    def _onchange_esewa_use_terminal(self):
        if self.esewa_use_terminal:
            self.use_payment_terminal = True
            self.payment_terminal = "custom"  # generic driver, our JS handles logic
