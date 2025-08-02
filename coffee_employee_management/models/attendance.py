from odoo import models, fields, api
from datetime import timedelta

class CoffeeAttendance(models.Model):
    _name = 'coffee.attendance'
    _description = 'Coffee Employee Attendance'
    _order = 'check_in desc'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)
    check_in = fields.Datetime(string='Check-In Time', required=True, default=fields.Datetime.now)
    check_out = fields.Datetime(string='Check-Out Time')
    hours_worked = fields.Float(string='Hours Worked', compute='_compute_hours', store=True)
    regular_hours = fields.Float(string='Regular Hours', compute='_compute_hours', store=True)
    overtime_hours = fields.Float(string='Overtime Hours', compute='_compute_hours', store=True)
    note = fields.Text(string='Notes')

    state = fields.Selection([
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], default='pending', string='Status', tracking=True)

    expected_daily_hours = fields.Float(string='Expected Hours', default=4.0,
                                        help='Threshold before overtime kicks in.')

    @api.depends('check_in', 'check_out', 'expected_daily_hours')
    def _compute_hours(self):
        for rec in self:
            if rec.check_in and rec.check_out:
                delta = rec.check_out - rec.check_in
                worked = delta.total_seconds() / 3600.0
                rec.hours_worked = round(worked, 2)
                expected = rec.expected_daily_hours or 4.0
                rec.regular_hours = round(min(worked, expected), 2)
                rec.overtime_hours = round(max(0.0, worked - expected), 2)
            else:
                rec.hours_worked = 0.0
                rec.regular_hours = 0.0
                rec.overtime_hours = 0.0
