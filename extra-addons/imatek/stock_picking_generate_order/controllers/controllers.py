# -*- coding: utf-8 -*-
# from odoo import http


# class StockPickingGenerateOrder(http.Controller):
#     @http.route('/stock_picking_generate_order/stock_picking_generate_order/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_picking_generate_order/stock_picking_generate_order/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_picking_generate_order.listing', {
#             'root': '/stock_picking_generate_order/stock_picking_generate_order',
#             'objects': http.request.env['stock_picking_generate_order.stock_picking_generate_order'].search([]),
#         })

#     @http.route('/stock_picking_generate_order/stock_picking_generate_order/objects/<model("stock_picking_generate_order.stock_picking_generate_order"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_picking_generate_order.object', {
#             'object': obj
#         })
