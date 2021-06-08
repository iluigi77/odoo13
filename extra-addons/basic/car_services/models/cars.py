# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Cars(models.Model):
    _name = 'car.model'
    _description = 'for store the car '

    name = fields.Char('Matrícula', help="Patente/matrícula del vehículo.", required=True)
    invoice_ids = fields.One2many('car.services.invoice', 'car_id' ,string='Facturas', help="Facturas asociadas")
    total_invoice= fields.Integer('Total de Facturas', compute="_get_total_invoice")

    """ for reports """
    total_line_qty = fields.Float('Cantidad de servicios consumidos', compute="_compute_total_lines")

    @api.depends('invoice_ids')
    def _compute_total_lines(self):
        for car in self:
            total_line_qty= 0
            for l in car.invoice_ids.line_ids:
                if l.invoice_id.state == 'done':
                    total_line_qty += l.qty

            car.total_line_qty= total_line_qty



    @api.depends('invoice_ids')
    def _get_total_invoice(self):
        for car in self:
            invs= car.invoice_ids.filtered(lambda x: x.state == 'done')
            car.total_invoice= len(invs)
