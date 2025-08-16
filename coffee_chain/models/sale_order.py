from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    outlet_id = fields.Many2one('coffee.outlet', string='Outlet', required=True)
    service_type = fields.Selection([
        ('dine_in', 'Dine-in'),
        ('takeaway', 'Takeaway'),
    ], string='Service Type', default='dine_in', required=True)

    payment_method_id = fields.Many2one(
        'account.payment.method',
        string='Payment Method',
        domain=[('payment_type', '=', 'inbound')]
    )

    coffee_menu_item_ids = fields.Many2many('coffee.menu.item', string='Coffee Menu Items', domain=[('status', 'in', ['active', 'seasonal'])])

    
    @api.onchange('coffee_menu_item_ids')
    def _onchange_coffee_menu_items(self):
        if self.coffee_menu_item_ids:
            self.order_line = [(5, 0, 0)]
            for item in self.coffee_menu_item_ids.filtered(lambda i: i.status in ['active', 'seasonal']):
                if not item.product_id:
                    item._create_or_update_product()
                if item.product_id:
                    self.order_line += [(0, 0, {
                        'product_id': item.product_id.id,
                        'product_uom_qty': 1,
                        'price_unit': item.price,
                        'milk_type': item.milk_type,
                        'size': item.size,
                        'syrup_flavor': item.syrup_flavor,
                        'extra_shot': item.extra_shot,
                    })]



    def _prepare_invoice(self):
        """
        Pass outlet and payment method to invoice.
        """
        invoice_vals = super()._prepare_invoice()
        invoice_vals.update({
            'outlet_id': self.outlet_id.id,
            'payment_method_id': self.payment_method_id.id,
        })
        return invoice_vals

    @api.model
    def default_get(self, fields_list):
        """
        Set default partner as 'Walk-in Customer' and default payment as 'Cash'.
        """
        res = super(SaleOrder, self).default_get(fields_list)

        walkin_customer = self.env['res.partner'].search([('name', '=', 'Walk-in Customer')], limit=1)
        if walkin_customer:
            res['partner_id'] = walkin_customer.id

        cash_method = self.env['account.payment.method'].search([('name', '=', 'Cash')], limit=1)
        if cash_method:
            res['payment_method_id'] = cash_method.id

        return res

  
    @api.model
    def create(self, vals):
        """
        Ensure totals, taxes, and order lines are correctly calculated for multiple coffee menu items,
        including customization options for Drinks.
        """
        if 'coffee_menu_item_ids' in vals and vals['coffee_menu_item_ids']:
            menu_items = self.env['coffee.menu.item'].browse(vals['coffee_menu_item_ids'][0][2])
            order_lines = []
            for item in menu_items:
                if not item.product_id:
                    item._create_or_update_product()
                if item.product_id:
                    # Add order line with customization fields
                    order_lines.append((0, 0, {
                        'product_id': item.product_id.id,
                        'product_uom_qty': 1,
                        'price_unit': item.price,
                        'milk_type': item.milk_type,
                        'size': item.size,
                        'syrup_flavor': item.syrup_flavor,
                        'extra_shot': item.extra_shot,
                    }))
            vals['order_line'] = order_lines
        return super(SaleOrder, self).create(vals)


