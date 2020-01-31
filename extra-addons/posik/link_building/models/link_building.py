# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

def get_month(argument):
    switcher = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre"
    }
    return switcher.get(argument, "Mes inválido")
    
class link_building(models.Model):
    _name = 'link_building.link_building'
    _description = 'link_building.link_building'

    def _get_hour(self):
        now= datetime.datetime.now()
        h_to_m= now.hour * 60
        minutes= h_to_m + now.minute
        return minutes/60 if minutes>0 else 0

    date_create = fields.Datetime(string='Fecha de creación', required= True, default = lambda self: datetime.datetime.now(), readonly= '1')
    hour_create = fields.Float(string='Hora Creación', default=_get_hour)
    date_informe = fields.Date(string='Fecha de informe', required= True, default= lambda self: datetime.datetime.now())
    month_informe = fields.Char(string='Mes de informe', required= True, compute='_onchange_date_informe')
    client_id = fields.Many2one('res.partner', string='Cliente', required= True)
    web_client = fields.Many2one('posik_client.web_site', string='Sitio Web', domain="[('client_id', '=', client_id)]" )
    url = fields.Char('Url Resultante')
    external_hours = fields.Float(string='Horas Reporte', default= 1.5)
    link_price = fields.Float('Precio de Enlace', digits='Product Price')
    provider = fields.Char('Proveedor')
    anchor = fields.Char('Anchor')
    seccion = fields.Char('Sección')
    portal = fields.Char('Portal')
    email = fields.Char('email')
    user = fields.Char('Usuario')
    password = fields.Char('password')
    total_timesheet_hours = fields.Float(string="Total de Horas Internas", default= 0)

    # timesheets_ids= fields.One2many('link_building.timesheet', 'link_building_id', string="Distribución de Horas")
    # timesheet_hours = fields.Float(string="Horas Invertidas")
    # total_timesheet_hours = fields.Float(string="Total de Horas Internas", default= 0, compute='_onchange_timesheets_ids')

    @api.onchange('date_informe')
    def _onchange_date_informe(self):
        for this in self:
            if this.date_informe:
                month= get_month(this.date_informe.month)
                this.month_informe= month + ' '+str(this.date_informe.year)
    
    """ @api.onchange('timesheets_ids')
    def _onchange_timesheets_ids(self):
        total= 0
        for t in self.timesheets_ids:
            total += t.hours
        self.total_timesheet_hours= total

    def add_timesheet_hours(self):
        if self.timesheet_hours > 0 :
            self.timesheets_ids= [(0,0,{
                'user_id': self.env.uid,
                'hours': self.timesheet_hours
            })]
        self.timesheet_hours= 0 """
    
    @api.onchange('client_id')
    def _onchange_client_id(self):
        self.web_client= None
    
class ResPartner(models.Model):
    _inherit ='res.partner'
    link_building_ids = fields.One2many('link_building.link_building', 'client_id', string = 'Link Building')
