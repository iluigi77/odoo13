# -*- coding: utf-8 -*-

from odoo import models, fields, api

class SalesOrderLine(models.Model):
    _inherit = 'sale.order.line'

    vertical_id = fields.Many2one('verticals.verticals', string= 'Vertical')

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    vertical_ids = fields.Many2many('verticals.verticals', string= 'Vetical')

    @api.onchange('vertical_ids')
    def _onchange_vertical_ids(self):
        self.order_line= [(2,t.id) for t in self.order_line if not t.vertical_id.id == False]
        for vertical in self.vertical_ids:
            #add line
            self.order_line = [(0,0, {
                'display_type': 'line_section',
                'name': vertical.name,
                'price_unit': 0.0,
                'product_id': None,             
                'product_uom_qty': 0,
                'customer_lead': 0.0,
                'vertical_id': vertical.id.origin,
            })]

            for p in vertical.mapped('product_ids'):
                product = self.env['product.product'].search([('product_tmpl_id', '=', p.id.origin)])
                self.order_line = [(0,0, {
                    'price_unit': product.list_price,
                    'product_id': product.id,             
                    'product_uom_qty': 1,
                    'customer_lead': 0.0,
                    'vertical_id': vertical.id.origin,
                    })]
        for line in self.order_line:
            line.product_id_change()
 
    def action_quotation_send(self):
        attachments= []
        result = super(SaleOrder, self ).action_quotation_send() 
        attachments=[(4,v.attachment_id.id) for v in self.vertical_ids if v.attachment_id]
        attachments +=[(4, p.product_tmpl_id.attachment_id.id) for p in self.order_line.mapped('product_id') if p.product_tmpl_id.attachment_id]
        result['context'].update({ 'attachment_ids' : attachments }) 
        return result

class MailComposeMessage(models.TransientModel):
    _inherit= 'mail.compose.message'

    def onchange_template_id(self, template_id, composition_mode, model, res_id):
        attachments= self._context['attachment_ids']
        result = super(MailComposeMessage, self ).onchange_template_id(template_id, composition_mode, model, res_id)
        attachments.append((4, result['value']['attachment_ids'][0][2][0]))
        result['value']['attachment_ids']= attachments
        return result