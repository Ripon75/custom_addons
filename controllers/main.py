from odoo import http
from odoo.http import request

class Hospital(http.Controller):
    # simple controller create
    @http.route('/patients/',website=True, auth='public')
    def hospital_patient(self, **kw):
        # hospital.patient = model_name
        patients = request.env['hospital.patient'].sudo().search([])
        # patients_image = request.env['res.partner'].sudo().search([])
        # om_hospital.patients_page = module_name . template_id
        return request.render("om_hospital.patients_page",{
            'patients': patients
        })

    # change dynamic information
    @http.route('/patients/details/<model("hospital.patient"):sp>/', website=True, auth='public')
    def patient_details(self, sp):
        return http.request.render("om_hospital.patient_details_info", {
            'patient_details': sp
        })

    class Customer(http.Controller):
        # simple controller create
        @http.route('/customer/', website=True, auth='public')
        def customer_information(self, **kw):
            # hospital.patient = model_name
            customer_info = request.env['res.partner'].sudo().search([])
            return request.render("om_hospital.customer_page", {
                'customer_info': customer_info
            })




