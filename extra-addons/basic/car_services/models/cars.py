# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Cars(models.Model):
    _name = 'car.model'
    _description = 'for store the car '

    name = fields.Char('Matrícula', help="Patente/matrícula del vehículo.", required=True)
    invoice_ids = fields.One2many('car.services.invoice', 'car_id' ,string='Facturas', help="Facturas asociadas")
    total_invoice= fields.Integer('Total de Facturas', compute="_get_total_invoice")

    """ for reports """
    total_line_qty = fields.Float('Cantidad de servicios consumidos',default=0)




    @api.depends('invoice_ids')
    def _get_total_invoice(self):
        for car in self:
            invs= car.invoice_ids.filtered(lambda x: x.state == 'done')
            car.total_invoice= len(invs)

    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            self.name = self.name.upper().strip()