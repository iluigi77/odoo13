# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class SaleConfirmPayment(models.TransientModel):
    _name = "sale.confirm.payment"
    _description = "Sale Confirm Payment"
    _rec_name = 'amount'
    _order = 'payment_date desc'

    def _get_default_amount(self):
        active_id = self.env.context.get("active_id", False)
        order = self.env["sale.order"].browse(active_id)
        # return abs(order.residual)

        if order.residual == 0:
            return order.amount_total
        else:
            return abs(order.residual)
    
    def _get_default_dollar_amount(self):
        active_id = self.env.context.get("active_id", False)
        order = self.env["sale.order"].browse(active_id)
        rate= order.current_dollar_rate
        if (rate == 0):
            rate= self.env['res.currency.line'].get_last_rate()

        # return abs(order.residual)/rate

        if order.payment_status == 'without':
            return order.amount_total / rate
        else:
            return abs(order.residual) / rate

    def _get_dollar_currency(self):
        currency= self.env['res.currency'].sudo().search([('name', '=', 'USD')], limit=1)
        return currency.id

    transaction_id = fields.Many2one("payment.transaction", readonly=True)
    
    acquirer_id = fields.Many2one("payment.acquirer", required=True)
    currency_id = fields.Many2one("res.currency")
    payment_date = fields.Date(string="Fecha de pago", required=True, default=fields.Date.context_today)
        
    amount = fields.Monetary(string="Monto", required=True, default=_get_default_amount)
    dollar_amount = fields.Monetary(string="Monto en Dólar", default=_get_default_dollar_amount)

    dollar_payment = fields.Boolean('Pago en dólar', default="True")
    current_dollar_rate = fields.Monetary(string="Tasa del Dólar", required=True)
    dollar_currency_id = fields.Many2one('res.currency', defult=_get_dollar_currency,
        string='Currency', readonly=True, store=True)
    
    amount_for_dollar= fields.Monetary(string="Monto en Dólar", compute='compute_amount_for_dollar')


    @api.onchange('dollar_amount')
    def _onchange_dollar_amount(self):
        self.amount = self.dollar_amount * self.current_dollar_rate
    
    @api.depends('dollar_amount', 'current_dollar_rate')
    def compute_amount_for_dollar(self):
        for p in self:
            p.amount_for_dollar= p.current_dollar_rate * p.dollar_amount

    @api.model
    def default_get(self, fields_list):
        defaults = super(SaleConfirmPayment, self).default_get(fields_list)
        active_id = self.env.context.get("active_id", False)
        if not active_id:
            raise UserError(_("Please select a sale order"))

        order = self.env["sale.order"].browse(active_id)
        defaults["currency_id"] = order.currency_id.id
        defaults["current_dollar_rate"] = order.current_dollar_rate

        tx = order.sudo().transaction_ids.get_last_transaction()
        if tx and tx.state in ["pending", "authorized"]:
            defaults["transaction_id"] = tx.id
            defaults["acquirer_id"] = tx.acquirer_id.id
            defaults["amount"] = tx.amount
        return defaults

    def do_confirm(self):

        active_id = self.env.context.get("active_id", False)
        order = self.env["sale.order"].browse(active_id)

        if self.amount <= 0:
            raise UserError(_("El monto debe ser positivo"))

        if self.transaction_id and self.transaction_id.amount == self.amount:
            transaction = self.transaction_id
        else:
            transaction = self.env["payment.transaction"].create(
                {
                    "amount": self.amount,
                    "acquirer_id": self.acquirer_id.id,
                    "acquirer_reference": order.name,
                    "partner_id": order.partner_id.id,
                    "sale_order_ids": [(4, order.id, False)],
                    "currency_id": self.currency_id.id,
                    "date": self.payment_date,
                    "state": "draft",
                }
            )


        if transaction.state != "done":
            transaction = transaction.with_context(payment_date=self.payment_date)
            transaction._set_transaction_pending()
            transaction._set_transaction_done()
            #transaction._post_process_after_done()

            # transaction._reconcile_after_transaction_done()
            transaction.write({'is_processed':True})
