from odoo import models, fields, api

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    
    # Computed field containing only active/seasonal coffee products for this order
    coffee_product_ids = fields.Many2many(
        'product.product',
        compute='_compute_coffee_products',
        string="Available Coffee Products"
    )

    product_id = fields.Many2one(
        'product.product',
        string="Product",
        domain="[('id', 'in', coffee_product_ids)]"
    )

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

    show_customization = fields.Boolean(
        compute='_compute_show_customization', string="Show Customization"
    )

    @api.depends('product_id')
    def _compute_show_customization(self):
        for line in self:
            line.show_customization = line.product_id.categ_id.name == 'Drinks' if line.product_id else False

    @api.depends('order_id.coffee_menu_item_ids')
    def _compute_coffee_products(self):
        for line in self:
            if line.order_id:
                products = line.order_id.coffee_menu_item_ids.filtered(
                    lambda i: i.status in ['active', 'seasonal'] and i.product_id
                ).mapped('product_id')
                line.coffee_product_ids = products
            else:
                line.coffee_product_ids = self.env['product.product']
