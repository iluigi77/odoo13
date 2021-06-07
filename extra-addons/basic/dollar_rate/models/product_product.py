# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp

""" need ihnerit from dollar_price (required install it) """
class ProductProduct(models.Model):
    _inherit = 'product.product'

    """ inherit fix price (from product_variant_sale_price) for compute rate"""
    # fix_price = fields.Float( string='Fix Price', compute='_compute_variant_dollar_price')
    
    # """ Calcula el precio en bs según la tasa establecida en Dolares
    # y guarda el valor en un campo computado"""
    # @api.depends('dollar_active', 'variant_dollar_price')
    # def _compute_variant_dollar_price(self):
    #     for product in self:
    #         if(product.dollar_active and product.product_variant_count> 1):
    #             """ actual_rate viene de dollar_price """
    #             rate= product.product_tmpl_id._get_rate()
    #             product.fix_price= product.variant_dollar_price * rate
    #             product.lst_price= product.variant_dollar_price * rate
    #         else:
    #             product.fix_price= product.product_tmpl_id.list_price
    #             product.lst_price= product.product_tmpl_id.list_price
            
        