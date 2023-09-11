odoo.define('freightbox.bill_of_lading', function (require) {
'use strict';
var publicWidget = require('web.public.widget');
var core = require('web.core');
var Widget = require('web.Widget');
var publicWidget = require('web.public.widget');
var rowIdx = 0;
var rpc = require('web.rpc');


    const Dialog = require('web.Dialog');
    const { qweb, _t } = require('web.core');

var WebsiteBOL = Widget.extend({
        // xmlDependencies: ['/freightbox/static/src/xml/SiPopup.xml'],
       
    start: function () {
        var self = this;
        console.log('-------------------------- call my start1')
        var res = this._super.apply(this.arguments).then(function () {


            // Create BOL submit action
            $('#bol_view_form').on('click', '.create_bol_submit', function (ev) {

                var parent_vals = [];
                // var bol_id = document.getElementById("bol_id").value;
                var transport_document_type_code = document.getElementById("transport_document_type_code").value;
                
                var number_of_originals = document.getElementsByName("number_of_originals")[0].value;
                var carrier_booking_reference = document.getElementsByName("carrier_booking_reference")[0].value;
                var is_electronic = document.getElementsByName("is_electronic")[0].value;
                var number_of_copies = document.getElementsByName("number_of_copies")[0].value;
                var is_shipped_onboard_type = document.getElementsByName("is_shipped_onboard_type")[0].value;
                var is_charges_displayed = document.getElementsByName("is_charges_displayed")[0].value;
                var location_name = document.getElementsByName("location_name")[0].value;
                var city_name = document.getElementsByName("city_name")[0].value;
                var un_location_code = document.getElementsByName("un_location_code")[0].value;
                var state_region = document.getElementsByName("state_region")[0].value;
                var country = document.getElementsByName("country")[0].value;
                var shipping_instruction_ID = document.getElementsByName("shipping_instruction_ID")[0].value;
                var transport_document_reference = document.getElementsByName("transport_document_reference")[0].value;
                var reciept_or_deliverytype_at_origin = document.getElementsByName("reciept_or_deliverytype_at_origin")[0].value;
                var reciept_or_deliverytype_at_dest = document.getElementsByName("reciept_or_deliverytype_at_dest")[0].value;
                var shipped_onboard_date = document.getElementsByName("shipped_onboard_date")[0].value;
                var issue_date = document.getElementsByName("issue_date")[0].value;
                var cargo_movement_type_at_origin = document.getElementsByName("cargo_movement_type_at_origin")[0].value;
                var cargo_movement_type_at_dest = document.getElementsByName("cargo_movement_type_at_dest")[0].value;
                var terms_and_conditions = document.getElementsByName("terms_and_conditions")[0].value;
                var received_for_shipment_date = document.getElementsByName("received_for_shipment_date")[0].value;
                var declared_value = document.getElementsByName("declared_value")[0].value;
                var service_contract_reference = document.getElementsByName("service_contract_reference")[0].value;
                var declared_value_currency = document.getElementsByName("declared_value_currency")[0].value;
                var issuer_code = document.getElementsByName("issuer_code")[0].value;
                var issuer_code_list_provider = document.getElementsByName("issuer_code_list_provider")[0].value;
                var no_of_rider_pages = document.getElementsByName("no_of_rider_pages")[0].value;
                var planned_arrival_date = document.getElementsByName("planned_arrival_date")[0].value;
                var planned_departure_date = document.getElementsByName("planned_departure_date")[0].value;
                var document_hash = document.getElementsByName("document_hash")[0].value;
                var pre_carried_by = document.getElementsByName("pre_carried_by")[0].value;


                var poi_location_name = document.getElementsByName("poi_location_name")[0].value;
                var poi_post_code = document.getElementsByName("poi_post_code")[0].value;
                var poi_un_location_code = document.getElementsByName("poi_un_location_code")[0].value;
                var poi_city_name = document.getElementsByName("poi_city_name")[0].value;
                var poi_street_name = document.getElementsByName("poi_street_name")[0].value;
                var poi_state_region = document.getElementsByName("poi_state_region")[0].value;
                var poi_street_number = document.getElementsByName("poi_street_number")[0].value;
                var poi_country = document.getElementsByName("poi_country")[0].value;
                var poi_floor = document.getElementsByName("poi_floor")[0].value;

                var por_location_name = document.getElementsByName("por_location_name")[0].value;
                var por_post_code = document.getElementsByName("por_post_code")[0].value;
                var por_un_location_code = document.getElementsByName("por_un_location_code")[0].value;
                var por_city_name = document.getElementsByName("por_city_name")[0].value;
                var por_street_name = document.getElementsByName("por_street_name")[0].value;
                var por_state_region = document.getElementsByName("por_state_region")[0].value;
                var por_street_number = document.getElementsByName("por_street_number")[0].value;
                var por_country = document.getElementsByName("por_country")[0].value;
                var por_floor = document.getElementsByName("por_floor")[0].value;

                var pol_location_name = document.getElementsByName("pol_location_name")[0].value;
                // var pol_post_code = document.getElementsByName("pol_post_code")[0].value;
                var pol_un_location_code = document.getElementsByName("pol_un_location_code")[0].value;
                var pol_city_name = document.getElementsByName("pol_city_name")[0].value;
                // var pol_street_name = document.getElementsByName("pol_street_name")[0].value;
                var pol_state_region = document.getElementsByName("pol_state_region")[0].value;
                // var pol_street_number = document.getElementsByName("pol_street_number")[0].value;
                var pol_country = document.getElementsByName("pol_country")[0].value;
                // var pol_floor = document.getElementsByName("pol_floor")[0].value;

                var pod_location_name = document.getElementsByName("pod_location_name")[0].value;
                // var pod_post_code = document.getElementsByName("pod_post_code")[0].value;
                var pod_un_location_code = document.getElementsByName("pod_un_location_code")[0].value;
                var pod_city_name = document.getElementsByName("pod_city_name")[0].value;
                // var pod_street_name = document.getElementsByName("pod_street_name")[0].value;
                var pod_state_region = document.getElementsByName("pod_state_region")[0].value;
                // var pod_street_number = document.getElementsByName("pod_street_number")[0].value;
                var pod_country = document.getElementsByName("pod_country")[0].value;
                // var pod_floor = document.getElementsByName("pod_floor")[0].value;

                var plod_location_name = document.getElementsByName("plod_location_name")[0].value;
                var plod_post_code = document.getElementsByName("plod_post_code")[0].value;
                var plod_un_location_code = document.getElementsByName("plod_un_location_code")[0].value;
                var plod_city_name = document.getElementsByName("plod_city_name")[0].value;
                var plod_street_name = document.getElementsByName("plod_street_name")[0].value;
                var plod_state_region = document.getElementsByName("plod_state_region")[0].value;
                var plod_street_number = document.getElementsByName("plod_street_number")[0].value;
                var plod_country = document.getElementsByName("plod_country")[0].value;
                var plod_floor = document.getElementsByName("plod_floor")[0].value;

                var oir_location_name = document.getElementsByName("oir_location_name")[0].value;
                var oir_post_code = document.getElementsByName("oir_post_code")[0].value;
                var oir_un_location_code = document.getElementsByName("oir_un_location_code")[0].value;
                var oir_city_name = document.getElementsByName("oir_city_name")[0].value;
                var oir_street_name = document.getElementsByName("oir_street_name")[0].value;
                var oir_state_region = document.getElementsByName("oir_state_region")[0].value;
                var oir_street_number = document.getElementsByName("oir_street_number")[0].value;
                var oir_country = document.getElementsByName("oir_country")[0].value;
                var oir_floor = document.getElementsByName("oir_floor")[0].value;

                var pre_location_name = document.getElementsByName("pre_location_name")[0].value;
                var pre_post_code = document.getElementsByName("pre_post_code")[0].value;
                var pre_latitude = document.getElementsByName("pre_latitude")[0].value;
                var pre_longitude = document.getElementsByName("pre_longitude")[0].value;
                var pre_un_location_code = document.getElementsByName("pre_un_location_code")[0].value;
                var pre_city_name = document.getElementsByName("pre_city_name")[0].value;
                var pre_street_name = document.getElementsByName("pre_street_name")[0].value;
                var pre_state_region = document.getElementsByName("pre_state_region")[0].value;
                var pre_street_number = document.getElementsByName("pre_street_number")[0].value;
                var pre_country = document.getElementsByName("pre_country")[0].value;
                var pre_floor = document.getElementsByName("pre_floor")[0].value;

                var bol_id = document.getElementById("bol_id").value;
                parent_vals.push({
                    'transport_document_type_code': transport_document_type_code,
                    'number_of_originals': number_of_originals,
                    'carrier_booking_reference': carrier_booking_reference,
                    'is_electronic': is_electronic,
                    'number_of_copies': number_of_copies,
                    'is_shipped_onboard_type': is_shipped_onboard_type,
                    'is_charges_displayed': is_charges_displayed,
                    'location_name': location_name,
                    'city_name': city_name,
                    'un_location_code': un_location_code,
                    'state_region': state_region,
                    'country': country,
                    'shipping_instruction_ID': shipping_instruction_ID,
                    'transport_document_reference': transport_document_reference,
                    'reciept_or_deliverytype_at_origin': reciept_or_deliverytype_at_origin,
                    'reciept_or_deliverytype_at_dest': reciept_or_deliverytype_at_dest,
                    'shipped_onboard_date': shipped_onboard_date,
                    'issue_date': issue_date,
                    'cargo_movement_type_at_origin': cargo_movement_type_at_origin,
                    'cargo_movement_type_at_dest': cargo_movement_type_at_dest,
                    'terms_and_conditions': terms_and_conditions,
                    'received_for_shipment_date': received_for_shipment_date,
                    'declared_value': declared_value,
                    'service_contract_reference': service_contract_reference,
                    'declared_value_currency': declared_value_currency,
                    'issuer_code': issuer_code,
                    'issuer_code_list_provider': issuer_code_list_provider,
                    'no_of_rider_pages': no_of_rider_pages,
                    'planned_arrival_date': planned_arrival_date,
                    'planned_departure_date': planned_departure_date,
                    'document_hash': document_hash,
                    'pre_carried_by': pre_carried_by,

                    'poi_location_name': poi_location_name,
                    'poi_post_code': poi_post_code,
                    'poi_un_location_code': poi_un_location_code,
                    'poi_city_name': poi_city_name,
                    'poi_street_name': poi_street_name,
                    'poi_state_region': poi_state_region,
                    'poi_street_number': poi_street_number,
                    'poi_country': poi_country,
                    'poi_floor': poi_floor,
                    'por_location_name': por_location_name,
                    'por_post_code': por_post_code,
                    'por_un_location_code': por_un_location_code,
                    'por_city_name': por_city_name,
                    'por_street_name': por_street_name,
                    'por_state_region': por_state_region,
                    'por_street_number': por_street_number,
                    'por_country': por_country,
                    'por_floor': por_floor,
                    'pol_location_name': pol_location_name,
                    'pol_un_location_code': pol_un_location_code,
                    'pol_city_name': pol_city_name,
                    'pol_state_region': pol_state_region,
                    'pol_country': pol_country,
                    'pod_location_name': pod_location_name,
                    'pod_un_location_code': pod_un_location_code,
                    'pod_city_name': pod_city_name,
                    'pod_state_region': pod_state_region,
                    'pod_country': pod_country,
                    'plod_location_name': plod_location_name,
                    'plod_post_code': plod_post_code,
                    'plod_un_location_code': plod_un_location_code,
                    'plod_city_name': plod_city_name,
                    'plod_street_name': plod_street_name,
                    'plod_state_region': plod_state_region,
                    'plod_street_number': plod_street_number,
                    'plod_country': plod_country,
                    'plod_floor': plod_floor,
                    'oir_location_name': oir_location_name,
                    'oir_post_code': oir_post_code,
                    'oir_un_location_code': oir_un_location_code,
                    'oir_city_name': oir_city_name,
                    'oir_street_name': oir_street_name,
                    'oir_state_region': oir_state_region,
                    'oir_street_number': oir_street_number,
                    'oir_country': oir_country,
                    'oir_floor': oir_floor,
                    'pre_location_name': pre_location_name,
                    'pre_post_code': pre_post_code,
                    'pre_latitude': pre_latitude,
                    'pre_longitude': pre_longitude,
                    'pre_un_location_code': pre_un_location_code,
                    'pre_city_name': pre_city_name,
                    'pre_street_name': pre_street_name,
                    'pre_state_region': pre_state_region,
                    'pre_street_number': pre_street_number,
                    'pre_country': pre_country,
                    'pre_floor': pre_floor,

                    'id':bol_id,
                    // 'is_shipper_owned': shipper_owned_tq,
                    // 'is_electronic': is_electronic_val,
                    
                });
                console.log('-------------------------- list',parent_vals)                

                rpc.query({
                    route: '/bol_vals',
                    params: {
                        parent_vals: parent_vals,
                    }
                }).then(function (res) {
                    console.log('-------------------------- call my start',res)
                });

            });
        return res;
    });
}

});
// publicWidget.registry.WebsiteBOLInstance = publicWidget.Widget.extend({
//     selector: '#bol_view_form',

//     /**
//      * @override
//      */
//     start: function () {
//         var def = this._super.apply(this, arguments);
//         this.instance = new WebsiteBOL(this);
//         return Promise.all([def, this.instance.attachTo(this.$el)]);
//     },
//     /**
//      * @override
//      */
//     destroy: function () {
//         this.instance.setElement(null);
//         this._super.apply(this, arguments);
//         this.instance.setElement(this.$el);
//     },
// });
return WebsiteBOL;
});
