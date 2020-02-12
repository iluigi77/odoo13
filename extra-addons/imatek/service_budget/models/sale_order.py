# -*- coding: utf-8 -*-

from odoo import models, fields, api

class OrderLine(models.Model):
    _inherit = 'sale.order.line'

    no_budgetable= fields.Boolean(string= 'No Contable')
    is_service= fields.Boolean(string= 'Es servicio')

    @api.model
    def create(self, values):
        id= values['product_id']
        p=self.env['product.product'].browse([id])
        values['no_budgetable'] = p.no_budgetable
        values['is_service'] = True if p.type== 'service' else False
        res = super(OrderLine, self).create(values)
        return res

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    amount_untaxed_service = fields.Monetary(string='Base Imponible', store=True, readonly=True, compute='_amount_all_services', tracking=5)
    amount_tax_service = fields.Monetary(string='Impuestos', store=True, readonly=True, compute='_amount_all_services')
    amount_total_service = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all_services' ,tracking=4)

    amount_untaxed_no_service = fields.Monetary(string='Base Imponible', store=True, readonly=True, compute='_amount_all_services', tracking=5)
    amount_tax_no_service = fields.Monetary(string='Impuestos', store=True, readonly=True, compute='_amount_all_services')
    amount_total_no_service = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all_services' ,tracking=4)

    @api.depends('order_line.price_total')
    def _amount_all_services(self):
        for order in self:
            amount_untaxed_no = amount_tax_no = 0.0
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                if line.is_service:
                    amount_untaxed_no += line.price_subtotal #Suma el subtotal
                    amount_tax_no += line.price_tax #suma el impuesto
                else:
                    amount_untaxed += line.price_subtotal #Suma el subtotal
                    amount_tax += line.price_tax #suma el impuesto
            order.update({
                'amount_untaxed_no_service': amount_untaxed,
                'amount_tax_no_service': amount_tax,
                'amount_total_no_service': amount_untaxed + amount_tax,
            })
            order.update({
                'amount_untaxed_service': amount_untaxed_no,
                'amount_tax_service': amount_tax_no,
                'amount_total_service': amount_untaxed_no + amount_tax_no,
            })
