# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PaymentAcquirer(models.Model):
    _inherit = "payment.acquirer"

    sale_order_ids = fields.Many2many('sale.order', string='Facturas')
