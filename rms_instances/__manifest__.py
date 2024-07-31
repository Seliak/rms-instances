{
    'name': 'Multi-Tenant RMS',
    'version': '17.0.1.0.0',
    'category': 'Custom',
    'summary': 'Manage multi-tenant instances using Docker',
    'author': 'PeGon Gmbh',
    "license": "AGPL-3",
    'depends': ['base'],
    'data': [
        'views/multi_tenant_views.xml',
        'wizards/multi_tenant_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
}
