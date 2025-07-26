from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    outlet_id = fields.Many2one('coffee.outlet', string='Outlet', required=True)

    service_type = fields.Selection([
        ('dine_in', 'Dine-in'),
        ('takeaway', 'Takeaway'),
    ], string='Service Type', default='dine_in', required=True)

    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('esewa', 'eSewa'),
        ('fonepay', 'Fonepay'),
        ('khalti', 'Khalti'),
        ('connectips', 'ConnectIPS'),
        ('mobile_banking', 'Mobile Banking'),
    ], string='Payment Method', required=True, default='cash')


    @api.model
    def default_get(self, fields_list):
        res = super(SaleOrder, self).default_get(fields_list)
        # Find the "Walk-in Customer" partner
        walkin_customer = self.env['res.partner'].search([('name', '=', 'Walk-in Customer')], limit=1)
        if walkin_customer:
            res['partner_id'] = walkin_customer.id
        return res
