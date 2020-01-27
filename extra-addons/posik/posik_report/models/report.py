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
    
    @api.depends('client_id')
    def _default_text(self):
        if self.client_id:
            text= ''
            dt= self.env['res.partner'].search([('id', '=', self.client_id)], limit= 1)
            if dt:
                text= dt[0].informe_text
            return text

    tittle= fields.Text(string='Título', default= _default_tittle, readonly='1')
    client_id = fields.Many2one('res.partner', string='Cliente', required= True)
    name_client = fields.Char(string='Nombre del Cliente', compute='_on_change_client_id', readonly="1")
    informe_text_client = fields.Text(string="Texto Inicio de Informes", required= True)
    activity_url = fields.Many2many('account.analytic.line', string='Tareas con URL', compute= '_on_change_client_id', readonly='1')
    activity_no_url = fields.Many2many('account.analytic.line', string='Tareas sin URL', compute= '_on_change_client_id', readonly='1')
    # link_building = fields.Many2one('link_building.link_building', string='Link Building', required= True)
    
    @api.onchange('client_id')
    def _on_change_client_id(self):
        for t in self.activity_url:
            self.activity_url= [(3,t.id.origin)]
        for t in self.activity_no_url:
            self.activity_no_url= [(3,t.id.origin)]

        if self.client_id:
            # client info
            self.name_client= self.client_id.name
            self.informe_text_client= self.client_id.informe_text

            # task
            dd= datetime.datetime.today()
            for t in self.client_id.activity_id:
                if t.date.month == dd.month and t.date.year == dd.year:
                    if t.url:
                        self.activity_url= [(4,t.id)]
                    else:
                        self.activity_no_url= [(4,t.id)]
            