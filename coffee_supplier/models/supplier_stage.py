from odoo import models, fields

class CoffeeSupplierStage(models.Model):
    _name = 'coffee.supplier.stage'
    _description = 'Supplier Stage'
    _order = 'sequence, id'

    name = fields.Char(string='Stage Name', required=True)
    sequence = fields.Integer(default=1)
    fold = fields.Boolean(string='Folded in Pipeline')
