{
    'name': 'Coffee Chain ERP',
    'version': '1.0',
    'summary': 'Manage coffee outlets',
    'author': 'Nush Ojha',
    'category': 'Management',
    'depends': ['base', 'crm', 'sale'],
    'data': ['views/coffee_views.xml',
             'data/coffee_outlet_data.xml',
             'security/ir.model.access.csv'],
    'installable': True,
    'application': True,
}
