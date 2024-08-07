from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HospitalAppointment(models.Model):
    _name = "hospital.appointment"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "hospital Appointment"
    _rec_name = 'ref'
    _order = 'id desc'

    patient_id = fields.Many2one('hospital.patient', string="patient", ondelete='cascade')
    operation_id = fields.Many2one('hospital.operation', string="operation")
    gender = fields.Selection(related='patient_id.gender')
    appointment_time = fields.Datetime(string='Appointment Time', default=fields.Datetime.now)
    booking_date = fields.Date(string=' Booking Date', default=fields.Date.context_today)
    ref = fields.Char(string='Reference', help="Reference from patient record")
    prescription = fields.Html(string='prescription')
    priority = fields.Selection([('0', 'Normal'), ('1', 'Low'), ('2', 'High'), ('3', 'very_High')], string='Priority')
    state = fields.Selection(
        [('draft', 'Draft'), ('in_consultation', 'In Consultation'), ('done', 'Done'), ('cancel', 'cancelled')],
        default='draft', string='Priority', required=True)
    doctor_id = fields.Many2one('res.users', string='Doctor', tracking=True)
    pharmacy_line_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string="Pharmacy Lines")
    hide_sales_prices = fields.Boolean(string=" Hide Sales Prices")
    # progress = fields.Integer(string="progress", compute='_compute_progress')
    duration = fields.Float(string="Duration")

    def unlink(self):
        if self.state != 'draft':
            raise ValidationError(_("You can delete only appointment in 'Draft' status"))
        return super(HospitalAppointment, self).unlink()

    @api.onchange('patient_id')
    def onchange_patient_id(self):
        self.ref = self.patient_id.ref

    def action_test(self):
        print("button_clicked!!!!!!!!!!")
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'click successfull',
                'type': 'rainbow_man',
            }
        }

    def action_in_consultation(self):
        for rec in self:
            if rec.state == 'draft':
                rec.state = 'in_consultation'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_cancel(self):
        action = self.env.ref('hospital.action_cancel_appointment').read()[0]
        return action

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    # @api.depends('state')
    # def _compute_progress(self):
    #     for rec in self:
    #         if rec.state == 'draft':
    #             progress = 25
    #         elif rec.state == 'in_consultation':
    #             progress = 50
    #         elif rec.state == 'done':
    #             progress = 100
    #         else:
    #             progress = 0
    #             rec.progress = progress
    #

class AppointmentPharmacyLines(models.Model):
    _name = "appointment.pharmacy.lines"
    _description = "Appointment Pharmacy Lines"

    product_id = fields.Many2one('product.product', required=True)
    price_unit = fields.Float(string='Price', related='product_id.list_price')
    quantity = fields.Integer(string='Quantity', default=1)
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment')
