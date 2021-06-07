# -*- coding: utf-8 -*-

from odoo import models, fields, api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    fiscal_print = fields.Boolean('Impresión Fiscal', required= True, default= False)

    """ agrega el campo fiscal print a la orden para que esta sea creada """
    @api.model
    def _order_fields(self, ui_order):
        obj = super(PosOrder, self)._order_fields(ui_order)
        obj['fiscal_print']= ui_order['fiscal_print']
        return obj

class PosConfig(models.Model): 
    _inherit = 'pos.config' 
 
    url_api = fields.Char('URL para la API Fiscal', required= True, default= 'http://localhost:8001/fiscal_printer ')
