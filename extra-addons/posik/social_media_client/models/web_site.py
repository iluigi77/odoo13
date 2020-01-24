# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WebSite(models.Model):
    _name = 'social_media_client.web_site'
    _description = 'web sites'

    web = fields.Char(string= 'Sitio Web', requiered= True)
    url = fields.Char(string= 'URL', requiered= True)
    logo = fields.Binary(string="Logotipo")

    client_id = fields.Many2one('res.partner', string='Clientes', readonly= True)

class SocialNetwork(models.Model):
    _name = 'social_media_client.social_network'
    _description = 'social networks'

    web = fields.Char(string= 'Sitio Web', requiered= True)
    url = fields.Char(string= 'URL', requiered= True)
    logo = fields.Binary(string="Logotipo")

    client_id = fields.Many2many('res.partner', string = 'Clientes')