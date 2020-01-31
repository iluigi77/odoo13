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
    task_id = fields.Many2one('project.task', string='Tarea', required= True, domain="[('client_id', '=', client_id)]")
    name_client = fields.Char(string='Nombre del Cliente', compute='_on_change_client_id', readonly="1")
    informe_text_client = fields.Text(string="Texto Inicio de Informes")
    activity_url = fields.Many2many('account.analytic.line', string='Tareas con URL', compute= '_on_change_client_id', readonly='1')
    seccion_ids = fields.Many2many('posik_client.informe_seccion', string='Secciones', compute= '_load_seccions', readonly='1')
    web_client_ids = fields.Many2many('posik_client.web_site', string='Sitios Web', compute= '_on_change_client_id', readonly='1')
    link_building_ids = fields.Many2many('link_building.link_building', string='Link Building', compute= '_on_change_client_id', readonly='1')
    advertising_investment_ids = fields.Many2many('posik_client.advertising_investment', string = 'Inversiones en Publicidad', compute='_on_change_client_id')

    hour_seccion = fields.One2many('posik_report.transcient_hours_seccion', 'report_id', string='Horas por Secciones')
    activities_seccion = fields.One2many('posik_report.transcient_activity', 'report_id', string='Actividades por Secciones')

    @api.onchange('client_id')
    def _load_seccions(self):
        seccions=self.env['posik_client.informe_seccion'].search([])
        self.seccion_ids= seccions

    @api.onchange('client_id')
    def _on_change_client_id(self):
        self.web_client_ids= [(3,t.id) for t in self.web_client_ids]
        self.link_building_ids= [(3,t.id) for t in self.link_building_ids]
        self.activity_url= [(3,t.id) for t in self.activity_url]
        self.advertising_investment_ids= [(3,t.id) for t in self.advertising_investment_ids]
        if not self.client_id:
            self.name_client= None
        else:
            dd= datetime.datetime.today()
            self.task_id = None if not self.client_id.task_id else self.client_id.task_id[0]
            self.name_client= self.client_id.name 
            self.informe_text_client= self.client_id.informe_text
            
            self.web_client_ids= [(4,t.id)for t in self.client_id.web_site]
            self.link_building_ids= [(4,t.id)for t in self.client_id.link_building_ids if t.date_informe.month == dd.month and t.date_informe.year == dd.year]
            self.activity_url= [(4,t.id) for t in self.client_id.activity_id if t.date.month == dd.month and t.date.year == dd.year]
            self.advertising_investment_ids= [(4,t.id) for t in self.client_id.advertising_investment_ids if t.date_informe.month == dd.month and t.date_informe.year == dd.year]
            self.generate_activities()

    def generate_activities(self):
        self.activities_seccion= [(3,t.id) for t in self.activities_seccion]
        res = {}
        for item in self.activity_url:
            # crea una entrada en el dict (seccion)
            res.setdefault(item['seccion_id']['name'], {})
            # a la entrada creada, le crea otra entrada (subseccion) y le a;ade un elemento al array
            res[item['seccion_id']['name']].setdefault(item['subseccion_id']['name'], []).append(item.read(["name", "url", "short_timesheet"])[0])
        
        for seccion in res:
            self.activities_seccion=[(0,0,{
                'header_name': seccion,
                'type_row': 'seccion',
            })]
            for sub in res[seccion]:
                self.activities_seccion=[(0,0,{
                    'header_name': sub,
                    'type_row': 'subseccion',
                })]
                for p in res[seccion][sub]:
                    self.activities_seccion=[(0,0,{
                        'header_name': '->',
                        'name': p['name'],
                        'url': p['url'],
                        'type_row': 'activity' if not p['short_timesheet'] else 'shor_activity',
                    })]

    def generate_hours_activities(self):
        self.hour_seccion= [(3,t.id) for t in self.hour_seccion]

        # res={}
        # for item in self.seccion_ids:
        #     res.setdefault(item['name'], [])

        activites= self.activity_url
        records= []
        for p in activites:
            records.append({
                "id": p.id,
                "name": p.name,
                "seccion": p.seccion_id.name,
                "key_seccion": p.seccion_id.id,
                "subseccion": p.subseccion_id.name,
                "key_subseccion": p.subseccion_id.id,
                "unit_amount": p.unit_amount,
                "url": p.url,
                "web_client": p.web_client.web,
                "short_timesheet": p.short_timesheet,
            })
        
        res_seccion = {}
        for item in records:
            res_seccion.setdefault(item['seccion'], []).append(item)
        
        for key in res_seccion:
            activ_record= res_seccion[key]
            name_seccion= activ_record[0]['seccion']
            total= 0
            for pp in activ_record:
                total += pp['unit_amount']
            print(total)
            self.hour_seccion= [(0,0,{
                'name': name_seccion,
                'hours_internal': total,
                'hours_external': total
            })]
            pass