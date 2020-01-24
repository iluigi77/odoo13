# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    logo = fields.Binary(string="Logotipo cliente")
    Informe_text = fields.Text(string="Texto Inicio de Informes")
    web_site = fields.One2many('social_media_client.web_site', 'client_id',string = 'Sitios Web')
    social_network = fields.Many2many('social_media_client.social_network', string = 'Redes Sociales')