odoo.define('pos_client.screens', function(require) {
    "use strict";

    var screens = require('point_of_sale.screens');
    // var pos_offline = require('pos_offline.screens');


    screens.ClientListScreenWidget.include({
        init: function(parent, options){
            this._super(parent, options)
        },

        save_client_details: function(partner){
            // console.log('[POS CLIENT]: validate client');

            if(this.validate_client(partner)){
                this._super(partner);
            }
        },

        validate_client: function(partner){
            var self = this;
            let requiredList = [];
            var fields = {};
            
            fields.id = partner.id || false;
            this.$('.client-details-contents .detail').each(function(idx,el){
                fields[el.name] = el.value || false;
            });
            this.$('.client-details-contents .vat').each(function(idx,el){
                fields[el.vat] = el.value || false;
            });
            this.$('.client-details-contents .city').each(function(idx,el){
                fields[el.city] = el.value || false;
            });
            this.$('.client-details-contents .street').each(function(idx,el){
                fields[el.street] = el.value || false;
            });

            if(!fields.name)
                requiredList.push({ label: 'Nombre ', item: '' })
            if(!fields.vat)
                requiredList.push({ label: 'RIF/CI ', item: '' })
            if(!fields.city)
                requiredList.push({ label: 'Ciudad ', item: '' })
            if(!fields.street)
                requiredList.push({ label: 'Zona ', item: '' })

            if (requiredList.length >0) {
                self.gui.show_popup('error-info-popup',{
                    'title': 'Algunos campos requeridos estan vacios',
                    'list_detail': requiredList
                });
                return false; /// Error: Campos requeridos
            }
            else{
                fields.vat= fields.vat.toUpperCase()
                if(!this.validVat(fields.vat)){
                    self.gui.show_popup('error-info-popup',{
                        'title': 'El formato para RIF/CI no es correcto',
                        'list_detail': [
                            {label: 'Venezolano: ', item: 'V12345678'},
                            {label: 'Extranjero: ', item: 'E12345678'},
                            {label: 'Jurídico: ', item: 'J123456789'},
                            {label: 'Gubernamental: ', item: 'G123456789'},
                            {label: 'Consejo Comunal: ', item: 'C123456789'},
                        ]
                    });
                    return false; /// Error: Formate de VAT incorrecto
                }
                else{
                    let found = this.uniqueVat(fields.vat, fields.id)
                    if(found){
                        self.gui.show_popup('error-info-popup',{
                            'title': 'Cliente ya existe',
                            'body': `El numero de RIF/CI ingresado, ya existe en el sistema.`,
                            'list_detail': [
                                {label: 'Cliente: ', item: found.name},
                                {label: 'RIF/CI: ', item: found.vat},
                                {label: 'Dirección: ', item: found.address},
                                {label: 'Telefono: ', item: found.phone},
                            ]
                        });
                        return false; /// Error: Vat duplicado

                    }
                    else{
                        /// the second param is the timeout
                        return true;
                    }
                }
            }
        },

        validVat: function(vat){
            let value= null;
            let num= '0';
            let isnum= false;

            if(vat.length> 0){
                switch(vat[0].toUpperCase()){
                    case 'V': 
                        value=[6,7,8,9]; // sin prefijo (V)
                    break;
                    case 'J': 
                        value=[9, 10]; // sin prefijo (J)
                    break;
                    case 'E': 
                        value=[7,8,9]; // sin prefijo (E)
                    break;
                    case 'G': 
                        value=[9, 10]; // sin prefijo (G)
                    break;
                    case 'C': 
                        value=[9, 10]; // sin prefijo (C)
                    break;
                    default : 
                        value=null;
                    break;
                }
                num = vat.substring(1, vat.length)
                
                isnum = /^\d+$/.test(num);
                
            }
            return ((!value) || !value.includes(num.length) || !isnum )? false: true;
        },

        uniqueVat: function(vat, id){
            var customers = this.pos.db.get_partners_sorted();
            let found= customers.find(user => {
                let uVat = user.vat || '';
                return ((vat.toUpperCase() === uVat.toUpperCase() ) && (!id || id !== user.id)) ;
            })
             return found;
        },

    });
    
    screens.PaymentScreenWidget.include({
        init: function(parent, options){
            this._super(parent, options)
        },

        is_select_client: function(){
            let client= this.pos.get_client();
            return !!client;
        },

        validate_order: function(force_validation) {
            if (!this.is_select_client()) {
                this.gui.show_popup('error-info-popup',{
                    'title': 'cliente no establecido',
                    'body':  'Debe seleccionar un cliente antes de continuar.',
                });
            }
            else{
                this._super(force_validation);
            }
        },
    });
});