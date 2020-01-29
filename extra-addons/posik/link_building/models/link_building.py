# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class link_building(models.Model):
    _name = 'link_building.link_building'
    _description = 'link_building.link_building'

    def _get_today(self):
        return datetime.datetime.today()

    date_create = fields.Date(string='Fecha de creación', required= True, default = _get_today, readonly= '1')
    month_informe = fields.Date(string='Mes de informe', required= True)
    client_id = fields.Many2one('res.partner', string='Cliente', required= True)
    web_client = fields.Many2one('posik_client.web_site', string='Sitio Web', domain="[('client_id', '=', client_id)]" )
    url = fields.Char('Url Resultante')
    hours = fields.Float(string='Horas Externas', default= 1.5)
    link_price = fields.Float('Precio de Enlace', digits='Product Price')
    provider = fields.Char('Proveedor')
    email = fields.Char('email')
    user = fields.Char('Usuario')
    password = fields.Char('password')

    timesheets_ids= fields.One2many('link_building.timesheet', 'link_building_id', string="Distribución de Horas")
    timesheet_hours = fields.Float(string="Horas Invertidas")
    total_timesheet_hours = fields.Float(string="Total de Horas Internas", default= 0, compute='_onchange_timesheets_ids')

    @api.onchange('timesheets_ids')
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
        self.timesheet_hours= 0
    

    """ month= fields.Integer('Mes', compute= '_get_month_informe', store= True)
    year= fields.Integer('Año', compute= '_get_month_informe', store= True)

    @api.onchange('month_informe')
    def _get_month_informe(self):
        if self.month_informe:
            self.month= int(self.month_informe.month)
            self.year= int(self.month_informe.year) """

    @api.onchange('client_id')
    def _onchange_client_id(self):
        self.web_client= None
    