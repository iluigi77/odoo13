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


___ 
## Backend.

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