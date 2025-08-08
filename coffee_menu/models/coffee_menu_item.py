from odoo import models, fields

class CoffeeMenuItem(models.Model):
    _name = 'coffee.menu.item'
    _description = 'Coffee Menu Item'
    _order = 'name'

    name = fields.Char(required=True)
    price = fields.Monetary(currency_field='currency_id', required=True)
    image = fields.Image(string="Image",max_width=128, max_height=128)
    
    category = fields.Selection([
        ('drinks', 'Drinks'),
        ('snacks', 'Snacks'),
        ('desserts', 'Desserts'),
        ('vegan', 'Vegan'),
    ], string="Category", required=True)

    description = fields.Text(string="Description")

    milk_type = fields.Selection([
        ('regular', 'Regular Milk'),
        ('skim', 'Skim Milk'),
        ('soy', 'Soy Milk'),
        ('almond', 'Almond Milk'),
        ('oat', 'Oat Milk'),
    ], string="Milk Type")

    size = fields.Selection([
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('large', 'Large'),
    ], string="Size")

    syrup_flavor = fields.Selection([
        ('vanilla', 'Vanilla'),
        ('caramel', 'Caramel'),
        ('hazelnut', 'Hazelnut'),
        ('none', 'None'),
    ], string="Syrup Flavor")

    extra_shot = fields.Boolean(string="Extra Espresso Shot")

    status = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('seasonal', 'Seasonal'),
        ('retired', 'Retired'),
    ], string="Menu Status", default='draft')

    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)