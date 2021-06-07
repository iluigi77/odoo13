# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.http import request
import datetime
import time



class ResCurrency(models.Model):
    _inherit= "res.currency"

    absolute_rate = fields.Float(compute='_compute_absolute_rate', string='Current Rate', digits=0,
                        help='The rate of the currency to the currency of rate 1.')

    def _compute_absolute_rate(self):
        self.absolute_rate= self.env['res.currency.line'].get_last_rate()

class CurrencyLine(models.Model):
    _name = 'res.currency.line'
    _description = 'currency line'
    _order = "name desc"

    """ Caso la tasa a una sola moneda (usd) """
    @api.model
    def _get_usd_currency(self):
        currency= self.env['res.currency'].sudo().search([('name', '=', 'USD')], limit=1)
        return currency.id

    """ Obtiene la moneda del sistema (Bs) """
    @api.model
    def _get_user_currency(self):
        currency_id = self.env['res.users'].sudo().browse(self._uid).company_id.currency_id
        return currency_id
        
    name = fields.Datetime(string='Fecha', required=True, index=True, default=lambda self: fields.datetime.now(), readonly=True)
    rate = fields.Float(string='Tasa', default=1.0)

    """ Campo para obtener la moneda usd desde el modelo de res.currency (nativo) """
    currency_usd_id = fields.Many2one('res.currency', string='Divisa', readonly=True, default= _get_usd_currency)

    """ Campo para obtener la moneda actual de la compañia """
    currency_company_id = fields.Many2one('res.currency', string='Moneda Base', store=True,
        compute= '_get_user_currency',default=lambda self: self._get_user_currency())

    """ identifica la tasa actual para la vista """
    actual = fields.Boolean(string='Tasa actual', compute='_check_last_rate')

    _sql_constraints = [
        ('dollar_rate_check', 'CHECK (rate>0)', 'La tasa debe ser estrictamente positiva.'),
    ]

    @api.model
    def create(self,vals):
        model_rate = super(CurrencyLine, self).create(vals)
        """ to do ... """
        return model_rate

    """ Para modificar el tipo de busquedad por defecto """
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        if operator in ['=', '!=']:
            try:
                date_format = '%Y-%m-%d'
                if self._context.get('lang'):
                    lang_id = self.env['res.lang']._search([('code', '=', self._context['lang'])], access_rights_uid=name_get_uid)
                    if lang_id:
                        date_format = self.browse(lang_id).date_format
                name = time.strftime('%Y-%m-%d', time.strptime(name, date_format))
            except ValueError:
                try:
                    args.append(('rate', operator, float(name)))
                except ValueError:
                    return []
                name = ''
                operator = 'ilike'
        return super(CurrencyLine, self)._name_search(name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)

    def get_last_rate(self):
        last = self.env['res.currency.line'].sudo().search([],limit=1)
        return float(last.rate) if last else 1

    def _check_last_rate(self):
        last = self.env['res.currency.line'].sudo().search([],limit=1)
        for rate in self:
            rate.actual= True if last and last.id == rate.id else False


    def increase_to_current_rate(self, base, value):
        return base* value

    def set_rate_all_products(self):
        products = self.env['product.template'].sudo().search([])
        value= self.rate
        increase = self.increase_to_current_rate

        for product in products:
            product.list_price= increase(product.dollar_price, value)
        
        return self.action_tree_product_template()

    def action_tree_product_template(self):
        self.ensure_one()
        action = self.env.ref('report_gap.action_report_gap').read()[0]
        return action