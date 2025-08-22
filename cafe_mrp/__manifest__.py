{
    'name': 'Mrp Calendar',
    'version': '1.0',
    'category': 'Manufacturing',
    'summary': 'Customizations for Manufacturing Orders in MyERP with Google Calendar integration',
    'depends': ['mrp'],  # standard MRP + Google Calendar
    'data': [
        'security/ir.model.access.csv',
        'views/mrp_google_calendar_views.xml',
    ],
    'installable': True,
    'application': False,
}
