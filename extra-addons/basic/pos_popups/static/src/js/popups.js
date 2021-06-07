odoo.define('pos_popups.popups', function (require) {
"use strict";

var PopupWidget = require('point_of_sale.popups');
var gui = require('point_of_sale.gui');

var SuccessInfoPopup = PopupWidget.extend({
    template: 'SuccessInfoPopup',
    show: function(options){
        var self = this;
        options = options || {};
        this._super(options);
        this.list = options.list || [];
        this.is_selected = options.is_selected || function (item) { return false; };
        this.renderElement();
    },
    click_item : function(event) {
        this.gui.close_popup();
        if (this.options.confirm) {
            var item = this.list[parseInt($(event.target).data('item-index'))];
            item = item ? item.item : item;
            this.options.confirm.call(self,item);
        }
    }
});
gui.define_popup({name:'success-info-popup', widget: SuccessInfoPopup});

var ErrorInfoPopup = PopupWidget.extend({
    template: 'ErrorInfoPopup',
    show: function(options){
        var self = this;
        options = options || {};
        this._super(options);
        this.list = options.list || [];
        this.is_selected = options.is_selected || function (item) { return false; };
        this.renderElement();
    },
    click_item : function(event) {
        this.gui.close_popup();
        if (this.options.confirm) {
            var item = this.list[parseInt($(event.target).data('item-index'))];
            item = item ? item.item : item;
            this.options.confirm.call(self,item);
        }
    }
});
gui.define_popup({name:'error-info-popup', widget: ErrorInfoPopup});

var WarningInfoPopup = PopupWidget.extend({
    template: 'WarningInfoPopup',
    show: function(options){
        var self = this;
        options = options || {};
        this._super(options);
        this.list = options.list || [];
        this.is_selected = options.is_selected || function (item) { return false; };
        this.renderElement();
    },
    click_item : function(event) {
        this.gui.close_popup();
        if (this.options.confirm) {
            var item = this.list[parseInt($(event.target).data('item-index'))];
            item = item ? item.item : item;
            this.options.confirm.call(self,item);
        }
    }
});
gui.define_popup({name:'warning-info-popup', widget: WarningInfoPopup});

return PopupWidget;
});