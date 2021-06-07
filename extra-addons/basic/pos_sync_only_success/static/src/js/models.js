odoo.define('pos_sync_only_success.models', function(require) {
    "use strict";

    var rpc = require("web.rpc");
    var models = require("point_of_sale.models");
    var field_utils = require("web.field_utils");

    var PosModelSuper = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        initialize: function(session, attributes) {
            // Compatibility with pos_cache module
            PosModelSuper.initialize.apply(this, arguments);
        },

        /***
         * Solo para mantener un control de los pedidos que se han sincronizado
         */
        _save_to_server: function (orders, options) {
            console.log('[SYNC SUCCESS]: saving orders...');
            return PosModelSuper._save_to_server.call(this, orders, options);
        },

        /***
         * Se reescribe completa para evitar el pdf
         */
        push_and_invoice_order: function(order){
            var self = this;
            var invoiced = new $.Deferred();
    
            if(!order.get_client()){
                invoiced.reject({code:400, message:'Missing Customer', data:{}});
                return invoiced;
            }
    
            var order_id = this.db.add_order(order.export_as_JSON());
    
            this.flush_mutex.exec(function(){
                var done = new $.Deferred(); // holds the mutex
    
                // send the order to the server
                // we have a 30 seconds timeout on this push.
                // FIXME: if the server takes more than 30 seconds to accept the order,
                // the client will believe it wasn't successfully sent, and very bad
                // things will happen as a duplicate will be sent next time
                // so we must make sure the server detects and ignores duplicated orders
    
                var transfer = self._flush_orders([self.db.get_order(order_id)], {timeout:30000, to_invoice:true});
    
                transfer.fail(function(error){
                    invoiced.reject(error);
                    done.reject();
                });
    
                // on success, get the order id generated by the server
                transfer.pipe(function(order_server_id){
    
                    // generate the pdf and download it
                    if (order_server_id.length) {
                        /// comentando este bloque se evita que se genere el pdf

                        // self.chrome.do_action('point_of_sale.pos_invoice_report',{additional_context:{
                        //     active_ids:order_server_id,
                        // }}).done(function () {
                        //     invoiced.resolve();
                        //     done.resolve();
                        // }).fail(function (error) {
                        //     invoiced.reject({code:401, message:'Backend Invoice', data:{order: order}});
                        //     done.reject();
                        // });

                        invoiced.resolve();
                        done.resolve();
                    } else {
                        // The order has been pushed separately in batch when
                        // the connection came back.
                        // The user has to go to the backend to print the invoice
                        invoiced.reject({code:401, message:'Backend Invoice', data:{order: order}});
                        done.reject();
                    }
                });
    
                return done;
    
            });
    
            return invoiced;
        },

    });
});

