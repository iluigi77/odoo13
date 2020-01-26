# -*- coding: utf-8 -*-
# from odoo import http


# class SocialMediaClient(http.Controller):
#     @http.route('/posik_client/posik_client/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/posik_client/posik_client/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('posik_client.listing', {
#             'root': '/posik_client/posik_client',
#             'objects': http.request.env['posik_client.posik_client'].search([]),
#         })

#     @http.route('/posik_client/posik_client/objects/<model("posik_client.posik_client"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('posik_client.object', {
#             'object': obj
#         })
