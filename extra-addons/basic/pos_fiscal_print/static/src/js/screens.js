odoo.define('pos_fiscal_print.screens', function(require) {
    "use strict";

    var screens = require('point_of_sale.screens');

    /// Capa1: numeros
    screens.NumpadWidget.include({
        init: function(parent){
            this._super(parent)
        },

        /***
         * elimina los articulos de la lista de productos a comprar si su cantidad es 0
         */
        clickDeleteLastChar: function(){
            this._super();
            if(this.state.attributes.buffer === "" && (this.state.attributes.mode== 'quantity')){
                this._super();
            }

        }
    });

    /// Capa1: lista de productos
    screens.ProductScreenWidget.include({
        init: function(parent, options){
            this._super(parent, options)
        },

        /***
         * verifica que los impuestos esten bien definidos para un producto dado
         * Nota: un producto tiene los impuestos bien definidos cuando tiene un (1)
         * y solo un (1) impuesto establecido por sucursal
         * Nota2: this.pos.taxes devuelve los impuestos definidos para la sucursal actual
         */
        filter_taxes_by_company: function(product){
            let taxes= [];
            let ptaxes_ids = product.taxes_id; // impuestos del producto
            let companyTaxes= {};
            
            /// se recorren los impuestos de la sucursal actual (this.pos.taxes)
            /// y estos se almacenan en un object.
            for (let i=0; i< this.pos.taxes.length; i++) 
                companyTaxes[this.pos.taxes[i].id]= this.pos.taxes[i];

            for (let i=0; i< ptaxes_ids.length; i++){
                let id= ptaxes_ids[i];
                if(companyTaxes[id])
                    taxes.push(companyTaxes[id]);
            }
            return taxes
        },
        
        /***
         * extiende y establece validaciones al seleccionar un producto a facturar
         */
        click_product: function(product) {
            self= this;
            let taxes= this.filter_taxes_by_company(product)
            if(taxes.length === 1 ){
                this._super(product)
            }
            else{
                self.gui.show_popup('error-info-popup',{
                    'title': 'Impuestos no definidos',
                    'body':  'El administrador no ha establecido correctamente los impuestos sobre este producto para esta sucursal, por eso producto no puede ser facturado.',
                    'detail':  '- '+product.display_name
                });
            }
            
        },
        
    })

    // Capa2
    screens.PaymentScreenWidget.include({
        init: function(parent, options){
            this._super(parent, options)
        },
        
        /***
         * Retorna true si el cliente esta seleccionado
         */
        is_select_client: function(){
            let client= this.pos.get_client();
            return !!client;
        },

        /***
         * valida que el cliente este seleccinado antes de avanzar a la pantalla de facturacion
         * Nota: ademas, mantiene el proceso original el cual consiste en validar que el pago
         * se haya completado
         */
        order_changes: function(){
            var self = this;
            var order = this.pos.get_order();
            if (!order) {
                return;
            } else if (order.is_paid() && this.is_select_client()) { /// add is_select_client() validation
                self.$('.next').addClass('highlight');
            }else{
                self.$('.next').removeClass('highlight');
            }
        },

        /***
         * Fix Bug: Actualiza el estilo del boton de validacion de pago, cuando se elimina
         * un metodo de pago 
         */
        click_delete_paymentline: function(cid){
            this._super(cid);
            var order = this.pos.get_order();
            if (order.is_paid() && this.is_select_client()) { 
                self.$('.next').addClass('highlight');
            }else{
                self.$('.next').removeClass('highlight');
            }
        },

    })

    // Capa3
    screens.ReceiptScreenWidget.include({
        init: function(parent, options){
            this._super(parent, options)
            this._lockedPrint = false; /// define el estado de bloqueo para el boton de imprimir
            this._lockedNext = true; /// define el estado de bloqueo para el boton de siguiente
        },
        
        /***
         * Extiende la funcion show y agrega el estado de bloqueo en el boton
         * de imprimir
         */
        show: function(){
            this._super();
            this.lock_print(false) /// desbloquea el boton de imprimir
            this.lock_next(true) /// bloquea el boton de siguiente
        },

        /***
         * maneja el estado de bloqueo del boton de imprimir
         */
        lock_print: function(locked) {
            this._lockedPrint = locked;
            if (locked) {
                this.$('.print').removeClass('highlight');
                this.$('.print_invoice').removeClass('highlight');
            } else {
                this.$('.print').addClass('highlight');
                this.$('.print_invoice').addClass('highlight');
            }
        },

        /***
         * maneja el estado de bloqueo del boton de siguiente
         */
        lock_next: function(locked) {
            this._lockedNext = locked;
            if (locked) {
                this.$('.next').removeClass('highlight');
            } else {
                this.$('.next').addClass('highlight');
            }
        },

        /***
         * verifica que los impuestos esten bien definidos para un producto dado
         * Nota: un producto tiene los impuestos bien definidos cuando tiene uno (1)
         * y solo un (1) impuesto establecido por sucursal
         * Nota2: this.pos.taxes devuelve los impuestos definidos para la sucursal actual
         */
        filter_taxes_by_company: function(companyTaxes, product){
            let taxes= [];
            let ptaxes_ids = product.taxes_id; //impuestos del producto
            // console.log('ptaxes_ids:: ', ptaxes_ids);
            
            for (let i=0; i< ptaxes_ids.length; i++){
                let id= ptaxes_ids[i];
                if(companyTaxes[id])
                    taxes.push(companyTaxes[id]);
            }
            // console.log('taxes:: ', taxes);
            return taxes;
        },

        /***
         * solicitud http a la API de la impresora fiscal
         */
        send_request_fiscal_print: function(serverName, obj){
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
                    // console.log('success');

                    if(response.ok){
                        self.gui.show_popup('success-info-popup', {
                            'title': 'Exito!',
                            'body':  'La Factura ha sido impresa correctamente',
                            'list_detail': [
                                { label: 'Código del pedido: ',  item: obj.order.pos_reference },
                                { label: 'Fecha de impresión: ', item: obj.order.date },
                            ]
                        });
                        resolve(true);
                    }
                    else{
                        console.log('[send_request_fiscal_print]: Looks like there was a problem. Status Code: ', response.status);
                        self.gui.show_popup('error-traceback', {
                            'title': 'Error',
                            'body':  'Ha ocurrido un error con la impresora fiscal. Verifique el papel de la impresora y que la misma este conectada correctamente.'+ '\n'+ 'Por favor, comuniquese con el departamento de sistema.'
                        });
                        reject(false)

                    }
                })
                .catch(function(err) {
                    console.log('[send_request_fiscal_print]: ', err);
                    self.gui.show_popup('error-traceback', {
                        'title': 'Error de conexión',
                        'body':  'Ha ocurrido un error de conexión con el aplicativo fiscal'+ '\n'+ 'Por favor, comuniquese con el departamento de sistema.'
                    });
                    reject(false)
                });
            });
        },

        /***
         * impresion fiscal desde odoo
         */
        fiscal_print: async function(){
            let self= this;
            let serverName= this.pos.config.url_api; 
            let orders= [];
            let payments= [];
            let cashier= this.pos.get_cashier();
            let orderModel = this.pos.get_order();
            let client= orderModel.attributes.client;
            let obj= {};
            let companyTaxes= {};
            let errProducts= [];
            
            try {
                /// se cargan los impuestos de la sucursal actual en un objeto
                for (let i=0; i< this.pos.taxes.length; i++) 
                    companyTaxes[this.pos.taxes[i].id]= this.pos.taxes[i];
                
                // console.log('companyTaxes:: ', companyTaxes);
                
                orderModel.orderlines.forEach(o => {
                    let p = o.get_product();
                    let tax= undefined;
    
                    let taxes = this.filter_taxes_by_company(companyTaxes, p);
    
                    if(taxes.length == 0){
                        console.log('El producto no posee impuesto en esta sucursal: ', p.display_name);
                        errProducts.push({
                            label: '[ '+p.display_name+ '] - ',
                            item: 'Sin impuestos para esta sucursal'
                        });
                    }
                    else if(taxes.length>1){
                        console.log('El producto posee mas de un impuesto para esta sucursal: ', p.display_name);
                        errProducts.push({
                            label: '[ '+p.display_name+ '] - ',
                            item: 'Mas de un impuestos para esta sucursal'
                        });
                    }
                    else {
                        tax= taxes[0].tax_type;
                    }
    
                    /// verifica que no se manden a facturar productos con cantidad 0
                    if(o.get_quantity() > 0){
                        orders.push({
                            'name': p.display_name,
                            'tax_type': tax,
                            'qty': o.quantity,
                            'price_unit': o.product.lst_price,
                        })
                    }
                });
                
                orderModel.paymentlines.forEach(p => {
                    payments.push({
                        'journal_name': p.name,
                        'amount': p.amount
                    })
                })
    
                if(errProducts.length> 0 ){
                    /// Err: error de impuestos
                    self.gui.show_popup('error-info-popup',{
                        'title': 'Impuestos mal definidos',
                        'list_detail':  errProducts
                    });
                }
                else{
                    /// se arma el objeto a imprimir
                    obj= {
                        'order': {
                            'date': orderModel.formatted_validation_date,                
                            'pos_reference': orderModel.uid, // name for add 'pedido' to the start 
                            'subtotal': orderModel.get_total_without_tax(),
                            'total': orderModel.get_total_with_tax(),
                            'products': orders,
                            'payment_methods': payments,
                        },
                        'client': {
                            'name': client? client.name: undefined,
                            'vat': client? client.vat: undefined, 
                            'street': (client.street || ' - '), 
                            'city':(client.city || ' "Valencia" '),
                            'phone': client.phone || ' - '
                        },
                        'user': {
                            'name': cashier? cashier.name: undefined
                        }  
                    }
                    let status= await this.send_request_fiscal_print(serverName, obj);
                    this.setStatus(orderModel, status)
                }
                
            } catch (error) {
                console.log('[fiscal_print]: ', error);
                this.setStatus(orderModel, false)
                
            }
            
        },
        
        setStatus: function(order, status){
            order.fiscal_print= status;
            if(status) { /// la factura se imprimió con éxito
                this.lock_print(true);
                this.lock_next(false);
            }
            else { /// falló la impresión
                this.lock_print(false);
                this.lock_next(true);
            }
        },

        renderElement: function() {
            var self = this;
            this._super();
            this.$('.button.print').unbind( "click" );
            this.$('.button.print_invoice').unbind( "click" );
            this.$('.next').unbind( "click" );

            /// ordenes sin pedido en venta
            this.$('.button.print').click(function(){
                let orderModel = self.pos.get_order();
                if(orderModel.fiscal_print){ /// si la factura ya ha sido impresa
                    self.gui.show_popup('warning-info-popup', {
                        'title': 'Factura Fiscal',
                        'body':  'Esta factura ya ha sido impresa anteriormente:',
                        'list_detail': [
                            { label: 'Código del pedido: ', item: orderModel.uid },
                            { label: 'Fecha de impresión: ', item: orderModel.formatted_validation_date },
                        ],
                    });
                }
                else{
                    if (!self._locked && !self._lockedPrint) { /// agrega validación para impedir que el boton se pueda ejecutar dos veces
                        self.lock_print(true);
                        self.fiscal_print();
                    }
                    else{
                        console.log('blocked btn');
                    }
                }
            });

            /// ordenes con pedido en venta
            this.$('.button.print_invoice').click(function () {
                let orderModel = self.pos.get_order();
                if(orderModel.fiscal_print){ /// si la factura ya ha sido impresa
                    self.gui.show_popup('warning-info-popup', {
                        'title': 'Factura Fiscal',
                        'body':  'Esta factura ya ha sido impresa anteriormente:',
                        'list_detail': [
                            { label: 'Código del pedido: ', item: orderModel.uid },
                            { label: 'Fecha de impresión: ', item: orderModel.formatted_validation_date },
                        ],
                    });
                }
                else{
                    if (!self._locked && !self._lockedPrint) { /// agrega validación para impedir que el boton se pueda ejecutar dos veces
                        self.lock_print(true);
                        self.fiscal_print();
                    }
                    else{
                        console.log('blocked btn');
                    }
                }
            });

            /***
             * Verifica el estatus de la factura actual, si no se ha impreso la factura
             * actual, no permite avanzar al siguiente cliente
             */
            this.$('.next').click(function(){
                let orderModel = self.pos.get_order();
                if (!self._locked && orderModel.fiscal_print) {
                    self.click_next();
                }
                else{
                    self.gui.show_popup('warning-info-popup', {
                        'title': 'Factura Fiscal',
                        'body':  'Para continuar con el siguiente cliente, primero se debe facturar al cliente actual',
                        
                    });
                }
            });
        },
    });

});