# -*- coding: utf-8 -*-

from odoo import models, fields, api

class report_gap(models.Model):
    _inherit = 'product.template'

    gap_value = fields.Float(string= "GAP (%)", compute="_compute_gap")
    gap_dollar = fields.Float(string= "GAP $(%)", compute="_compute_gap_dollar")

    @api.depends('list_price', 'standard_price')
    def _compute_gap(self):
        for record in self:
            if (record.list_price and record.standard_price ):
                val= (((record.list_price - record.standard_price)/ record.standard_price)*100)
                record.gap_value= round(val,2)
            else:
                record.gap_value= 0

    @api.depends('dollar_price', 'dollar_coste')
    def _compute_gap_dollar(self):
        for record in self:
            if (record.dollar_price and record.dollar_coste ):
                val= (((record.dollar_price - record.dollar_coste)/ record.dollar_coste)*100)
                record.gap_dollar= round(val,2)
            else:
                record.gap_dollar= 0