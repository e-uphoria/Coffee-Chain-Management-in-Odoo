from odoo import models, fields, api

class CoffeeOutlet(models.Model):
    _name = 'coffee.outlet'
    _description = 'Coffee Outlet'

    name = fields.Char(string="Outlet Name", required=True)
    location = fields.Char(string="Location")
    manager = fields.Char(string="Manager")

    # Link to CRM Customers
    customer_id = fields.Many2one('res.partner', string='Customer')

    # Link to CRM Leads/Opportunities
    lead_id = fields.Many2one('crm.lead', string='Related Lead')

    @api.model
    def create(self, vals):
        outlet = super().create(vals)
        # Create a CRM Lead opportunity linked to this outlet
        lead_vals = {
            'name': f'Opportunity for {outlet.name}',
            'partner_id': outlet.customer_id.id or False,
            'coffee_outlet_id': outlet.id,
            'type': 'opportunity',
        }
        lead = self.env['crm.lead'].create(lead_vals)
        outlet.lead_id = lead.id
        return outlet


class ResPartner(models.Model):
    _inherit = 'res.partner'

    coffee_outlet_ids = fields.One2many('coffee.outlet', 'customer_id', string="Coffee Outlets")



