# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.addons import decimal_precision as dp

""" need ihnerit from dollar_price (required install it) """
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    """ DOLLAR RATE """
    actual_rate= fields.Float(string='Tasa Actual', compute="_compute_rate")
    list_price= fields.Float(string='Precio de venta', compute='_compute_list_price_bs') # Precio calculado en Bs segun la tasa actual

    """ Obtiene la tasa actual del dólar """
    def _get_rate(self):
        return self.actual_rate

    """ calcula la tasa actual del dólar """
    def _compute_rate(self):
        rate= self.dollar_currency_id.absolute_rate
        self.actual_rate= rate

    """ Calcula el precio en bs según la tasa establecida en Dolares
    y guarda el valor en un campo computado"""
    @api.depends('dollar_active', 'dollar_price')
    def _compute_list_price_bs(self):
        for product in self:
            if(product.dollar_active):
                product.list_price= product.dollar_price * product.actual_rate


    """ send to master view for dollar rate """
    def action_view_dollar_rate(self):
        self.ensure_one()
        action = self.env.ref('dollar_rate.currency_rate_records_action_window').read()[0]
        # action['domain'] = [
        #     ('currency_id', '=', self.dollar_currency_id.id), 
        #     ('company_id','=',self.company_id.id)
        # ]
        return action
    
    

        