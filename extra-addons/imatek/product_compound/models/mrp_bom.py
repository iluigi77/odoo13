# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpBom(models.Model):
    _inherit='mrp.bom'

    main_list = fields.Boolean(string='Lista Principal', default= False)

    @api.constrains('main_list')
    def _constrain_main_list(self):
        if (self.main_list): # si se esta activando la moneda por defecto
            records = self.env['mrp.bom'].search([
                ('main_list', '=', True), 
                ('id', '!=', self.id)
            ])
            for record in records:
                record.main_list = False
        return False
