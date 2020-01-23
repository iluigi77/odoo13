# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class serialized_products(models.Model):
#     _name = 'serialized_products.serialized_products'
#     _description = 'serialized_products.serialized_products'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
