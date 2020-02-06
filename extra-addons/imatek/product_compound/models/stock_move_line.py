# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class ProductCompoundMoveLine(models.Model):
#     _name = 'product_compound.move.line'
#     _rec= 'product_tmpl_id'

#     stock_move_line_id = fields.Many2one('stock.move.line', string='Lote/N° Serial')

#     product_tmpl_id = fields.Many2one('product.template', string='Product')
#     product_qty= fields.Integer(string='Cantidad', default=1)

# class StockMoveLine(models.Model):
#     _inherit='stock.move.line'

#     product_compound_line_ids = fields.One2many('product_compound.move.line', 'stock_move_line_id',string='Productos compuestos')