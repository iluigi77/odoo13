# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class TranscientHoursSeccion(models.Model):
    _name ="posik_report.transcient_hours_seccion"

    index = fields.Integer(string='Index')
    name = fields.Char('Sección', required=True)
    report_id = fields.Many2one('posik_report.posik_report', string='Report')
    seccion_id = fields.Many2one('posik_report.informe_seccion', string='Report')
    hours_internal = fields.Float('Total Horas')
    hours_external = fields.Float('Horas para reporte')


class InformeSeccion(models.Model):
    _inherit = 'posik_client.informe_seccion'

    hours_seccion_id = fields.One2many('posik_report.transcient_hours_seccion', 'seccion_id', string="Horas por seccion")