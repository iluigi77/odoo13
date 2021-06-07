# -*- coding: utf-8 -*-

from collections import OrderedDict
import json
import re
import uuid
from functools import partial

from lxml import etree
from dateutil.relativedelta import relativedelta
from werkzeug.urls import url_encode

from odoo import api, exceptions, fields, models, _
from odoo.tools import email_re, email_split, email_escape_char, float_is_zero, float_compare, \
    pycompat, date_utils
from odoo.tools.misc import formatLang

from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning, AccessDenied

from odoo.addons import decimal_precision as dp
import logging

_logger = logging.getLogger(__name__)


""" Facturas """
class AccountMove(models.Model):
    _inherit = 'account.move'

    fiscal_print = fields.Boolean('Impresión Fiscal', required= True, default= False)


    def action_fiscal_print_order(self):
        # if (self.user_id.id != self.env.user.id):
        #     raise AccessDenied("Permiso denegado: El usuario '%s' no puede generar esta nota de crédito." %(self.env.user.name))
        if self.fiscal_print:
            raise UserError(_("La factura ya se ha impreso anteriormente."))
        else: 
            widget_action= {
                "type": "ir.actions.client",
                # "tag": "GenerateReportXZWidget",
                "tag": "PrinterOrderWidget",
                'context': {'invoice_id': self.id},
            }
            return widget_action

    def get_invoice(self):
        products= []
        # Products
        for line in self.invoice_line_ids:
            products.append({
                # 'name': line.name, # variant name
                'name': line.product_id.name,
                'tax_type': line.tax_ids.tax_type,
                'qty': line.quantity,
                'price_unit': line.price_unit,
            })

        return {
            'user':{
                "name": self.env.user.name
            },
            'client':{
                "name": self.partner_id.name,
                "vat": self.partner_id.vat,
                "phone": self.partner_id.phone or ' - ',
                "street": self.partner_id.street or ' - ',
                "city": self.partner_id.city or '"Valencia"',
            },
            'order': {
                "pos_reference": self.name,
                "date" : self.create_date.strftime("%d/%m/%Y"),
                "products" : products,
                "payment_methods": []
            }
        }

        # return {
        #     'current_user' : self.env.user.name,
        #     'cashier_name' : self.user_id.name,
        #     'client_name' : self.partner_id.name,
        #     'client_vat' : self.partner_id.vat,
        #     'invoice_number' : self.number,
        #     'phone' : self.partner_id.phone,
        #     'address' : self.partner_id.city,
        #     'date' : self.create_date.strftime("%d/%m/%Y"),
        #     'products' : products
        # }

  
    def set_status_print(self, status):
        self.fiscal_print = status