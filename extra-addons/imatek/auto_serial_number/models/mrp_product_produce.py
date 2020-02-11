# -*- coding: utf-8 -*-

from odoo import models, fields, api


class MrpProductProduce(models.TransientModel):
    _inherit = 'mrp.product.produce'

    suggested_next_serial = fields.Char('N° Serie sugerido',default= lambda self: self.env['ir.sequence'].next_by_code('stock.lot.serial'),
        help="N° Serie sugerido", readonly=True)