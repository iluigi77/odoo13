# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class TranscientActivity(models.Model):
    _name ="posik_report.transcient_activity"
    
    header_name= fields.Char('Sección') 
    name = fields.Char('Descripción')
    report_id = fields.Many2one('posik_report.posik_report', string='Report')
    url = fields.Char('URL')
    # pic_bin = fields.Binary('Imagen')
    type_row = fields.Selection([
        ('seccion', 'Sección'),
        ('subseccion', 'Subsección'),
        ('activity', 'Actividad'),
        ('shor_activity', 'Actividad Corta')
    ], string='Tipo', default='activity', required=True) 