from odoo import models, fields

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    outlet_id = fields.Many2one('coffee.outlet', string='Outlet')

