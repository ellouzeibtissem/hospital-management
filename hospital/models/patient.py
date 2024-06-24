from odoo import api, fields, models, _
from datetime import date
from odoo.exceptions import ValidationError


class HospitalPatient(models.Model):
    _name = "hospital.patient"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "hospital Patient"

    name = fields.Char(string='Name', tracking=True)
    ref = fields.Char(string='Reference')
    date_of_birth = fields.Date(string='Date of birth')
    age = fields.Integer(string='Age', compute='_compute_age_', tracking=True)
    gender = fields.Selection([('male', 'Male'), ('female', 'Female')], string='Gender', tracking=True,
                              default='female')
    tags = fields.Char(string='Tags')
    active = fields.Boolean(string='Active', default=True)
    appointment_id = fields.Many2one("hospital.appointment", string="Appointment")
    image = fields.Image(string='Image')
    tag_ids = fields.Many2many('patient.tag', string="tags")
    appointment_count = fields.Integer(string="Appointment Count", compute='_compute_appointment_count', store=True)
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointments")
    parent = fields.Char(string="parent")
    marital_status = fields.Selection([('married', 'Married'), ('single', 'Single')], string="marital Status",
                                      tracking=True)
    partner_name = fields.Char(string="Partner Name")

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = self.env['hospital.appointment'].search_count([('patient_id', '=', rec.id)])

    @api.ondelete(at_uninstall=False)
    def _check_appointments(self):
        for rec in self:
            if rec.appointment_ids:
                raise ValidationError(_("You can not delete a patient with appointments!"))

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth and rec.date_of_birth > fields.Date.today():
                raise ValidationError(_("the entered date of birth is not acceptabe !"))

    @api.model
    def create(self, vals):
        print("ibtissem", vals)
        print(".........", self.env['ir.sequence'])
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).create(vals)

    def write(self, vals):
        if not self.ref and not vals.get(''):
            print("write method is triggered", vals)
        return super(HospitalPatient, self).write(vals)

    def action_done(self):
        print("...................")
        return

    @api.depends('date_of_birth')
    def _compute_age_(self):
        print('self...............', self)
        for rec in self:

            today = date.today()
            if rec.date_of_birth:
                rec.age = (today.year - rec.date_of_birth.year)
            else:
                rec.age = 0

    def name_get(self):
        patient_list = []
        for record in self:
            name = record.ref + record.name
            patient_list.append((record.id, name))
        return patient_list

    def action_test(self):
        print("Clicked")
        return