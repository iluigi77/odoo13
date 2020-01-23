# Odoo
## Frontend.

### Quitar botones de crear , editar o abrir modal en los campos de una vista
~~~
<field name="code" options="{'no_quick_create':True,'no_create_edit':True,'no_open':True}"/>
~~~

### Mostrar campo relacional como tree view
~~~
<tree>
    <field name="my_field_relation" />
</tree>
~~~

### Page para mostrar treeview
~~~
<xpath expr="//page[@name='general_information']//group[1]" position="after">
    <page name="list_for_vertical_lot" >
        <group string="Lote Vertical">
            <tree >
                <field name="products_by_lots" />
            </tree>
        </group>
    </page>    
</xpath>
~~~

### Heredar por name
~~~
<xpath expr="//group[@name='group_general']" position="inside">
    <field name="vertical_id"/>
</xpath>
~~~

### Heredar por bloques
~~~
<xpath expr="//form//sheet//notebook[1]" position="before">
    <group>
        <field name="vertical_id"/>
    </group>
</xpath>
~~~

### heredar en la cabecera de product form, al lado de actualizar inventario
~~~
<xpath expr="//form//sheet//field[1]" position="after">
    <button string="tester" type="action" name="show_list_products_by_lots" />
</xpath> 
~~~


___ 
## Backend.

### Ternario
~~~
resultado = valor_si if condicion else valor_no

~~~

### Heredar de un modelo
~~~
_inherit = 'product.template'
~~~

### Agregar tuplas al order line
~~~
products_lot = self.vertical_id.mapped('product_ids')
    for p in products_lot:
        product = self.env['product.product'].search([('product_tmpl_id', '=', p.id)])
        self.order_line = [(0,0, {
            'price_unit': product.list_price,
            'product_id': product.id,             
            'product_uom_qty': 1,
            'customer_lead': 0.0,
            'group_lot': self.vertical_id.id,
            })]
        for line in self.order_line:
            line.product_id_change()
~~~

### Almacenar datos binarios
~~~
pdf_bin = fields.Binary(string='PDF Adjunto')
~~~

### Mapeo de registros
~~~
map_record= recorset.mapped('campo')
~~~

### Actualizar registro
~~~
line.update({
    'price_subtotal':0
})

@api.depends('order_line.price_total')
def _amount_all(self):
    """
    Compute the total amounts of the SO.
    """
    for order in self:
        amount_untaxed = amount_tax = 0.0
        for line in order.order_line:
            amount_untaxed += line.price_subtotal
            amount_tax += line.price_tax
        order.update({
            'amount_untaxed': amount_untaxed,
            'amount_tax': amount_tax,
            'amount_total': amount_untaxed + amount_tax,
        })
~~~


# mientras
~~~
@api.onchange('order_line')
def _onchange_order_line(self):
    for line in self.order_line:
        p= line.product_id
        if p.product_tmpl_id.no_budgetable:
            line.price_unit= 0
            line.product_id_change()
~~~



~~~
<xpath expr="//group[@name='note_group']" position="replace">
                    <group name="note_group" col="6">
                        <group colspan="2">
                            <field name="note" nolabel="1" placeholder="Terms and conditions..."/>
                        </group>
                        <group class="oe_subtotal_footer oe_right" colspan="2" name="sale_total">
                            <field name="amount_untaxed" widget='monetary' options="{'currency_field': 'currency_id'}"/>
                            <field name="amount_tax" widget='monetary' options="{'currency_field': 'currency_id'}"/>
                            <div class="oe_subtotal_footer_separator oe_inline o_td_label">
                                <label for="amount_total" />
                            </div>
                            <field name="amount_total" nolabel="1" class="oe_subtotal_footer_separator" widget='monetary' options="{'currency_field': 'currency_id'}"/>
                        </group>
                        <group class="oe_subtotal_footer oe_right" colspan="2" name="sale_total_services">
                            <field name="amount_untaxed_service" widget='monetary' options="{'currency_field': 'currency_id'}"/>
                            <field name="amount_tax_service" widget='monetary' options="{'currency_field': 'currency_id'}"/>
                            <div class="oe_subtotal_footer_separator oe_inline o_td_label">
                                <label for="amount_total_service" />
                            </div>
                            <field name="amount_total_service" nolabel="1" class="oe_subtotal_footer_separator" widget='monetary' options="{'currency_field': 'currency_id'}"/>
                        </group>
                        <group class="oe_subtotal_footer oe_right" colspan="2" name="sale_total_no_services">
                            <field name="amount_untaxed_no_service" widget='monetary' options="{'currency_field': 'currency_id'}"/>
                            <field name="amount_tax_no_service" widget='monetary' options="{'currency_field': 'currency_id'}"/>
                            <div class="oe_subtotal_footer_separator oe_inline o_td_label">
                                <label for="amount_total_no_service" />
                            </div>
                            <field name="amount_total_no_service" nolabel="1" class="oe_subtotal_footer_separator" widget='monetary' options="{'currency_field': 'currency_id'}"/>
                        </group>
                        
                        <div class="oe_clear"/>
                    </group>
                </xpath>
~~~