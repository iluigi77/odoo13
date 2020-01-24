# -*- coding: utf-8 -*-
# from odoo import http


# class PosikProject(http.Controller):
#     @http.route('/posik_project/posik_project/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/posik_project/posik_project/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('posik_project.listing', {
#             'root': '/posik_project/posik_project',
#             'objects': http.request.env['posik_project.posik_project'].search([]),
#         })

#     @http.route('/posik_project/posik_project/objects/<model("posik_project.posik_project"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('posik_project.object', {
#             'object': obj
#         })
