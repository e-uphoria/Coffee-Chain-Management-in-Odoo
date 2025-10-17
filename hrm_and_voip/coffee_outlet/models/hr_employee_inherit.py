from odoo import models, fields, api

class HREmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    outlet_id = fields.Many2one('coffee.outlet', string='Outlet')
    role = fields.Selection([
        ('manager', 'Manager'),
        ('cashier', 'Cashier'),
        ('waiter', 'Waiter'),
        ('cook', 'Cook'),
        ('barista', 'Barista'),
    ], string='Role', required=True)
    
    stage_id = fields.Many2one(
        'coffee.employee.stage',
        string='Stage',
        group_expand='_read_group_stage_ids',
        tracking=True
    )
    advance_salary = fields.Float(string='Advance Salary', default=0.0, tracking=True)
    is_defaulter = fields.Boolean(string='Defaulter', compute='_compute_defaulter', store=True)

    @api.depends('advance_salary', 'stage_id')
    def _compute_defaulter(self):
        for rec in self:
            rec.is_defaulter = rec.advance_salary > 0 and rec.stage_id and rec.stage_id.code in ['resigned', 'inactive']

    @api.model
    def _read_group_stage_ids(self, stages, domain, order=None, lazy=False):
        return self.env['coffee.employee.stage'].search([], order=order or 'sequence')