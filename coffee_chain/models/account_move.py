from odoo import models, fields

class AccountMove(models.Model):
    _inherit = 'account.move'

    outlet_id = fields.Many2one('coffee.outlet', string='Outlet')
    payment_method_id = fields.Many2one('account.payment.method', string='Payment Method')
