{
    'name': 'eSewa Payment',
    'summary': 'eSewa payment provider for Website/Portal checkout and POS',
    'version': '1.0',
    'author': 'Nush Ojha',
    'category': 'Accounting/Payment Providers',
    'license': 'LGPL-3',
    'depends': ['payment', 'website_sale', 'point_of_sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/payment_provider_data.xml',
        'views/payment_esewa_views.xml',
        'views/payment_esewa_templates.xml',
        'views/pos_esewa_views.xml',
    ],
    'assets': {
        'point_of_sale.assets': [
            'payment_esewa/static/src/pos/esewa_payment.js',
        ],
    },
    'application': False,
    'installable': True,
}
