# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ServiceInvoiceLine(models.Model):
    _name = 'car.services.invoice.line'
    _description = 'for store the service in invoice'

    invoice_id = fields.Many2one('car.services.invoice', string='Factura Asociada')
    # state = fields.Char('Nombre', related="invoice_id.state", help="Estado de la factura.")

    service_id = fields.Many2one('car.services', string='Servicio')
    name = fields.Char('Nombre', related="service_id.name", help="Nombre del servicio.")
    
    qty = fields.Float(string="Cantidad", default=1)
    cost_unit = fields.Monetary(string="Costo del servicio", related="service_id.cost")
    cost_total = fields.Monetary(string="total", compute="_compute_cost_line")

    currency_id = fields.Many2one('res.currency', string='Currency', required=True, readonly=True, default=lambda self: self.env.company.currency_id)
    

    @api.depends('qty', 'cost_unit')
    def _compute_cost_line(self):
        for l in self:
            l.cost_total= l.qty * l.cost_unit



class ServiceInvoice(models.Model):
    _name = 'car.services.invoice'
    _description = 'for store the invoice for car service'

    name = fields.Char('Numero de Factura', help="Numero de factura.", required=True,  default=lambda self: _('New'))
    partner_name = fields.Char('Propietario', help="Nombre y apellido del propietario del vehiculo", required=True)

    car_id = fields.Many2one('car.model', string='Matrícula', help="Patente/matrícula del vehículo." , required=True)
    line_ids = fields.One2many('car.services.invoice.line', 'invoice_id', string='Servicios')
    

    amount_total = fields.Monetary(string="Total", compute="_compute_total_amount")
    total_service_qty = fields.Float(string="Total servicios", compute="_compute_total_service_qty")
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, readonly=True, default=lambda self: self.env.company.currency_id)
    
    state = fields.Selection([
            ('draft','Borrador'),
            ('done', 'Realizado'),
            # ('cancel', 'Cancelado'),
        ], string='Estado', index=True, readonly=True, default='draft',
        track_visibility='onchange', copy=False,
        )

    @api.depends('line_ids')
    def _compute_total_amount(self):
        for inv in self:
            amount_total = 0
            for line in inv.line_ids:
                amount_total += line.cost_total

            inv.update({ 'amount_total': amount_total })

    @api.depends('line_ids', 'line_ids.qty')
    def _compute_total_service_qty(self):
        for inv in self:
            total_qty = 0
            for line in inv.line_ids:
                total_qty += line.qty

            inv.update({ 'total_service_qty': total_qty })



    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['name'] = self.env['ir.sequence'].with_context(force_company=vals['company_id']).next_by_code('car_service.invoice') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('car_service.invoice') or _('New')
        result = super(ServiceInvoice, self).create(vals)
        return result

    def action_confirm(self):
        self.update({ 'state': 'done' })
        qty=0
        for line in self.line_ids:
            qty += line.qty
            line.service_id.total_line_qty += line.qty
            line.service_id.total_line_amount += line.cost_total

        self.car_id.total_line_qty += qty
