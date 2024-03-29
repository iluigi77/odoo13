# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

def get_month(argument):
    switcher = {
        1: 'Enero',
        2: 'Febrero',
        3: 'Marzo',
        4: 'Abril',
        5: 'Mayo',
        6: 'Junio',
        7: 'Julio',
        8: 'Agosto',
        9: 'Septiembre',
        10: 'Octubre',
        11: 'Noviembre',
        12: 'Diciembre'
    }
    return switcher.get(argument, 'es inválido')


class posik_project(models.Model):
    _inherit = 'project.task'

    client_id = fields.Many2one('res.partner', string='Cliente', required= True)
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
    # _order = 'pic_activity'

    def _get_hour(self):
        now= datetime.datetime.now()
        h_to_m= now.hour * 60
        minutes= h_to_m + now.minute
        return minutes/60 if minutes>0 else 0
    
    client_id = fields.Many2one('res.partner', string='Cliente' ,required= True)
    web_client = fields.Many2one('posik_client.web_site', string='Sitio Web', required= True, domain="[('client_id', '=', client_id)]" )
    seccion_id = fields.Many2one('posik_client.informe_seccion', string='Sección', required= True)
    subseccion_id = fields.Many2one('posik_client.informe_subseccion', string='Subsección', domain="[('parent_seccion_id', '=', seccion_id)]")
    url = fields.Char(string= 'URL')
    pic_activity = fields.Binary(string='Foto de Actividad')
    short_timesheet = fields.Boolean(string="Parte corta", default= False)

    date_informe = fields.Date(string='Fecha de Informe', required= True, default= lambda self: datetime.datetime.now())
    month_informe = fields.Char(string='Mes de informe', required= True, compute='_onchange_date_informe')
    hour_create = fields.Float(string='Hora Creación', default=_get_hour)

    @api.onchange('date_informe')
    def _onchange_date_informe(self):
        for this in self:
            if this.date_informe:
                month= get_month(this.date_informe.month)
                this.month_informe= month + ' '+str(this.date_informe.year)

    @api.onchange('seccion_id')
    def _onchange_seccion_id(self):
        self.subseccion_id= None if not self.seccion_id.subseccion_id else self.seccion_id.subseccion_id[0]

    @api.onchange('client_id')
    def _onchange_client_id(self):
        self.web_client= None if not self.client_id.web_site else self.client_id.web_site[0]

class ResPartner(models.Model):
    _inherit = 'res.partner'

    activity_id = fields.One2many('account.analytic.line', 'client_id', string='Actividades')
    task_id = fields.One2many('project.task', 'client_id', string = 'Tareas Asociadas')
