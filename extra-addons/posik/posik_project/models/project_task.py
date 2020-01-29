# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class posik_project(models.Model):
    _inherit = 'project.task'

    client_id = fields.Many2one('res.partner', string='Cliente', required= True)
    timesheet_no_time_ids = fields.One2many('account.analytic.line', 'task_id', string= 'Partes de tiempo cortas')
    short_timesheet_hours = fields.Float(string="Horas en partes cortas")

    @api.onchange('short_timesheet_hours','timesheet_ids')
    def _onchange_short_timesheet_hours(self):
        total = 0
        for line in self.timesheet_ids:
            if line.short_timesheet: 
                total = total+1

        # total= total+1 for line in self.timesheet_ids if line.short_timesheet
        media= total if total==0 else self.short_timesheet_hours / total
        for line in self.timesheet_ids:
            if line.short_timesheet:
                line.unit_amount= media

    @api.onchange('client_id')
    def _onchange_client_id(self):
        for line in self.timesheet_ids:
            line.web_client= None if not self.client_id.web_site else self.client_id.web_site[0]
            line.client_id= self.client_id

class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'
    _order = 'pic_activity'

    def _get_today(self):
        return datetime.datetime.now()

    date_init = fields.Datetime(string='Fecha de Inicio', default=_get_today,  readonly='1')
    client_id = fields.Many2one('res.partner', string='Cliente' ,required= True)
    web_client = fields.Many2one('posik_client.web_site', string='Sitio Web', required= True, domain="[('client_id', '=', client_id)]" )
    seccion_id = fields.Many2one('posik_client.informe_seccion', string='Sección', required= True)
    subseccion_id = fields.Many2one('posik_client.informe_subseccion', string='Subsección', domain="[('parent_seccion_id', '=', seccion_id)]")
    url = fields.Char(string= 'URL')
    pic_activity = fields.Binary(string='Foto de Actividad')
    short_timesheet = fields.Boolean(string="Parte corta", default= False)

    @api.onchange('seccion_id')
    def _onchange_seccion_id(self):
        self.subseccion_id= None if not self.seccion_id.subseccion_id else self.seccion_id.subseccion_id[0]

    @api.onchange('client_id')
    def _onchange_client_id(self):
        self.web_client= None if not self.client_id.web_site else self.client_id.web_site[0]

class ResPartner(models.Model):
    _inherit = 'res.partner'

    activity_id = fields.One2many('account.analytic.line', 'client_id', string='Actividades')
