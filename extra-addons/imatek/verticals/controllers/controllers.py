# -*- coding: utf-8 -*-
# from odoo import http


# class Verticals(http.Controller):
#     @http.route('/verticals/verticals/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/verticals/verticals/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('verticals.listing', {
#             'root': '/verticals/verticals',
#             'objects': http.request.env['verticals.verticals'].search([]),
#         })

#     @http.route('/verticals/verticals/objects/<model("verticals.verticals"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('verticals.object', {
#             'object': obj
#         })
