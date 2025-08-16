from odoo import models, fields

class CafeQualityCheck(models.Model):
    _name = 'cafe.qc'
    _description = 'Quality Check'

    manufacturing_order_id = fields.Many2one('cafe.manufacturing.order', string='Manufacturing Order', required=True, ondelete='cascade')
    check_date = fields.Datetime(string='Check Date', default=fields.Datetime.now)
    checked_by = fields.Char(string='Checked By')
    result = fields.Selection([('pass', 'Pass'), ('fail', 'Fail')], string='Result')
    notes = fields.Text(string='Notes')
