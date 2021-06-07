/*
* @Author: D.Jane
* @Email: jane.odoo.sp@gmail.com
*/
odoo.define('pos_stock_quantity.pos_stock', function (require) {
    "use strict";
    var models = require('point_of_sale.models');
    var screens = require('point_of_sale.screens');
    var rpc = require('web.rpc');
    var utils = require('web.utils');
    var Bus = require('bus.Longpolling');

    var task;
    var round_di = utils.round_decimals;
    var round_pr = utils.round_precision;

    models.load_fields('product.product', ['type']);
    // models.load_fields('pos.config', ['manager_passw']); // no es necesario , porque el nucleo se trae toda la conf

    var _super_pos = models.PosModel.prototype;
    models.PosModel = models.PosModel.extend({
        initialize: function (session, attributes) {

            this.stock_location_modifier();

            _super_pos.initialize.call(this, session, attributes);

            var self = this;
            var bus = new Bus(this.chrome);
            bus.on('notification', this, function (notifications) {
                var stock_quant = notifications.filter(function (item) {
                    return item[0][1] === 'pos.stock.channel';
                }).map(function (item) {
                    return item[1];
                });
                var flat_stock_quant = _.reduceRight(stock_quant, function (a, b) {
                    return a.concat(b)
                }, []);

                self.on_stock_notification(flat_stock_quant);
            });
            bus.startPolling();
        },
        get_model: function (_name) {
            var _index = this.models.map(function (e) {
                return e.model;
            }).indexOf(_name);
            if (_index > -1) {
                return this.models[_index];
            }
            return false;
        },
        load_qty_after_load_product: function () {
            var wait = this.get_model('account.fiscal.position');
            var _wait_super_loaded = wait.loaded;
            wait.loaded = function (self, fiscal_positions) {
                var done = $.Deferred();
                _wait_super_loaded(self, fiscal_positions);

                var ids = Object.keys(self.db.product_by_id).map(function (item) {
                    return parseInt(item);
                });

                rpc.query({
                    model: 'product.product',
                    method: 'read',
                    args: [ids, ['qty_available']]
                }).then(function (res) {
                    self.db.qty_by_product_id = {};
                    res.forEach(function (product) {
                        self.db.qty_by_product_id[product.id] = product.qty_available;
                    });
                    self.refresh_qty();
                    done.resolve();
                });

                return done;
            }
        },
        stock_location_modifier: function () {
            this.stock_location_ids = [];

            var wait = this.get_model('pos.category');
            var _super_loaded = wait.loaded;

            wait.loaded = function (self, categories) {
                var done = new $.Deferred();
                _super_loaded(self, categories);

                if (!self.config.show_qty_available) {
                    return done.resolve();
                }

                if (self.config.allow_out_of_stock) {
                    self.config.limit_qty = 0;
                }

                if (self.config.location_only) {
                    rpc.query({
                        model: 'stock.quant',
                        method: 'get_qty_available',
                        args: [self.config.location_id[0]]
                    }).then(function (res) {
                        self.stock_location_ids = _.uniq(res.map(function (item) {
                            return item.location_id[0];
                        }));
                        self.compute_qty_in_pos_location(res);
                        done.resolve();
                    });
                } else {
                    self.load_qty_after_load_product();
                    done.resolve();
                }
                return done;
            };
        },
        on_stock_notification: function (stock_quant) {
            var self = this;
            var product_ids = stock_quant.map(function (item) {
                return item.product_id[0];
            });

            if (this.config && this.config.show_qty_available && product_ids.length > 0) {
                $.when(self.qty_sync(product_ids)).done(function () {
                    self.refresh_qty();
                });
            }
        },
        qty_sync: function (product_ids) {
            var self = this;
            var done = new $.Deferred();
            if (this.config && this.config.show_qty_available && this.config.location_only) {
                rpc.query({
                    model: 'stock.quant',
                    method: 'get_qty_available',
                    args: [false, self.stock_location_ids, product_ids]
                }).then(function (res) {
                    self.recompute_qty_in_pos_location(product_ids, res);
                    done.resolve();
                });

            } else if (this.config && this.config.show_qty_available) {
                rpc.query({
                    model: 'product.product',
                    method: 'read',
                    args: [product_ids, ['qty_available']]
                }).then(function (res) {
                    res.forEach(function (product) {
                        self.db.qty_by_product_id[product.id] = product.qty_available;
                    });
                    done.resolve();
                });
            } else {
                done.resolve();
            }
            return done.promise();
        },
        compute_qty_in_pos_location: function (res) {
            var self = this;
            self.db.qty_by_product_id = {};
            res.forEach(function (item) {
                var product_id = item.product_id[0];
                if (!self.db.qty_by_product_id[product_id]) {
                    self.db.qty_by_product_id[product_id] = item.quantity;
                } else {
                    self.db.qty_by_product_id[product_id] += item.quantity;
                }
            })
        },
        recompute_qty_in_pos_location: function (product_ids, res) {
            var self = this;
            var res_product_ids = res.map(function (item) {
                return item.product_id[0];
            });

            var out_of_stock_ids = product_ids.filter(function (id) {
                return res_product_ids.indexOf(id) === -1;
            });

            out_of_stock_ids.forEach(function (id) {
                self.db.qty_by_product_id[id] = 0;
            });

            res_product_ids.forEach(function (product_id) {
                self.db.qty_by_product_id[product_id] = false;
            });

            res.forEach(function (item) {
                var product_id = item.product_id[0];

                if (!self.db.qty_by_product_id[product_id]) {
                    self.db.qty_by_product_id[product_id] = item.quantity;
                } else {
                    self.db.qty_by_product_id[product_id] += item.quantity;
                }
            });
        },
        refresh_qty: function () {
            var self = this;
            $('.product-list').find('.qty-tag').each(function () {
                var $product = $(this).parents('.product');
                var id = parseInt($product.attr('data-product-id'));
                var product= self.db.get_product_by_id(id);
                var qty = self.db.qty_by_product_id[id];

                if (qty === false) {
                    return;
                }

                if (qty === undefined) {
                    self.db.qty_by_product_id[id] = 0;
                    qty = 0;
                }
                let text_qty= qty;
                if(product.to_weight){
                    text_qty+= ` (${self.units_by_id[product.uom_id[0]].name})`
                }
                $(this).text(text_qty).show('fast');

                if (qty <= self.config.limit_qty) {
                    $(this).addClass('sold-out');
                    if (!self.config.allow_out_of_stock) {
                        // $product.addClass('disable');
                    }
                } else {
                    $(this).removeClass('sold-out');
                    $product.removeClass('disable');
                }
            });
        },
        get_product_image_url: function (product) {
            return window.location.origin + '/web/image?model=product.product&field=image_medium&id=' + product.id;
        }
    });

    screens.ProductListWidget.include({
        render_product: function (product) {
            if (this.pos.config.show_qty_available && product.type !== 'product') {
                this.pos.db.qty_by_product_id[product.id] = false;
            }
            return this._super(product);
        },
        renderElement: function () {
            this._super();
            var self = this;
            var done = $.Deferred();
            clearInterval(task);
            task = setTimeout(function () {
                if (self.pos.config.show_qty_available) {
                    self.pos.refresh_qty();
                } else {
                    $(self.el).find('.qty-tag').hide();
                }
                done.resolve();
            }, 100);
            return done;
        }
    });

    // Capa3
    screens.ReceiptScreenWidget.include({
        init: function(parent, options){
            var self = this;
            this._super(parent, options);
        },

        /***
         * Se extiende de fiscal print (modulo de lambu) 
         * modifica las cantidades de inventario en la ventana estatica
         */
        setStatus: function(order, status){
            this._super(order, status);
            if (this.pos.config.show_qty_available) {
                this.setAvailableQty();
            }
        },

        setAvailableQty: function () {
            let self = this;
            let order = this.pos.get_order();
            let orderlines = order.get_orderlines();
            orderlines.forEach(function (line) {
                const id= line.product.id;
                if (self.pos.db.qty_by_product_id[id]) {
                    self.pos.db.qty_by_product_id[id] -= line.quantity;
                }
            });
            order['availables_for_negative_stock']= {};
            
        },
        
    });

    var _super_orderline = models.Orderline.prototype;
    models.Orderline = models.Orderline.extend({
        set_quantity: function (quantity) {
            const REMOVE= 'remove';
            let self= this;
            let old_quantity= this.quantity;
            let product= this.product;

            /* set quantity for super */
            _super_orderline.set_quantity.call(this, quantity);

            /* check qty available */
            
            if (   quantity=== REMOVE || quantity==='' 
                || !this.pos.gui.current_screen 
                || !this.pos.config.show_qty_available || this.pos.config.allow_out_of_stock || product.type !== 'product' 
                || this.is_unlock_product(this.order, product)){
                    /**
                     *  if only remove or qty null (then, no efect, continue)
                     *  if not curren screen (no load screen, no should run my code)
                     *  if config allow stock negative (then no work my code)
                     *  if the product is unlock for super passw (then, no efect, continue)
                     *  if qty available if great than limit config (then, no efect, continue)
                     */
                    return;
            }
            
            let qty_available= this.check_available(product)

            if(qty_available >= this.pos.config.limit_qty ){
                return;
            }
            else{
                /** 
                 *  if qty available is less/equal than 0, then
                 *  reset qty to old value
                 */
                _super_orderline.set_quantity.call(this, old_quantity);

                /* and reset buffer to old value */
                this.pos.gui.current_screen.numpad.state.attributes.buffer= (old_quantity || '').toString();

                /* validattion for to weight product with available qty less than 1 kg  */
                if(product.to_weight && (old_quantity=== undefined || old_quantity===null) &&(qty_available> -1 && qty_available<0)){
                    /**
                     * product is to weight
                     * is new order line
                     * real qty available is positive and less than 1 
                     */
                    // IS NEW LINE FOR TO WEIGHT PRODUCT
                    return;
                }
                else{
                    /* Management alert ... */
                    if(this.pos.config.manager_passw){
                        this.pos.gui.show_popup('order_reminder', {
                            max_available: this.pos.config.limit_qty,
                            product_name: product.display_name,
                            product: product,
                            line: self,
                            old_quantity: old_quantity,
                            new_quantity: quantity
                        });
                    }
                    else{
                        this.pos.gui.show_popup('error-info-popup', {
                            'title': 'Error de clave',
                            'body':  'Esta caja no posee una clave de administrador definida, por favor contacte con el departamento de sistema',
                        });
                    }
                }
            }

        },

        find_order_line: function(line){
            return !(this.order.orderlines.indexOf(line) === -1)
        },

        is_unlock_product: function(order, product){
            if(order['availables_for_negative_stock']){
                return order['availables_for_negative_stock'][product.id] || false;
            }
            else{
                return false;
            }
        },

        check_available: function (p) {
            
            let self = this;
            var orderLines = this.order.orderlines
            // console.log('this.pos.db:: ', this.pos.db);
            
            let qty_available = this.pos.db.qty_by_product_id[p.id];
            var unit = this.get_unit();
            
            let sum_qty = 0;
            if(!this.find_order_line(self)){
                sum_qty += self.quantity;
            }
            orderLines.forEach(line=>{
                
                if(line.product.id === p.id){
                    sum_qty += line.quantity;
                }
            })

            let qty= (qty_available - sum_qty);
            
            /* set precision */
            qty= qty.toFixed(3);
            qty= parseFloat(qty);
            // if (unit.rounding) {
            //     /* copy from core */
            //     qty = round_pr(qty, unit.rounding);
            // } else {
            //     qty = round_pr(qty, 1);
            // }
            return qty;
            
        }
    });

      //Capa1: lista de productos
      screens.ProductScreenWidget.include({
        init: function(parent, options){
            this._super(parent, options)
        },

        
        /***
         * extiende y establece validaciones al seleccionar un producto a facturar
         */
        click_product: function(product) {
            self= this;
            let opt= {};
            // let qty_available = this.pos.db.qty_by_product_id[product.id];
            if(!product.to_weight){
                this._super(product)
            }else{
                opt['quantity']= 0;
               this.pos.get_order().add_product(product, opt);
           }
        },
    })
    
});