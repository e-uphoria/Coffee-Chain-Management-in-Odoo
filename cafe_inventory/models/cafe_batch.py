from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import date

class CafeBatch(models.Model):
    _name = "cafe.batch"
    _description = "Cafe Batch / Lot (lightweight over stock.lot)"

    name = fields.Char(
        required=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('cafe.batch') or 'New'
    )
    product_id = fields.Many2one('cafe.product', string='Product', required=True)
    qty = fields.Float(default=0.0)
    expiry_date = fields.Date()
    outlet_id = fields.Many2one('coffee.outlet', string="Outlet")
    is_expired = fields.Boolean(compute="_compute_is_expired", store=True)

    @api.depends('expiry_date')
    def _compute_is_expired(self):
        today = date.today()
        for r in self:
            r.is_expired = bool(r.expiry_date and r.expiry_date < today)

    @api.model
    def create(self, vals):
        product_id = vals.get('product_id')
        if not self.env['cafe.product'].browse(product_id).exists():
            raise UserError("Selected product does not exist.")

        outlet_id = vals.get('outlet_id')
        if outlet_id and not self.env['coffee.outlet'].browse(outlet_id).exists():
            raise UserError("Selected outlet does not exist.")

        if vals.get('qty', 0) < 0:
            raise UserError("Quantity cannot be negative.")

        return super(CafeBatch, self).create(vals)
