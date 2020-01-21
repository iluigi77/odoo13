# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    # pdf_attach_id = fields.Many2one ('ir.attachment', string = 'Attachment pdf', ondelete = 'cascade')
    pdf_bin = fields.Binary(string='PDF Adjunto')
    vertical_id = fields.Many2many('verticals.verticals', string="Lote Vertical")

    #for show products
    products_by_lots = fields.Many2many('product.template', string= 'Lote', compute='_get_products_from_lot', store= False)

    @api.onchange('vertical_id')
    def _get_products_from_lot(self):
        lots = self.vertical_id.mapped('product_ids')
        self.products_by_lots= lots
        # self.products_by_lots= []
        # idd= self.vertical_id.id
        # if idd:
        #     lots = self.env['verticals.verticals'].search([('id', '=', idd)]).mapped('product_ids')

