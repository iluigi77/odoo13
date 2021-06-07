odoo.define('pos_offline.screens', function(require) {
    "use strict";

    var screens = require('point_of_sale.screens');
    var rpc = require("web.rpc");
    var core = require('web.core');
    var _t = core._t;


    screens.ClientListScreenWidget.include({
        init: function(parent, options){
            this._super(parent, options)
        },

        save_client_details: function(partner){
            console.log('[Offline]: save client with timeout');
            this.save_client_details_with_timeout(partner, 20000); 
        },

        /***
         * se copia el mismo codigo de 'save_client_details', pero se le agrega
         * el timeout, para evitar esperas con inanición 
         */
        // what happens when we save the changes on the client edit form -> we fetch the fields, sanitize them,
        // send them to the backend for update, and call saved_client_details() when the server tells us the
        // save was successfull.
        save_client_details_with_timeout: function(partner, timeout) {
            var self = this;

            var fields = {};
            this.$('.client-details-contents .detail').each(function(idx,el){
                if (self.integer_client_details.includes(el.name)){
                    var parsed_value = parseInt(el.value, 10);
                    if (isNaN(parsed_value)){
                        fields[el.name] = false;
                    }
                    else{
                        fields[el.name] = parsed_value
                    }
                }
                else{
                    fields[el.name] = el.value || false;
                }
            });

            if (!fields.name) {
                this.gui.show_popup('error',_t('A Customer Name Is Required'));
                return;
            }

            if (this.uploaded_picture) {
                fields.image_1920 = this.uploaded_picture;
            }

            fields.id = partner.id || false;

            var contents = this.$(".client-details-contents");
            contents.off("click", ".button.save");


            rpc.query({
                    model: 'res.partner',
                    method: 'create_from_ui',
                    args: [fields],
                }, {
                    timeout: timeout,   /// add timeout fro validate
                    shadow: true,
                })
                .then(function(partner_id){
                    self.saved_client_details(partner_id);
                    // $( "#offlineAlert" ).hide();
                    $(".pos-topheader").css({"background": "393939", "color": "grey"});
                }).catch(function(error){
                    error.event.preventDefault();
                    var error_body = _t('Your Internet connection is probably down.');
                    if (error.message.data) {
                        var except = error.message.data;
                        error_body = except.arguments && except.arguments[0] || except.message || error_body;
                    }
                    // $( "#offlineAlert" ).show(); // show offline alert
                    $(".pos-topheader").css({"background": "orange", "color": "black"});
                    self.gui.show_popup('error',{
                        'title': _t('Error: Could not Save Changes'),
                        'body': error_body,
                    });
                       
                    contents.on('click','.button.save',function(){ self.save_client_details(partner); });
                });
        },

    });
    
  
});