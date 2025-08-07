{
    'name': 'Coffee Supplier Directory',
    'version': '1.0',
    'summary': 'Manage coffee bean suppliers with pipeline and multiple views',
    'description': '''
Supplier Directory for Coffee Chain ERP
=======================================
- Track coffee bean suppliers, contact info, bean origins
- Manage contracts and pricing
- Pipeline stages for supplier relationship management
- Multiple views: Kanban, Tree, Form, Calendar, Pivot, Graph
    ''',
    'author': 'Nush Ojha',
    'category': 'Operations',
    'depends': ['base', 'contacts', 'mail'],
    'data': [
        'security/coffee_supplier_security.xml',
        'security/ir.model.access.csv',
        'security/coffee_supplier_rules.xml',
        'report/coffee_supplier_templates.xml',
        'report/coffee_supplier_report.xml',
        'views/supplier_views.xml',
        'data/stage_data.xml',
        'views/supplier_stage_views.xml',
        
        'views/price_list_views.xml',
        
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'sequence': 10,
}
