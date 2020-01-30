# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SocialNetwork(models.Model):
    _name = 'posik_client.social_network'
    _description = 'social networks'
    _rec_name = 'web'

    web = fields.Char(string= 'Red Social', required= True)
    url = fields.Char(string= 'URL', required= True)

    social_network_id = fields.One2many('posik_client.my_social_network', 'social_network_id', string = 'Cuentas en esta Red', required=True)


class MySocialNetwork(models.Model):
    _name = 'posik_client.my_social_network'
    _description = 'social networks from client'

    name = fields.Char(string= 'Nombre', required= True)
    url = fields.Char(string= 'url', required= True)
    logo = fields.Binary(string="Logotipo")
    social_network_id = fields.Many2one('posik_client.social_network',string = 'Redes Sociales', required=True)
    client_id = fields.Many2one('res.partner', string='Clientes', readonly= True)