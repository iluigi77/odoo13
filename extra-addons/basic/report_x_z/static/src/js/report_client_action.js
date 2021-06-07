odoo.define('report_x_z.ReportClientAction', function(require) {
    "use strict";

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');

    var GenerateReportXZWidget = AbstractAction.extend({
        template: "GenerateReportXZWidget",
        /**
         * @override
         * @see Widget.init
         */
        init: function(parent, options) {
            this._super.apply(this, arguments);

            this.parent = parent;
            this.options = _.extend({}, options);
            this.context = _.extend({}, this.options.context);
            
            this.reportOptios={};
        },

        /**
         * @override
         * @see Widget.willStart
         */
        willStart: function() {
            let self= this;
            return Promise.all([
                this._super(),
                self.getUserContext()
            ]);
        },
        
        /**
         * @override
         * @see Widget.start
         */
        start: function() {
            let self= this;
            return this._super().then(( ) => {
                let params= self.reportOptios;
                self.generateReport(params);
            });
        },

        canBeRemoved: function(){
            return $.when();
        },

        getUserContext: async function() {
            let self= this;
            return this._rpc({
                model: 'pos.session',
                method: 'get_context_report',
                args: [self.context.uid]
            })
            .then( (response) =>{
                self.reportOptios['type_report'] = self.context.type_report;
                self.reportOptios['cashier_name'] = response.cashier_name;
                // self.reportOptios['register_box'] = response.register_box;
                
            })
            // self.reportOptios['type_report'] = self.context.type_report;
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
                    console.log('success', response.ok, response.status);

                    // if(response.ok){
                    //     resolve(200);
                    // }
                    // else{
                    //     console.error('[REPORT_XZ]: Looks like there was a problem. Status Code: ', response.status);
                    //     reject(response.status)
                    // }
                    if(response.status === 200 || response.status === 201 || response.status === 500) // por ahora, los 500 no valen
                        resolve(200);
                    else
                        reject(response.status)
                })
                .catch(function(err) {
                    console.error('[REPORT_XZ 1]: ', err);
                    reject(500)
                });
            });
        },

        /**
         * Print credit note on fiscal print
         *
         */
        generateReport: async function(params){
            let self = this;
            // let serverName= 'http://localhost:8000/report_xz.php';
            let serverName= 'http://localhost/a/report_xz.php';
            try {
                let status = await this.send_request_to_print(serverName, params);
                self.render(status);
            } catch (error) {
                console.error('[REPORT_XZ 2]: ', error);
                // if status code error == 401, Unauthorized user
                self.render(error);
            }
            
        },

        render: function(status){
            $("#id_alert").removeClass(`alert alert-info alert-warning alert-danger`);
            $("#id_text").text('');
            
            if(status === 200){
                $("#id_text").text("El reporte " + this.reportOptios.type_report + " se ha generado exitosamente.");
                $("#id_alert").addClass(`alert alert-info`);
            }
            if(status === 401){
                $("#id_text").text("Permiso denegado: El usuario '" +this.reportOptios.cashier_name+ "' no puede ejecutar reportes " + this.reportOptios.type_report + " en esta caja. ");
                $("#id_alert").addClass(`alert alert-warning`);
            }
            if(status === 500){
                $("#id_text").text("Ha ocurrido un error al intentar generar el reporte " + this.reportOptios.type_report);
                $("#id_alert").addClass(`alert alert-danger`);
            }
        }

    });

    core.action_registry.add('GenerateReportXZWidget', GenerateReportXZWidget);

    return {
        GenerateReportXZWidget:GenerateReportXZWidget,
    };
});