from odoo import models, fields

class CafeProduct(models.Model):
    _name = 'cafe.product'
    _description = 'Cafe Product'

    name = fields.Char(string='Product Name', required=True)
    description = fields.Text(string='Description')
    product_type = fields.Selection([
        ('beverage', 'Beverage'),
        ('food', 'Food'),
        ('other', 'Other'),
    ], string='Product Type', default='other')
    price = fields.Float(string='Price')
    # uom_id = fields.Many2one('uom.uom', string='Unit of Measure', required=True)
