# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp

class ProductProduct(models.Model):
    _inherit = 'product.product'

    variant_dollar_price= fields.Float(string='Precio en Dólar') # Precio en Dollar
