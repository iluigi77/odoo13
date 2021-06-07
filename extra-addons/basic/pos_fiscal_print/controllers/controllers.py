# -*- coding: utf-8 -*-
from odoo import http
import json

class FiscalPrint(http.Controller):
    @http.route('/fiscal_print/test/', auth='public', type='json', csrf=False, method=['POST'])
    def test_funtion(self, **kw):
        print('test fpr fiscal print')
        return json.dumps({'status': 'ok'})