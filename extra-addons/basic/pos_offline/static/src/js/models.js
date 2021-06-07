odoo.define('pos_offline.models', function(require) {
    "use strict";

    var rpc = require("web.rpc");
    var models = require("point_of_sale.models");

    var PosModelSuper = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        initialize: function(session, attributes) {
            // Compatibility with pos_cache module
            PosModelSuper.initialize.apply(this, arguments);
        },


        set_synch: function(state, pending) {
            PosModelSuper.set_synch.call(this, state, pending);
            let statusSync= this.get('synch')
            if ((statusSync.state == 'err') || (statusSync.state == 'disconnected')){
                // $( "#offlineAlert" ).show();
                $(".pos-topheader").css({"background": "orange", "color": "black"});
            }
            else{
                // $( "#offlineAlert" ).hide();
                $(".pos-topheader").css({"background": "393939", "color": "grey"});
            }
        }



    });
});


