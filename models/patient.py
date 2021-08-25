# -*- coding: utf-8 -*-
from  odoo import  api, fields, models, _
from odoo.exceptions import ValidationError

class HospitalPatient(models.Model):
    # this model store data into database
    _name = "hospital.patient"

    # for add chatter
    _inherit = ["mail.thread", 'mail.activity.mixin']

    _description = "Hospital Patent"

    # tracking = True means change status of chatter
    name = fields.Char(string='Name', required=True, tracking=True)

    # for serial number (and need data/data.xml)
    reference = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))

    age = fields.Integer(string='Age', tracking=True)

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, default='male', tracking=True)

    note = fields.Text(string='Description')

    # for progressbar
    state = fields.Selection([('draft','Draft'), ('confirm','Confirm'),
                              ('done','Done'),('cancel','Cancel')],default="draft",string="Status", tracking=True)
    # get data from database
    responsible_id = fields.Many2one('res.partner', string="Responsible")

    # count number of appointment which are create
    appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appointment_count')

    image = fields.Binary(string="Patient image")

    phone = fields.Integer(string="Phone")

    # One2many('model_name', 'Many2one field this model' string="")
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointment")


    def _compute_appointment_count(self):
        # when one variable contain multiple value then occur singleton error
        # iterate for remove singleton error
        for rec in self:
            # get number of appointment from hospital.appointment model
            # search_count(ORM) method count matching condition (every model have)
            appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])
            # print(rec.id)
            rec.appointment_count = appointment_count

    def action_confirm(self):
        # self.state = 'confirm' is ok but recommended the bottom iterate
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        # for remove singleton error
        for rec in self:
            rec.state = 'done'

    def action_draft(self):
        # for remove singleton error
        for rec in self:
            rec.state = 'draft'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'


    # overwrite create methode
    # and create sequence number
    @api.model
    def create(self, vals):

        # default note assign by New Patient
        if not vals.get('note'):
            vals['note'] = 'New Patient'
        # new replace by code
        if vals.get('reference', _('New')) == _('New'):
            vals['reference'] = self.env['ir.sequence'].next_by_code('hospital.patient') or _('New')
        res = super(HospitalPatient, self).create(vals)
        # vals = model_name(id)
        # res = record information
        return res


#   overwrite default_get function
#   the default_get function execute when create record and collect default field value
    @api.model
    def default_get(self, fields):
        res = super(HospitalPatient, self).default_get(fields)
        # print("fields---",fields)
        # print("res---",res)
        # set default value female and use condition
        # res['gender'] = 'female'
        return res


    # check the user name exist or nate
    @api.constrains('name')
    def check_name(self):
        for rec in self:
            patients = self.env['hospital.patient'].search([('name', '=', rec.name),('id','!=',rec.id)])
            if patients:
                raise ValidationError("Name %s Already exist" % self.name)


    # check validation
    @api.constrains('age')
    def check_age(self):
        for rec in self:
            if  self.age == 0:
                # _() means translat
                raise ValidationError(_("Age can not be zero"))



    # combination of name and reference
    def name_get(self):
        result = []
        for rec in self:
            name = '['+rec.reference + '] ' +rec.name
            result.append((rec.id, name))
        return result