from odoo import models, fields

class CoffeeOutlet(models.Model):
    _name = 'coffee.outlet'
    _description = 'Coffee Outlet'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    street = fields.Char(string='Street')
    area = fields.Char(string='Area')
    city = fields.Char(string='City')
    state = fields.Char(string='State')
    country = fields.Char(string='Country')
    phone = fields.Char(string='Phone')
    manager_id = fields.Many2one('hr.employee', string='Manager')
    active = fields.Boolean(string='Active', default=True)

