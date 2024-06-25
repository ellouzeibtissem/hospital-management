from odoo import api, fields, models, _


class ResGroups(models.Model):
    _inherit = "res.groups"

    # def get_application_groups(self, domain):
    #     group_id = self.env.ref('stock.group_stock_picking_wave').id
    #     res = super(ResGroups, self).get_application_groups(domain + [('id', '!=', group_id)])
    #     return res
