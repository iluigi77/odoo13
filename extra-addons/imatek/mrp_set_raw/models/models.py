# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class mrp_set_raw(models.Model):
#     _name = 'mrp_set_raw.mrp_set_raw'
#     _description = 'mrp_set_raw.mrp_set_raw'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
