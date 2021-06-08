# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CarServices(models.Model):
    _name = 'car.services'
    _description = 'for store the car service'

    name = fields.Char('Nombre', help="Nombre del servicio.", required=True)
    cost = fields.Monetary(string="Costo del servicio")
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, readonly=True, default=lambda self: self.env.company.currency_id)
    
    """ For reports """
    line_ids = fields.One2many('car.services.invoice.line', 'service_id',string='lineas asociadas')

    total_line_qty = fields.Float('Cantidad vendida', compute="_compute_total_lines", store=True)
    total_line_amount = fields.Float('Monto total', compute="_compute_total_lines")

    @api.depends('line_ids')
    def _compute_total_lines(self):
        for serv in self:
            total_line_amount= 0
            total_line_qty= 0
            for l in serv.line_ids:
                if l.invoice_id.state == 'done':
                    total_line_amount +=l.cost_total
                    total_line_qty += l.qty

            serv.total_line_amount= total_line_amount
            serv.total_line_qty= total_line_qty