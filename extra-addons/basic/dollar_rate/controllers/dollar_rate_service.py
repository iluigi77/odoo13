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


class DollarRate(http.Controller):
    """ get last dollar rate from odoo """
    @http.route('/rate/last-rate', auth='none', type='http', csrf=False, method=['GET'], cors='*')
    def get_last_rate(self, **kw):
        rate = request.env['res.currency.line'].sudo().search( [ ], limit= 1)
        actual_rate = {
            'id': rate.id, 
            'name': rate.name.strftime("%Y-%m-%d %H:%M:%S.%f"),
            'rate': rate.rate, 
            'currency_company_id': rate.currency_company_id.id, 
            'currency_id': rate.currency_id.id, 
            'actual': rate.actual
        }
        return json.dumps(actual_rate)