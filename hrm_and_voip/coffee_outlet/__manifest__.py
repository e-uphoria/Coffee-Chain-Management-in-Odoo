{
    'name': 'Coffee Chain Management',
    'version': '1.0',
    'category': 'Operations',
    'summary': 'Manage Coffee Outlets, Employees and Menu',
    'description': 'A module to manage multiple coffee outlets, employees, and menu items.',
    'depends': ['base', 'hr', 'product'],
    'data': [
    'security/ir.model.access.csv',
    'views/coffee_outlet_views.xml',
    'views/outlet_menu.xml',
    'views/coffee_employee_views.xml',
    'views/coffee_employee_stage_views.xml',
    'data/coffee_outlets_data.xml',
    'data/coffee_employees_data.xml',
],

    'installable': True,
    'application': True,
}
