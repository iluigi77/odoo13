# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _get_current_company(self):
        return self.env.company

    company_id = fields.Many2one('res.company', 'Company', index=1,
        default= _get_current_company)
    # change_default=True
    
