# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductCategory(models.Model):
    _inherit='product.category'

    is_sensorica = fields.Boolean(string='Es Sensórica', default= False)
    is_component = fields.Boolean(string='Es Componente', default= False)

class ProductTemplate(models.Model):
    _inherit='product.template'

    is_sensorica = fields.Boolean(string='Sensórica', compute='_on_change_categ_id', store=True)
    is_component = fields.Boolean(string='Componente', compute='_on_change_categ_id', store=True)

    @api.onchange('categ_id')
    def _on_change_categ_id(self):
        for this in self:
            if this.categ_id:
                this.is_sensorica= this.categ_id.is_sensorica
                this.is_component= this.categ_id.is_component