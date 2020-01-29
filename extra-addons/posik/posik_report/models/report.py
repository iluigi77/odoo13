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

class PosikReport(models.Model):
    _name = 'posik_report.posik_report'
    _description = 'posik_report.posik_report'

    def _get_month(self):
        date= datetime.datetime.today()
        yyyy = date.strftime("%Y")
        month_name= get_month(date.month)
        return month_name +' '+ yyyy

    date_name= fields.Char(string='Mes y Año', default=_get_month, readonly="1")
    tittle= fields.Text(string='Título', 
        default= lambda self: "Informe de trabajos Mto. Web y Marketing Digital  " + self._get_month(), 
        readonly='1')
    client_id = fields.Many2one('res.partner', string='Cliente', required= True)
    name_client = fields.Char(string='Nombre del Cliente', compute='_on_change_client_id', readonly="1")
    informe_text_client = fields.Text(string="Texto Inicio de Informes")
    
    activity_url = fields.Many2many('account.analytic.line', string='Tareas con URL', compute= '_on_change_client_id', readonly='1')
    # activity_no_url = fields.Many2many('account.analytic.line', string='Tareas sin URL', compute= '_on_change_client_id', readonly='1')

    seccion_ids = fields.Many2many('posik_client.informe_seccion', string='Secciones', compute= '_load_seccions', readonly='1')
    web_client_ids = fields.Many2many('posik_client.web_site', string='Sitios Web', compute= '_load_web_clients', readonly='1')

    @api.onchange('client_id')
    def _load_seccions(self):
        seccions=self.env['posik_client.informe_seccion'].search([])
        self.seccion_ids= seccions

    @api.onchange('client_id')
    def _load_web_clients(self):
        webs_client=[]
        if self.client_id:
            webs_client=self.env['posik_client.web_site'].search([('client_id', '=', self.client_id.id)])
            self.web_client_ids= webs_client

    @api.onchange('client_id')
    def _on_change_client_id(self):
        for report in self:
            text= report.client_id.informe_text if report.client_id else ''
            report.informe_text_client= text

            for t in report.activity_url:
                report.activity_url= [(3,t.id.origin)]
            # for t in report.activity_no_url:
            #     report.activity_no_url= [(3,t.id.origin)]

            if report.client_id:
                # client info
                report.name_client= report.client_id.name
                report.informe_text_client= report.client_id.informe_text

                # task
                dd= datetime.datetime.today()
                activities= [(4,t.id) for t in report.client_id.activity_id if t.date.month == dd.month and t.date.year == dd.year]
                report.activity_url= activities
                # for t in report.client_id.activity_id:
                #     if t.date.month == dd.month and t.date.year == dd.year:
                        # report.activity_url= [(4,t.id) ]
                        # if t.url:
                        #     report.activity_url= [(4,t.id)]
                        # else:
                        #     report.activity_no_url= [(4,t.id)]
                
