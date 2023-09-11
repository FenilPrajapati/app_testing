odoo.define('freightbox.freight_box_dashboard', function (require) {
    "use strict";
    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');
    var _t = core._t;
    var rpc = require('web.rpc');
    var QWeb = core.qweb;
    const Session = require('web.session');


    var FreightBoxDashboardTemplate = AbstractAction.extend({
            template: 'FreightBoxDashboardMain',
            events: {
                'click .freight_enquiry':'freight_enquiry',
                'click .freight_rc':'freight_rc',
                'click .freight_draft_po':'freight_draft_po',
                'click .freight_sq':'freight_sq',
                'click .freight_draft_so':'freight_draft_so',
                'click .freight_po':'freight_po',
                'click .freight_so':'freight_so',
                'click .freight_job':'freight_job',
                'click .freight_transport':'freight_transport',
                'click .freight_open_si': 'freight_open_si',
                'click .freight_draft_si': 'freight_draft_si',
                'click .freight_update_si': 'freight_update_si',
                'click .freight_approved_si':'freight_approved_si',
                'click .freight_draft_bol':'freight_draft_bol',
                'click .freight_update_bol': 'freight_update_bol',
                'click .freight_hold_bol': 'freight_hold_bol',
                'click .freight_amend_bol': 'freight_amend_bol',
                'click .freight_switch_bol': 'freight_switch_bol',
                'click .freight_issue_bol': 'freight_issue_bol',
                'click .freight_surrender_bol': 'freight_surrender_bol',
                'click .freight_release_cargo': 'freight_release_cargo',
            },

            start: function () {
                var self = this;
//                core.bus.on('barcode_scanned', this, this._onBarcodeScanned);
                self.session = Session;
                var def = this._rpc({
                        model: 'freight.dashboard',
                        method: 'get_freight_dashboard_data',
                        args: [[]],
//                        args: [[['id', '=', this.session.company_id]], ['name']],
                    }).then(function (data){
//                        alert("companies:"+ companies["crm_count"]);
                        self.crm_count = data["crm_count"];
                        self.rc_count = data["rc_count"];
                        self.draft_po_count = data["draft_po_count"];
                        self.sq_count = data["sq_count"];
                        self.draft_so_count = data["draft_so_count"];
                        self.po_count = data["po_count"];
                        self.so_count = data["so_count"];
                        self.job_count = data["job_count"];
                        self.transport_count = data["transport_count"];
                        self.open_si_count = data["open_si_count"];
                        self.draft_si_count = data["draft_si_count"];
                        self.update_si_count = data["update_si_count"];
                        self.approve_si_count = data["approve_si_count"];
                        self.draft_bol_count = data["draft_bol_count"];
                        self.update_bol_count = data["update_bol_count"];
                        self.hold_bol_count = data["hold_bol_count"];
                        self.amend_bol_count = data["amend_bol_count"];
                        self.switch_bol_count = data["switch_bol_count"];
                        self.issue_bol_count = data["issue_bol_count"];
                        self.surrender_bol_count = data["surrender_bol_count"];
                        self.release_cargo_count = data["release_cargo_count"];
//                        self.company_image_url = self.session.url('/web/image', {model: 'res.company', id: self.session.company_id, field: 'logo',});
                        self.$el.html(QWeb.render("FreightBoxDashboardMain", {widget: self}));
//                        self.start_clock();
                    });
                // Make a RPC call every day to keep the session alive
//                self._interval = window.setInterval(this._callServer.bind(this), (60*60*1000*24));
                return Promise.all([def, this._super.apply(this, arguments)]);
            },

            /*willStart: function () {
                this._rpc({
                method: 'get_freight_dashboard_data',
                model: 'crm.lead',
            }).then(function (result) {
                // we write on the prototype to share the information between
                // all pad widgets instances, across all actions
//                FieldPad.prototype.isPadConfigured = result;
            });
//            return "test";
//        return this._super.apply(this, arguments);
            },*/

            /*init: function(ev) {

                var self = this;

//                self.test_cal();
//                ev.stopPropagation();

                *//*this._rpc({
                    model: 'freight.dashboard',
                    method: 'get_freight_dashboard_data',

                }).then(function () {
//                    self.reload();
                });*//*

            },
*/

            freight_enquiry: function(ev){
                var self = this;
                ev.stopPropagation();
                ev.preventDefault();
//                var $action = $(ev.currentTarget);
                console.log('Takes us to list of Enquiry Screen')

                self._rpc({
                 model: 'crm.lead',
                 method: 'action_get_crm_freightbox_views',
//                args: ["freightbox.freight_box_crm_tree"],
                }).then(function (data) {
                var crm_form_id = data['crm_form_id'];
                var crm_tree_id = data['crm_tree_id'];
                self.do_action({
                    name: _t("Inquiries"),
                    type: 'ir.actions.act_window',
                    res_model: 'crm.lead',
                    view_mode: 'tree',
                    context: {
                        'is_freight_crm': true,
                        'default_type': 'opportunity',
                        'default_is_freight_box_crm': true
                    },
                    domain: [['is_freight_box_crm','=', true]],
                    views: [[crm_tree_id, 'list'], [crm_form_id, 'form']],
//                    target: 'main'
                });
                });


            },

            freight_rc: function(ev){
                var self = this;
                ev.stopPropagation();
                ev.preventDefault();
    //            var $action = $(ev.currentTarget);
                console.log('Takes us to list of Rate Comparision screen')
                self._rpc({
                 model: 'crm.lead',
                 method: 'action_get_crm_freightbox_views',
//                args: ["freightbox.freight_box_crm_tree"],
                }).then(function (data) {
                    var rfq_form_id = data['rfq_form_id'];
                    var rfq_tree_id = data['rfq_tree_id'];
                    self.do_action({
                        name: _t("Rate Comparision"),
                        type: 'ir.actions.act_window',
                        res_model: 'request.for.quote',
                        view_mode: 'tree',
                        view_mode: 'tree',
                        context : {'group_by': 'booking_id'},
                        views: [[rfq_tree_id, 'list'], [rfq_form_id, 'form']],
    //                    target: 'main'
                    });
                });

            },

            freight_draft_po: function(ev){
                var self = this;
                ev.stopPropagation();
                ev.preventDefault();
    //            var $action = $(ev.currentTarget);
                console.log('Takes us to list of Draft PO screen')



                self._rpc({
                 model: 'crm.lead',
                 method: 'action_get_crm_freightbox_views',
//                args: ["freightbox.freight_box_crm_tree"],
                }).then(function (data) {
                var po_form_id = data['po_form_id'];
                var po_tree_id = data['po_tree_id'];
                self.do_action({
                    name: _t("Draft PO"),
                    type: 'ir.actions.act_window',
                    res_model: 'purchase.order',
                    view_mode: 'tree',
                    context: {
                        'default_is_freight_box_po': true
                    },
                    domain: [['is_freight_box_po','=', true], ['state','=', 'draft']],
                    views: [[po_tree_id, 'list'], [po_form_id, 'form']],
//                    target: 'main'
                });
                });
            },

            freight_sq: function(ev){
                var self = this;
                ev.stopPropagation();
                ev.preventDefault();
    //            var $action = $(ev.currentTarget);
                console.log('Takes us to list of Shipment QuoteS screen')

                self._rpc({
                 model: 'crm.lead',
                 method: 'action_get_crm_freightbox_views',
//                args: ["freightbox.freight_box_crm_tree"],
                }).then(function (data) {
                var sq_form_id = data['sq_form_id'];
                var sq_tree_id = data['sq_tree_id'];
                self.do_action({
                    name: _t("Shipment Quote"),
                    type: 'ir.actions.act_window',
                    res_model: 'shipment.quote',
                    view_mode: 'tree',
                    views: [[sq_tree_id, 'list'], [sq_form_id, 'form']],
//                    target: 'main'
                });
                });
            },

            
            freight_draft_so: function(ev){
                var self = this;
                ev.stopPropagation();
                ev.preventDefault();
    //            var $action = $(ev.currentTarget);
                console.log('Takes us to list of DRAFT SO screen')

                self._rpc({
                    model: 'crm.lead',
                    method: 'action_get_crm_freightbox_views',
   //                args: ["freightbox.freight_box_crm_tree"],
                   }).then(function (data) {
                   var so_form_id = data['so_form_id'];
                   var so_tree_id = data['so_tree_id'];

                self.do_action({
                name: _t("Draft SO"),
                type: 'ir.actions.act_window',
                res_model: 'sale.order',
                view_mode: 'tree',
                context: {
                    'default_is_freight_box_so': true
                },
                domain: [['is_freight_box_so','=', true], ['state','=', 'draft']],
                views: [[so_tree_id, 'list'], [so_form_id, 'form']],
            });
            });
        },

            freight_po: function(ev){
                var self = this;
                ev.stopPropagation();
                ev.preventDefault();
    //            var $action = $(ev.currentTarget);
                console.log('Takes us to list of Purchase OrderS screen')

                self._rpc({
                    model: 'crm.lead',
                    method: 'action_get_crm_freightbox_views',
   //                args: ["freightbox.freight_box_crm_tree"],
                   }).then(function (data) {
                   var po_form_id = data['po_form_id'];
                   var po_tree_id = data['po_tree_id'];

                // var options = {
                //     on_reverse_breadcrumb: this.on_reverse_breadcrumb,
                // };

                self.do_action({
                name: _t("Purchase Order"),
                type: 'ir.actions.act_window',
                res_model: 'purchase.order',
                view_mode: 'tree',
                // views: [[false, 'list'], [false, 'form']],
                context: {
                        'default_is_freight_box_po': true
                    },
                domain: [['is_freight_box_po','=', true], ['state', '!=', 'draft']],
                views: [[po_tree_id, 'list'], [po_form_id, 'form']],
                // target: 'main'

            });
        });
    },



            freight_so: function(ev){
                var self = this;
                ev.stopPropagation();
                ev.preventDefault();
    //            var $action = $(ev.currentTarget);
                console.log('Takes us to list of Sale OrderS screen')

                self._rpc({
                    model: 'crm.lead',
                    method: 'action_get_crm_freightbox_views',
   //                args: ["freightbox.freight_box_crm_tree"],
                   }).then(function (data) {
                   var so_form_id = data['so_form_id'];
                   var so_tree_id = data['so_tree_id'];

                self.do_action({
                name: _t("Sale Order"),
                type: 'ir.actions.act_window',
                res_model: 'sale.order',
                view_mode: 'tree',
                views: [[false, 'list'], [false, 'form']],
                context: {
                    'default_is_freight_box_so': true
                },
                domain: [['is_freight_box_so','=', true], ['state', '!=', 'draft']],
                views: [[so_tree_id, 'list'], [so_form_id, 'form']],
                // context: {'form_view_ref': 'freightbox.sale_order_form_view_freightbox'},
    //            context: {
    //                'search_default_month': true,
    //            },
                // domain: [['state','=', 'draft']],
                // target: 'main'
            
            });
        });
    },

            freight_job: function(ev){
                var self = this;
                ev.stopPropagation();
                ev.preventDefault();
                console.log('Takes us to list of JobS screen')

                self._rpc({
                    model: 'crm.lead',
                    method: 'action_get_crm_freightbox_views',
   //                args: ["freightbox.freight_box_crm_tree"],
                   }).then(function (data) {
                   var job_form_id = data['job_form_id'];
                   var job_tree_id = data['job_tree_id'];

                self.do_action({
                    name: _t("Job"),
                    type: 'ir.actions.act_window',
                    res_model: 'job',
                    view_mode: 'tree',
                    views: [[job_tree_id, 'list'], [job_form_id, 'form']],
    //                domain: [['employee_id','=', this.login_employee.id]],
                //     target: 'main' //self on some of them
                // }, {
                //         on_reverse_breadcrumb: this.on_reverse_breadcrumb
                    });
                });
            },
        
            freight_transport: function(ev){
                var self = this;
                ev.stopPropagation();
                ev.preventDefault();
                console.log('Takes us to list of TRANSPORT screen')

                self._rpc({
                    model: 'crm.lead',
                    method: 'action_get_crm_freightbox_views',
   //                args: ["freightbox.freight_box_crm_tree"],
                   }).then(function (data) {
                   var transport_form_id = data['transport_form_id'];
                   var transport_tree_id = data['transport_tree_id'];


                self.do_action({
                    name: _t("Transport"),
                    type: 'ir.actions.act_window',
                    res_model: 'transport',
                    view_mode: 'tree',
                    views: [[transport_tree_id, 'list'], [transport_form_id, 'form']],
    //                domain: [['employee_id','=', this.login_employee.id]],
                //     target: 'main' //self on some of them
                // }, {
                //         on_reverse_breadcrumb: this.on_reverse_breadcrumb
                    });
                });
            },

            freight_open_si: function(ev){
                var self = this;
                ev.stopPropagation();
                ev.preventDefault();
    //            var $action = $(ev.currentTarget);
                console.log('Takes us to list of OPEN Shipping Instructions Screen')

                self._rpc({
                    model: 'crm.lead',
                    method: 'action_get_crm_freightbox_views',
   //                args: ["freightbox.freight_box_crm_tree"],
                   }).then(function (data) {
                   var open_si_form_id = data['open_si_form_id'];
                   var open_si_tree_id = data['open_si_tree_id'];

                self.do_action({
                    name: _t("Open SI "),
                    type: 'ir.actions.act_window',
                    res_model: 'shipping.instruction',
                    view_mode: 'tree',
                    views: [[open_si_tree_id, 'list'], [open_si_form_id, 'form']],
    //            context: {
    //                'search_default_month': true,
    //            },
                    domain: [['state','=', 'open']],
                    // target: 'main'
                });
            });
        },


            freight_draft_si: function(ev){
                var self = this;
                ev.stopPropagation();
                ev.preventDefault();
    //            var $action = $(ev.currentTarget);
                console.log('Takes us to list of DRAFT Shinpping Instaructions screen')

                self._rpc({
                    model: 'crm.lead',
                    method: 'action_get_crm_freightbox_views',
   //                args: ["freightbox.freight_box_crm_tree"],
                   }).then(function (data) {
                   var draft_si_form_id = data['draft_si_form_id'];
                   var draft_si_tree_id = data['draft_si_tree_id'];

                self.do_action({
                    name: _t("Draft SI"),
                    type: 'ir.actions.act_window',
                    res_model: 'shipping.instruction',
                    view_mode: 'tree',
                    views: [[draft_si_tree_id, 'list'], [draft_si_form_id, 'form']],
        //            context: {
        //                'search_default_month': true,
        //            },
                    domain: [['state','=', 'draft']],
                    // target: 'main'
                });
            });
        },

            freight_update_si: function(ev){
                var self = this;
                ev.stopPropagation();
                ev.preventDefault();
    //            var $action = $(ev.currentTarget);
                console.log('Takes us to list of UPDATED Shipping Instructions Screen')

                self._rpc({
                    model: 'crm.lead',
                    method: 'action_get_crm_freightbox_views',
   //                args: ["freightbox.freight_box_crm_tree"],
                   }).then(function (data) {
                   var update_si_form_id = data['update_si_form_id'];
                   var update_si_tree_id = data['update_si_tree_id'];

                self.do_action({
                    name: _t("Update SI "),
                    type: 'ir.actions.act_window',
                    res_model: 'shipping.instruction',
                    view_mode: 'tree',
                    views: [[update_si_tree_id, 'list'], [update_si_form_id, 'form']],
        //            context: {
        //                'search_default_month': true,
        //            },
                    domain: [['state','=', 'updated']],
                    // target: 'main'
                });
            });
        },

            freight_approved_si: function(ev){
                var self = this;
                ev.stopPropagation();
                ev.preventDefault();
    //            var $action = $(ev.currentTarget);
                console.log('Takes us to list of APPROVED Shipping Instructions Screen')

                self._rpc({
                    model: 'crm.lead',
                    method: 'action_get_crm_freightbox_views',
   //                args: ["freightbox.freight_box_crm_tree"],
                   }).then(function (data) {
                   var approved_si_form_id = data['approved_si_form_id'];
                   var approved_si_tree_id = data['approved_si_tree_id'];

                self.do_action({
                    name: _t("Approved SI"),
                    type: 'ir.actions.act_window',
                    res_model: 'shipping.instruction',
                    view_mode: 'tree',
                    views: [[approved_si_tree_id, 'list'], [approved_si_form_id, 'form']],
        //            context: {
        //                'search_default_month': true,
        //            },
                    domain: [['state','=', 'accepted']],
                    // target: 'main'
                });
            });
        },


            freight_draft_bol: function(e) {
                var self = this;
                e.stopPropagation();
                e.preventDefault();
                console.log('Takes us to list of DRAFT Bill of Ladings Screen')
                self._rpc({
                    model: 'crm.lead',
                    method: 'action_get_crm_freightbox_views',
   //                args: ["freightbox.freight_box_crm_tree"],
                   }).then(function (data) {
                   var draft_bol_form_id = data['draft_bol_form_id'];
                   var draft_bol_tree_id = data['draft_bol_tree_id'];

                self.do_action({
                    name: _t("Draft BOL "),
                    type: 'ir.actions.act_window',
                    res_model: 'bill.of.lading',
                    view_mode: 'tree',
                    views: [[draft_bol_tree_id, 'list'], [draft_bol_form_id, 'form']],
        //            context: {
        //                'search_default_month': true,
        //            },
                    domain: [['state','=', 'draft']],
                    // target: 'main'
                });
            });
        },


        freight_update_bol: function(e) {
             var self = this;
            e.stopPropagation();
            e.preventDefault();
            console.log('Takes us to list of UPDATED Bill of Ladings Screen')
            self._rpc({
                model: 'crm.lead',
                method: 'action_get_crm_freightbox_views',
//                args: ["freightbox.freight_box_crm_tree"],
               }).then(function (data) {
               var update_bol_form_id = data['update_bol_form_id'];
               var update_bol_tree_id = data['update_bol_tree_id'];

            self.do_action({
                name: _t("Update BOL "),
                type: 'ir.actions.act_window',
                res_model: 'bill.of.lading',
                view_mode: 'tree',
                views: [[update_bol_tree_id, 'list'], [update_bol_form_id, 'form']],
    //            context: {
    //                'search_default_month': true,
    //            },
                domain: [['state','=', 'update']],
                // target: 'main'
            });
        });
    },

        freight_hold_bol: function(e) {
             var self = this;
            e.stopPropagation();
            e.preventDefault();
            console.log('Takes us to list of HOLD Bill of Lading Screen')
            self._rpc({
                model: 'crm.lead',
                method: 'action_get_crm_freightbox_views',
//                args: ["freightbox.freight_box_crm_tree"],
               }).then(function (data) {
               var hold_bol_form_id = data['hold_bol_form_id'];
               var hold_bol_tree_id = data['hold_bol_tree_id'];

            self.do_action({
                name: _t("Hold BOL "),
                type: 'ir.actions.act_window',
                res_model: 'bill.of.lading',
                view_mode: 'tree',
                views: [[hold_bol_tree_id, 'list'], [hold_bol_form_id, 'form']],
    //            context: {
    //                'search_default_month': true,
    //            },
                domain: [['state','=', 'hold']],
                // target: 'main'
            });
        });
    },


        freight_amend_bol: function(e) {
             var self = this;
            e.stopPropagation();
            e.preventDefault();
            console.log('Takes us to list of AMEND Bill of Ladings Screen')
            self._rpc({
                model: 'crm.lead',
                method: 'action_get_crm_freightbox_views',
//                args: ["freightbox.freight_box_crm_tree"],
               }).then(function (data) {
               var amend_bol_form_id = data['amend_bol_form_id'];
               var amend_bol_tree_id = data['amend_bol_tree_id'];

            self.do_action({
                name: _t("Amend BOL "),
                type: 'ir.actions.act_window',
                res_model: 'bill.of.lading',
                view_mode: 'tree',
                views: [[amend_bol_tree_id, 'list'], [amend_bol_form_id, 'form']],
    //            context: {
    //                'search_default_month': true,
    //            },
                domain: [['state','=', 'amend']],
                // target: 'main'
            });
        });
    },


        freight_switch_bol: function(e) {
            var self = this;
           e.stopPropagation();
           e.preventDefault();
           console.log('Takes us to list of SWITCH Bill of Ladings Screen')
           self._rpc({
            model: 'crm.lead',
            method: 'action_get_crm_freightbox_views',
//                args: ["freightbox.freight_box_crm_tree"],
           }).then(function (data) {
           var switch_bol_form_id = data['switch_bol_form_id'];
           var switch_bol_tree_id = data['switch_bol_tree_id'];

        self.do_action({
               name: _t("Switch BOL "),
               type: 'ir.actions.act_window',
               res_model: 'bill.of.lading',
               view_mode: 'tree',
               views: [[switch_bol_tree_id, 'list'], [switch_bol_form_id, 'form']],
   //            context: {
   //                'search_default_month': true,
   //            },
               domain: [['state','=', 'switch']],
            //    target: 'main'
            });
        });
    },


        freight_issue_bol: function(e) {
             var self = this;
            e.stopPropagation();
            e.preventDefault();
            console.log('Takes us to list of ISSUE Bill of Ladings Screen')
            self._rpc({
                model: 'crm.lead',
                method: 'action_get_crm_freightbox_views',
//                args: ["freightbox.freight_box_crm_tree"],
               }).then(function (data) {
               var issue_bol_form_id = data['issue_bol_form_id'];
               var issue_bol_tree_id = data['issue_bol_tree_id'];

            self.do_action({
                name: _t("Issue BOL "),
                type: 'ir.actions.act_window',
                res_model: 'bill.of.lading',
                view_mode: 'tree',
                views: [[issue_bol_tree_id, 'list'], [issue_bol_form_id, 'form']],
    //            context: {
    //                'search_default_month': true,
    //            },
                domain: [['state','=', 'approve']],
                // target: 'main'
            });
        });
    },

        freight_surrender_bol: function(e) {
            var self = this;
           e.stopPropagation();
           e.preventDefault();
           console.log('Takes us to list of SURRENDERED Bill of Ladings Screen')
           self._rpc({
            model: 'crm.lead',
            method: 'action_get_crm_freightbox_views',
//                args: ["freightbox.freight_box_crm_tree"],
           }).then(function (data) {
           var surrender_bol_form_id = data['surrender_bol_form_id'];
           var surrender_bol_tree_id = data['surrender_bol_tree_id'];

        self.do_action({
               name: _t("Surrendered BOL "),
               type: 'ir.actions.act_window',
               res_model: 'bill.of.lading',
               view_mode: 'tree',
               views: [[surrender_bol_tree_id, 'list'], [surrender_bol_form_id, 'form']],
   //            context: {
   //                'search_default_month': true,
   //            },
               domain: [['state','=', 'done']],
            //    target: 'main'
            });
        });
    },

        freight_release_cargo: function(e) {
            var self = this;
           e.stopPropagation();
           e.preventDefault();
           console.log('Takes us to list of RELASED CARGO')
           self._rpc({
            model: 'crm.lead',
            method: 'action_get_crm_freightbox_views',
//                args: ["freightbox.freight_box_crm_tree"],
           }).then(function (data) {
           var release_cargo_form_id = data['release_cargo_form_id'];
           var release_cargo_tree_id = data['release_cargo_tree_id'];

        self.do_action({
               name: _t("Released Cargo "),
               type: 'ir.actions.act_window',
               res_model: 'job',
               view_mode: 'tree',
               views: [[release_cargo_tree_id, 'list'], [release_cargo_form_id, 'form']],
   //            context: {
   //                'search_default_month': true,
   //            },
               domain: [['state','=', 'cargo_released']],
            //    target: 'main'
            });
        });
    },

            /*freight_draft_bol: function(ev){
                var self = this;
                ev.stopPropagation();
                ev.preventDefault();
                console.log('entered function hr payslip')

                var options = {
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb,
                };

                this.do_action({
                name: _t("Bill Of Lading"),
                type: 'ir.actions.act_window',
                res_model: 'bill.of.lading',
                view_mode: 'tree','form',
                views: [[false, 'list'], [false, 'form']],
    //            context: {
    //                'search_default_month': true,
    //            },
    //            domain: [['employee_id','=', this.login_employee.id]],
                target: 'current'
            }, options)
            },*/

       });
    //    alert("bolllllllllllllllllllllllllllllll");
        core.action_registry.add('freight_box_dashboard', FreightBoxDashboardTemplate);

    return FreightBoxDashboardTemplate;

    });