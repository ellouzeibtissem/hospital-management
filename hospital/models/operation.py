from odoo import api, fields, models, _



class HospitalOperation(models.Model):
    _name = "hospital.operation"
    _description = "hospital Operation"
    _log_access = False 
    doctor_id = fields.Many2one('res.users', string='Doctor', tracking=True)





