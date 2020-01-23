# -*- coding: utf-8 -*-
# from odoo import http


# class ClientDiscount(http.Controller):
#     @http.route('/client_discount/client_discount/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/client_discount/client_discount/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('client_discount.listing', {
#             'root': '/client_discount/client_discount',
#             'objects': http.request.env['client_discount.client_discount'].search([]),
#         })

#     @http.route('/client_discount/client_discount/objects/<model("client_discount.client_discount"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('client_discount.object', {
#             'object': obj
#         })
