from odoo import models, fields

class CoffeeSupplierPrice(models.Model):
    _name = 'coffee.supplier.price'
    _description = 'Supplier Price List'

    supplier_id = fields.Many2one('coffee.supplier', required=True, ondelete='cascade')
    product_name = fields.Char(string='Product / Bean Type', required=True)
    unit_price = fields.Monetary(string='Unit Price', required=True)
    currency_id = fields.Many2one('res.currency', required=True, default=lambda self: self.env.company.currency_id)
    minimum_order_qty = fields.Float(string='Min Order Qty', default=1.0)
    notes = fields.Text(string='Notes')
