# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    logo = fields.Binary(string="Logotipo cliente")
    web_site = fields.One2many('posik_client.web_site', 'client_id',string = 'Sitios Web')
    my_social_network = fields.One2many('posik_client.my_social_network', 'client_id',string = 'Redes Sociales')
    advertising_investment_ids = fields.One2many('posik_client.advertising_investment', 'client_id', string = 'Inversiones en Publicidad')

