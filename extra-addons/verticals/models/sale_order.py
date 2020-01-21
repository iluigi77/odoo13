# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SalesOrderLine(models.Model):
    _inherit = 'sale.order.line'

    group_lot = fields.Many2one('verticals.verticals', string= 'Lote Vetical')

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    pdf_bin = fields.Binary(string='PDF Adjunto')
    vertical_id = fields.Many2one('verticals.verticals', string= 'Lote Vetical')


    @api.onchange('vertical_id')
    def _onchange_vertical_id(self):
        if self.vertical_id:

            self.order_line = [(0,0, {
                'display_type': 'line_section',
                'name': self.vertical_id.name,
                'price_unit': 0.0,
                'product_id': None,             
                'product_uom_qty': 0,
                'customer_lead': 0.0,
            })]
            for line in self.order_line:
                line.product_id_change()

            products_lot = self.vertical_id.mapped('product_ids')
            for p in products_lot:
                product = self.env['product.product'].search([('product_tmpl_id', '=', p.id)])
                self.order_line = [(0,0, {
                    'price_unit': product.list_price,
                    'product_id': product.id,             
                    'product_uom_qty': 1,
                    'customer_lead': 0.0,
                    'group_lot': self.vertical_id.id,
                    })]
                for line in self.order_line:
                    line.product_id_change()
 
                self.vertical_id=None
