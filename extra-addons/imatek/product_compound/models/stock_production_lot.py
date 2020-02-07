# -*- coding: utf-8 -*-

from odoo import models, fields, api

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'
    
    def default_materials(self):
        lot= []
        idd= self._context.get('default_product_tmpl_id')
        if idd:
            records= self.env['mrp.bom'].search([
                ('product_tmpl_id','=', idd),
                ('main_list','=', True)
                ], limit= 1)
            if records:
                for p in records.mapped('bom_line_ids'):
                    lot.append((0,0, {
                        'product_tmpl_id': p.product_tmpl_id.id,             
                        'product_qty': p.product_qty,
                        }))
        return lot

    product_tmpl_id = fields.Many2one(
        'product.template', 'Product Template',
        related='product_id.product_tmpl_id', readonly=False,
        help="Technical: used in views")

    mrp_bom_id = fields.Many2one('mrp.bom', string='Lista de Materiales', domain="[('product_tmpl_id', '=', product_tmpl_id)]")
    product_compound_line_ids = fields.One2many('product_compound.line', 'stock_product_lot_id', string='Materiales', default= default_materials)

    @api.onchange('mrp_bom_id')
    def _onchange_mrp_bom_id(self):
        if self.mrp_bom_id:
            for p in self.mrp_bom_id.mapped('bom_line_ids'):
                self.product_compound_line_ids = [(0,0, {
                    'product_tmpl_id': p.product_tmpl_id.id,             
                    'product_qty': p.product_qty,
                    })]
 
        self.mrp_bom_id=None