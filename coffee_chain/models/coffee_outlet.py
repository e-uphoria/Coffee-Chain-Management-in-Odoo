from odoo import models, fields, api

class CoffeeOutlet(models.Model):
    _name = 'coffee.outlet'
    _description = 'Coffee Outlet'

    name = fields.Char(string="Outlet Name", required=True)
    location = fields.Char(string="Location")
    manager = fields.Char(string="Manager")
    code = fields.Char(string="Code", required=True, help="Short code for the outlet, e.g., KTM-01")
    phone = fields.Char(string="Phone")
    email = fields.Char(string="Email")
    state = fields.Selection([('active', 'Active'), ('inactive', 'Inactive')], default='active')
    outlet_type = fields.Selection([('owned', 'Owned'), ('franchise', 'Franchise')], string="Outlet Type")


    # Link to CRM Customers
    customer_id = fields.Many2one('res.partner', string='Customer')

    # Link to CRM Leads/Opportunities
    lead_id = fields.Many2one('crm.lead', string='Related Lead')
    sale_order_ids = fields.One2many('sale.order', 'outlet_id', string="Sales Orders")


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



