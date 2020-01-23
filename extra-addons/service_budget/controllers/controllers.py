# -*- coding: utf-8 -*-
# from odoo import http


# class ServiceBudget(http.Controller):
#     @http.route('/service_budget/service_budget/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/service_budget/service_budget/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('service_budget.listing', {
#             'root': '/service_budget/service_budget',
#             'objects': http.request.env['service_budget.service_budget'].search([]),
#         })

#     @http.route('/service_budget/service_budget/objects/<model("service_budget.service_budget"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('service_budget.object', {
#             'object': obj
#         })
