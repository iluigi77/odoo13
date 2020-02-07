# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    code_albaran= fields.Char(string= 'Código de Albaran')

    
