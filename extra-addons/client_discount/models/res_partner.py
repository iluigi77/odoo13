# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    discount_category = fields.Float(string='Descuento (%)', digits='Discount', default=0.0)

