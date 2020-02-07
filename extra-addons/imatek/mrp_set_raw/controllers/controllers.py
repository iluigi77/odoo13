# -*- coding: utf-8 -*-
# from odoo import http


# class MrpSetRaw(http.Controller):
#     @http.route('/mrp_set_raw/mrp_set_raw/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mrp_set_raw/mrp_set_raw/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mrp_set_raw.listing', {
#             'root': '/mrp_set_raw/mrp_set_raw',
#             'objects': http.request.env['mrp_set_raw.mrp_set_raw'].search([]),
#         })

#     @http.route('/mrp_set_raw/mrp_set_raw/objects/<model("mrp_set_raw.mrp_set_raw"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mrp_set_raw.object', {
#             'object': obj
#         })
