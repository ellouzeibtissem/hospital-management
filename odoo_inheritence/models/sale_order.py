from odoo import api, fields, models, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    confirmed_user_id = fields.Many2one('res.users', string='Confirmed User')


# def test_function(self):
#     return
    def action_confirm(self):
        print("success.............")
        super(SaleOrder, self).action_confirm()
        self.confirmed_user_id = self.env.user.id