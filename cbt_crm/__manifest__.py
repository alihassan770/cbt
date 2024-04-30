# -*- coding: utf-8 -*-
{
    'name': "CBT CRM Customization",

    'summary': "This module add some extra fields on lead form and sync fields on contacts with crm lead",

    'description': """
This module add some extra fields on lead form and sync fields on contacts with crm lead
    """,

    'author': "HSxTech",
    'website': "https://www.hsxtech.net",
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','crm','contacts'],
    'data': [
        # 'security/ir.model.access.csv',
        'views/crm_lead.xml',
        'views/res_partner.xml',
    ],
    # only loaded in demonstration mode
    'application': True,
    'installable': True,
}

