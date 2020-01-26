# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class posik_project(models.Model):
    _inherit = 'project.task'

    def _get_today(self):
        return datetime.datetime.today()

    # user_id = fields.Many2one('res.partner', string='Usuario')
    pic_task = fields.Binary(string='Foto de Actividad')
    date_init = fields.Date(string='Fecha de Inicio', default=_get_today,  readonly='1')
    duration_time = fields.Float(string='Tiempo de duración Estimado')
    url = fields.Char(string= 'URL')
    client_id = fields.Many2one('res.partner', string='Cliente', required= True)
    web_client = fields.Many2one('posik_client.web_site', string='Sitio Web')
    seccion_id = fields.Many2one('posik_client.informe_seccion', string='Sección', required= True)
    subseccion_id = fields.Many2one('posik_client.informe_subseccion', string='Subsección')
