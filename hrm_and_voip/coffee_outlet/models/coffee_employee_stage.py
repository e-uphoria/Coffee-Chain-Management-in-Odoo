from odoo import models, fields

class CoffeeEmployeeStage(models.Model):
    _name = 'coffee.employee.stage'
    _description = 'Employee Stage'
    _order = 'sequence, id'

    name = fields.Char(required=True)
    code = fields.Selection([
        ('new', 'New'),
        ('active', 'Active'),
        ('on_leave', 'On Leave'),
        ('inactive', 'Inactive'),
        ('resigned', 'Resigned'),
    ], required=True, default='new')
    sequence = fields.Integer(default=10)