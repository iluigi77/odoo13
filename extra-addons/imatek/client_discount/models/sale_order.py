# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SalesOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_category_id = fields.Many2one('product.category', string='Categoría')
    

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        discount= self.partner_id.discount_category if self.partner_id else 0
        for line in self.order_line:
            line.discount= discount
            line.product_id_change()

    @api.onchange('order_line')
    def _onchange_order_line(self):
        discount= self.partner_id.discount_category if self.partner_id else 0
        for line in self.order_line:
            line.discount= discount
            line.product_category_id= line.product_id.product_tmpl_id.categ_id