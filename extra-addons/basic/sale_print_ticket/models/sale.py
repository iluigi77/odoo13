# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def print_ticket(self):
        return self.env.ref('sale_print_ticket.action_ticket_sale')\
            .with_context(discard_logo_check=True).report_action(self)