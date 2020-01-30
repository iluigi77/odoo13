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

class PosikProvider(models.Model):
    _name = 'posik_client.provider'
    _description = 'Providers for Posik'

    name = fields.Char(string='Nombre Proveedor', required= True)
    advertising_investment = fields.One2many('posik_client.advertising_investment', 'provider_id', string='Inversiones Publicitarias')


class AdvertisingInvestment(models.Model):
    _name = 'posik_client.advertising_investment'
    _description = 'Informe Subseccions'

    def _get_today(self):
        return datetime.datetime.now()

    provider_id = fields.Many2one('posik_client.provider', string='Proveedor', required=True)
    client_id = fields.Many2one('res.partner', string="Cliente", required=True)
    web_client = fields.Many2one('posik_client.web_site', string="Web del cliente", required=True, domain="[('client_id', '=', client_id)]")
    importe = fields.Float(string='Importe', required= True, default= 0)
    date_informe = fields.Date(string='Fecha de informe', required= True, default=_get_today)
    month_informe = fields.Char(string='Mes de informe', required= True, compute='_onchange_date_informe')

    @api.onchange('date_informe')
    def _onchange_date_informe(self):
        for this in self:
            if this.date_informe:
                month= get_month(this.date_informe.month)
                this.month_informe= month + ' '+str(this.date_informe.year)
    