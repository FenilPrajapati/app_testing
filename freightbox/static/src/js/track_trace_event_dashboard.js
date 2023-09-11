odoo.define('freightbox.track_trace_event_dashboard', function (require) {
"use strict";
var core = require('web.core');
var ListController = require('web.ListController');
var ListModel = require('web.ListModel');
var ListRenderer = require('web.ListRenderer');
var ListView = require('web.ListView');
var SampleServer = require('web.SampleServer');
var view_registry = require('web.view_registry');

var QWeb = core.qweb;
let dashboardValues;
SampleServer.mockRegistry.add('track.trace.event/retrieve_dashboard', () => {
    return Object.assign({}, dashboardValues);
});


//--------------------------------------------------------------------------
// List View
//--------------------------------------------------------------------------

var TntListDashboardRenderer = ListRenderer.extend({
    events:_.extend({}, ListRenderer.prototype.events, {
        'click .o_dashboard_action': '_onDashboardActionClicked',
    }),
    /**
     * @override
     * @private
     * @returns {Promise}
     */
    _renderView: function () {
        var self = this;
        return this._super.apply(this, arguments).then(function () {
            var values = self.state.dashboardValues;
            var tnt_dashboard = QWeb.render('freightbox.TnTEventDashboard', {
                values: values,
            });
            self.$el.prepend(tnt_dashboard);
        });
    },

    /**
     * @private
     * @param {MouseEvent}
     */
//    _onDashboardActionClicked: function (e) {
//        e.preventDefault();
//        var $action = $(e.currentTarget);
//        this.trigger_up('dashboard_open_action', {
//            action_name: $action.attr('name')+"_list",
//            action_context: $action.attr('context'),
//        });

    _onDashboardActionClicked: function (e) {
        e.preventDefault();
        var $action = $(e.currentTarget);
        var $action = $(e.currentTarget);
        this.trigger_up('dashboard_open_action', {
            action_name: $action.attr('name')+"_list",
            action_context: $action.attr('context'),
        });

    },
});

var TntListDashboardModel = ListModel.extend({
    /**
     * @override
     */
    init: function () {
        this.dashboardValues = {};
        this._super.apply(this, arguments);
    },

    /**
     * @override
     */
    __get: function (localID) {
        var result = this._super.apply(this, arguments);
        if (_.isObject(result)) {
            result.dashboardValues = this.dashboardValues[localID];
        }
        return result;
    },
    /**
     * @override
     * @returns {Promise}
     */
    __load: function () {
        return this._loadDashboard(this._super.apply(this, arguments));
    },
    /**
     * @override
     * @returns {Promise}
     */
    __reload: function () {
        return this._loadDashboard(this._super.apply(this, arguments));
    },

    /**
     * @private
     * @param {Promise} super_def a promise that resolves with a dataPoint id
     * @returns {Promise -> string} resolves to the dataPoint id
     */
    _loadDashboard: function (super_def) {
        var self = this;
        var dashboard_def = this._rpc({
            model: 'track.trace.event',
            method: 'retrieve_dashboard',
        });
        return Promise.all([super_def, dashboard_def]).then(function(results) {
            var id = results[0];
            dashboardValues = results[1];
            self.dashboardValues[id] = dashboardValues;
            return id;
        });
    },
});

var TntListDashboardController = ListController.extend({
    custom_events: _.extend({}, ListController.prototype.custom_events, {
        dashboard_open_action: '_onDashboardOpenAction',
    }),

    /**
     * @private
     * @param {OdooEvent} e
     */
    _onDashboardOpenAction: function (e) {
        return this.do_action(e.data.action_name,
            {additional_context: JSON.parse(e.data.action_context)});
    },
});

var TntListDashboardView = ListView.extend({
    config: _.extend({}, ListView.prototype.config, {
        Model: TntListDashboardModel,
        Renderer: TntListDashboardRenderer,
        Controller: TntListDashboardController,
    }),
});

view_registry.add('tnt_event_dashboard', TntListDashboardView);
return {
    TntListDashboardModel: TntListDashboardModel,
    TntListDashboardRenderer: TntListDashboardRenderer,
    TntListDashboardController: TntListDashboardController,
};

});
