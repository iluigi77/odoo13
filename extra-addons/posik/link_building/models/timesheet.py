# -*- coding: utf-8 -*-

from odoo import models, fields, api
import datetime

class link_building(models.Model):
    _name = 'link_building.timesheet'
    _description = 'timesheet for link_building'

    def _get_today(self):
        return datetime.datetime.today()

    user_id = fields.Many2one('res.users',
        string='Aplicadas por',
        default=lambda self: self.env.uid,
        index=True, tracking=True, readonly='1')
    hours = fields.Float(string="Horas de trabajo")
    date = fields.Date(string='Fecha', default= _get_today, readonly='1')
    link_building_id = fields.Many2one('link_building.link_building', string='Link Building')