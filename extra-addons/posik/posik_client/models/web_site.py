# -*- coding: utf-8 -*-

from odoo import models, fields, api


class WebSite(models.Model):
    _name = 'posik_client.web_site'
    _description = 'web sites'
    _rec_name = 'web'

    web = fields.Char(string= 'Sitio Web', required= True)
    url = fields.Char(string= 'URL', required= True)
    logo = fields.Binary(string="Logotipo")

    client_id = fields.Many2one('res.partner', string='Clientes', readonly= True)

