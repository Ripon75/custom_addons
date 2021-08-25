# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Hospital Management',
    'version' : '1.0',
    'summary': 'Hospital Management Software',
    'sequence': 10,
    'description': """ Hospital Management Software """,
    'category': 'Productivity',
    'website': 'https://www.eorange.shop',

    'depends' : ['sale',
                 'mail'
                 ],
    'data': [
        # first security file
         'security/ir.model.access.csv',
        # second data file
         'data/data.xml',
        # third wizard file
         'wizard/create_appointment_view.xml',
        # forth view file
         'views/patient_view.xml',
         'views/kids_view.xml',
         'views/patient_gender_view.xml',
          'views/appointment_view.xml',
         'views/sale.xml',
         'views/template.xml',
         'views/doctor_view.xml',
         # fifth report file
         'report/report.xml',
         'report/patient_card.xml',

          ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}