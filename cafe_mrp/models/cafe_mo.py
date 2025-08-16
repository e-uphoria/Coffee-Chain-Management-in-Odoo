from odoo import models, fields, api

class CafeQualityCheck(models.Model):
    _name = 'cafe.qc'
    _description = 'Quality Check'

    manufacturing_order_id = fields.Many2one('cafe.manufacturing.order', string='Manufacturing Order', required=True, ondelete='cascade')
    check_date = fields.Datetime(string='Check Date', default=fields.Datetime.now)
    checked_by = fields.Char(string='Checked By')
    result = fields.Selection([('pass', 'Pass'), ('fail', 'Fail')], string='Result')
    notes = fields.Text(string='Notes')

class CafeManufacturingOrder(models.Model):
    _name = 'cafe.manufacturing.order'
    _description = 'Manufacturing Order'

    name = fields.Char(string='MO Reference', required=True, copy=False, readonly=True, default='New')
    product_id = fields.Many2one('cafe.product', string='Product', required=True)
    bom_id = fields.Many2one('cafe.bom', string='BoM', required=True)
    quantity = fields.Float(string='Quantity', required=True, default=1.0)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft')
    qc_ids = fields.One2many('cafe.qc', 'manufacturing_order_id', string='Quality Checks')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('cafe.manufacturing.order') or 'New'
        return super().create(vals)

    def action_start(self):
        self.state = 'in_progress'

    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancelled'
