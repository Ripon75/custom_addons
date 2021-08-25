# -*- coding: utf-8 -*-
from  odoo import  api, fields, models, _
from odoo.exceptions import ValidationError

class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ["mail.thread", 'mail.activity.mixin']
    _description = "Hospital Appointment"

    # order number show descending order
    # _order = 'name desc'

    name = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))

    patient_id = fields.Many2one('hospital.patient', string="Patient Name", required=True)

    # [related = "patient_id.age"] means set patient age automatically
    age = fields.Integer(string='Age', related="patient_id.age", tracking=True)

    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, default='male', tracking=True)

    doctor_id = fields.Many2one('hospital.doctor', string="Doctor")

    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'),
                              ('done', 'Done'), ('cancel', 'Cancel')], default="draft", string="Status", tracking=True)

    note = fields.Text(string='Description')

    date_appointment = fields.Date(string="Date")

    time_appointment = fields.Datetime(string="Set Time")

    prescription = fields.Text(string="Prescription")

    # one2many('model_name','many2one relationship field this model', string="")
    prescription_line_ids = fields.One2many('appointment.prescription.lines', 'appointment_id',
                                            string="Prescription Lines")


    def action_confirm(self):
        self.state = 'confirm'

    def action_done(self):
        self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.state = 'cancel'



    # # overwrite create methode
    @api.model
    def create(self, vals):

        # default note assign by New Patient
        if not vals.get('note'):
            vals['note'] = 'New Patient'
        # new replace by code
        if vals.get('name', _('New')) == _('New'):
            vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        res = super(HospitalAppointment, self).create(vals)
        return res


   # assign related data (when select name automatically select gender)
    @api.onchange('patient_id')
    def onchange_patient_id(self):
        # means if select patient_id (patient name)
        if self.patient_id:
            # if patient have gender
            if self.patient_id.gender:
                # set patient gender
                self.gender = self.patient_id.gender
            # if patient have note/description
            if self.patient_id.note:
                # set patient description
                self.note = self.patient_id.note
        else:
            # if patient not select then gender and note are being empty
            self.gender = ''
            self.note = ''


    # override the unlink method
    def unlink(self):
        if self.state == 'done':
            raise ValidationError("You can not delete %s as the done state" %self.name)
        return super(HospitalAppointment, self).unlink()


    # anather model for one2many relation
class AppointmentPrescriptionLines(models.Model):
    _name = "appointment.prescription.lines"
    _description = "Appointment Prescription Lines"

    name = fields.Char(string="Medicine", required=True)
    quantity = fields.Integer(string="Quantity")
    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")