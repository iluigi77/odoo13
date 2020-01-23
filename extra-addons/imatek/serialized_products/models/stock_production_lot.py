# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    quantity_serialize= fields.Integer('Cantidad')
    stock_product_lot_id = fields.Many2many('stock.production.lot', string='Producto Serializado')

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    mrp_bom_id = fields.Many2one('mrp.bom', string='Lista de Materiales')
    material_product_id = fields.Many2many('product.template', string='Materiales')

    @api.onchange('mrp_bom_id')
    def _onchange_mrp_bom_id(self):
        ids= self.material_product_id.mapped('id')
        for id in ids:
            self.material_product_id=[(3,id)]
        for p in self.mrp_bom_id.bom_line_ids:
            self.material_product_id = [(4,p.product_tmpl_id.id)]
        # self.material_product_id= []
            

