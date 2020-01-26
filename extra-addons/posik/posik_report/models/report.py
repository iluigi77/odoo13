# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class PosikReport(models.Model):
    _name = 'posik_report.posik_report'
    _description = 'posik_report.posik_report'

    def _default_tittle(self):
        text= "Informe de trabajos Mto. Web y Marketing Digital  "
        date= datetime.datetime.today()
        mmyyyy = date.strftime("%m/%Y")
        return text+mmyyyy

    client_id = fields.Many2one('res.partner', string='Cliente')
    tittle= fields.Text(string='Título', default= _default_tittle)

    name_client = fields.Char(string='Nombre del Cliente', compute='_on_change_client_id', readonly="1")
    informe_text_client = fields.Char(string='Texto inicio informes')

    @api.onchange('client_id')
    def _on_change_client_id(self):
        if self.client_id:
            self.name_client= self.client_id.name
            self.informe_text_client= self.client_id.informe_text
    