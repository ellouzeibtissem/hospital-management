from odoo import api, fields, models, _
from datetime import date


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
