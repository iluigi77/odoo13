odoo.define('pos_fiscal_print.models', function(require) {
    "use strict";

    var models = require('point_of_sale.models');
    models.load_fields('account.tax','tax_type');
    models.load_fields('pos.order','fiscal_print');

    // For loading a completly new model with fields:
    /// agrega el tax_type a la carga del modelo statico
    var models = require('point_of_sale.models');
    models.load_models([
        {
            model:  'account.tax',
            fields: ['name','amount', 'price_include', 'include_base_amount', 'amount_type', 'children_tax_ids', 'tax_type'],
            domain: function(self) {return [['company_id', '=', self.company && self.company.id || false]]},
            loaded: function(self, taxes){
                self.taxes = taxes;
                self.taxes_by_id = {};
                _.each(taxes, function(tax){
                    self.taxes_by_id[tax.id] = tax;
                });
                _.each(self.taxes_by_id, function(tax) {
                    tax.children_tax_ids = _.map(tax.children_tax_ids, function (child_tax_id) {
                        return self.taxes_by_id[child_tax_id];
                    });
                });
            },
        }
    ],{'after': 'account.tax'});

    // almacena si ya la factura ha sido impresa o no (boolean: fiscal_print)
    var order_super = models.Order.prototype;
    models.Order = models.Order.extend({
        init_from_JSON: function (json) {
            order_super.init_from_JSON.apply(this, arguments);
            this.fiscal_print = json.fiscal_print? json.fiscal_print: false;
        },
        export_as_JSON: function () {
            return _.extend(order_super.export_as_JSON.apply(this, arguments), {
                fiscal_print: this.fiscal_print? this.fiscal_print: false ,
            });
        },
        export_for_printing: function () {
            var res = order_super.export_for_printing.apply(this, arguments);
            res.fiscal_print = this.fiscal_print? this.fiscal_print: false;
            return res;
        },
    });



});