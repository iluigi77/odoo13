# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductCompoundLine(models.Model):
    _name = 'product_compound.line'

    stock_product_lot_id = fields.Many2one('stock.production.lot', string='Lote/N° Serial')

    product_tmpl_id = fields.Many2one('product.template', string='Product', domain="[('is_component', '=', True)]")
    product_qty= fields.Integer(string='Cantidad', default=1)


class ProductTmpl(models.Model):
    _inherit='product.template'

    product_compound_line_ids = fields.One2many('product_compound.line', 'product_tmpl_id',string='Productos compuestos')