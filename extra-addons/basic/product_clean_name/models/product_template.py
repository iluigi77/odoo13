# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            self.name = self.name.upper().strip()
    
