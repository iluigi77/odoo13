# -*- coding: utf-8 -*-

from odoo import models, fields, api

class AccountTaxGroup(models.Model):
    _inherit = 'account.tax.group'

    taxes_id = fields.One2many('account.tax', 'tax_group_id', string='Impuestos') # for link with taxes