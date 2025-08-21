from odoo import models, fields

class CoffeeHelp(models.Model):
    _name = 'coffee.help'
    _description = 'Coffee Module Help'

    title = fields.Char(string="Title", required=True)
    description = fields.Html(string="Description")
