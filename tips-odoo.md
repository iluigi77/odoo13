# JS
### static
~~~
/// convierte un array en un objeto con la key indicada
const convertArrayToObject = (array, key) => {
    const initialValue = {};
    return array.reduce((obj, item) => {
        return {
        ...obj,
        [item[key]]: item,
        };
    }, initialValue);
};
~~~

# Odoo

## Frontend.

### Color in treeview line
~~~
<tree decoration-muted="scrapped == True" string="Stock Moves">
    ...
</tree>

decoration-bf : shows the line in BOLD

decoration-it : shows the line in ITALICS

decoration-danger : shows the line in LIGHT RED

decoration-info : shows the line in LIGHT BLUE

decoration-muted : shows the line in LIGHT GRAY

decoration-primary : shows the line in LIGHT PURPLE

decoration-success : shows the line in LIGHT GREEN

decoration-warning : shows the line in LIGHT BROWN
~~~

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


### [HERENCIA]: agregar grupo admin a elemento
~~~
<!-- base.group_system -->
<xpath expr="//button[@name='action_view_invoice']" position='attributes'>
    <attribute name="groups">base.group_system</attribute>
</xpath>
~~~

### [HERENCIA]: agregar modo debug a elemento
~~~
<!-- base.group_no_one -->
<xpath expr="//button[@name='action_view_invoice']" position='attributes'>
    <attribute name="groups">base.group_no_one</attribute>
</xpath>
~~~

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

### operators for search
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

### excute sql query
~~~
@api.one
def test(self):
    self.env.cr.execute("""
        SELECT a.id as id, COALESCE(MAX(m.date),a.date) AS date
        FROM account_asset_asset a
        LEFT JOIN account_asset_depreciation_line rel ON (rel.asset_id = a.id)
        LEFT JOIN account_move m ON (rel.move_id = m.id)
        WHERE a.id IN %s
        GROUP BY a.id, m.date """, (tuple(self.ids),))
    result = dict(self.env.cr.fetchall())
    return result
~~~

### [xmlrpc]: config
~~~
url = "http://127.0.0.1:8069"
db = "dbname"
username = 'admin'
password = 'passw'
common = client.ServerProxy('{}/xmlrpc/2/common'.format(url))
common_models = client.ServerProxy('{}/xmlrpc/2/object'.format(url))
~~~

### [xmlrpc]: use
~~~
@api.one
def test(self):
    # Read all products
    # uid = self._get_uid()
    model_name = 'product.template'
    partner_ids = common_models.execute_kw(db, uid, password, model_name, 'search', [[['default_code', '=', 'PR/06171']]] )
    partner_records = common_models.execute_kw(db, uid, password, model_name, 'read', [partner_ids])
    return partner_records   
~~~

### json to string
~~~
return json.dumps({'status': True})
~~~

### string to json
~~~
return json.loads('string_to_convert')
~~~

### switcher
~~~
switcher = {
    1: "Enero",
    2: "Febrero",
    3: "Marzo",
    4: "Abril",
    5: "Mayo",
    6: "Junio",
    7: "Julio",
    8: "Agosto",
    9: "Septiembre",
    10: "Octubre",
    11: "Noviembre",
    12: "Diciembre"
}
return switcher.get(argument, "Mes inválido")
~~~

### [object]: retorna lo que se quiere si el key no existe
~~~
obj.get('attachment_ids', [])
~~~
