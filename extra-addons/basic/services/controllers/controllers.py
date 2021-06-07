# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.addons import web
from odoo.http import request
from odoo.service import security
from odoo.exceptions import Warning
import odoo.addons.web.controllers.main as main

import json
import werkzeug
import werkzeug.utils
import time
from datetime import datetime

import logging

_logger = logging.getLogger(__name__)


class Services(http.Controller):
    @http.route('/product', auth='none', type='http', csrf=False, method=['GET'], cors='*')
    def get_all(self, **kw):
        product = request.env['product.product'].sudo().search( [], limit= 1)
        return json.dumps(product.read(['id', 'display_name', 'list_price', 'barcode', 'dollar_active', 'dollar_price']))
    
    @http.route('/product/<string:code>', auth='none', type='http', csrf=False, method=['GET'], cors='*')
    def get_one(self, code, **kw):
        product = request.env['product.product'].sudo().search( [['barcode', '=', code]], limit= 1)
        return json.dumps(product.read(['id', 'display_name', 'list_price', 'barcode', 'dollar_active', 'dollar_price']))

