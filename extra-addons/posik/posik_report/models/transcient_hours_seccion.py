# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class TranscientHoursSeccion(models.Model):
    _name ="posik_report.transcient_hours_seccion"

    name = fields.Char('Sección', required=True)
    report_id = fields.Many2one('posik_report.posik_report', string='Report')
    hours_internal = fields.Float('Total Horas')
    hours_external = fields.Float('Horas para reporte')