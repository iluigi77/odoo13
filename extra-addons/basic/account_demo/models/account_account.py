# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountAccount(models.Model):
    _inherit = 'account.account'

    old_account = fields.Boolean('Data demo')
    old_account_code = fields.Boolean('Código excel')
