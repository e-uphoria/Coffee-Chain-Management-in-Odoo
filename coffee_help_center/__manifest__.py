{
    'name': 'Coffee Chain Help Center',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Dynamic Help Pages inside Coffee Chain ERP',
    'author': 'Nush Ojha',
    'depends': ['base', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/help_article_menu.xml',
        'views/help_article_views.xml',
        'views/website_help_templates.xml',
        'views/help_article_erp_menu.xml',
    ],
    'installable': True,
    'application': True,
}
