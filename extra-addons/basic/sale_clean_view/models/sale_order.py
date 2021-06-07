# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.exceptions import Warning
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, float_compare, float_is_zero

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    """ ya lo estableci en el modulo de sale payment register """
    current_dollar_rate = fields.Float('Tasa establecida')

    def _set_current_rate(self):
        current_rate= self.env['res.currency.line'].get_last_rate()
        for sale in self:
            sale.current_dollar_rate= current_rate

    def action_confirm(self):
        if len(self.order_line) < 1:
            raise ValidationError("No puede confirmar una cotizacion sin productos seleccionados")

        res= super(SaleOrder,self).action_confirm()
        self._set_current_rate()
        return res

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    
    @api.onchange('product_id')
    def product_id_change(self):
        if not self.order_id.partner_id:
            raise ValidationError('Debe seleccionar un cliente para poder acceder a los productos disponibles')
        else:
            super(SaleOrderLine, self).product_id_change()