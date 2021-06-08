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

    total_line_qty = fields.Float('Cantidad vendida',default=0)
    total_line_amount = fields.Float('Monto total',default=0)

    @api.onchange('name')
    def _onchange_name(self):
        if self.name:
            self.name = self.name.upper().strip()
