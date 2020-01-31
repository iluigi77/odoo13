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
    seccion_ids = fields.Many2many('posik_client.informe_seccion', string='Secciones', compute= '_load_seccions', readonly='1')
    activity_url = fields.Many2many('account.analytic.line', string='Tareas con URL')
    web_client_ids = fields.Many2many('posik_client.web_site', string='Sitios Web', readonly='1')
    link_building_ids = fields.Many2many('link_building.link_building', string='Link Building')
    advertising_investment_ids = fields.Many2many('posik_client.advertising_investment', string = 'Inversiones en Publicidad', relation="m2m_adv_invest_2_report")
    hour_price_ids = fields.Many2many('posik_client.hour_price', string = 'Precios por Hora')

    hour_seccion = fields.One2many('posik_report.transcient_hours_seccion', 'report_id', string='Horas por Secciones')
    # activities_seccion = fields.One2many('posik_report.transcient_activity', 'report_id', string='Actividades por Secciones', relation="m2m_activ_seccion_2_report")

    compute= fields.Boolean(string="Obtener datos para el report", default= False)


    def generate_report(self):
        self.web_client_ids= [(3,t.id) for t in self.web_client_ids]
        self.link_building_ids= [(3,t.id) for t in self.link_building_ids]
        self.activity_url= [(3,t.id) for t in self.activity_url]
        self.advertising_investment_ids= [(3,t.id) for t in self.advertising_investment_ids]
        self.hour_price_ids= [(3,t.id) for t in self.hour_price_ids]
        if self.client_id:
            dd= datetime.datetime.today()
            self.web_client_ids= [(4,t.id)for t in self.client_id.web_site]
            self.link_building_ids= [(4,t.id)for t in self.client_id.link_building_ids if t.date_informe.month == dd.month and t.date_informe.year == dd.year and t.client_id.id == self.client_id.id]
            self.advertising_investment_ids= [(4,t.id) for t in self.client_id.advertising_investment_ids if t.date_informe.month == dd.month and t.date_informe.year == dd.year]
            self.hour_price_ids= [(4,t.id) for t in self.client_id.hour_price_id if t.date_informe.month == dd.month and t.date_informe.year == dd.year]
            for t in self.client_id.activity_id:
                if (t.date.month == dd.month and t.date.year == dd.year) and (t.task_id.id == self.task_id.id and t.client_id.id== self.client_id.id):
                    self.activity_url= [(4,t.id)]
            self.generate_hours_activities()
            self.compute= True

    @api.onchange('activity_url')
    def _onchange_activities(self):
        res={}
        for item in self.seccion_ids:
            line=item.id.origin
            res.setdefault(line, [])
        
        for p in self.activity_url:
            item2= {
                'name': p.name, 
                'seccion_id': p.seccion_id, 
                'subseccion_id': p.subseccion_id, 
                'unit_amount': p.unit_amount, 
                'url': p.url, 
                'web_client': p.web_client, 
                'short_timesheet': p.short_timesheet,
            }
            res.setdefault(p['seccion_id']['id'], []).append(item2)
        
        for line in self.hour_seccion:
            seccion_id=self.env['posik_client.informe_seccion'].browse([line.seccion_id.id])
            hour_seccion_id= line.id.origin
            record= res[line.seccion_id.id]
            total= 0
            if seccion_id.link_building:
                for lb in self.link_building_ids:
                    total += lb['external_hours']
            else:
                for pp in record:
                    total += pp['unit_amount']
            self.hour_seccion= [(1,hour_seccion_id,{'hours_internal': total})]


    def generate_hours_activities(self):
        self.hour_seccion= [(2,t.id) for t in self.hour_seccion]

        res={}
        for item in self.seccion_ids:
            res.setdefault(item['id'], [])
        
        for p in self.activity_url:
            item= p.read([
                'name', 'seccion_id', 'subseccion_id', 'unit_amount', 
                'url', 'web_client', 'short_timesheet',
            ])[0]
            res.setdefault(p['seccion_id']['id'], []).append(item)
        
        for key in res:
            seccion_id=self.env['posik_client.informe_seccion'].browse([key])
            record= res[key]
            total= 0
            if seccion_id.link_building:
                for lb in self.link_building_ids:
                    total += lb['external_hours']
            else:
                for pp in record:
                    total += pp['unit_amount']
            self.hour_seccion= [(0,0,{
                'name': seccion_id.name,
                'seccion_id': key, 
                # 'seccion_id': seccion_id.id,
                'hours_internal': total,
                'hours_external': total
            })]


    @api.onchange('client_id')
    def _load_seccions(self):
        seccions=self.env['posik_client.informe_seccion'].search([])
        self.seccion_ids= seccions

    @api.onchange('client_id')
    def _on_change_client_id(self):
        if not self.client_id:
            self.name_client= None
        else:
            self.task_id = None if not self.client_id.task_id else self.client_id.task_id[0]
            self.name_client= self.client_id.name 
            self.informe_text_client= self.client_id.informe_text
            
    """ def generate_activities(self):
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
    """


    # def _total_hour_price(self):
    #     for p in self.hour_price_ids:
    #         price= p.hour_price
    #         discount_price= p.discount_hour_price / 100
    #         total =0
    #         for seccion in p.seccion_id:
    #             horas=0
    #             for copy in self.hour_seccion:
    #                 if copy.seccion_id.id == seccion.id:
    #                     horas= copy.seccion_id.hours_external
                
    #             total+= (price*horas)*discount_price
                