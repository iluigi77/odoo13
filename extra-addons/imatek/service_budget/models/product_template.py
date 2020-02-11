# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    no_budgetable = fields.Boolean(string='No presupuestable', default= False)

    @api.onchange('type')
    def _on_change_type(self):
        self.no_budgetable=  True if (self.type== 'service') else False
        