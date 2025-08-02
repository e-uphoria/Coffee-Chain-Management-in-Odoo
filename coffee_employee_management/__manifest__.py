{
    'name': 'Coffee Employee & Attendance Management',
    'version': '1.0',
    'summary': 'Manage employees, advance salary, and attendance',
    'category': 'Human Resources',
    'author': 'Nush Ojha',
    'depends': ['base', 'mail', 'hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/employee_views.xml',
        'views/attendance_views.xml',
        
    ],
    'installable': True,
    'application': True,
}