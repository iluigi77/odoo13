# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountTax(models.Model):
    _inherit = 'account.tax'

    tax_type = fields.Selection([
        ('0', 'Exento'),      # 0%
        ('2', 'Tasa REDU (8%)'),   # 8%
        ('1', 'Tasa GRAL (16%)'),   # 16%
        ('3', 'Tasa ADIC (22%)')    # 22%
        ], string='Tipo de Tasa', default='0', required= True)
