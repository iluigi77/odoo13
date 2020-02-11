# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    attachment_id = fields.Many2one ('ir.attachment', string = 'Adjuntar pdf', ondelete = 'cascade')
    vertical_ids = fields.Many2many('verticals.verticals', string="Vertical")

    #for show products
    vertical_products = fields.Many2many('product.template', string= 'Lote', compute='_get_products_from_lot', store= False)

    @api.onchange('vertical_id')
    def _get_products_from_lot(self):
        p = self.vertical_ids.mapped('product_ids')
        self.vertical_products= p

