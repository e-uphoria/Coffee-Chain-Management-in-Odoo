{
    'name': 'Coffee Chain ERP',
    'version': '1.0',
    'summary': 'Manage coffee outlets',
    'author': 'Nush Ojha',
    'category': 'Management',
    'depends': ['base', 'crm', 'sale', 'account', 'sale_management', 'stock', 'point_of_sale', 'pos_restaurant', 'web', 'website'],
    'data': ['security/ir.model.access.csv',
             'views/coffee_views.xml', 
             'views/coffee_help_views.xml',
             'views/sales_reporting_views.xml',
             'views/coffee_pos_views.xml', 
             'data/coffee_outlet_data.xml',
             ],
    'assets': {
    
    'point_of_sale.assets': [
        'coffee_chain/static/src/js/coffee_pos.js',
        'coffee_chain/static/src/js/pos_customization.js',
        'coffee_chain/static/src/xml/coffee_pos_templates.xml',
    ],
},

    'installable': True,
    'application': True,
}