/*
* @Author: D.Jane
* @Email: jane.odoo.sp@gmail.com
*/
odoo.define('pos_stock_quantity.popups', function (require) {
    "use strict";
    var gui = require('point_of_sale.gui');
    var PopupWidget = require('point_of_sale.popups');

    var Reminder = PopupWidget.extend({
        template: 'Reminder',
        events: {
            'keyup .input-key':  'input_key',
            'click .button.cancel':  'click_cancel',
            'click .button.confirm': 'click_confirm',
        },
        show: function(options){
            options = options || {};
            this._super(options);
            this.srcValue = '';
            this.$('.input-key').focus();

        },

        click_cancel: function () {
            this.gui.close_popup();
        },

        click_confirm: function () {
            let self = this;
            let password= this.pos.config.manager_passw;
            let pw = this.srcValue;

            if (password) {
                /**
                 * if password is defined
                 */
                
                if (pw !== password.toString()) {
                    /* error to passw */
                    self.pos.gui.show_popup('error',{
                        'title': _t('Contraseña Incorrecta'),
                        'body': 'Contraseña incorrecta, no se puede liberar el producto',
                    });
                } else {
                    /* password success */
                    let line = this.options.line;
                    let order = this.options.line.order;

                    /* Unlock product for current order */
                    this.unlock_product_by_order(order, self.options.product);

                    /* find current line */
                    let found= order.orderlines.find(l => l=== line);

                    if(found){
                        /**
                         * if found current line,
                         * set value 
                         */
                        line.set_quantity(this.options.new_quantity || 1);
                    }
                    else{
                        /**
                         * else,
                         * get another line from orderlines (same product) 
                         */
                        let another_line= order.orderlines.find(l => l.product.id=== line.product.id)
                        /** 
                         * set qty on another line
                         */
                        let qty= parseFloat(this.options.new_quantity1) || 1;
                        another_line.set_quantity(another_line.quantity+qty);
                    }
                    this.gui.close_popup();
                }
            }
            else{
                /**
                 * else,
                 * passw not defined
                 */
                this.pos.gui.show_popup('error-info-popup', {
                    'title': 'Error de clave',
                    'body':  'Esta caja no posee una clave de administrador definida, por favor contacte con el departamento de sistema',
                });
            }
        },

        input_key: function(e) {
            if(e.key!= "Enter"){
                var $value = this.$('.input-key');
                let mask= $value.val();
                let newbuff= $value.val().replaceAll('•','');
    
                this.srcValue= (mask.length< this.srcValue.length )? this.srcValue.substring(0,this.srcValue.length-1): this.srcValue + newbuff
                $value.val($value.val().replaceAll(/./g, '•'));
            }
            else{
                this.click_confirm();
            }
        },

        unlock_product_by_order: function(order, product){
            order['availables_for_negative_stock']= order['availables_for_negative_stock'] || {};
            order['availables_for_negative_stock'][product.id]= true;
            
        }
    });

    gui.define_popup({name: 'order_reminder', widget: Reminder});
});
