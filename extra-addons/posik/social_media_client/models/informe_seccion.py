# -*- coding: utf-8 -*-

from odoo import models, fields, api



# class InformeSubSeccion(models.Model):
#     _name = 'social_media_client.subseccion'
#     _description = 'Informe Subseccions'

#     tittle = fields.Char(string= 'Título de la Subsección', requiered= True)

#     parent_seccion = fields.Many2many('social_media_client.informe_seccion', string="Sección padre")

class InformeSeccion(models.Model):
    _name = 'social_media_client.informe_seccion'
    _description = 'Informe Seccions'

    tittle = fields.Char(string= 'Título de Sección', requiered= True)
    description = fields.Char(string= 'Texto Descriptivo')
    note = fields.Text(string="Nota de la Sección")

    # subseccion_id = fields.Many2many('social_media_client.subseccion', string="Subsecciones")