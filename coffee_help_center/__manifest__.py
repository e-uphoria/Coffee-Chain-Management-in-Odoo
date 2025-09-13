{
    'name': 'Coffee Chain Help Center',
    'version': '1.0',
    'category': 'Tools',
    'summary': 'Dynamic Help Pages inside Coffee Chain ERP',
    'author': 'Nush Ojha',
    'depends': ['base', 'web', 'website'],
    'data': [
        'security/ir.model.access.csv',
        'views/help_article_views.xml',         # load views first
        'views/help_article_menu.xml',          # then menu & actions
        'views/help_article_erp_menu.xml',     # ERP menu/action
        'views/website_help_templates.xml',    # website templates last
    ],

    'installable': True,
    'application': True,
}
