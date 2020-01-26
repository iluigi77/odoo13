# -*- coding: utf-8 -*-

from odoo import models, fields, api



class InformeSubSeccion(models.Model):
    _name = 'posik_client.informe_subseccion'
    _description = 'Informe Subseccions'

    name = fields.Char(string= 'Título de la Subsección', required= True)

    parent_seccion_id = fields.Many2one('posik_client.informe_seccion', string="Sección padre", relation='posik_informe_seccion_subseccion')

class InformeSeccion(models.Model):
    _name = 'posik_client.informe_seccion'
    _description = 'Informe Seccions'

    name = fields.Char(string= 'Título de Sección', required= True)
    description = fields.Char(string= 'Texto Descriptivo')
    note = fields.Text(string="Nota de la Sección")

    subseccion_id = fields.One2many('posik_client.informe_subseccion', 'parent_seccion_id', string="Subsecciones", relation='smc_subseccion_informe_seccion')