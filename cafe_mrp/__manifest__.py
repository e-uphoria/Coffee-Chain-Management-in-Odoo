{
    'name': 'Cafe Manufacturing',
    'version': '1.0',
    'summary': 'Manage production of food and beverages in a café',
    'description': 'Recipes, manufacturing orders, and quality control for a café.',
    'category': 'Manufacturing',
    'author': 'Anjali Sapkota',
    'depends': ['base', 'product', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/cafe_bom_views.xml',
        'report/report_manufacturing_order.xml',
        'views/cafe_mo_views.xml',
        'views/cafe_product_views.xml',
        'views/menu.xml',

    ],
    'installable': True,
    'application': True,
}
