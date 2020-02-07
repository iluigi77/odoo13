# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SalesOrderLine(models.Model):
    _inherit = 'sale.order.line'

    vertical = fields.Many2one('verticals.verticals', string= 'Vertical')
    vertical_id = fields.Integer(string= 'Vertical ID')
    product_category_id = fields.Many2one('product.category', string='Categoría')

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    pdf_bin = fields.Binary(string='PDF Adjunto')
    # vertical_id = fields.Many2one('verticals.verticals', string= 'Vetical')
    vertical_id = fields.Many2many('verticals.verticals', string= 'Vetical')

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            discount= self.partner_id.discount_category
            for line in self.order_line:
                line.discount= discount
                line.product_id_change()

    @api.onchange('vertical_id')
    def _onchange_vertical_id(self):
        self.order_line= [(2,t.id) for t in self.order_line if not t.vertical.id == False]

        for vertical in self.vertical_id:
            lot= vertical
            discount= 0
            if self.partner_id:
                discount= self.partner_id.discount_category

            self.order_line = [(0,0, {
                'display_type': 'line_section',
                'name': lot.name,
                'price_unit': 0.0,
                'product_id': None,             
                'product_uom_qty': 0,
                'customer_lead': 0.0,
                'vertical': lot.id.origin,
                'vertical_id': lot.id.origin,
            })]
            for line in self.order_line:
                line.product_id_change()

            products_lot = vertical.mapped('product_ids')
            for p in products_lot:
                product = self.env['product.product'].search([('product_tmpl_id', '=', p.id.origin)])
                self.order_line = [(0,0, {
                    'price_unit': product.list_price,
                    'product_id': product.id,             
                    'product_uom_qty': 1,
                    'customer_lead': 0.0,
                    'vertical': lot.id.origin,
                    'vertical_id': lot.id.origin,
                    'discount': discount,
                    })]
            for line in self.order_line:
                line.product_id_change()
 
                # self.vertical_id=None

    @api.onchange('order_line')
    def _onchange_order_line(self):
        for line in self.order_line:
            discount= 0
            if self.partner_id:
                discount= self.partner_id.discount_category
            line.discount= discount
            line.product_category_id= line.product_id.product_tmpl_id.categ_id
            
    def action_quotation_send(self):
        attachments= []
        result = super(SaleOrder, self ).action_quotation_send() 
        attachments=[(4,vertical.pdf_bin.id) for vertical in self.vertical_id if vertical.pdf_bin]
        attachments +=[(4, p.product_tmpl_id.pdf_bin.id) for p in self.order_line.mapped('product_id') if p.product_tmpl_id.pdf_bin]
        result['context'].update({ 'attachment_ids' : attachments }) 
        return result


class MailComposeMessage(models.TransientModel):
    _inherit= 'mail.compose.message'

    def onchange_template_id(self, template_id, composition_mode, model, res_id):
        attachments= self._context['attachment_ids']
        result = super(MailComposeMessage, self ).onchange_template_id(template_id, composition_mode, model, res_id)
        old= (4, result['value']['attachment_ids'][0][2][0]) 
        attachments.append(old)
        result['value']['attachment_ids']= attachments
        return result