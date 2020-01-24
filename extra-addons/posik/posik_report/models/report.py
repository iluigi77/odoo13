# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosikReport(models.Model):
    _name = 'posik_report.posik_report'
    _description = 'posik_report.posik_report'

    # client_id = fields.Many2one('res.partner', string='Cliente')
    client_id = fields.Char(string='Cliente')
