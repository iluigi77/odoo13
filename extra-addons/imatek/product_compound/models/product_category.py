# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductCategory(models.Model):
    _inherit='product.category'

    is_sensorica = fields.Boolean(string='Es Sensórica', default= False)
    is_component = fields.Boolean(string='Es Componente', default= False)
    is_service = fields.Boolean(string='Es Servicio', default= False)

class ProductTemplate(models.Model):
    _inherit='product.template'

    is_sensorica = fields.Boolean(string='Sensórica', compute='_on_change_categ_id')
    is_component = fields.Boolean(string='Componente', compute='_on_change_categ_id')
    is_service = fields.Boolean(string='Servicio', compute='_on_change_categ_id')

    @api.depends('categ_id')
    def _on_change_categ_id(self):
        if self.categ_id:
            self.is_sensorica= self.categ_id.is_sensorica
            self.is_component= self.categ_id.is_component
            self.is_service= self.categ_id.is_service