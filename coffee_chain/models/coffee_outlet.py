from odoo import models, fields

class CoffeeOutlet(models.Model):
    _name = 'coffee.outlet'
    _description = 'Coffee Outlet'

    name = fields.Char(string="Outlet Name", required=True)
    location = fields.Char(string="Location")
    manager = fields.Char(string="Manager")
