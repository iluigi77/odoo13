# -*- coding: utf-8 -*-

from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    suggested_next_serial = fields.Char('N° Serie sugerido',default= lambda self: self.env['ir.sequence'].next_by_code('stock.lot.serial'),
        help="N° Serie sugerido", readonly=True)