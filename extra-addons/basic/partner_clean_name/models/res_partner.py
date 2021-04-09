# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            self.name = self.name.upper().strip()
    
