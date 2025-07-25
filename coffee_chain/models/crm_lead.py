from odoo import models, fields

class CrmLead(models.Model):
    _inherit = 'crm.lead'

    coffee_outlet_id = fields.Many2one('coffee.outlet', string='Coffee Outlet')
    coffee_outlet_ids = fields.One2many('coffee.outlet', 'lead_id', string='Coffee Outlets')