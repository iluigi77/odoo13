# -*- coding: utf-8 -*-
# from odoo import http


# class SocialMediaClient(http.Controller):
#     @http.route('/social_media_client/social_media_client/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/social_media_client/social_media_client/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('social_media_client.listing', {
#             'root': '/social_media_client/social_media_client',
#             'objects': http.request.env['social_media_client.social_media_client'].search([]),
#         })

#     @http.route('/social_media_client/social_media_client/objects/<model("social_media_client.social_media_client"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('social_media_client.object', {
#             'object': obj
#         })
