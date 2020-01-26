# -*- coding: utf-8 -*-
# from odoo import http


# class LinkBuilding(http.Controller):
#     @http.route('/link_building/link_building/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/link_building/link_building/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('link_building.listing', {
#             'root': '/link_building/link_building',
#             'objects': http.request.env['link_building.link_building'].search([]),
#         })

#     @http.route('/link_building/link_building/objects/<model("link_building.link_building"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('link_building.object', {
#             'object': obj
#         })
