# -*- coding: utf-8 -*-
from  odoo import  api, fields, models, _

class HospitalDoctor(models.Model):
    _name = "hospital.doctor"
    _inherit = ["mail.thread", 'mail.activity.mixin']
    _description = "Hospital Doctor"

    name = fields.Char(string='Name', tracking=True)

    # (copy="False") means this field not copied
    age = fields.Integer(string='Age', tracking=True, copy="False")
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, default='male', tracking=True)

    note = fields.Text(string='Description')
    image = fields.Binary(string="Doctor image")


    # override the copy function
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            # _() means translate
            default['name'] = _("%s (Copy)", self.name)
        default['note'] = "Copied Record"
        return super(HospitalDoctor, self).copy(default=default)