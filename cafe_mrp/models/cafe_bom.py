from odoo import models, fields

class CafeBoMIngredient(models.Model):
    _name = 'cafe.bom.ingredient'
    _description = 'BoM Ingredient Line'

    bom_id = fields.Many2one('cafe.bom', string='BoM', required=True, ondelete='cascade')
    ingredient_id = fields.Many2one('cafe.product', string='Ingredient', required=True)
    quantity = fields.Float(string='Quantity', required=True)

class CafeBoM(models.Model):
    _name = 'cafe.bom'
    _description = 'Recipe BoM'

    name = fields.Char(string='BoM Name', required=True)
    product_id = fields.Many2one('cafe.product', string='Product', required=True)
    ingredient_line_ids = fields.One2many('cafe.bom.ingredient', 'bom_id', string='Ingredients')
