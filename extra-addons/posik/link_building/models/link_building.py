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
    task = fields.Many2one('project.task', string='Tareas', domain="[('client_id', '=', client_id)]")
    url = fields.Char('Url Resultante')
    hours = fields.Float(string='Horas')
    link_price = fields.Float('Precio de Enlace', digits='Product Price')
    provider = fields.Char('Proveedor')
    email = fields.Char('email')
    user = fields.Char('Usuario')
    password = fields.Char('password')

    month= fields.Integer('Mes', compute= '_get_month_informe', store= True)
    year= fields.Integer('Año', compute= '_get_month_informe', store= True)

    @api.onchange('month_informe')
    def _get_month_informe(self):
        if self.month_informe:
            self.month= int(self.month_informe.month)
            self.year= int(self.month_informe.year)

    @api.onchange('client_id')
    def _onchange_client_id(self):
        self.web_client= None
        self.task= None
    
    @api.model
    def create(self, values):
        res= super(link_building, self).create(values)
        task= self.env['project.task'].search([('id', '=', values['task'])], limit=1)
        mm=  values['month']
        yy= values['year']
        task.update({
            'month': mm,
            'year': yy
        })
        return res