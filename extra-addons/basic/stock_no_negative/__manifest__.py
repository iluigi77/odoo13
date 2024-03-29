# ?? 2015-2016 Akretion (http://www.akretion.com)
# @author Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


{
    "name": "Stock Disallow Negative",
    "version": "13.0.1.0.0",
    "category": "Stock",
    # "category": "Inventory, Logistic, Storage",
    "license": "AGPL-3",
    "summary": "Disallow negative stock levels by default",
    'maintainer': ["Luis González"],
    "author": "Akretion,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/stock-logistics-workflow",
    "depends": ["stock"],
    "data": ["views/product_product_views.xml", "views/stock_location_views.xml"],
    "installable": True,
}
