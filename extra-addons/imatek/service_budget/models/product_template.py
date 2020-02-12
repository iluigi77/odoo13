# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    no_budgetable = fields.Boolean(string='No presupuestable', default= False)

    @api.onchange('type')
    def _on_change_type_inherit(self):
        if self.type == 'product':
            self.no_budgetable= False 
            cate_sw_id = self.env['product.category'].search([('type', '=', 'software')], limit=1)
            if cate_sw_id and self.categ_id.type== 'service':
                self.categ_id= cate_sw_id[0].id

        elif self.type == 'service':
            cate_service_id = self.env['product.category'].search([('type', '=', 'service')], limit=1)
            if cate_service_id:
                self.categ_id= cate_service_id[0].id
        else:
            pass

    @api.onchange('categ_id')
    def _on_change_categ_id_inherit(self):
        product_id = self.env['product.product'].search([('product_tmpl_id', '=', self.id.origin)], limit=1)
        if self.categ_id:
            if self.categ_id.type == 'sensorica' or self.categ_id.type == 'software':
                self.type= 'product'
                self.no_budgetable= False 
                self.tracking= 'serial'

            elif self.categ_id.type == 'component':
                self.type= 'product'
                self.no_budgetable= True 
                self.tracking= 'none'

            elif self.categ_id.type == 'service':
                self.type= 'service'
                self.no_budgetable= True 
                self.tracking= 'none'

            else:
                pass
        self.onchange_tracking() #for template
        product_id.onchange_tracking() # for product
            
