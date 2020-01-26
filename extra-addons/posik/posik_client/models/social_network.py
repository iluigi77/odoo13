# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SocialNetwork(models.Model):
    _name = 'posik_client.social_network'
    _description = 'social networks'
    _rec_name = 'web'

    web = fields.Char(string= 'Red Social', required= True)
    url = fields.Char(string= 'URL', required= True)
    logo = fields.Binary(string="Logotipo")

    client_id = fields.Many2many('res.partner', string = 'Clientes')