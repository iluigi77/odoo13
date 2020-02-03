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
    
    name= fields.Char(string="Reporte", compute="_get_name", readonly=True)
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

    hour_seccion_id = fields.One2many('posik_report.transcient_hours_seccion', 'report_id', string='Horas por Secciones')
    # activities_seccion = fields.One2many('posik_report.transcient_activity', 'report_id', string='Actividades por Secciones', relation="m2m_activ_seccion_2_report")
    text_total_price= fields.Text(string='Resumen de monto por horas', default='No existen tarifas por horas establecidas', compute="compute_text_total_price")
    total_price_link_building= fields.Float(string='Total', default= 0, readonly='1')
    total_time_link_building= fields.Float(string='Tiempo Total', default= 0, readonly='1')
    compute= fields.Boolean(string="Obtener datos para el report", default= False)
    
    def compute_text_total_price(self):
        if self.hour_price_ids:
            text= "Iguala mensual 1 de "
            text_hours= ''
            first= True

            tarifas= self.hour_price_ids 
            res={}
            for hour_seccion in self.hour_seccion_id:
                res.setdefault(hour_seccion.seccion_id.id, []).append({ 'hours_external':hour_seccion.hours_external })
            
            total=0
            for t in tarifas:
                discount= t.discount_hour_price / 100
                price= t.hour_price
                horas= 0
                for seccion in t.seccion_id:
                    idd=seccion.id if type(seccion.id) is int else seccion.id.origin
                    hour_by_seccion= res[idd][0]
                    horas += hour_by_seccion['hours_external']
                    print("para la seccion %s: %.4f (float) equivalente a %02d:%02d horas " %(seccion.name, horas, int(horas), (horas % 1 * 60)) )
                    print("a %.2f €/hora " %(price) )

                if horas>0:
                    if not first: text_hours+= " y "
                    text_hours += "%02d:%02d horas de trabajo al mes a %s€/hora" %(int(horas), (horas % 1 * 60), price)
                    first= False
                    # anidar apartados

                    total_by_hp= (price* horas)

                    if discount>0:
                        text_hours += ", con un descuento de %d %%" %((discount*100))
                        total_by_hp= total_by_hp-(total_by_hp* discount) 
                    total+= total_by_hp
            if not first:
                text+= '%.2f € calculada para un total de %s' %(total,text_hours)
                self.text_total_price= text
            else:
                self.text_total_price= "No existen tarifas por horas establecidas"
        else:
            self.text_total_price= "No existen tarifas por horas establecidas"

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

    def generate_hours_activities(self):
        self.hour_seccion_id= [(2,t.id) for t in self.hour_seccion_id]

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
                price_lb= 0
                for lb in self.link_building_ids:
                    total += lb['external_hours']
                    price_lb += lb['link_price']
                self.total_time_link_building= total
                self.total_price_link_building= price_lb
            else:
                for pp in record:
                    total += pp['unit_amount']
            self.hour_seccion_id= [(0,0,{
                'name': seccion_id.name,
                'seccion_id': key, 
                # 'seccion_id': seccion_id.id,
                'hours_internal': total,
                'hours_external': total
            })]
        self.compute_text_total_price()

    @api.onchange('activity_url', 'link_building_ids')
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
        
        for line in self.hour_seccion_id:
            seccion_id=self.env['posik_client.informe_seccion'].browse([line.seccion_id.id])
            hs_id= line.id.origin
            record= res[line.seccion_id.id]
            total= 0
            if seccion_id.link_building:
                price_lb= 0
                for lb in self.link_building_ids:
                    total += lb['external_hours']
                    price_lb += lb['link_price']
                self.total_time_link_building= total
                self.total_price_link_building= price_lb
            else:
                for pp in record:
                    total += pp['unit_amount']
            self.hour_seccion_id= [(1,hs_id,{
                'hours_internal': total,
                'hours_external': total if line.hours_external == line.hours_internal else line.hours_external
                })]
        self.compute_text_total_price()

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
            
    @api.onchange('tittle', 'date_name')
    def _get_name(self):
        name="undefined"
        if self.client_id: 
            name=self.client_id.name 
        self.name= 'report - %s %s' %(name, self.date_name)