# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    dollar_active= fields.Boolean(string='Producto en Dólar', default=True)
    dollar_price= fields.Float(string='Precio en Dólar') # Precio en Dollar
    dollar_currency_id = fields.Many2one('res.currency', compute='_get_dollar_currency',
        string='Currency', readonly=True, store=True)

    """ Cuando el precio en Dólar es activado, se obtiene la moneda (usd) """
    @api.depends('dollar_active')
    def _get_dollar_currency(self):
        for product in self:
            if(product.dollar_active):
                currency= self.env['res.currency'].sudo().search([('name', '=', 'USD')], limit=1)
                product.dollar_currency_id= currency.id


        