# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import RedirectWarning, UserError, ValidationError, AccessError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    client_tax_group_id = fields.Many2one('account.tax.group', string='Grupo de Impuestos')
    supplier_tax_group_id = fields.Many2one('account.tax.group', string='Grupo de Impuestos Proveedor')

    @api.onchange('company_id')
    def _onchange_company_id(self):
        self.taxes_id= [(3,tax.id) for tax in self.taxes_id]
        self.supplier_taxes_id= [(3,tax.id) for tax in self.supplier_taxes_id]

    @api.onchange('client_tax_group_id')
    def _onchange_client_tax_group_id(self):
        if self.client_tax_group_id:
            companies= []
            if self.company_id:
                companies= self.company_id._get_companies()
            else:
                companies= self.env['res.company'].sudo().search([]).ids

            ids = [(tax.id) for tax in self.client_tax_group_id.taxes_id if (tax.type_tax_use== 'sale' and tax.company_id.id in companies)] 
            self.taxes_id = [(6, 0, ids)]
            self.client_tax_group_id= None
    
    @api.onchange('supplier_tax_group_id')
    def _onchange_supplier_tax_group_id(self):
        if self.supplier_tax_group_id:
            companies= []
            if self.company_id:
                companies= self.company_id._get_companies()
            else:
                companies= self.env['res.company'].sudo().search([]).ids

            ids = [(tax.id) for tax in self.supplier_tax_group_id.taxes_id if (tax.type_tax_use== 'purchase' and tax.company_id.id in companies)] 
            self.supplier_taxes_id = [(6, 0, ids)]
            self.supplier_tax_group_id= None

    @api.constrains('taxes_id')
    def _validate_for_taxes_id(self):
        if False:
            companies= []
            if self.company_id:
                companies= self.company_id._get_companies()
            else:
                companies= self.env['res.company'].sudo().search([]).ids

            obj_company={}
            for company in companies:
                obj_company.setdefault(company, 0)

            for tax in self.taxes_id:
                obj_company[tax.company_id.id] += 1

            if(not self._check_tax(obj_company.values()) ):
                raise UserError("Los impuestos de cliente no están bien definidos para todas las compañias en este producto.")

    @api.constrains('supplier_taxes_id')
    def _validate_for_supplier_taxes_id(self):
        if False:
            companies= []
            if self.company_id:
                companies= self.company_id._get_companies()
            else:
                companies= self.env['res.company'].sudo().search([]).ids

            obj_company={}
            for company in companies:
                obj_company.setdefault(company, 0)

            for tax in self.supplier_taxes_id:
                obj_company[tax.company_id.id] += 1

            if(not self._check_tax(obj_company.values()) ):
                raise UserError("Los impuestos de Proveedor no están bien definidos para todas las compañias en este producto.")
    
    def _check_tax(self, taxes):
        for tax in taxes:
            if not tax== 1:
                return False
        return True 

class resCompany(models.Model):
    _inherit = 'res.company'

    def _get_companies(self):
        companies= []
        if not self.child_ids:
            return [self.id]
        else:
            companies+= [self.id] 
            for child in self.sudo().child_ids:
                companies += child._get_companies()
            return companies
