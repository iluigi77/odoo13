# -*- coding: utf-8 -*-
# from odoo import http


# class ProductCompound(http.Controller):
#     @http.route('/product_compound/product_compound/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/product_compound/product_compound/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('product_compound.listing', {
#             'root': '/product_compound/product_compound',
#             'objects': http.request.env['product_compound.product_compound'].search([]),
#         })

#     @http.route('/product_compound/product_compound/objects/<model("product_compound.product_compound"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('product_compound.object', {
#             'object': obj
#         })
