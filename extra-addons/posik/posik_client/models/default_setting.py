# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DefautlText(models.Model):
    _name = 'posik_client.default_setting'
    _description = 'default setting for posik client'

    def _default_text(self):
        text= ''
        if 'default_informe_text' in self.env['posik_client.default_setting']._fields:
            dt= self.env['posik_client.default_setting'].search([], limit= 1)
            if dt:
                text= dt[0].default_informe_text
        return text

    default_informe_text = fields.Text(string="Texto Inicio de Informes", required= True, default= _default_text)

    @api.model
    def create(self, values):
        self.env['posik_client.default_setting'].search([]).unlink()
        return super(DefautlText, self).create(values)

 
class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _default_text(self):
        text= ''
        if 'default_informe_text' in self.env['posik_client.default_setting']._fields:
            dt= self.env['posik_client.default_setting'].search([], limit= 1)
            if dt:
                text= dt[0].default_informe_text
        return text

    informe_text = fields.Text(string="Texto Inicio de Informes", default= _default_text)
    