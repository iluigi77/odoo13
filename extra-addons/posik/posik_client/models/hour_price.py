# -*- coding: utf-8 -*-

from odoo import models, fields, api

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
    # seccion_id = fields.One2many('posik_client.informe_seccion', 'hour_price_id', string="Secciones")

class ResPartner(models.Model):
    _inherit = 'res.partner'

    hour_price_id = fields.One2many('posik_client.hour_price', 'client_id', string="Precios por Hora")


