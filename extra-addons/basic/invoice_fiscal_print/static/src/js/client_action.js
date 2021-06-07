odoo.define('invoice_fiscal_print.clientAction', function(require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');

    console.log('[INVOICE]: load static widget');
    // var PrinterOrderWidget = Widget.extend(FieldManagerMixin, {
    var PrinterOrderWidget = AbstractAction.extend({
        template: "PrinterOrderWidget",
        /**
         * @override
         * @see Widget.init
         */
        init: function(parent, options) {
            this._super.apply(this, arguments);

            this.parent = parent;
            this.options = _.extend({}, options);
            this.context = _.extend({}, this.options.context);
            
            this.invoice={};
        },

        /**
         * @override
         * @see Widget.willStart
         */
        willStart: function() {
            let self= this
            console.log('[INVOICE]: will start');
            
            return Promise.all([
                this._super(),
            ]);
        },
        
        /**
         * @override
         * @see Widget.start
         */
        start: function() {
            let self= this;
            return this._super().then(( ) => {
                self.getInvoice();
            });
        },

        canBeRemoved: function(){
            return $.when();
        },

        render: function(status){
            $("#id_alert").removeClass(`alert alert-info alert-warning alert-danger`);
            $("#id_text").text('');
            
            if(status === 200){
                $("#id_text").text("La factura físcal se ha generado exitosamente.");
                $("#id_alert").addClass(`alert alert-info`);
            }
            if(status === 401){
                $("#id_text").text("Permiso denegado: El usuario '" +this.invoice.current_user+ "' no puede generar esta factura físcal.");
                $("#id_alert").addClass(`alert alert-warning`);
            }
            if(status === 500){
                $("#id_text").text("Ha ocurrido un error al intentar generar la factura físcal.");
                $("#id_alert").addClass(`alert alert-danger`);
            }
        },

        /**
         * get invoice from server
         *
         * @returns {Promise} invoice items from server request
         */
        getInvoice: async function() {
            let self= this;
            console.log('GET INVOICE');
            
            return this._rpc({
                model: 'account.move',
                method: 'get_invoice',
                args: [self.context.invoice_id]
            })
            .then( (invoice) =>{
                self.invoice = invoice;
                self.printInvoice(invoice)
            })
        },

        /**
         * Set printer status on model
         *
         */
        setStatusPrint: function(code) {
            let self= this;
            this.render(code);
            let status= code === 200;
            return this._rpc({
                model: 'account.move',
                method: 'set_status_print',
                args: [self.context.invoice_id, status]
            })
        },

        /**
         * Print credit note on fiscal print
         *
         */
        printInvoice: async function(params){
            // let serverName='http://localhost:8000/print_invoice.php'
            let serverName='http://localhost:5000/printer/print-invoice'
            
            try {
                let code= await this.send_request_to_print(serverName, params);
                this.setStatusPrint(code);
            } catch (error) {
                console.error('[printInvoice]: ', error);
                this.setStatusPrint(error);

            }
            
        },

        /***
         * solicitud http a la API de la impresora fiscal
         */
        send_request_to_print: function(serverName, obj){
            let self= this;
            // console.log('send to fiscal print...');
            console.log(`request to: ${serverName}`, obj);
            
            return new Promise((resolve, reject) => {
                fetch((serverName), {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(obj)
                })
                .then(function(response) {
                    console.log('success');

                    if(response.ok){
                        resolve(200);
                    }
                    else{
                        console.error('[send_request_fiscal_print]: Looks like there was a problem. Status Code: ', response.status);
                        reject(response.status)
                    }
                })
                .catch(function(err) {
                    console.error('[send_request_fiscal_print]: ', err);
                    reject(500)
                });
            });
        },
       
    });

    core.action_registry.add('PrinterOrderWidget', PrinterOrderWidget);

    return {
        PrinterOrderWidget:PrinterOrderWidget,
    };
});