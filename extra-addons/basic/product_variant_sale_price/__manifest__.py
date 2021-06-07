
{
    # 'name': 'Product Variant Sale Price',
    'name': 'product_variant_sale_price',
    'summary': 'Precio de venta por Variantes fixed',
    'version': '12.0.1.0.0',
    'author': "Luis González",
    'maintainer': ["Luis González"],
    'category': 'Product',
    # 'installable': True,
    'depends': [
        'account',
        'sale',
        'product',
    ],
    'data': [
        'views/product_views.xml',
    ],
    'post_init_hook': 'set_sale_price_on_variant',
}
