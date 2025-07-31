from odoo import models, fields

class CoffeeMenuTag(models.Model):
    _name = 'coffee.menu.tag'
    _description = 'Menu Tag'

    name = fields.Char(required=True)
