from odoo import models, fields, api

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

    # Bridge to Odoo Product
    product_id = fields.Many2one('product.product', string="Linked Product", readonly=True, copy=False)

    @api.model
    def create(self, vals):
        record = super().create(vals)
        record._create_or_update_product()
        return record

    def write(self, vals):
        res = super().write(vals)
        for rec in self:
            rec._create_or_update_product()
        return res

    def _create_or_update_product(self):
        Product = self.env['product.product']
        for item in self:
            vals = {
                'name': item.name,
                'list_price': item.price,
                'type': 'consu',
                'sale_ok': True,
                'purchase_ok': False,
            }
            if not item.product_id:
                product = Product.create(vals)
                super(CoffeeMenuItem, item).write({'product_id': product.id})
            else:
                item.product_id.write(vals)
