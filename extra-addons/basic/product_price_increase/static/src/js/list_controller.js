odoo.define('product_price_increase.ListController', function (require) {
"use strict";

var ListController = require('web.ListController');


ListController.include({
    
    renderButtons: function ($node) {
        let out = this._super($node)
        let self = this;
        if (this.renderer.state.context.save_btn_price_change) {
            this.$buttons.append('<button type="button" class="btn btn-primary o_save_price_change">Aplicar Cambios</button>')
            this.$buttons.find('.o_save_price_change').click(() => {
                this._rpc({
                    model: 'increase.line',
                    method: 'apply_increase',
                    args: [],
                    context: this.renderer.state.context,
                }).then(result => {
                    console.log(result);
                    
                    this.do_action(result)
                })
            })
        }
        return out
    }
    
    
});

});
