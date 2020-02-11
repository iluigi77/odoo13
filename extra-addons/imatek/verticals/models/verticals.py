# -*- coding: utf-8 -*-

from odoo import models, fields, api


class verticals(models.Model):
    _name = 'verticals.verticals'
    _description = 'Lots verticals for products'

    name = fields.Char(string= 'Vertical', required= True)
    description = fields.Text(string= 'Descripción del Vertical', required= False)
    attachment_id = fields.Many2one('ir.attachment', string='Attachment', ondelete='cascade')

    product_ids = fields.Many2many('product.template', string= 'Productos')
    sale_order_id = fields.Many2many('sale.order', string="Factura")
    sale_order_line_ids = fields.One2many('sale.order.line', 'vertical_id',string='Productos en facturas')


