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

class InformeSeccion(models.Model):
    _inherit = 'posik_client.informe_seccion'

    hour_price_id = fields.Many2many('posik_client.hour_price', string="Precio de Hora Asociado")
    # hour_price_id = fields.Many2one('posik_client.hour_price', string="Precio de Hora Asociado")

class HourPrice(models.Model):
    _name = 'posik_client.hour_price'
    _description = 'Hours Price'

    def _default_name(self):
        record= self.env['posik_client.hour_price'].search([])
        return "Precio de hora " + str(len(record)+1)

    name = fields.Char(string= 'Descripción', default= _default_name, required= True)
    hour_price = fields.Float(string="Precio de la Hora", required=True)
    discount_hour_price = fields.Float(string="Descuento(%)")
    client_id = fields.Many2one('res.partner', string="Cliente")
    seccion_id = fields.Many2many('posik_client.informe_seccion', string="Secciones")
    date_informe = fields.Date(string='Fecha de informe', required= True, default=lambda self: datetime.datetime.now())
    month_informe = fields.Char(string='Mes de informe', required= True, compute='_onchange_date_informe')

    @api.onchange('date_informe')
    def _onchange_date_informe(self):
        for this in self:
            if this.date_informe:
                month= get_month(this.date_informe.month)
                this.month_informe= month + ' '+str(this.date_informe.year)

    # seccion_id = fields.One2many('posik_client.informe_seccion', 'hour_price_id', string="Secciones")

class ResPartner(models.Model):
    _inherit = 'res.partner'

    hour_price_id = fields.One2many('posik_client.hour_price', 'client_id', string="Precios por Hora")


