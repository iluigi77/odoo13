# -*- coding: utf-8 -*-

from odoo import models, fields, api


class IncreaseLine(models.TransientModel):
    _name = 'increase.line'

    increase_id = fields.Many2one('list_price.increase.wizard', string='wizard incremento')

    product_id = fields.Many2one('product.product', string='Product', 
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]",
        change_default=True, ondelete='restrict', check_company=True)  # Unrequired company
        
    product_template_id = fields.Many2one('product.template', string='Product Template', 
        related="product_id.product_tmpl_id", domain=[('sale_ok', '=', True)])

    name = fields.Char('Name', related="product_template_id.name", index=True, required=True, translate=True)
    barcode = fields.Char('Barcode', related='product_template_id.barcode', readonly=False)
    
    list_price = fields.Float('Precio de venta', related="product_template_id.list_price", digits='Product Price', default=0.0)
    standard_price = fields.Float('Precio de compra', related="product_template_id.standard_price", digits='Product Price', default=0.0)

    dollar_price= fields.Float(string='Precio de Venta ($)', related='product_template_id.dollar_price' , required=True) # Precio en Dollar
    dollar_coste= fields.Float(string='Costo ($)', related='product_template_id.dollar_coste' , required=True) # Costo en Dollar

    gap_value = fields.Float(string= "GAP (%)", related='product_template_id.gap_value')
    gap_dollar = fields.Float(string= "GAP $(%)", related='product_template_id.gap_dollar')

    new_price = fields.Float(
        'Nuevo Precio de venta',
        digits='Product Price',
        help="Último Precio de venta del producto")

    new_cost = fields.Float(
        'Nuevo costo',
        digits='Product Price',
        help="Último Costo de compra del producto")

    gap_list_price = fields.Float(string= "GAP Venta (%)", compute="_compute_gap_list_price")
    gap_coste = fields.Float(string= "GAP Coste (%)", compute="_compute_gap_coste")

    @api.depends('list_price', 'new_price')
    def _compute_gap_list_price(self):
        for record in self:
            if (record.list_price and record.new_price ):
                val= (((record.new_price - record.list_price)/ record.list_price)*100)
                record.gap_list_price= round(val,2)
            else:
                record.gap_list_price= 0

    @api.depends('standard_price', 'new_cost')
    def _compute_gap_coste(self):
        for record in self:
            if (record.standard_price and record.new_cost ):
                val= (((record.new_cost - record.standard_price)/ record.standard_price)*100)
                record.gap_coste= round(val,2)
            else:
                record.gap_coste= 0

    
    @api.model
    def apply_increase(self):
        lines= self.env['increase.line'].sudo().search([])
        if lines:
            if lines[0].increase_id.target == 'sale':
                for l in lines:
                    l.product_template_id.list_price= l.new_price
            else:
                for l in lines:
                    l.product_template_id.standard_price= l.new_cost

        view_tree_id = self.env.ref('report_gap.product_template_tree_view_gap_inherit').id
        view_form_id = self.env.ref('product.product_template_form_view').id

        return {'type': 'ir.actions.act_window',
                'name': ('Indicador GAP'),
                'res_model': 'product.template',
                'target': 'main',
                'view_mode': 'tree, form',
                'views': [[view_tree_id, 'list'], [view_form_id, 'form']],
        }

