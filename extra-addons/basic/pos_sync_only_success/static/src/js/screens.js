odoo.define('pos_sync_only_success.screens', function(require) {
    "use strict";

    var screens = require('point_of_sale.screens');

    // Capa2
    screens.PaymentScreenWidget.include({
        init: function(parent, options){
            this._super(parent, options);
        },

        /***
         * se extiende la funcion para evitar que la sync de pedidos 
         * se realice antes de imprimir la factura
         */
        finalize_validation: function(){

            var self = this;
            var order = this.pos.get_order();

            if (order.is_paid_with_cash() && this.pos.config.iface_cashdrawer) { 

                    this.pos.proxy.printer.open_cashbox();
            }

            order.initialize_validation_date();
            order.finalized = true;

            if (order.is_to_invoice()) {
                /**
                 * se elimina todo el cod del bloque para 
                 * evitar sinc de ordenes y ventas
                 * */
               self.gui.show_screen('receipt');
            } else {
                /**
                 * se elimina todo el cod del bloque para 
                 * evitar sinc de ordenes y ventas
                 * */
                this.gui.show_screen('receipt');
            }

        }

    });

    // Capa3
    screens.ReceiptScreenWidget.include({
        init: function(parent, options){
            var self = this;
            this._super(parent, options);
        },

        /***
         * Se extiende de fiscal print (modulo de lambu) para hacer que sincronice el pedido
         * si y solo si la facturación ha sido exitosa
         */
        setStatus: function(order, status){
            this._super(order, status);
            order.fiscal_print= !!status;
            if(status){ /// solo guarda los pedidos que han sido impresos
                if(order.is_to_invoice()){

                    this.pos.push_order(order,{to_invoice:true});
                    /* var invoiced = this.pos.push_and_invoice_order(order);
                    this.invoicing = true;
                    
                    /// se evita el mensaje al fallar la sinc. y el refresh en la capa
                    // invoiced.fail(this._handleFailedPushForInvoice.bind(this, order, true)); // refresh
                    
                    invoiced.done(function(){
                        this.invoicing = false;
                        // this.gui.show_screen('receipt'); /// se evita el refresh de la capa
                    }); */
                }
                else{
                    this.pos.push_order(order);
                }
            }

        }
        
    });
});