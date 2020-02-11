# -*- coding: utf-8 -*-
# from odoo import http


# class AutoSerialNumber(http.Controller):
#     @http.route('/auto_serial_number/auto_serial_number/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/auto_serial_number/auto_serial_number/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('auto_serial_number.listing', {
#             'root': '/auto_serial_number/auto_serial_number',
#             'objects': http.request.env['auto_serial_number.auto_serial_number'].search([]),
#         })

#     @http.route('/auto_serial_number/auto_serial_number/objects/<model("auto_serial_number.auto_serial_number"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('auto_serial_number.object', {
#             'object': obj
#         })
