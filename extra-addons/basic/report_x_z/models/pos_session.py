# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning, AccessDenied


class PosSession(models.Model):
    _inherit = 'pos.session'

    def generate_report_x(self):
        if True: # Validations
            cashier= self.user_id.name
            widget_action= {
                "type": "ir.actions.client",
                "tag": "GenerateReportXZWidget",
                'context': {
                    'cashier_name': cashier,
                    'type_report': 'x'
                    },
            }
            return widget_action
        else: 
            raise UserError(_("El reporte ya se ha impreso anteriormente."))

    def generate_report_z(self):
        if True: # Validations
            cashier= self.user_id.name
            widget_action= {
                "type": "ir.actions.client",
                "tag": "GenerateReportXZWidget",
                'context': {
                    'cashier_name': cashier,
                    'type_report': 'z'
                    },
            }
            return widget_action
        else: 
            raise UserError(_("El reporte ya se ha impreso anteriormente."))

    def get_context_report(self):
        cashier_name= self.env.user.name
        # get session
        last_session= self.env['pos.session'].search([('user_id','=',self.env.user.id)], limit=1)


        """ for add validations """
        if( not last_session):
            raise UserError("El usuario " + cashier_name + " no tiene una sesión activa en alguna caja.")
        """ ////////////////////// """
        
        return {
            'cashier_name' : cashier_name,
            # 'register_box' : last_session.config_id.name
        }