# -*- coding: utf-8 -*-
# from odoo import http


# class PosikReport(http.Controller):
#     @http.route('/posik_report/posik_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/posik_report/posik_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('posik_report.listing', {
#             'root': '/posik_report/posik_report',
#             'objects': http.request.env['posik_report.posik_report'].search([]),
#         })

#     @http.route('/posik_report/posik_report/objects/<model("posik_report.posik_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('posik_report.object', {
#             'object': obj
#         })
