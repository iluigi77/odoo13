# -*- coding: utf-8 -*-
{
    "name": "sale_payment_register",
    "summary": "Agregar registro de pago en los pedidos de ventas",
    "version": "13.0.1.0.0",
    "category": "Sales",
    "author": "Luis González",
    "maintainer": ["Luis González"],
    "depends": [
        "sale", 
        "payment",
        "sale_clean_view",
    ],
    "license": "LGPL-3",
    "data": [
        "wizard/sale_confirm_payment_view.xml",
        "views/sale_view.xml", 
        "views/transaction_view.xml", 
        ],

}
