# Odoo

## Frontend.

### readonly dinamico
~~~
<field name='short_timesheet'/> 
<field name="unit_amount" widget="timesheet_uom"  attrs="{'readonly':[('short_timesheet','=',True)]}" />
~~~

### Default order
~~~
<tree string="Sales Order Lines"  default_order="sequence desc">
    <field name="order_id"/>
    <field name="sequence"/>
</tree>
~~~

### boton en un field del treeview
~~~
<button type="object" icon="gtk-delete" name="unlink"/>
~~~

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


### [HERENCIA]
~~~
<record id="discount_in_order_line" model="ir.ui.view">
    <field name="name">sale.order.discount_order_line</field>
    <field name="model">sale.order</field>
    <field name="inherit_id" ref="sale.view_order_form"/>
    <field name="arch" type="xml">
        <xpath expr="//field[@name='order_line']//tree//field[@name='discount']" position="replace">
            <field name="discount" string="Desc.%"/>
        </xpath>
    </field>
</record>
~~~



### [HERENCIA]: Heredar field y agregar atributo
~~~
<xpath expr="//field[@name='vat']" position="attributes">
    <attribute name="string">VAT</attribute>
</xpath>
~~~

### [HERENCIA]: Heredar por name
~~~
<xpath expr="//group[@name='group_general']" position="inside">
    <field name="vertical_id"/>
</xpath>
~~~

### [HERENCIA]: Heredar por bloques
~~~
<xpath expr="//form//sheet//notebook[1]" position="before">
    <group>
        <field name="vertical_id"/>
    </group>
</xpath>
~~~

### [HERENCIA]: heredar en la cabecera de product form, al lado de actualizar inventario
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

### search operators
~~~
Can anyone provide me a scenario where we need to use these operators in domain:

1. =?         es igual a = pero retorna True si el lado derecho es Falso o None
2. =like      es igual a la like pero no le agrega los %%
3. =ilike     es igual a =like pero ignorando mayúsculas y minusculals
4. like       es un like con %%
5. ilike      es un like con %% ignorando mayúsuculas y minusuculas
6. child_of
~~~

### Operaciones con records
~~~
record in recset1           # include
record not in recset1       # not include
recset1 + recset2           # extend
recset1 | recset2           # union
recset1 & recset2           # intersect
recset1 - recset2           # difference
~~~

### Operaciones magicas con registros sin orm
~~~
(0, 0,  { values })    link to a new record that needs to be created with the given values dictionary
(1, ID, { values })    update the linked record with id = ID (write values on it)
(2, ID)                remove and delete the linked record with id = ID (calls unlink on ID, that will delete the object completely, and the link to it as well)
(3, ID)                cut the link to the linked record with id = ID (delete the relationship between the two objects but does not delete the target object itself)
(4, ID)                link to existing record with id = ID (adds a relationship)
(5)                    unlink all (like using (3,ID) for all linked records)
(6, 0, [IDs])          replace the list of linked IDs (like using (5) then (4,ID) for each ID in the list of IDs)
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

### Default order
~~~
class NameClass(....):
    _inherit = "name.class"
    _order = "custom_field_name, other_field ..." (you can add option asc or desc too)
~~~

# mientras
~~~
 <page string='Actividades'>
                                <field name="activities_seccion" mode='tree'>
                                    <tree
                                        decoration-bf="type_row == 'seccion'"
                                        decoration-info="type_row == 'subseccion'"
                                        decoration-warning="type_row == 'shor_activity'"
                                        >
                                        <field name='header_name'/>
                                        <field name='name'/>
                                        <field name='url'/>
                                        <field name='type_row' invisible="1"/>
                                    </tree>
                                </field>
                                <div class="oe_clear"/>
                            </page>
~~~

# baul
~~~
def generate_activities(self):
    self.activities_seccion= [(3,t.id) for t in self.activities_seccion]
    res = {}
    for item in self.activity_url:
        # crea una entrada en el dict (seccion)
        res.setdefault(item['seccion_id']['name'], {})
        # a la entrada creada, le crea otra entrada (subseccion) y le a;ade un elemento al array
        res[item['seccion_id']['name']].setdefault(item['subseccion_id']['name'], []).append(item.read(["name", "url", "short_timesheet"])[0])
    
    for seccion in res:
        self.activities_seccion=[(0,0,{
            'header_name': seccion,
            'type_row': 'seccion',
        })]
        for sub in res[seccion]:
            self.activities_seccion=[(0,0,{
                'header_name': sub,
                'type_row': 'subseccion',
            })]
            for p in res[seccion][sub]:
                self.activities_seccion=[(0,0,{
                    'header_name': '->',
                    'name': p['name'],
                    'url': p['url'],
                    'type_row': 'activity' if not p['short_timesheet'] else 'shor_activity',
                })] 
~~~