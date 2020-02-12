# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.category'

    type = fields.Selection([
        ('none', 'Ninguno'),
        ('service', 'Servicio'),
        ('sensorica', 'Sensórica'),
        ('software', 'Software'),
        ('component', 'Componente')], string='Tipo de Categoría', default=None)
        