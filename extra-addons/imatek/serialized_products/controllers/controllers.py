# -*- coding: utf-8 -*-
# from odoo import http


# class SerializedProducts(http.Controller):
#     @http.route('/serialized_products/serialized_products/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/serialized_products/serialized_products/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('serialized_products.listing', {
#             'root': '/serialized_products/serialized_products',
#             'objects': http.request.env['serialized_products.serialized_products'].search([]),
#         })

#     @http.route('/serialized_products/serialized_products/objects/<model("serialized_products.serialized_products"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('serialized_products.object', {
#             'object': obj
#         })
