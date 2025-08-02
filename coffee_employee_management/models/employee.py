from odoo import models, fields, api

class HREmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    stage_id = fields.Many2one(
        'coffee.employee.stage',
        string='Stage',
        group_expand='_read_group_stage_ids',
        tracking=True
    )
    advance_salary = fields.Float(
        string='Advance Salary Taken',
        default=0.0,
        tracking=True
    )
    is_defaulter = fields.Boolean(
        string='Defaulter',
        compute='_compute_defaulter',
        store=True
    )

    @api.depends('advance_salary', 'stage_id')
    def _compute_defaulter(self):
        """Mark employee as defaulter if they took advance salary and are resigned/inactive."""
        for rec in self:
            if rec.advance_salary > 0 and rec.stage_id and rec.stage_id.code in ['resigned', 'inactive']:
                rec.is_defaulter = True
            else:
                rec.is_defaulter = False

    @api.model
    def _read_group_stage_ids(self, stages, domain, order=None, lazy=False):
        """Ensures stage grouping works in kanban."""
        return self.env['coffee.employee.stage'].search([], order=order or 'sequence')


class CoffeeEmployeeStage(models.Model):
    _name = 'coffee.employee.stage'
    _description = 'Employee Status Stage'
    _order = 'sequence, id'

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    code = fields.Selection([
        ('new', 'New'),
        ('active', 'Active'),
        ('on_leave', 'On Leave'),
        ('inactive', 'Inactive'),
        ('resigned', 'Resigned'),
    ], required=True, default='new')
