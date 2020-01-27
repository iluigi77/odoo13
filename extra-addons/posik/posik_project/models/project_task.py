# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class posik_project(models.Model):
    _inherit = 'project.task'

    client_id = fields.Many2one('res.partner', string='Cliente', required= True)

    @api.onchange('client_id')
    def _onchange_client_id(self):
        for line in self.timesheet_ids:
            line.web_client= None
            line.client_id= self.client_id

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    def _get_today(self):
        return datetime.datetime.today()


    date_init = fields.Date(string='Fecha de Inicio', default=_get_today,  readonly='1')
    client_id = fields.Many2one('res.partner', string='Cliente' ,required= True)
    web_client = fields.Many2one('posik_client.web_site', string='Sitio Web', required= True, domain="[('client_id', '=', client_id)]" )
    seccion_id = fields.Many2one('posik_client.informe_seccion', string='Sección', required= True)
    subseccion_id = fields.Many2one('posik_client.informe_subseccion', string='Subsección', domain="[('parent_seccion_id', '=', seccion_id)]")
    url = fields.Char(string= 'URL')
    pic_activity = fields.Binary(string='Foto de Actividad')

    @api.onchange('seccion_id')
    def _onchange_seccion_id(self):
        self.subseccion_id= None

    # @api.onchange('client_id')
    # def _get_task_client(self):
    #     return self.task_id

class ResPartner(models.Model):
    _inherit = 'res.partner'

    activity_id = fields.One2many('account.analytic.line', 'client_id', string='Actividades')
