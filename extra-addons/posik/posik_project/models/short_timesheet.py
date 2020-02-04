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

class ShortTimeSheet(models.Model):
    _name = 'posik_project.short_timesheet'
    _description = 'timesheet with short time'

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

    task_id = fields.Many2one('project.task', string='Tarea')
    timesheet_ids = fields.One2many('account.analytic.line', 'parent_timesheet_id', string='Tareas Cortas')
    name = fields.Char(string='Descripción', required= True)
    unit_amount= fields.Float(string='Duración', widget="timesheet_uom")
    project_id = fields.Many2one('project.project', string='Projecto', default=lambda self: self.env.context.get('default_project_id'),
        index=True, tracking=True, check_company=True, change_default=True)


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

    def open_wizard(self): 
        if self.short_timesheet: 
            return False 
        else: 
            return { 
                'tag' : 'reload', 
                'type' : 'ir.actions.act_window', 
                'name': 'SubActividades', 
                'res_model': 'posik_project.short_timesheet', 
                'view_mode': 'form', 
                'view_id ref="posik_project_short_timesheet_form_view"': '', 
                'target': 'new', 
                # 'domain': "[('parent_timesheet_id', '=', %s)]" % self.id, 
                'context': { 
                    'default_project_id': self.project_id.id, 
                    'default_client_id': self.client_id.id,  
                    'default_tasker_id': self.task_id.id,  
                    # 'default_parent_timesheet_id': self.id,  
                    'default_name':'' 
                    }, 
                # 'limit': 1 
            } 


class AccountAnalyticLine(models.Model):
    _inherit= 'account.analytic.line'

    parent_timesheet_id = fields.Many2one('posik_project.short_timesheet', string='Nodo Padre')

class ProjectTask(models.Model):
    _inherit= 'project.task'

    short_timesheet_ids = fields.One2many('posik_project.short_timesheet', 'task_id',string='Parte Corta')
