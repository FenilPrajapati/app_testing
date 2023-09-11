odoo.define('freightbox.track_trace', function (require) {
'use strict';
console.log(">>>>> TNT STANDALONE JS")
var publicWidget = require('web.public.widget');
const Dialog = require('web.Dialog');
const { qweb, _t } = require('web.core')
publicWidget.registry.websiteTrackTrace = publicWidget.Widget.extend({
    selector: '.track_trace_btn',
    events: {
          'click': '_onclick_track_trace',
    },

    /**
     * @override
     */
    start: function () {
        var self = this;
    },

    _click_track_trace: function () {
        console.log(">>>>> TNT STANDALONE TRACK METHOD CALL.")
        var self = this;
        var carrier_booking_ref = document.getElementById("carrier_booking_reference_tnt").value;
        var transport_document_reference = document.getElementById("transport_document_reference_tnt").value;
        var container_id = document.getElementById("container_id_tnt").value;
        if (transport_document_reference == ""){
            transport_document_reference = null;
        } else {
            transport_document_reference = transport_document_reference;
        }
        if (container_id == ""){
            container_id = null;
        } else {
            container_id = container_id;
        }
        if (carrier_booking_ref == ""){
            carrier_booking_ref = null;
        } else {
            carrier_booking_ref = carrier_booking_ref;
        }
        console.log("carrier_booking_ref : "+ carrier_booking_ref);
        console.log("container_id : "+ container_id);
        console.log("transport_document_reference : "+ transport_document_reference);
        if (carrier_booking_ref == null && transport_document_reference == null && container_id == null) {
//            window.alert("Provide Carrier Booking Reference To Proceed.");
//            document.getElementById("carrier_booking_reference_tnt").focus();
//            document.getElementById("carrier_booking_reference_div").innerHTML = "Please fill this field";
//            document.getElementById("carrier_booking_reference_div").style.color="Red";
            document.getElementById("not_cb_warning").innerHTML = "Provide Carrier Booking ef., B/L Ref. or Container ID(s) to track shipment.";
            document.getElementById("not_cb_warning").style.color = "red";
            document.getElementById("carrier_booking_reference_tnt").focus();
            return;
        } else {
            console.log("------------------ standalone_list_of_container Call 0----------------")
            var url = "/standalone_list_of_containers/" + carrier_booking_ref + "/tdr/" + transport_document_reference + "/container/" + container_id;
            window.location.href = url;

        }
    },
    _onclick_track_trace: function (ev) {
        this._click_track_trace();
    },
});

publicWidget.registry.updateDestnationEta = publicWidget.Widget.extend({
    selector: '.update_destination_eta',
    events: {
          'click': '_onclick_update_destination_eta',
    },

    /**
     * @override
     */
    start: function () {
        var self = this;
    },

    _click_destination_eta: function () {
        var self = this;
        var rpc = require('web.rpc');
        var datetime_eta_elements = document.getElementsByClassName('destination_eta');
        console.log('>>>>>>datetime_eta_elements : ',datetime_eta_elements)
        for (var i=0; i<datetime_eta_elements.length; i++) {
            console.log(">> Index : ",i)
            console.log(">> Container ID : ",datetime_eta_elements[i].name)
            console.log(">> Destination ETA : ",datetime_eta_elements[i].value)

            rpc.query({
                model: 'track.trace.event',
                method: 'update_estination_eta',
                args: [null, datetime_eta_elements[i].name, datetime_eta_elements[i].value],
            }).then(function (result) {
                console.log(result);
            });
        }
        var warning_field = document.getElementById("not_cb_warning")
        warning_field.innerHTML = "Update Destination ETA process completed.";
        warning_field.style.color = "green";
    },
    _onclick_update_destination_eta: function (ev) {
        this._click_destination_eta();
    },
});
});