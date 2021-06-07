from odoo import models, fields, api

class IncreasePriceWizard(models.TransientModel):

    _name = 'list_price.increase.wizard'

    def _get_default_products(self):
        products= self.env['product.template'].browse(self.env.context.get('active_ids'))
        return products

    def _get_current_rate(self):
        rate_model= self.env['res.currency.line']
        rate= rate_model.get_last_rate() or 1
        return rate

    product_ids = fields.Many2many('product.template', string='Productos', default=_get_default_products)

    lines_ids = fields.One2many('increase.line', 'increase_id', string='Productos')
    dollar_rate = fields.Float('Tasa del dolar', required=True, default= _get_current_rate)
    value = fields.Float('Aumento', required=True)
    type = fields.Selection([
        ('fixed','Fijo'), 
        ('percentage',' Porcentaje')
        ],'Tipo de aumento', default='fixed', required=1) 
        
    target = fields.Selection([
        ('sale','De Venta'), 
        ('coste',' De Costo')
        ],'Modificar Precio', required=1) 

    base = fields.Selection([
        ('sale','Precio de Venta'), 
        ('coste','Costo'),
        ('dollar','Tasa del Dólar'),
        ], 'Basado en', required=1)
    
    def increase_by_percentage(self, base, percentage):
        return base + (base * (percentage / 100))

    def increase_fixed(self, base, increase):
        return base + increase

    """ base is dollar price, value is dollar rate """
    def increase_to_current_rate(self, base, value):
        return base* value

    def set_list_price(self):
        self.env['increase.line'].sudo().search([]).unlink()

        record = self
        lines= []
        value= record.value
        target= 'new_price' if record.target== 'sale' else 'new_cost'

        if(record.type == 'fixed'):
            """ for fixed increase """
            increase= self.increase_fixed
        else:
            """ for percentage increase """
            increase = self.increase_by_percentage

        if (record.base == 'sale'): 
            base= 'list_price'
        elif (record.base == 'coste'):
            base= 'standard_price'
        else:
            """ basado en la tasa del dollar """
            base= 'dollar_price' if record.target== 'sale' else 'dollar_coste'
            increase = self.increase_to_current_rate
            value= self.dollar_rate

        for product in record.product_ids:
            values = { 'product_id': product.id}
            values[target]=increase(product[base], value)
            record.lines_ids= [(0,0,values)]
        
        view_id= 'product_price_increase.action_increase_price_preview_price' if record.target== 'sale'  else 'product_price_increase.action_increase_price_preview_cost'
        action = self.env.ref(view_id).read()[0]
        return action
                