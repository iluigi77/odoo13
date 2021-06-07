# -*- coding: utf-8 -*-

from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    # acquirer_id = fields.Many2one("payment.acquirer", related="transaction_ids.acquirer_id", store=True)
    payment_amount = fields.Monetary(string="Amount Payment", compute="_compute_payment")
    residual = fields.Monetary(string='Total Restante',
        compute='_compute_payment', help="Remaining amount due.")

    payment_status = fields.Selection(
        [
            ("without", "Sin Pagar"),
            ("initiated", "Iniciado"),
            ("partial", "Parcial"),
            ("done", "Pagado")
        ],
        default="without",
        compute="_compute_payment"
    )

    acquirer_ids = fields.Many2many('payment.acquirer', string='Métodos de pago usados',
        compute='_get_payment_acquirer')  
    

    @api.depends('transaction_ids')
    def _get_payment_acquirer(self):
        self.acquirer_ids = self.transaction_ids.mapped('acquirer_id')  


    @api.depends("transaction_ids", "invoice_ids")
    def _compute_payment(self):
        for order in self:
            amount = 0
            transactions = order.sudo().transaction_ids.filtered(lambda a: a.state == "done")
            
            for transaction in transactions:
                amount += transaction.amount

            order.payment_amount = amount
            order.residual= amount
            if order.payment_amount > 0:
                
                if order.payment_amount < order.amount_total:
                    order.payment_status = "partial"
                    order.residual = order.amount_total - order.payment_amount

                if order.payment_amount >= order.amount_total:
                    order.payment_status = "done"
                    order.residual= 0

            if not order.payment_amount:
                order.payment_status = "without"