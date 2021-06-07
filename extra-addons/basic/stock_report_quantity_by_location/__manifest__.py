
{
    "name": "Stock Report Quantity By Location",
    "summary": "Stock Report Quantity By Location",
    "version": "13.0.1.0.0",
    'maintainer': ["Luis González"],
    "author": ["Odoo Community Association (OCA)"],
    # "category": "Warehouse Management",
    "category": "Stock",
    "license": "AGPL-3",
    "depends": [
        "product",
        "stock",
    ],
    "data": [
        'wizards/stock_report_quantity_by_location_views.xml',
    ],
    "installable": True,
}
