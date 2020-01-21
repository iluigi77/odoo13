# -*- coding: utf-8 -*-

from odoo import models, fields, api


class verticals(models.Model):
    _name = 'verticals.verticals'
    _description = 'Lots verticals for products'

    name = fields.Char(string= 'Codigo de Lote', required= True)
    description = fields.Text(string= 'Descripción del Lote', required= False)
    pdf_bin = fields.Binary(string='PDF Adjunto')

    product_ids = fields.Many2many('product.template', string= 'Productos')
    sale_order_id = fields.One2many('sale.order', 'vertical_id', string="Factura")


