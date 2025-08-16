def create_access_rights(env):
    # Coffee Attendance access
    if not env['ir.model.access'].search([('name', '=', 'access_coffee_attendance')]):
        env['ir.model.access'].create({
            'name': 'access_coffee_attendance',
            'model_id': env['ir.model'].search([('model', '=', 'coffee.attendance')], limit=1).id,
            'group_id': False,
            'perm_read': True,
            'perm_write': True,
            'perm_create': True,
            'perm_unlink': True,
        })

    # Coffee Employee Stage access
    if not env['ir.model.access'].search([('name', '=', 'access_coffee_employee_stage')]):
        env['ir.model.access'].create({
            'name': 'access_coffee_employee_stage',
            'model_id': env['ir.model'].search([('model', '=', 'coffee.employee.stage')], limit=1).id,
            'group_id': False,
            'perm_read': True,
            'perm_write': True,
            'perm_create': True,
            'perm_unlink': True,
        })
