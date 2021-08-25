# -*- coding: utf-8 -*-
from  odoo import  api, fields, models, _

class CreateAppointmentWizard(models.TransientModel):
    # this model is not store data into database
    _name = "create.appointment.wizard"
    _description = "Create Appointment Wizard"

    date_appointment = fields.Date(string='Date', required=True)
    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True)

    def action_create_appointment(self):
        # set date field using dictionary
        vals = {
            'patient_id': self.patient_id.id,
            'date_appointment': self.date_appointment
        }
        appointment_rec = self.env['hospital.appointment'].create(vals)

       # return view using python code (created wizard show in a new form view)
        return {
            'name': _('Appointment'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hospital.appointment',
            'res_id': appointment_rec.id,
            'target': 'new'
        }

   # filter appointment
    def action_view_appointment(self):
        action = self.env.ref('om_hospital.action_hospital_appointment').read()[0]
        action['domain'] = [('patient_id', '=', self.patient_id.id)]
        return action

