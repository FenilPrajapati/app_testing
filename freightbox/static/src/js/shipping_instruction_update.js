odoo.define('freightbox.shipping_instruction_update', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
var core = require('web.core');
var Widget = require('web.Widget');
var publicWidget = require('web.public.widget');
var rpc = require('web.rpc');

    const Dialog = require('web.Dialog');
    const { qweb, _t } = require('web.core');

var WebsiteShippingInstructionsUpdate = Widget.extend({
    xmlDependencies: ['/freightbox/static/src/xml/SiUpdatePopup.xml'],

    start: function () {
        var self = this;
        var res = this._super.apply(this.arguments).then(function () {

          // Edit/View added  Popup of References
            $('#rc_update_tbody').on('click', '.edit_rc_view', function () {
                var child = $(this).closest('tr');
                child.each(function () {
                    var id = $(this).attr('id');
                    var dialog = new Dialog(this, {
                        title: _t("Edit Shipping Instruction - References"),
                        $content: $(qweb.render('freightbox.update_added_rc_popup')),
                            buttons: [{
                                text: _t('Edit'),
                                classes: "btn-primary",
                                close: false,
                                click: function () {
                                    var reference_type = document.getElementById("reference_type_rc_form").value;
                                    document.getElementById("new_reference_type_update_rc_"+id).value = reference_type;

                                    var reference_value = document.getElementById("reference_value_rc_form").value;
                                    document.getElementById("new_reference_value_update_rc_"+id).value = reference_value;

                                    var rc_created_by = document.getElementById("ref_array_created_by_form").value
                                    document.getElementById("ref_array_created_by_"+id).value = rc_created_by;

                                    var update_edit_formrc = document.getElementById('update_edit_formrc');
                                    for(var i=0; i < update_edit_formrc.elements.length; i++){
                                        if(update_edit_formrc.elements[i].value === '' && update_edit_formrc.elements[i].hasAttribute('required')){
                                            if (reference_type == ""){
                                                 document.getElementById("reference_type_rc_form").focus();
                                                 document.getElementById("ref_type_div").innerHTML = "Please fill this field";
                                                 document.getElementById("ref_type_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("ref_type_div").innerHTML = "";
                                            }

                                            if (reference_value == "") {
                                                document.getElementById("reference_value_rc_form").focus();
                                                 document.getElementById("ref_value_div").innerHTML = "Please fill this field";
                                                 document.getElementById("ref_value_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("ref_value_div").innerHTML = "";
                                            }
                                            if (rc_created_by == "") {
                                                document.getElementById("ref_array_created_by_form").focus();
                                                 document.getElementById("ref_array_created_div").innerHTML = "Please fill this field";
                                                 document.getElementById("ref_array_created_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("ref_array_created_div").innerHTML = "";
                                            }
                                        }
                                    }
                                    dialog.close();

                                }
                            }],
                    });
                    dialog.opened().then(function () {

                    var update_edit_formrc = document.getElementById('update_edit_formrc');
                    for(var i=0; i < update_edit_formrc.elements.length; i++){
                        if(update_edit_formrc.elements[i].hasAttribute('required')){
                            update_edit_formrc.elements[i].style.background='#ADD8E6';
                        }
                    }
                         //   var view_row_count = document.getElementById("row_count").innerHTML;
                            var reference_type = document.getElementById("new_reference_type_update_rc_"+id).value;
                            document.getElementById("reference_type_rc_form").value = reference_type;

                            var reference_value = document.getElementById("new_reference_value_update_rc_"+id).value;
                            document.getElementById("reference_value_rc_form").value = reference_value;

                            var rc_created_by = document.getElementById("ref_array_created_by_"+id).value;
                            document.getElementById("ref_array_created_by_form").value = rc_created_by;

                    });
                    dialog.open();
                    //  self.on_click_view_references();
                });

            }),

         // Edit/View addded - SL Popup
             $('#sl_update_tbody').on('click', '.edit_update_sl', function () {
                var child = $(this).closest('tr');
                child.each(function () {
                    var id = $(this).attr('id');
                    var dialog = new Dialog(this, {
                        title: _t("Shipping Instruction - Edit Shipment Locations"),
                        $content: $(qweb.render('freightbox.update_edit_added_sl_popup')),
                            buttons: [{
                                text: _t('Edit'),
                                classes: "btn-primary",
                                close: false,
                                click: function () {

                                    var location_type = document.getElementById("location_type_form").value;
                                    document.getElementById("new_location_type_update_sl_"+id).value = location_type;

                                    var location_name = document.getElementById("location_name_form").value;
                                    document.getElementById("new_location_name_update_sl_"+id).value = location_name;

                                    var latitude = document.getElementById("latitude_form").value;
                                    document.getElementById("new_latitude_update_sl_"+id).value = latitude;

                                    var longitude = document.getElementById("longitude_form").value;
                                    document.getElementById("new_longitude_update_sl_"+id).value = longitude;

                                    var un_location_code = document.getElementById("un_location_code_form").value;
                                    document.getElementById("new_un_location_code_update_sl_"+id).value = un_location_code;

                                    var street_name = document.getElementById("street_name_form").value;
                                    document.getElementById("new_street_name_code_update_sl_"+id).value = street_name;

                                    var street_number = document.getElementById("street_number_form").value;
                                    document.getElementById("new_street_number_code_update_sl_"+id).value = street_number;

                                    var floor = document.getElementById("floor_form").value;
                                    document.getElementById("new_floor_update_sl_"+id).value = floor;

                                    var post_code = document.getElementById("post_code_form").value;
                                    document.getElementById("new_post_code_update_sl_"+id).value = post_code;

                                    var city_name = document.getElementById("city_name_form").value;
                                    document.getElementById("new_city_name_update_sl_"+id).value = city_name;

                                    var state_region = document.getElementById("state_region_form").value;
                                    document.getElementById("new_state_region_update_sl_"+id).value = state_region;

                                    var country = document.getElementById("country_form").value;
                                    document.getElementById("new_country_update_sl_"+id).value = country;

                                    var displayed_name = document.getElementById("displayed_name_form").value;
                                    document.getElementById("new_displayed_name_update_sl_"+id).value = displayed_name;

                                    var sl_created_by = document.getElementById("sl_array_created_by_form").value;
                                    document.getElementById("sl_array_created_by_"+id).value = sl_created_by;


                                    var edit_formsl = document.getElementById('edit_formsl');
                                    for(var i=0; i < edit_formsl.elements.length; i++){
                                        if(edit_formsl.elements[i].value === '' && edit_formsl.elements[i].hasAttribute('required')){
                                            if (location_type == ""){
                                                 document.getElementById("location_type_form").focus();
                                                 document.getElementById("loc_type_div").innerHTML = "Please fill this field";
                                                 document.getElementById("loc_type_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("loc_type_div").innerHTML = "";
                                            }
                                            if (location_name == ""){
                                                if (location_type === "POL" || location_type === "POD"){
                                                 document.getElementById("location_name_form").focus();
                                                 document.getElementById("loc_div").innerHTML = "Please fill this field";
                                                 document.getElementById("loc_div").style.color="Red";
                                                return;
                                                }
                                            } else {
                                                document.getElementById("loc_div").innerHTML = "";
                                            }
                                            if (latitude == ""){
                                                if (location_type === "POL" || location_type === "POD"){
                                                 document.getElementById("latitude_form").focus();
                                                 document.getElementById("lat_div").innerHTML = "Please fill this field";
                                                 document.getElementById("lat_div").style.color="Red";
                                                 return;
                                                 }
                                            } else {
                                                document.getElementById("lat_div").innerHTML = "";
                                            }
                                            if (longitude == ""){
                                                if (location_type === "POL" || location_type === "POD"){
                                                 document.getElementById("longitude_form").focus();
                                                 document.getElementById("long_div").innerHTML = "Please fill this field";
                                                 document.getElementById("long_div").style.color="Red";
                                                 return;
                                                 }
                                            } else {
                                                document.getElementById("long_div").innerHTML = "";
                                            }
                                            if (un_location_code == ""){
                                            if (location_type === "POL" || location_type === "POD"){
                                                 document.getElementById("un_location_code_form").focus();
                                                 document.getElementById("un_loc_code_div").innerHTML = "Please fill this field";
                                                 document.getElementById("un_loc_code_div").style.color="Red";
                                                 return;
                                                 }
                                            } else {
                                                document.getElementById("un_loc_code_div").innerHTML = "";
                                            }
                                            if (street_name == ""){
                                                if (location_type === "POL" || location_type === "POD"){
                                                 document.getElementById("street_name_form").focus();
                                                 document.getElementById("st_name_div").innerHTML = "Please fill this field";
                                                 document.getElementById("st_name_div").style.color="Red";
                                                 return;
                                                 }
                                            } else {
                                                document.getElementById("st_name_div").innerHTML = "";
                                            }
                                            if (street_number == ""){
                                                if (location_type === "POL" || location_type === "POD"){
                                                 document.getElementById("street_number_form").focus();
                                                 document.getElementById("st_no_div").innerHTML = "Please fill this field";
                                                 document.getElementById("st_no_div").style.color="Red";
                                                 return;
                                                 }
                                            } else {
                                                document.getElementById("st_no_div").innerHTML = "";
                                            }
                                            if (floor == ""){
                                                if (location_type === "POL" || location_type === "POD"){
                                                 document.getElementById("floor_form").focus();
                                                 document.getElementById("floor_div").innerHTML = "Please fill this field";
                                                 document.getElementById("floor_div").style.color="Red";
                                                 return;
                                                 }
                                            } else {
                                                document.getElementById("floor_div").innerHTML = "";
                                            }
                                            if (post_code == ""){
                                                if (location_type === "POL" || location_type === "POD"){
                                                 document.getElementById("post_code_form").focus();
                                                 document.getElementById("post_code_div").innerHTML = "Please fill this field";
                                                 document.getElementById("post_code_div").style.color="Red";
                                                 return;
                                                 }
                                            } else {
                                                document.getElementById("post_code_div").innerHTML = "";
                                            }
                                            if (city_name == ""){
                                                if (location_type === "POL" || location_type === "POD"){
                                                 document.getElementById("city_name_form").focus();
                                                 document.getElementById("city_div").innerHTML = "Please fill this field";
                                                 document.getElementById("city_div").style.color="Red";
                                                 return;
                                                 }
                                            } else {
                                                document.getElementById("city_div").innerHTML = "";
                                            }
                                            if (state_region == ""){
                                                if (location_type === "POL" || location_type === "POD"){
                                                 document.getElementById("state_region_form").focus();
                                                 document.getElementById("st_reg_div").innerHTML = "Please fill this field";
                                                 document.getElementById("st_reg_div").style.color="Red";
                                                 return;
                                                 }
                                            } else {
                                                document.getElementById("st_reg_div").innerHTML = "";
                                            }
                                            if (country == ""){
                                                if (location_type === "POL" || location_type === "POD"){
                                                document.getElementById("country_form").focus();
                                                 document.getElementById("country_div").innerHTML = "Please fill this field";
                                                 document.getElementById("country_div").style.color="Red";
                                                 return;
                                                 }
                                            } else {
                                                document.getElementById("country_div").innerHTML = "";
                                            }
                                            if (sl_created_by == ""){
                                                document.getElementById("sl_array_created_by_form").focus();
                                                 document.getElementById("sl_array_created_by").innerHTML = "Please fill this field";
                                                 document.getElementById("sl_array_created_by").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("sl_array_created_by").innerHTML = "";
                                            }
                                        }
                                    }
                                    if (location_type === "PRE" ||
                                        location_type === "POL" ||
                                        location_type === "POD" ||
                                        location_type === "PDE" ||
                                        location_type === "PCF" ||
                                        location_type === "OIR" ||
                                        location_type === "PSR") {
                                             document.getElementById("loc_type_div").innerHTML = "";
                                        } else {
                                            document.getElementById("location_type_form").value = "";
                                             document.getElementById("location_type_form").focus();
                                             document.getElementById("loc_type_div").innerHTML = "Please double click and select any from dropdown";
                                             document.getElementById("loc_type_div").style.color="Red";
                                             return;
                                        }
                                    dialog.close();


                                }
                            }],
                    });
                    dialog.opened().then(function () {

                    var edit_formsl = document.getElementById('edit_formsl');
                    for(var i=0; i < edit_formsl.elements.length; i++){
                        if(edit_formsl.elements[i].hasAttribute('required')){
                            edit_formsl.elements[i].style.background='#ADD8E6';
                        }
                    }


                     $("#location_type_form").on('change', function() {
                                var loc_type = document.getElementById("location_type_form").value;
                                            if (loc_type == "Place of Receipt (PRE)") {
                                                document.getElementById("location_type_form").value = "PRE";
                                                document.getElementById("location_name_form").style.background='#FFFFFF';
                                                document.getElementById("latitude_form").style.background='#FFFFFF';
                                                document.getElementById("longitude_form").style.background='#FFFFFF';
                                                document.getElementById("un_location_code_form").style.background='#FFFFFF';
                                                document.getElementById("street_name_form").style.background='#FFFFFF';
                                                document.getElementById("street_number_form").style.background='#FFFFFF';
                                                document.getElementById("floor_form").style.background='#FFFFFF';
                                                document.getElementById("post_code_form").style.background='#FFFFFF';
                                                document.getElementById("city_name_form").style.background='#FFFFFF';
                                                document.getElementById("state_region_form").style.background='#FFFFFF';
                                                document.getElementById("country_form").style.background='#FFFFFF';
                                            }
                                            if (loc_type == "Port of Loading (POL)") {
                                                document.getElementById("location_type_form").value = "POL";
                                                document.getElementById("location_name_form").style.background='#ADD8E6';
                                                 $("#location_name_form").attr('required',"required");
                                                document.getElementById("latitude_form").style.background='#ADD8E6';
                                                $("#latitude_form").attr('required',"required");
                                                document.getElementById("longitude_form").style.background='#ADD8E6';
                                                $("#longitude_form").attr('required',"required");
                                                document.getElementById("un_location_code_form").style.background='#ADD8E6';
                                                $("#un_location_code_form").attr('required',"required");
                                                document.getElementById("street_name_form").style.background='#ADD8E6';
                                                $("#street_name_form").attr('required',"required");
                                                document.getElementById("street_number_form").style.background='#ADD8E6';
                                                $("#street_number_form").attr('required',"required");
                                                document.getElementById("floor_form").style.background='#ADD8E6';
                                                $("#floor_form").attr('required',"required");
                                                document.getElementById("post_code_form").style.background='#ADD8E6';
                                                $("#post_code_form").attr('required',"required");
                                                document.getElementById("city_name_form").style.background='#ADD8E6';
                                                $("#city_name_form").attr('required',"required");
                                                document.getElementById("state_region_form").style.background='#ADD8E6';
                                                $("#state_region_form").attr('required',"required");
                                                document.getElementById("country_form").style.background='#ADD8E6';
                                                $("#country_form").attr('required',"required");
                                            }
                                            if (loc_type == "Port of Discharge (POD)") {
                                                document.getElementById("location_type_form").value = "POD";
                                                 document.getElementById("location_name_form").style.background='#ADD8E6';
                                                 $("#location_name_form").attr('required',"required");
                                                document.getElementById("latitude_form").style.background='#ADD8E6';
                                                $("#latitude_form").attr('required',"required");
                                                document.getElementById("longitude_form").style.background='#ADD8E6';
                                                $("#longitude_form").attr('required',"required");
                                                document.getElementById("un_location_code_form").style.background='#ADD8E6';
                                                $("#un_location_code_form").attr('required',"required");
                                                document.getElementById("street_name_form").style.background='#ADD8E6';
                                                $("#street_name_form").attr('required',"required");
                                                document.getElementById("street_number_form").style.background='#ADD8E6';
                                                $("#street_number_form").attr('required',"required");
                                                document.getElementById("floor_form").style.background='#ADD8E6';
                                                $("#floor_form").attr('required',"required");
                                                document.getElementById("post_code_form").style.background='#ADD8E6';
                                                $("#post_code_form").attr('required',"required");
                                                document.getElementById("city_name_form").style.background='#ADD8E6';
                                                $("#city_name_form").attr('required',"required");
                                                document.getElementById("state_region_form").style.background='#ADD8E6';
                                                $("#state_region_form").attr('required',"required");
                                                document.getElementById("country_form").style.background='#ADD8E6';
                                                $("#country_form").attr('required',"required");
                                            }
                                            if (loc_type == "Place of Delivery (PDE)") {
                                                document.getElementById("location_type_form").value = "PDE";
                                                document.getElementById("location_name_form").style.background='#FFFFFF';
                                                document.getElementById("latitude_form").style.background='#FFFFFF';
                                                document.getElementById("longitude_form").style.background='#FFFFFF';
                                                document.getElementById("un_location_code_form").style.background='#FFFFFF';
                                                document.getElementById("street_name_form").style.background='#FFFFFF';
                                                document.getElementById("street_number_form").style.background='#FFFFFF';
                                                document.getElementById("floor_form").style.background='#FFFFFF';
                                                document.getElementById("post_code_form").style.background='#FFFFFF';
                                                document.getElementById("city_name_form").style.background='#FFFFFF';
                                                document.getElementById("state_region_form").style.background='#FFFFFF';
                                                document.getElementById("country_form").style.background='#FFFFFF';
                                            }
                                            if (loc_type == "Pre-carriage from (PCF)") {
                                                document.getElementById("location_type_form").value = "PCF";
                                                document.getElementById("location_name_form").style.background='#FFFFFF';
                                                document.getElementById("latitude_form").style.background='#FFFFFF';
                                                document.getElementById("longitude_form").style.background='#FFFFFF';
                                                document.getElementById("un_location_code_form").style.background='#FFFFFF';
                                                document.getElementById("street_name_form").style.background='#FFFFFF';
                                                document.getElementById("street_number_form").style.background='#FFFFFF';
                                                document.getElementById("floor_form").style.background='#FFFFFF';
                                                document.getElementById("post_code_form").style.background='#FFFFFF';
                                                document.getElementById("city_name_form").style.background='#FFFFFF';
                                                document.getElementById("state_region_form").style.background='#FFFFFF';
                                                document.getElementById("country_form").style.background='#FFFFFF';
                                            }
                                            if (loc_type == "Onward Inland Routing (OIR)"){
                                                document.getElementById("location_type_form").value = "OIR";
                                                document.getElementById("location_name_form").style.background='#FFFFFF';
                                                document.getElementById("latitude_form").style.background='#FFFFFF';
                                                document.getElementById("longitude_form").style.background='#FFFFFF';
                                                document.getElementById("un_location_code_form").style.background='#FFFFFF';
                                                document.getElementById("street_name_form").style.background='#FFFFFF';
                                                document.getElementById("street_number_form").style.background='#FFFFFF';
                                                document.getElementById("floor_form").style.background='#FFFFFF';
                                                document.getElementById("post_code_form").style.background='#FFFFFF';
                                                document.getElementById("city_name_form").style.background='#FFFFFF';
                                                document.getElementById("state_region_form").style.background='#FFFFFF';
                                                document.getElementById("country_form").style.background='#FFFFFF';
                                            }
            });
                            //   var view_row_count = document.getElementById("row_count").innerHTML;

                            var location_type = document.getElementById("new_location_type_update_sl_"+id).value;
                            document.getElementById("location_type_form").value = location_type;

                            var location_name = document.getElementById("new_location_name_update_sl_"+id).value;
                            document.getElementById("location_name_form").value = location_name;

                            var latitude = document.getElementById("new_latitude_update_sl_"+id).value;
                            document.getElementById("latitude_form").value = latitude;

                            var longitude = document.getElementById("new_longitude_update_sl_"+id).value;
                            document.getElementById("longitude_form").value = longitude;

                            var un_location_code = document.getElementById("new_un_location_code_update_sl_"+id).value;
                            document.getElementById("un_location_code_form").value = un_location_code;

                            var street_name = document.getElementById("new_street_name_code_update_sl_"+id).value;
                            document.getElementById("street_name_form").value = street_name;

                            var street_number = document.getElementById("new_street_number_code_update_sl_"+id).value;
                            document.getElementById("street_number_form").value = street_number;

                            var floor = document.getElementById("new_floor_update_sl_"+id).value;
                            document.getElementById("floor_form").value = floor;

                            var post_code = document.getElementById("new_post_code_update_sl_"+id).value;
                            document.getElementById("post_code_form").value = post_code;

                            var city_name = document.getElementById("new_city_name_update_sl_"+id).value;
                            document.getElementById("city_name_form").value = city_name;

                            var state_region = document.getElementById("new_state_region_update_sl_"+id).value;
                            document.getElementById("state_region_form").value = state_region;

                            var country = document.getElementById("new_country_update_sl_"+id).value;
                            document.getElementById("country_form").value = country;

                            var displayed_name = document.getElementById("new_displayed_name_update_sl_"+id).value;
                            document.getElementById("displayed_name_form").value = displayed_name;

                            var sl_created_by = document.getElementById("sl_array_created_by_"+id).value;
                            document.getElementById("sl_array_created_by_form").value = sl_created_by;

                    });
                    dialog.open();
                    //  self.on_click_view_shipment_location();
                });

            }),


        // Edit/View Added DP Popup
             $('#dp_update_tbody').on('click', '.update_edit_dp', function () {
                var child = $(this).closest('tr');
                child.each(function () {
                    var id = $(this).attr('id');
                    var dialog = new Dialog(this, {
                        title: _t("Shipping Instruction - Edit Document View"),
                        $content: $(qweb.render('freightbox.update_added_dp_popup')),
                            buttons: [{
                                text: _t('Edit'),
                                classes: "btn-primary",
                                close: false,
                                click: function () {
                                    var party_name = document.getElementById("party_name_dp_form").value;
                                    document.getElementById("new_party_name_update_dp_"+id).value = party_name;

                                    var tax_reference_1 = document.getElementById("tax_reference_1_dp_form").value;
                                    document.getElementById("new_tax_reference_1_update_dp_"+id).value = tax_reference_1;

                                    var public_key = document.getElementById("public_key_form").value;
                                    document.getElementById("new_public_key_update_dp_"+id).value = public_key;

                                    var street = document.getElementById("street_form").value;
                                    document.getElementById("new_street_update_dp_"+id).value = street;

                                    var street_number = document.getElementById("street_number_form").value;
                                    document.getElementById("new_street_number_update_dp_"+id).value = street_number;

                                    var floor = document.getElementById("floor_form").value;
                                    document.getElementById("new_floor_update_dp_"+id).value = floor;

                                    var post_code = document.getElementById("post_code_form").value;
                                     document.getElementById("new_post_code_update_dp_"+id).value = post_code;

                                    var city = document.getElementById("city_form").value;
                                    document.getElementById("new_city_update_dp_"+id).value = city;

                                    var state_region = document.getElementById("state_region_form").value;
                                    document.getElementById("new_state_region_update_dp_"+id).value = state_region;

                                    var country = document.getElementById("country_form").value;
                                    document.getElementById("new_country_update_dp_"+id).value = country;

                                    var tax_reference_2 = document.getElementById("tax_reference_2_form").value;
                                     document.getElementById("new_tax_reference_2_update_dp_"+id).value = tax_reference_2;

                                    var nmfta_code = document.getElementById("nmfta_code_form").value;
                                    document.getElementById("new_nmfta_code_update_dp_"+id).value = nmfta_code;

                                    var party_function = document.getElementById("party_function_form").value;
                                    document.getElementById("new_party_function_update_dp_"+id).value = party_function;

                                    var address_line = document.getElementById("address_line_form").value;
                                    document.getElementById("new_address_line_update_dp_"+id).value = address_line;

                                    var name = document.getElementById("name_form").value;
                                    document.getElementById("new_name_update_dp_"+id).value = name;

                                    var email = document.getElementById("email_form").value;
                                    document.getElementById("new_email_update_dp_"+id).value = email;

                                    var phone = document.getElementById("phone_form").value;
                                    document.getElementById("new_phone_update_dp_"+id).value = phone;

                                    var dp_modified_by = document.getElementById("dp_array_created_by_form").value;
                                    document.getElementById("dp_array_created_by_"+id).value = dp_modified_by;

                                    var is_to_be_notified = document.getElementById("is_to_be_notified_form");
                                    if(is_to_be_notified.checked == true){
                                        document.getElementById("new_is_to_be_notified_update_dp_"+id).checked = true;
                                    } else {
                                        document.getElementById("new_is_to_be_notified_update_dp_"+id).checked = false;
                                    }

                                    var update_formdp = document.getElementById('update_formdp');
                                    for(var i=0; i < update_formdp.elements.length; i++){
                                        if(update_formdp.elements[i].value === '' && update_formdp.elements[i].hasAttribute('required')){
                                            if (party_name == ""){
                                                 document.getElementById("party_name_dp_form").focus();
                                                 document.getElementById("party_name_div").innerHTML = "Please fill this field";
                                                 document.getElementById("party_name_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("party_name_div").innerHTML = "";
                                            }
                                            if (tax_reference_1 == ""){
                                                 document.getElementById("tax_reference_1_dp_form").focus();
                                                 document.getElementById("tax_reference_1_div").innerHTML = "Please fill this field";
                                                 document.getElementById("tax_reference_1_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("tax_reference_1_div").innerHTML = "";
                                            }
                                            if (public_key == ""){
                                                 document.getElementById("public_key_form").focus();
                                                 document.getElementById("public_key_div").innerHTML = "Please fill this field";
                                                 document.getElementById("public_key_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("public_key_div").innerHTML = "";
                                            }
                                            if (street == ""){
                                                 document.getElementById("street_form").focus();
                                                 document.getElementById("street_div").innerHTML = "Please fill this field";
                                                 document.getElementById("street_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("street_div").innerHTML = "";
                                            }
                                            if (street_number == ""){
                                                 document.getElementById("street_number_form").focus();
                                                 document.getElementById("street_no_div").innerHTML = "Please fill this field";
                                                 document.getElementById("street_no_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("street_no_div").innerHTML = "";
                                            }
                                            if (floor == ""){
                                                 document.getElementById("floor_form").focus();
                                                 document.getElementById("floor_div").innerHTML = "Please fill this field";
                                                 document.getElementById("floor_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("floor_div").innerHTML = "";
                                            }
                                            if (post_code == ""){
                                                 document.getElementById("post_code_form").focus();
                                                 document.getElementById("post_code_div").innerHTML = "Please fill this field";
                                                 document.getElementById("post_code_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("post_code_div").innerHTML = "";
                                            }
                                            if (city == ""){
                                                 document.getElementById("city_form").focus();
                                                 document.getElementById("city_div").innerHTML = "Please fill this field";
                                                 document.getElementById("city_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("city_div").innerHTML = "";
                                            }
                                            if (state_region == ""){
                                                 document.getElementById("state_region_form").focus();
                                                 document.getElementById("state_region_div").innerHTML = "Please fill this field";
                                                 document.getElementById("state_region_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("state_region_div").innerHTML = "";
                                            }
                                            if (country == ""){
                                                 document.getElementById("country_form").focus();
                                                 document.getElementById("country_div").innerHTML = "Please fill this field";
                                                 document.getElementById("country_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("country_div").innerHTML = "";
                                            }
                                            if (tax_reference_2 == ""){
                                                 document.getElementById("tax_reference_2_form").focus();
                                                 document.getElementById("tax_ref_2_div").innerHTML = "Please fill this field";
                                                 document.getElementById("tax_ref_2_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("tax_ref_2_div").innerHTML = "";
                                            }
                                            if (nmfta_code == ""){
                                                 document.getElementById("nmfta_code_form").focus();
                                                 document.getElementById("nmfta_code_div").innerHTML = "Please fill this field";
                                                 document.getElementById("nmfta_code_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("nmfta_code_div").innerHTML = "";
                                            }
                                            if (party_function == ""){
                                                 document.getElementById("party_function_form").focus();
                                                 document.getElementById("party_fn_div").innerHTML = "Please fill this field";
                                                 document.getElementById("party_fn_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("party_fn_div").innerHTML = "";
                                            }
                                            if (name == ""){
                                                 document.getElementById("name_form").focus();
                                                 document.getElementById("name_div").innerHTML = "Please fill this field";
                                                 document.getElementById("name_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("name_div").innerHTML = "";
                                            }
                                            if (phone == ""){
                                                 document.getElementById("phone_form").focus();
                                                 document.getElementById("phone_div").innerHTML = "Please fill this field";
                                                 document.getElementById("phone_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("phone_div").innerHTML = "";
                                            }
                                            if (email == ""){
                                                 document.getElementById("email_form").focus();
                                                 document.getElementById("email_div").innerHTML = "Please fill this field";
                                                 document.getElementById("email_div").style.color="Red";
                                                 return;
                                            } else {

                                                document.getElementById("email_div").innerHTML = "";
                                            }
                                            if (dp_modified_by == ""){
                                                 document.getElementById("dp_array_created_by_form").focus();
                                                 document.getElementById("dp_array_created_by_div").innerHTML = "Please fill this field";
                                                 document.getElementById("dp_array_created_by_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("dp_array_created_by_div").innerHTML = "";
                                            }

                                        }
                                    }
                                    if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email))
                                      {
                                        document.getElementById("email_div").innerHTML = "";
                                      }
                                      else {
                                        document.getElementById("email_form").focus();
                                        document.getElementById("email_div").innerHTML = "Please Enter a valid email";
                                        document.getElementById("email_div").style.color="Red";
                                        return;
                                      }

                                    /*  var re = /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/im;
                         if (re.test(phone) == true){
                             document.getElementById("phone_div").innerHTML = "";
                         } else {
                             document.getElementById("phone_form").focus();
                             document.getElementById("phone_div").innerHTML = "Please fill this field";
                             document.getElementById("phone_div").style.color="Red";
                             return;
                         }

*/
                       /* var is_to_be_notified = document.getElementById("is_to_be_notified_form");
                                    if(is_to_be_notified.checked != true){
                                        is_to_be_notified.checked = true;
                                    }*/

                                    dialog.close();

                                }
                            }],
                    });
                    dialog.opened().then(function () {

                        var update_formdp = document.getElementById('update_formdp');
                        for(var i=0; i < update_formdp.elements.length; i++){
                            if(update_formdp.elements[i].hasAttribute('required')){
                                update_formdp.elements[i].style.background='#ADD8E6';
                            }
                        }

                         //   var view_row_count = document.getElementById("row_count").innerHTML;
                            var party_name = document.getElementById("new_party_name_update_dp_"+id).value;
                            document.getElementById("party_name_dp_form").value = party_name;

                            var tax_reference_1 = document.getElementById("new_tax_reference_1_update_dp_"+id).value;
                            document.getElementById("tax_reference_1_dp_form").value = tax_reference_1;

                            var public_key = document.getElementById("new_public_key_update_dp_"+id).value;
                            document.getElementById("public_key_form").value = public_key;

                            var street = document.getElementById("new_street_update_dp_"+id).value;
                            document.getElementById("street_form").value = street;

                            var street_number = document.getElementById("new_street_number_update_dp_"+id).value;
                            document.getElementById("street_number_form").value = street_number;

                            var floor = document.getElementById("new_floor_update_dp_"+id).value;
                            document.getElementById("floor_form").value = floor;

                            var post_code = document.getElementById("new_post_code_update_dp_"+id).value;
                            document.getElementById("post_code_form").value = post_code;

                            var city = document.getElementById("new_city_update_dp_"+id).value;
                            document.getElementById("city_form").value = city;

                            var state_region = document.getElementById("new_state_region_update_dp_"+id).value;
                            document.getElementById("state_region_form").value = state_region;

                            var country = document.getElementById("new_country_update_dp_"+id).value;
                            document.getElementById("country_form").value = country;

                            var tax_reference_2 = document.getElementById("new_tax_reference_2_update_dp_"+id).value;
                            document.getElementById("tax_reference_2_form").value = tax_reference_2;

                            var nmfta_code = document.getElementById("new_nmfta_code_update_dp_"+id).value;
                            document.getElementById("nmfta_code_form").value = nmfta_code;

                            var party_function = document.getElementById("new_party_function_update_dp_"+id).value;
                            document.getElementById("party_function_form").value = party_function;

                            var address_line = document.getElementById("new_address_line_update_dp_"+id).value;
                            document.getElementById("address_line_form").value = address_line;

                            var name = document.getElementById("new_name_update_dp_"+id).value;
                            document.getElementById("name_form").value = name;

                            var email = document.getElementById("new_email_update_dp_"+id).value;
                            document.getElementById("email_form").value = email;

                            var phone = document.getElementById("new_phone_update_dp_"+id).value;
                            document.getElementById("phone_form").value = phone;

                            var dp_created_by = document.getElementById("dp_array_created_by_"+id).value;
                            document.getElementById("dp_array_created_by_form").value = dp_created_by;

                            var is_to_be_notified = document.getElementById("new_is_to_be_notified_update_dp_"+id);
                            if(is_to_be_notified.checked == true){
                                document.getElementById("is_to_be_notified_form").checked = true;
                            } else {
                                document.getElementById("is_to_be_notified_form").checked = false;
                            }
                    });
                    dialog.open();
                    //  self.on_click_view_document_parties();
                });

            }),

        // Edit/View Transport Equipment Popup
            $('#tq_update_tbody').on('click', '.edit_update_tq', function () {
                var child = $(this).closest('tr');
                child.each(function () {
                    var id = $(this).attr('id');
                    var dialog = new Dialog(this, {
                        title: _t("Shipping Instruction - Edit Transport Equipment"),
                        $content: $(qweb.render('freightbox.edit_transport_eqipment_update_popup')),
                        buttons: [{
                            text: _t('Edit'),
                            classes: "btn-primary",
                            close: false,
                            click: function () {
                                // field 1
                                var equipment_reference_tq = document.getElementById("equipment_reference_tq_form").value;
                                document.getElementById("new_update_eq_id_"+id).value  = equipment_reference_tq;

                                // field 2
                                var weight_unit_tq = document.getElementById("weight_unit_tq_form").value;
                                document.getElementById("new_wt_unit_update_tq_"+id).value  = weight_unit_tq;

                                // field 3
                                var cargo_gross_weight = document.getElementById("cargo_gross_weight_form").value;
                                document.getElementById("new_cgw_update_tq_"+id).value = cargo_gross_weight;

                                // field 4
                                var container_tare_weight = document.getElementById("container_tare_weight_form").value;
                                document.getElementById("new_ctw_update_tq_"+id).value = container_tare_weight;

                                // field 5
                                var iso_equipment_code = document.getElementById("iso_equipment_code_form").value;
                                document.getElementById("new_iso_eq_code_update_tq_"+id).value = iso_equipment_code;

                                // field 6
                                var is_shipper_owned = document.getElementById("is_shipper_owned_form");
                                if(is_shipper_owned.checked == true){
                                    document.getElementById("new_is_shipper_owned_update_tq_"+id).checked = true;
                                } else {
                                    document.getElementById("new_is_shipper_owned_update_tq_"+id).checked = false;
                                }


                                // field 7
                                var temperature_min = document.getElementById("temperature_min_form").value;
                                document.getElementById("new_temp_min_update_tq_"+id).value = temperature_min;

                                // field 8
                                var temperature_max = document.getElementById("temperature_max_form").value;
                                document.getElementById("new_temp_max_update_tq_"+id).value = temperature_max;

                                // field 9
                                var temperature_unit = document.getElementById("temperature_unit_form").value;
                                document.getElementById("new_temp_unit_update_tq_"+id).value = temperature_unit;

                                // field 10
                                var humidity_min = document.getElementById("humidity_min_form").value;
                                document.getElementById("new_humidity_min_update_tq_"+id).value = humidity_min;

                                // field 11
                                var humidity_max = document.getElementById("humidity_max_form").value;
                                document.getElementById("new_humidity_max_update_tq_"+id).value = humidity_max;

                                // field 12
                                var ventilation_min = document.getElementById("ventilation_min_form").value;
                                document.getElementById("new_ventilation_min_update_tq_"+id).value = ventilation_min;

                                // field 13
                                var ventilation_max = document.getElementById("ventilation_max_form").value;
                                document.getElementById("new_ventilation_max_update_tq_"+id).value = ventilation_max;

                                // field 14
                                var seal_number = document.getElementById("seal_number_form").value;
                                document.getElementById("new_seal_no_update_tq_"+id).value = seal_number;

                                // field 15
                                var seal_source = document.getElementById("seal_source_form").value;
                                document.getElementById("new_seal_source_update_tq_"+id).value = seal_source;

                                // field 16
                                var seal_type = document.getElementById("seal_type_form").value;
                                document.getElementById("new_seal_type_update_tq_"+id).value = seal_type;

                                var tq_array_created_by = document.getElementById("tq_array_created_by_form").value;
                                document.getElementById("tq_array_created_by_"+id).value = tq_array_created_by;

                                var update_edit_formtq = document.getElementById('update_edit_formtq');
                                for(var i=0; i < update_edit_formtq.elements.length; i++){
                                if(update_edit_formtq.elements[i].value === '' && update_edit_formtq.elements[i].hasAttribute('required')){
                                    if (equipment_reference_tq == ""){
                                         document.getElementById("equipment_reference_tq_form").focus();
                                         document.getElementById("equipment_reference_div").innerHTML = "Please fill this field";
                                         document.getElementById("equipment_reference_div").style.color="Red";
                                         return;
                                    } else {
                                        document.getElementById("equipment_reference_div").innerHTML = "";
                                    }
                                    if (weight_unit_tq == ""){
                                         document.getElementById("weight_unit_tq_form").focus();
                                         document.getElementById("weight_unit_div").innerHTML = "Please fill this field";
                                         document.getElementById("weight_unit_div").style.color="Red";
                                         return;
                                    } else {
                                        document.getElementById("weight_unit_div").innerHTML = "";
                                    }
                                    if (cargo_gross_weight == ""){
                                         document.getElementById("cargo_gross_weight_form").focus();
                                         document.getElementById("cgw_unit_div").innerHTML = "Please fill this field";
                                         document.getElementById("cgw_unit_div").style.color="Red";
                                         return;
                                    } else {
                                        document.getElementById("cgw_unit_div").innerHTML =  "";
                                    }
                                    if (container_tare_weight == ""){
                                        if(is_shipper_owned.checked == true){
                                         document.getElementById("container_tare_weight_form").focus();
                                         document.getElementById("ctw_unit_div").innerHTML = "Please fill this field";
                                         document.getElementById("ctw_unit_div").style.color="Red";
                                         return;
                                         }
                                    } else {
                                        document.getElementById("ctw_unit_div").innerHTML = "";
                                    }
                                    if (iso_equipment_code == ""){
                                        if(is_shipper_owned.checked == true){
                                         document.getElementById("iso_equipment_code_form").focus();
                                         document.getElementById("iso_equipment_code_div").innerHTML = "Please fill this field";
                                         document.getElementById("iso_equipment_code_div").style.color="Red";
                                         return;
                                         }
                                    } else {
                                        document.getElementById("iso_equipment_code_div").innerHTML = "";
                                    }
                                    if (seal_number == ""){
                                         document.getElementById("seal_number_form").focus();
                                         document.getElementById("seal_number_div").innerHTML = "Please fill this field";
                                         document.getElementById("seal_number_div").style.color="Red";
                                         return;
                                    } else {
                                         document.getElementById("seal_number_div").innerHTML = "";
                                    }
                                    if (seal_type == "") {
                                         document.getElementById("seal_type_form").focus();
                                         document.getElementById("seal_type_div").innerHTML = "Please fill this field";
                                         document.getElementById("seal_type_div").style.color="Red";
                                    } else {
                                         document.getElementById("seal_type_div").innerHTML = "";
                                    }
                                    if (tq_array_created_by == "") {
                                         document.getElementById("tq_array_created_by_form").focus();
                                         document.getElementById("tq_array_created_by_div").innerHTML = "Please fill this field";
                                         document.getElementById("tq_array_created_by_div").style.color="Red";
                                         return;
                                    } else {
                                         document.getElementById("tq_array_created_by_div").innerHTML = "";
                                    }
                                }
                                }

                               var reg = /^[+-]?\d+(\.\d+)?$/;
                    if (reg.test(temperature_min)){
                        document.getElementById("temperature_min_div").innerHTML = "";
                    } else {
                             document.getElementById("temperature_min_form").focus();
                            document.getElementById("temperature_min_div").innerHTML = "Please enter a valid number or 0";
                            document.getElementById("temperature_min_div").style.color="Red";
                            return;
                    }
                    if (reg.test(temperature_max)){
                        document.getElementById("temperature_max_div").innerHTML = "";
                    } else {
                            document.getElementById("temperature_max_form").focus();
                            document.getElementById("temperature_max_div").innerHTML = "Please enter a valid number or 0";
                            document.getElementById("temperature_max_div").style.color="Red";
                            return;
                    }
                    if (reg.test(humidity_min)){
                        document.getElementById("humidity_min_div").innerHTML = "";
                    } else {
                                document.getElementById("humidity_min_form").focus();
                                document.getElementById("humidity_min_div").innerHTML = "Please enter a valid number or 0";
                                document.getElementById("humidity_min_div").style.color="Red";
                                return;
                    }
                    if (reg.test(humidity_max)){
                        document.getElementById("humidity_max_div").innerHTML = "";
                    } else {
                                document.getElementById("humidity_max_form").focus();
                                document.getElementById("humidity_max_div").innerHTML = "Please enter a valid number or 0";
                                document.getElementById("humidity_max_div").style.color="Red";
                                return;
                    }
                    if (reg.test(ventilation_min)){
                        document.getElementById("ventilation_min_div").innerHTML = "";
                    } else {
                                document.getElementById("ventilation_min_form").focus();
                                document.getElementById("ventilation_min_div").innerHTML = "Please enter a valid number or 0";
                                document.getElementById("ventilation_min_div").style.color="Red";
                                return;
                    }
                    if (reg.test(ventilation_max)){
                        document.getElementById("ventilation_max_div").innerHTML = "";
                    } else {
                                document.getElementById("ventilation_max_form").focus();
                                document.getElementById("ventilation_max_div").innerHTML = "Please enter a valid number or 0";
                                document.getElementById("ventilation_max_div").style.color="Red";
                                return;
                    }

                            dialog.close();
                            }
                        }],
                    });
                    dialog.opened().then(function () {

                        var update_edit_formtq = document.getElementById('update_edit_formtq');
                        for(var i=0; i < update_edit_formtq.elements.length; i++){
                            if(update_edit_formtq.elements[i].hasAttribute('required')){
                                update_edit_formtq.elements[i].style.background='#ADD8E6';
                            }
                        }
                        // Update each field values from main row
                        // field 1
                        var equipment_reference_tq = document.getElementById("new_update_eq_id_"+id).value;
                        document.getElementById("equipment_reference_tq_form").value = equipment_reference_tq;

                        // field 2
                        var weight_unit_tq = document.getElementById("new_wt_unit_update_tq_"+id).value;
                        document.getElementById("weight_unit_tq_form").value = weight_unit_tq;

                        // field 3
                        var cargo_gross_weight = document.getElementById("new_cgw_update_tq_"+id).value;
                        document.getElementById("cargo_gross_weight_form").value = cargo_gross_weight;

                        // field 4
                        var container_tare_weight = document.getElementById("new_ctw_update_tq_"+id).value;
                        document.getElementById("container_tare_weight_form").value = container_tare_weight;

                        // field 5
                        var iso_equipment_code = document.getElementById("new_iso_eq_code_update_tq_"+id).value;
                        document.getElementById("iso_equipment_code_form").value = iso_equipment_code;

                        // field 6
                        var is_shipper_owned = document.getElementById("new_is_shipper_owned_update_tq_"+id);
                        if(is_shipper_owned.checked == true){
                            document.getElementById("is_shipper_owned_form").checked = true;
                        } else {
                            document.getElementById("is_shipper_owned_form").checked = false;
                        }

                        // field 7
                        var temperature_min = document.getElementById("new_temp_min_update_tq_"+id).value;
                        document.getElementById("temperature_min_form").value = temperature_min;

                        // field 8
                        var temperature_max = document.getElementById("new_temp_max_update_tq_"+id).value;
                        document.getElementById("temperature_max_form").value = temperature_max;

                        // field 9
                        var temperature_unit = document.getElementById("new_temp_unit_update_tq_"+id).value;
                        document.getElementById("temperature_unit_form").value = temperature_unit;

                        // field 10
                        var humidity_min = document.getElementById("new_humidity_min_update_tq_"+id).value;
                        document.getElementById("humidity_min_form").value = humidity_min;

                        // field 11
                        var humidity_max = document.getElementById("new_humidity_max_update_tq_"+id).value;
                        document.getElementById("humidity_max_form").value = humidity_max;

                        // field 12
                        var ventilation_max = document.getElementById("new_ventilation_min_update_tq_"+id).value;
                        document.getElementById("ventilation_min_form").value = ventilation_max;

                        // field 13
                        var ventilation_max = document.getElementById("new_ventilation_max_update_tq_"+id).value;
                        document.getElementById("ventilation_max_form").value = ventilation_max;

                        // field 14
                        var seal_number = document.getElementById("new_seal_no_update_tq_"+id).value;
                        document.getElementById("seal_number_form").value = seal_number;

                        // field 15
                        var seal_source = document.getElementById("new_seal_source_update_tq_"+id).value;
                        document.getElementById("seal_source_form").value = seal_source;

                        // field 16
                        var seal_type = document.getElementById("new_seal_type_update_tq_"+id).value;
                        document.getElementById("seal_type_form").value = seal_type;

                        // field 17
                        var tq_array_created_by = document.getElementById("tq_array_created_by_"+id).value;
                        document.getElementById("tq_array_created_by_form").value = tq_array_created_by;

                    });
                    dialog.open();
                });
            });



            // Edit/View Added Cargo Item Popup
            $('#cargo_tbody_update_si').on('click', '.edit_added_cargo_item', function () {
                var child = $(this).closest('tr');
                child.each(function () {
                    var id = $(this).attr('id');
                    var dialog = new Dialog(this, {
                        title: _t("Shipping Instruction - Edit Cargo Items"),
                        $content: $(qweb.render('freightbox.edit_added_cargo_item_popup')),
                        buttons: [{
                                text: _t('Edit'),
                                classes: "btn-primary",
                                close: false,
                                click: function () {
                                    var view_cargo_line_item_id = document.getElementById("cargo_line_item_id_form").value;
                                    document.getElementById("update_cargo_line_items_id_"+id).value = view_cargo_line_item_id;

                                    var shipping_marks = document.getElementById("shipping_marks_form").value;
                                    document.getElementById("update_shipping_marks_id_"+id).value = shipping_marks;

                                    var carrier_booking_reference = document.getElementById("carrier_booking_reference_form").value;
                                    document.getElementById("update_carrier_booking_reference_id_"+id).value = carrier_booking_reference;

                                    var description_of_goods = document.getElementById("description_of_goods_form").value;
                                    document.getElementById("update_description_of_goods_id_"+id).value = description_of_goods;

                                    var hs_code = document.getElementById("hs_code_form").value;
                                    document.getElementById("update_hs_code_id_"+id).value = hs_code;

                                    var no_of_packages = document.getElementById("no_of_packages_form").value;
                                    document.getElementById("update_number_of_packages_id_"+id).value = no_of_packages;

                                    var weight = document.getElementById("weight_form").value;
                                    document.getElementById("update_weight_id_"+id).value = weight;

                                    var volume = document.getElementById("volume_form").value;
                                    document.getElementById("update_volume_id_"+id).value = volume;

                                    var weight_unit = document.getElementById("weight_unit_form").value;
                                    document.getElementById("update_weight_unit_id_"+id).value = weight_unit;

                                    var volume_unit = document.getElementById("volume_unit_form").value;
                                    document.getElementById("update_volume_unit_id_"+id).value = volume_unit;

                                    var package_code = document.getElementById("package_code_form").value;
                                    document.getElementById("update_package_code_id_"+id).value = package_code;

                                    var equipment_reference = document.getElementById("equipment_reference_form").value;
                                    document.getElementById("update_equipment_reference_id_"+id).value = equipment_reference;

                                    var cargo_edited_by = document.getElementById("cargo_array_created_by_form").value;
                                    document.getElementById("cargo_array_created_by_"+id).value = cargo_edited_by;


                                    var edit_added_cargo_form = document.getElementById('edit_added_cargo_form');
                                    for(var e=0; e < edit_added_cargo_form.elements.length; e++){
                                        if(edit_added_cargo_form.elements[e].value === '' && edit_added_cargo_form.elements[e].hasAttribute('required')){
                                            if (view_cargo_line_item_id == ""){
                                                 document.getElementById("cargo_line_item_id_form").focus();
                                                 document.getElementById("cargo_line_item_id_div").innerHTML = "Please fill this field";
                                                 document.getElementById("cargo_line_item_id_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("cargo_line_item_id_div").innerHTML = "";
                                            }
                                             if (shipping_marks == ""){
                                                 document.getElementById("shipping_marks_form").focus();
                                                 document.getElementById("shipping_marks_div").innerHTML = "Please fill this field";
                                                 document.getElementById("shipping_marks_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("shipping_marks_div").innerHTML = "";
                                            }
                                            if (description_of_goods == ""){
                                                 document.getElementById("description_of_goods_form").focus();
                                                 document.getElementById("description_of_goods_div").innerHTML = "Please fill this field";
                                                 document.getElementById("description_of_goods_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("description_of_goods_div").innerHTML = "";
                                            }
                                            if (hs_code == ""){
                                                 document.getElementById("hs_code_form").focus();
                                                 document.getElementById("hs_code_div").innerHTML = "Please fill this field";
                                                 document.getElementById("hs_code_div").style.color="Red";
                                                 return;
                                            } else {
                                                 document.getElementById("hs_code_div").innerHTML = "";
                                            }
                                            if (no_of_packages == ""){
                                                 document.getElementById("no_of_packages_form").focus();
                                                 document.getElementById("no_of_packages_div").innerHTML = "Please fill this field";
                                                 document.getElementById("no_of_packages_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("no_of_packages_div").innerHTML = "";
                                            }
                                            if (weight == ""){
                                                 document.getElementById("weight_form").focus();
                                                 document.getElementById("weight_div").innerHTML = "Please fill this field";
                                                 document.getElementById("weight_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("weight_div").innerHTML = "";
                                            }
                                            if (weight_unit == ""){
                                                 document.getElementById("weight_unit_form").focus();
                                                 document.getElementById("weight_unit_div").innerHTML = "Please fill this field";
                                                 document.getElementById("weight_unit_div").style.color="Red";
                                            } else
                                            if (package_code == ""){
                                                 document.getElementById("package_code_form").focus();
                                                 document.getElementById("package_code_div").innerHTML = "Please fill this field";
                                                 document.getElementById("package_code_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("package_code_div").innerHTML = "";
                                            }
                                            if (equipment_reference == "") {
                                                document.getElementById("equipment_reference_form").focus();
                                                 document.getElementById("equipment_reference_div").innerHTML = "Please fill this field";
                                                 document.getElementById("equipment_reference_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("equipment_reference_div").innerHTML = "";
                                            }
                                            if (cargo_edited_by == "") {
                                                document.getElementById("cargo_array_created_by_form").focus();
                                                 document.getElementById("cargo_array_created_by_div").innerHTML = "Please fill this field";
                                                 document.getElementById("cargo_array_created_by_div").style.color="Red";
                                                 return;
                                            }else {
                                                document.getElementById("cargo_array_created_by_div").innerHTML = "";
                                            }
                                        }
                                    }
                                    if (no_of_packages != ""){
                                        var regex = /^\d*[]?\d*$/;
                                        if(regex.test(no_of_packages)){
                                            document.getElementById("no_of_packages_div").innerHTML = "";
                                        } else{
                                             document.getElementById("no_of_packages_form").focus();
                                             document.getElementById("no_of_packages_div").innerHTML = "Please enter a valid number";
                                             document.getElementById("no_of_packages_div").style.color="Red";
                                             return;
                                        }
                                    }
                                    dialog.close();
                                }
                            }],
                    });
                    dialog.opened().then(function () {

                        var edit_added_cargo_form = document.getElementById('edit_added_cargo_form');
                        for(var e=0; e < edit_added_cargo_form.elements.length; e++){
                            if(edit_added_cargo_form.elements[e].hasAttribute('required')){
                                edit_added_cargo_form.elements[e].style.background='#ADD8E6';
                            }
                        }
                            var view_cargo_line_item_id = document.getElementById("update_cargo_line_items_id_"+id).value;
                            document.getElementById("cargo_line_item_id_form").value = view_cargo_line_item_id;

                            var shipping_marks = document.getElementById("update_shipping_marks_id_"+id).value;
                            document.getElementById("shipping_marks_form").value = shipping_marks;

                            var carrier_booking_reference = document.getElementById("update_carrier_booking_reference_id_"+id).value;
                            document.getElementById("carrier_booking_reference_form").value = carrier_booking_reference;

                            var description_of_goods = document.getElementById("update_description_of_goods_id_"+id).value;
                            document.getElementById("description_of_goods_form").value = description_of_goods;

                            var hs_code = document.getElementById("update_hs_code_id_"+id).value;
                            document.getElementById("hs_code_form").value = hs_code;

                            var no_of_packages = document.getElementById("update_number_of_packages_id_"+id).value;
                            document.getElementById("no_of_packages_form").value = no_of_packages;

                            var weight = document.getElementById("update_weight_id_"+id).value;
                            document.getElementById("weight_form").value = weight;

                            var volume = document.getElementById("update_volume_id_"+id).value;
                            document.getElementById("volume_form").value = volume;

                            var weight_unit = document.getElementById("update_weight_unit_id_"+id).value;
                            document.getElementById("weight_unit_form").value = weight_unit;

                            var volume_unit = document.getElementById("update_volume_unit_id_"+id).value;
                            document.getElementById("volume_unit_form").value = volume_unit;

                            var package_code = document.getElementById("update_package_code_id_"+id).value;
                            document.getElementById("package_code_form").value = package_code;

                            var equipment_reference = document.getElementById("update_equipment_reference_id_"+id).value;
                            document.getElementById("equipment_reference_form").value = equipment_reference;

                            var cargo_created_by = document.getElementById("cargo_array_created_by_"+id).value;
                            document.getElementById("cargo_array_created_by_form").value = cargo_created_by;
                    });
                    dialog.open();
                });
            });

            // To delete current row -References
            $('#rc_update_tbody').on('click', '.remove_rc_update', function () {
                var child = $(this).closest('tr').nextAll();
                $(this).closest('tr').remove();
            });

            // To delete current row -Shipment Locations
            $('#sl_update_tbody').on('click', '.remove_sl_update', function () {
                var child = $(this).closest('tr').nextAll();
                $(this).closest('tr').remove();
            });

            // To delete current row -Document parties
            $('#dp_update_tbody').on('click', '.remove_dp_update', function () {
                var child = $(this).closest('tr').nextAll();
                $(this).closest('tr').remove();
            });

            // To delete current row - Transport Equipment
            $('#tq_update_tbody').on('click', '.remove_tq_update', function () {
                var child = $(this).closest('tr').nextAll();
                $(this).closest('tr').remove();
            });

            // To delete current row - cargo items
            $('#cargo_tbody_update_si').on('click', '.remove_cargo_update', function () {
                var child = $(this).closest('tr').nextAll();
                // Removing the current row.
                $(this).closest('tr').remove();
            });

               // Add new line on References
            $('#shipping_instructions_update_form').on('click', '.update_add_rc_div', function (ev) {
                var self = this;
                var dialog = new Dialog(this, {
                    title: _t("Shipping Instruction - References"),
                    $content: $(qweb.render('freightbox.update_add_rc_popup')),
                    buttons: [{
                        text: _t('Add'),
                        classes: "btn-primary",
                        close: false,
                        click: function () {
                            var reference_type = document.getElementById("reference_type_rc_form").value;
                            var reference_value = document.getElementById("reference_value_rc_form").value;
                            var ref_array_created_by = document.getElementById("ref_array_created_by_form").value;

                            var update_formrc = document.getElementById('update_formrc');
                            for(var i=0; i < update_formrc.elements.length; i++){
                                if(update_formrc.elements[i].value === '' && update_formrc.elements[i].hasAttribute('required')){
                                    if (reference_type == ""){
                                         document.getElementById("reference_type_rc_form").focus();
                                         document.getElementById("ref_type_div").innerHTML = "Please fill this field";
                                         document.getElementById("ref_type_div").style.color="Red";
                                         return;
                                    } else {
                                        document.getElementById("ref_type_div").innerHTML = "";
                                    }

                                    if (reference_value == "") {
                                        document.getElementById("reference_value_rc_form").focus();
                                         document.getElementById("ref_value_div").innerHTML = "Please fill this field";
                                         document.getElementById("ref_value_div").style.color="Red";
                                         return;
                                    } else {
                                        document.getElementById("ref_value_div").innerHTML = "";
                                    }
                                    if (ref_array_created_by == "") {
                                        document.getElementById("ref_array_created_by_form").focus();
                                         document.getElementById("ref_array_created_div").innerHTML = "Please fill this field";
                                         document.getElementById("ref_array_created_div").style.color="Red";
                                         return;
                                    } else {
                                        document.getElementById("ref_array_created_div").innerHTML = "";
                                    }
                                }
                            }
                            dialog.close();

                            var rc_last_row_id = $('#rc_update_tbody tr:last').attr('id');
                            if (rc_last_row_id == undefined){
                                rc_last_row_id = 0;
                            }

                            $('#rc_update_tbody').append(`<tr class="added_rc_lines" id="${++rc_last_row_id}">
                            <td class="row-index rc_row_index">
                                <p class='form-control' id="row_count_rc" readonly="readonly" name="row_count_rc" >${rc_last_row_id}</p></td>

                            </td>
                            <td>
                                <input type="text" name="new_reference_type_update_rc" placeholder="Maximum allowed characters 3" maxlength="3"
                                class='form-control reference_type_rc' value="${reference_type}"  readonly="readonly"
                                id="new_reference_type_update_rc_${rc_last_row_id}"/>
                            </td>
                            <td>
                                <input type="text" name="new_reference_value_update_rc" placeholder="Maximum allowed characters 100" maxlength="100"
                                class='form-control reference_value_rc' value="${reference_value}"  readonly="readonly"
                                id="new_reference_value_update_rc_${rc_last_row_id}"/>
                            </td>
                            <td>
                                <input type="hidden" name="references_array_created_by"
                                  class='form-control ref_array_created_by' value="${ref_array_created_by}"
                                  id="ref_array_created_by_${rc_last_row_id}"/>
                            </td>
                            <td>
                                <button class="btn btn-primary edit_rc_view" id="edit_rc_view"
                                type="button"><small><i class="fa fa-pencil"></i> </small></button>
                            </td>
                            <td>
                                <button class="btn btn-primary remove_rc_update" id="remove_rc_update"
                                type="button"><small><i class='fa fa-trash-o'></i></small></button>
                            </td>
                        </tr>`);
                        }
                    }],
                });
                dialog.opened().then(function () {
                    var update_formrc = document.getElementById('update_formrc');
                    for(var i=0; i < update_formrc.elements.length; i++){
                        if(update_formrc.elements[i].hasAttribute('required')){
                            update_formrc.elements[i].style.background='#ADD8E6';
                        }
                    }
                    var ref_created_by = document.getElementById("si_updated_by").value;
                    document.getElementById("ref_array_created_by_form").value = ref_created_by;
               });
                dialog.open();
            });

            // Add new line on Shipment Locations
            $('#shipping_instructions_update_form').on('click', '.update_add_sl_div', function (ev) {
                var self = this;
                var dialog = new Dialog(this, {
                    title: _t("Shipping Instruction - Shipment Locations"),
                    $content: $(qweb.render('freightbox.update_add_sl_popup')),
                    buttons: [{
                        text: _t('Add'),
                        classes: "btn-primary",
                        close: false,
                        click: function () {
                            var location_type = document.getElementById("location_type_form").value;
                            var location_name = document.getElementById("location_name_form").value;
                            var latitude = document.getElementById("latitude_form").value;
                            var longitude = document.getElementById("longitude_form").value;
                            var un_location_code = document.getElementById("un_location_code_form").value;
                            var street_name = document.getElementById("street_name_form").value;
                            var street_number = document.getElementById("street_number_form").value;
                            var floor = document.getElementById("floor_form").value;
                            var post_code = document.getElementById("post_code_form").value;
                            var city_name = document.getElementById("city_name_form").value;
                            var state_region = document.getElementById("state_region_form").value;
                            var country = document.getElementById("country_form").value;
                            var displayed_name = document.getElementById("displayed_name_form").value;
                            var sl_array_created_by = document.getElementById("sl_array_created_by_form").value;

                            var update_formsl = document.getElementById('update_formsl');
                            for(var i=0; i < update_formsl.elements.length; i++){
                                if(update_formsl.elements[i].value === '' && update_formsl.elements[i].hasAttribute('required')){
                                    if (location_type == ""){
                                         document.getElementById("location_type_form").focus();
                                         document.getElementById("loc_type_div").innerHTML = "Please fill this field";
                                         document.getElementById("loc_type_div").style.color="Red";
                                         return;
                                    } else {
                                        document.getElementById("loc_type_div").innerHTML = "";
                                    }
                                    if (location_name == ""){
                                        if (location_type === "POL" || location_type === "POD"){
                                         document.getElementById("location_name_form").focus();
                                         document.getElementById("loc_div").innerHTML = "Please fill this field";
                                         document.getElementById("loc_div").style.color="Red";
                                        return;
                                        }
                                    } else {
                                        document.getElementById("loc_div").innerHTML = "";
                                    }
                                    if (latitude == ""){
                                        if (location_type === "POL" || location_type === "POD"){
                                         document.getElementById("latitude_form").focus();
                                         document.getElementById("lat_div").innerHTML = "Please fill this field";
                                         document.getElementById("lat_div").style.color="Red";
                                         return;
                                         }
                                    } else {
                                        document.getElementById("lat_div").innerHTML = "";
                                    }
                                    if (longitude == ""){
                                        if (location_type === "POL" || location_type === "POD"){
                                         document.getElementById("longitude_form").focus();
                                         document.getElementById("long_div").innerHTML = "Please fill this field";
                                         document.getElementById("long_div").style.color="Red";
                                         return;
                                         }
                                    } else {
                                        document.getElementById("long_div").innerHTML = "";
                                    }
                                    if (un_location_code == ""){
                                        if (location_type === "POL" || location_type === "POD"){
                                         document.getElementById("un_location_code_form").focus();
                                         document.getElementById("un_loc_code_div").innerHTML = "Please fill this field";
                                         document.getElementById("un_loc_code_div").style.color="Red";
                                         return;
                                         }
                                    } else {
                                        document.getElementById("un_loc_code_div").innerHTML = "";
                                    }
                                    if (street_name == ""){
                                        if (location_type === "POL" || location_type === "POD"){
                                         document.getElementById("street_name_form").focus();
                                         document.getElementById("st_name_div").innerHTML = "Please fill this field";
                                         document.getElementById("st_name_div").style.color="Red";
                                         return;
                                         }
                                    } else {
                                        document.getElementById("st_name_div").innerHTML = "";
                                    }
                                    if (street_number == ""){
                                        if (location_type === "POL" || location_type === "POD"){
                                         document.getElementById("street_number_form").focus();
                                         document.getElementById("st_no_div").innerHTML = "Please fill this field";
                                         document.getElementById("st_no_div").style.color="Red";
                                         return;
                                         }
                                    } else {
                                        document.getElementById("st_no_div").innerHTML = "";
                                    }
                                    if (floor == ""){
                                        if (location_type === "POL" || location_type === "POD"){
                                         document.getElementById("floor_form").focus();
                                         document.getElementById("floor_div").innerHTML = "Please fill this field";
                                         document.getElementById("floor_div").style.color="Red";
                                         return;
                                         }
                                    } else {
                                        document.getElementById("floor_div").innerHTML = "";
                                    }
                                    if (post_code == ""){
                                        if (location_type === "POL" || location_type === "POD"){
                                         document.getElementById("post_code_form").focus();
                                         document.getElementById("post_code_div").innerHTML = "Please fill this field";
                                         document.getElementById("post_code_div").style.color="Red";
                                         return;
                                         }
                                    } else {
                                        document.getElementById("post_code_div").innerHTML = "";
                                    }
                                    if (city_name == ""){
                                        if (location_type === "POL" || location_type === "POD"){
                                         document.getElementById("city_name_form").focus();
                                         document.getElementById("city_div").innerHTML = "Please fill this field";
                                         document.getElementById("city_div").style.color="Red";
                                         return;
                                         }
                                    } else {
                                        document.getElementById("city_div").innerHTML = "";
                                    }
                                    if (state_region == ""){
                                        if (location_type === "POL" || location_type === "POD"){
                                         document.getElementById("state_region_form").focus();
                                         document.getElementById("st_reg_div").innerHTML = "Please fill this field";
                                         document.getElementById("st_reg_div").style.color="Red";
                                         return;
                                         }
                                    } else {
                                        document.getElementById("st_reg_div").innerHTML = "";
                                    }
                                    if (country == ""){
                                        if (location_type === "POL" || location_type === "POD"){
                                        document.getElementById("country_form").focus();
                                         document.getElementById("country_div").innerHTML = "Please fill this field";
                                         document.getElementById("country_div").style.color="Red";
                                         return;
                                         }
                                    } else {
                                        document.getElementById("country_div").innerHTML = "";
                                    }
                                    if (sl_array_created_by == ""){
                                        document.getElementById("sl_array_created_by_form").focus();
                                         document.getElementById("sl_array_created_by").innerHTML = "Please fill this field";
                                         document.getElementById("sl_array_created_by").style.color="Red";
                                         return;
                                    } else {
                                        document.getElementById("sl_array_created_by").innerHTML = "";
                                    }
                                }
                            }
                            if (location_type === "PRE" ||
                                        location_type === "POL" ||
                                        location_type === "POD" ||
                                        location_type === "PDE" ||
                                        location_type === "PCF" ||
                                        location_type === "OIR" ||
                                        location_type === "PSR") {
                                             document.getElementById("loc_type_div").innerHTML = "";
                                        } else {
                                            document.getElementById("location_type_form").value = "";
                                             document.getElementById("location_type_form").focus();
                                             document.getElementById("loc_type_div").innerHTML = "Please double click and select any from dropdown";
                                             document.getElementById("loc_type_div").style.color="Red";
                                             return;
                                        }
                            dialog.close();
                            var sl_last_row_id = $('#sl_update_table tr:last').attr('id');
                            if (sl_last_row_id == undefined){
                                sl_last_row_id = 0;
                            }

                            $('#sl_update_tbody').append(`<tr class="added_sl_lines" id="${++sl_last_row_id}">
                            <td class="row-index sl_row_index">
                                <p class='form-control' id="row_count_sl" name="row_count_sl" readonly="readonly" >${sl_last_row_id}</p></td>

                            </td>
                            <td>
                                <input type="text" name="new_location_type_update_sl" placeholder="Maximum allowed characters 3"
                                class='form-control location_type_sl' value="${location_type}" readonly="readonly"
                                id="new_location_type_update_sl_${sl_last_row_id}"/>
                            </td>

                            <td>
                                <input type="text" name="new_location_name_update_sl" placeholder="Maximum allowed characters 100"
                                class='form-control location_name_sl' value="${location_name}" readonly="readonly"
                                id="new_location_name_update_sl_${sl_last_row_id}"/>
                            </td>
                            <td>
                                <input type="text" name="new_latitude_update_sl" placeholder="Maximum allowed characters 10"
                                class='form-control latitude_sl' value="${latitude}" readonly="readonly" id="new_latitude_update_sl_${sl_last_row_id}"/>
                            </td>
                            <td>
                                <input type="text" name="new_longitude_update_sl" placeholder="Maximum allowed characters 11"
                                class='form-control longitude_sl' value="${longitude}" readonly="readonly" id="new_longitude_update_sl_${sl_last_row_id}"/>
                            </td>
                            <td>
                                <input type="text" name="new_un_location_code_update_sl" placeholder="Maximum allowed characters 5"
                                class='form-control un_location_code_sl' value="${un_location_code}" readonly="readonly"
                                id="new_un_location_code_update_sl_${sl_last_row_id}"/>
                            </td>
                            <td>
                                <input type="text" name="new_street_name_code_update_sl" placeholder="Maximum allowed characters 100"
                                class='form-control street_name_sl' value="${street_name}" readonly="readonly"
                                id="new_street_name_code_update_sl_${sl_last_row_id}"/>
                            </td>
                            <td>
                                <input type="text" name="new_street_number_code_update_sl" placeholder="Maximum allowed characters 50"
                                class='form-control street_number_sl' value="${street_number}" readonly="readonly"
                                id="new_street_number_code_update_sl_${sl_last_row_id}"/>
                            </td>
                            <td>
                                <input type="text" name="new_floor_update_sl" placeholder="Maximum allowed characters 50"
                                class='form-control floor_sl' value="${floor}" readonly="readonly" id="new_floor_update_sl_${sl_last_row_id}"/>
                            </td>
                            <td>
                                <input type="text" name="new_post_code_update_sl" placeholder="Maximum allowed characters 10"
                                class='form-control post_code_sl' value="${post_code}" readonly="readonly" id="new_post_code_update_sl_${sl_last_row_id}"/>
                            </td>
                            <td>
                                <input type="text" name="new_city_name_update_sl" placeholder="Maximum allowed characters 65"
                                class='form-control city_name_sl' value="${city_name}" readonly="readonly" id="new_city_name_update_sl_${sl_last_row_id}"/>
                            </td>
                            <td>
                                <input type="text" name="new_state_region_update_sl" placeholder="Maximum allowed characters 65"
                                class='form-control state_region_sl' value="${state_region}" readonly="readonly" id="new_state_region_update_sl_${sl_last_row_id}"/>
                            </td>
                            <td>
                                <input type="text" name="new_country_update_sl" placeholder="Maximum allowed characters 75"
                                class='form-control country_sl' value="${country}" readonly="readonly" id="new_country_update_sl_${sl_last_row_id}"/>
                            </td>
                            <td>
                                <input type="text" name="new_displayed_name_update_sl" placeholder="Maximum allowed characters 250"
                                class='form-control displayed_name_sl' value="${displayed_name}" readonly="readonly" id="new_displayed_name_update_sl_${sl_last_row_id}"/>
                            </td>
                            <td>
                                <input type="hidden" name="shipment_location_array_created_by"
                                class='form-control sl_array_created_by' value="${sl_array_created_by}"
                                id="sl_array_created_by_${sl_last_row_id}"/>
                            </td>
                            <td>
                                <button class="btn btn-primary edit_update_sl" id="edit_update_sl"
                                type="button"><small><i class="fa fa-pencil"></i> </small></button>
                            </td>
                            <td>
                                <button class="btn btn-primary remove_sl_update" id="remove_sl_update"
                                type="button"><small><i class='fa fa-trash-o'></i></small></button>
                            </td>
                        </tr>`);
                        }
                    }],
                });
                dialog.opened().then(function () {
                    var update_formsl = document.getElementById('update_formsl');
                    for(var i=0; i < update_formsl.elements.length; i++){
                        if(update_formsl.elements[i].hasAttribute('required')){
                            update_formsl.elements[i].style.background='#ADD8E6';
                        }
                    }
                    $("#location_type_form").on('change', function() {
                                var loc_type = document.getElementById("location_type_form").value;
                                            if (loc_type == "Place of Receipt (PRE)") {
                                                document.getElementById("location_type_form").value = "PRE";
                                                document.getElementById("location_name_form").style.background='#FFFFFF';
                                                document.getElementById("latitude_form").style.background='#FFFFFF';
                                                document.getElementById("longitude_form").style.background='#FFFFFF';
                                                document.getElementById("un_location_code_form").style.background='#FFFFFF';
                                                document.getElementById("street_name_form").style.background='#FFFFFF';
                                                document.getElementById("street_number_form").style.background='#FFFFFF';
                                                document.getElementById("floor_form").style.background='#FFFFFF';
                                                document.getElementById("post_code_form").style.background='#FFFFFF';
                                                document.getElementById("city_name_form").style.background='#FFFFFF';
                                                document.getElementById("state_region_form").style.background='#FFFFFF';
                                                document.getElementById("country_form").style.background='#FFFFFF';
                                            }
                                            if (loc_type == "Port of Loading (POL)") {
                                                document.getElementById("location_type_form").value = "POL";
                                                document.getElementById("location_name_form").style.background='#ADD8E6';
                                                 $("#location_name_form").attr('required',"required");
                                                document.getElementById("latitude_form").style.background='#ADD8E6';
                                                $("#latitude_form").attr('required',"required");
                                                document.getElementById("longitude_form").style.background='#ADD8E6';
                                                $("#longitude_form").attr('required',"required");
                                                document.getElementById("un_location_code_form").style.background='#ADD8E6';
                                                $("#un_location_code_form").attr('required',"required");
                                                document.getElementById("street_name_form").style.background='#ADD8E6';
                                                $("#street_name_form").attr('required',"required");
                                                document.getElementById("street_number_form").style.background='#ADD8E6';
                                                $("#street_number_form").attr('required',"required");
                                                document.getElementById("floor_form").style.background='#ADD8E6';
                                                $("#floor_form").attr('required',"required");
                                                document.getElementById("post_code_form").style.background='#ADD8E6';
                                                $("#post_code_form").attr('required',"required");
                                                document.getElementById("city_name_form").style.background='#ADD8E6';
                                                $("#city_name_form").attr('required',"required");
                                                document.getElementById("state_region_form").style.background='#ADD8E6';
                                                $("#state_region_form").attr('required',"required");
                                                document.getElementById("country_form").style.background='#ADD8E6';
                                                $("#country_form").attr('required',"required");
                                            }
                                            if (loc_type == "Port of Discharge (POD)") {
                                                document.getElementById("location_type_form").value = "POD";
                                                 document.getElementById("location_name_form").style.background='#ADD8E6';
                                                 $("#location_name_form").attr('required',"required");
                                                document.getElementById("latitude_form").style.background='#ADD8E6';
                                                $("#latitude_form").attr('required',"required");
                                                document.getElementById("longitude_form").style.background='#ADD8E6';
                                                $("#longitude_form").attr('required',"required");
                                                document.getElementById("un_location_code_form").style.background='#ADD8E6';
                                                $("#un_location_code_form").attr('required',"required");
                                                document.getElementById("street_name_form").style.background='#ADD8E6';
                                                $("#street_name_form").attr('required',"required");
                                                document.getElementById("street_number_form").style.background='#ADD8E6';
                                                $("#street_number_form").attr('required',"required");
                                                document.getElementById("floor_form").style.background='#ADD8E6';
                                                $("#floor_form").attr('required',"required");
                                                document.getElementById("post_code_form").style.background='#ADD8E6';
                                                $("#post_code_form").attr('required',"required");
                                                document.getElementById("city_name_form").style.background='#ADD8E6';
                                                $("#city_name_form").attr('required',"required");
                                                document.getElementById("state_region_form").style.background='#ADD8E6';
                                                $("#state_region_form").attr('required',"required");
                                                document.getElementById("country_form").style.background='#ADD8E6';
                                                $("#country_form").attr('required',"required");
                                            }
                                            if (loc_type == "Place of Delivery (PDE)") {
                                                document.getElementById("location_type_form").value = "PDE";
                                                document.getElementById("location_name_form").style.background='#FFFFFF';
                                                document.getElementById("latitude_form").style.background='#FFFFFF';
                                                document.getElementById("longitude_form").style.background='#FFFFFF';
                                                document.getElementById("un_location_code_form").style.background='#FFFFFF';
                                                document.getElementById("street_name_form").style.background='#FFFFFF';
                                                document.getElementById("street_number_form").style.background='#FFFFFF';
                                                document.getElementById("floor_form").style.background='#FFFFFF';
                                                document.getElementById("post_code_form").style.background='#FFFFFF';
                                                document.getElementById("city_name_form").style.background='#FFFFFF';
                                                document.getElementById("state_region_form").style.background='#FFFFFF';
                                                document.getElementById("country_form").style.background='#FFFFFF';
                                            }
                                            if (loc_type == "Pre-carriage from (PCF)") {
                                                document.getElementById("location_type_form").value = "PCF";
                                                document.getElementById("location_name_form").style.background='#FFFFFF';
                                                document.getElementById("latitude_form").style.background='#FFFFFF';
                                                document.getElementById("longitude_form").style.background='#FFFFFF';
                                                document.getElementById("un_location_code_form").style.background='#FFFFFF';
                                                document.getElementById("street_name_form").style.background='#FFFFFF';
                                                document.getElementById("street_number_form").style.background='#FFFFFF';
                                                document.getElementById("floor_form").style.background='#FFFFFF';
                                                document.getElementById("post_code_form").style.background='#FFFFFF';
                                                document.getElementById("city_name_form").style.background='#FFFFFF';
                                                document.getElementById("state_region_form").style.background='#FFFFFF';
                                                document.getElementById("country_form").style.background='#FFFFFF';
                                            }
                                            if (loc_type == "Onward Inland Routing (OIR)"){
                                                document.getElementById("location_type_form").value = "OIR";
                                                document.getElementById("location_name_form").style.background='#FFFFFF';
                                                document.getElementById("latitude_form").style.background='#FFFFFF';
                                                document.getElementById("longitude_form").style.background='#FFFFFF';
                                                document.getElementById("un_location_code_form").style.background='#FFFFFF';
                                                document.getElementById("street_name_form").style.background='#FFFFFF';
                                                document.getElementById("street_number_form").style.background='#FFFFFF';
                                                document.getElementById("floor_form").style.background='#FFFFFF';
                                                document.getElementById("post_code_form").style.background='#FFFFFF';
                                                document.getElementById("city_name_form").style.background='#FFFFFF';
                                                document.getElementById("state_region_form").style.background='#FFFFFF';
                                                document.getElementById("country_form").style.background='#FFFFFF';
                                            }
            });
                    var sl_created_by = document.getElementById("si_updated_by").value;
                    document.getElementById("sl_array_created_by_form").value = sl_created_by;
               });
                dialog.open();
            });

            // Add new line on Document Parties
               $('#shipping_instructions_update_form').on('click', '.update_add_dp_div', function (ev) {
                var self = this;
                var dialog = new Dialog(this, {
                title: _t("Shipping Instruction - Document Parties"),
                $content: $(qweb.render('freightbox.update_add_dp_popup')),
                buttons: [{
                    text: _t('Add'),
                    classes: "btn-primary",
                    close: false,
                    click: function () {
                    var party_name = document.getElementById("party_name_dp_form").value;
                    var tax_reference_1 = document.getElementById("tax_reference_1_dp_form").value;
                    var public_key = document.getElementById("public_key_form").value;
                    var street = document.getElementById("street_form").value;
                    var street_number = document.getElementById("street_number_form").value;
                    var floor = document.getElementById("floor_form").value;
                    var post_code = document.getElementById("post_code_form").value;
                    var city = document.getElementById("city_form").value;
                    var state_region = document.getElementById("state_region_form").value;
                    var country = document.getElementById("country_form").value;
                    var tax_reference_2 = document.getElementById("tax_reference_2_form").value;
                    var nmfta_code = document.getElementById("nmfta_code_form").value;
                    var party_function = document.getElementById("party_function_form").value;
                    var address_line = document.getElementById("address_line_form").value;
                    var name = document.getElementById("name_form").value;
                    var email = document.getElementById("email_form").value;
                    var phone = document.getElementById("phone_form").value;
                    var is_to_be_notified_val
                    var is_to_be_notified = document.getElementById("is_to_be_notified_form");
                        if(is_to_be_notified.checked == true){
                            is_to_be_notified_val = true;
                        } else {
                            is_to_be_notified_val = false;
                        }
                    var dp_array_created_by = document.getElementById("dp_array_created_by_form").value;

                    var update_formdp = document.getElementById('update_formdp');
                    for(var i=0; i < update_formdp.elements.length; i++){
                        if(update_formdp.elements[i].value === '' && update_formdp.elements[i].hasAttribute('required')){
                            if (party_name == ""){
                                 document.getElementById("party_name_dp_form").focus();
                                 document.getElementById("party_name_div").innerHTML = "Please fill this field";
                                 document.getElementById("party_name_div").style.color="Red";
                                 return;
                            } else {
                                document.getElementById("party_name_div").innerHTML = "";
                            }
                            if (tax_reference_1 == ""){
                                 document.getElementById("tax_reference_1_dp_form").focus();
                                 document.getElementById("tax_reference_1_div").innerHTML = "Please fill this field";
                                 document.getElementById("tax_reference_1_div").style.color="Red";
                                 return;
                            } else {
                                document.getElementById("tax_reference_1_div").innerHTML = "";
                            }
                            if (public_key == ""){
                                 document.getElementById("public_key_form").focus();
                                 document.getElementById("public_key_div").innerHTML = "Please fill this field";
                                 document.getElementById("public_key_div").style.color="Red";
                                 return;
                            } else {
                                document.getElementById("public_key_div").innerHTML = "";
                            }
                            if (street == ""){
                                 document.getElementById("street_form").focus();
                                 document.getElementById("street_div").innerHTML = "Please fill this field";
                                 document.getElementById("street_div").style.color="Red";
                                 return;
                            } else {
                                document.getElementById("street_div").innerHTML = "";
                            }
                            if (street_number == ""){
                                 document.getElementById("street_number_form").focus();
                                 document.getElementById("street_no_div").innerHTML = "Please fill this field";
                                 document.getElementById("street_no_div").style.color="Red";
                                 return;
                            } else {
                                document.getElementById("street_no_div").innerHTML = "";
                            }
                            if (floor == ""){
                                 document.getElementById("floor_form").focus();
                                 document.getElementById("floor_div").innerHTML = "Please fill this field";
                                 document.getElementById("floor_div").style.color="Red";
                                 return;
                            } else {
                                document.getElementById("floor_div").innerHTML = "";
                            }
                            if (post_code == ""){
                                 document.getElementById("post_code_form").focus();
                                 document.getElementById("post_code_div").innerHTML = "Please fill this field";
                                 document.getElementById("post_code_div").style.color="Red";
                                 return;
                            } else {
                                document.getElementById("post_code_div").innerHTML = "";
                            }
                            if (city == ""){
                                 document.getElementById("city_form").focus();
                                 document.getElementById("city_div").innerHTML = "Please fill this field";
                                 document.getElementById("city_div").style.color="Red";
                                 return;
                            } else {
                                document.getElementById("city_div").innerHTML = "";
                            }
                            if (state_region == ""){
                                 document.getElementById("state_region_form").focus();
                                 document.getElementById("state_region_div").innerHTML = "Please fill this field";
                                 document.getElementById("state_region_div").style.color="Red";
                                 return;
                            } else {
                                document.getElementById("state_region_div").innerHTML = "";
                            }
                            if (country == ""){
                                 document.getElementById("country_form").focus();
                                 document.getElementById("country_div").innerHTML = "Please fill this field";
                                 document.getElementById("country_div").style.color="Red";
                                 return;
                            } else {
                                document.getElementById("country_div").innerHTML = "";
                            }
                            if (tax_reference_2 == ""){
                                 document.getElementById("tax_reference_2_form").focus();
                                 document.getElementById("tax_ref_2_div").innerHTML = "Please fill this field";
                                 document.getElementById("tax_ref_2_div").style.color="Red";
                                 return;
                            } else {
                                document.getElementById("tax_ref_2_div").innerHTML = "";
                            }
                            if (nmfta_code == ""){
                                 document.getElementById("nmfta_code_form").focus();
                                 document.getElementById("nmfta_code_div").innerHTML = "Please fill this field";
                                 document.getElementById("nmfta_code_div").style.color="Red";
                                 return;
                            } else {
                                document.getElementById("nmfta_code_div").innerHTML = "";
                            }
                            if (party_function == ""){
                                 document.getElementById("party_function_form").focus();
                                 document.getElementById("party_fn_div").innerHTML = "Please fill this field";
                                 document.getElementById("party_fn_div").style.color="Red";
                                 return;
                            } else {
                                document.getElementById("party_fn_div").innerHTML = "";
                            }
                            if (name == ""){
                                 document.getElementById("name_form").focus();
                                 document.getElementById("name_div").innerHTML = "Please fill this field";
                                 document.getElementById("name_div").style.color="Red";
                                 return;
                            } else {
                                document.getElementById("name_div").innerHTML = "";
                            }
                            if (phone == ""){
                                 document.getElementById("phone_form").focus();
                                 document.getElementById("phone_div").innerHTML = "Please fill this field";
                                 document.getElementById("phone_div").style.color="Red";
                                 return;
                            } else {
                                document.getElementById("phone_div").innerHTML = "";
                            }
                            if (email == ""){
                                 document.getElementById("email_form").focus();
                                 document.getElementById("email_div").innerHTML = "Please fill this field";
                                 document.getElementById("email_div").style.color="Red";
                                 return;
                            } else {

                                document.getElementById("email_div").innerHTML = "";
                            }
                            if (dp_array_created_by == ""){
                                 document.getElementById("dp_array_created_by_form").focus();
                                 document.getElementById("dp_array_created_by_div").innerHTML = "Please fill this field";
                                 document.getElementById("dp_array_created_by_div").style.color="Red";
                                 return;
                            } else {
                                document.getElementById("dp_array_created_by_div").innerHTML = "";
                            }

                        }
                    }
                    if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(email))
                      {
                        document.getElementById("email_div").innerHTML = "";
                      }
                      else {
                        document.getElementById("email_form").focus();
                        document.getElementById("email_div").innerHTML = "Please Enter a valid email";
                        document.getElementById("email_div").style.color="Red";
                        return;
                      }

                      /*  if(is_to_be_notified.checked != true){
                            is_to_be_notified.checked = true;
                        }*/
                     /* var re = /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/im;
                         if (re.test(phone) == true){
                             document.getElementById("phone_div").innerHTML = "";
                         } else {
                             document.getElementById("phone_form").focus();
                             document.getElementById("phone_div").innerHTML = "Please fill this field";
                             document.getElementById("phone_div").style.color="Red";
                             return;
                         }*/
                    dialog.close();

                    var dp_last_row_id = $('#dp_update_table tr:last').attr('id');
                    if (dp_last_row_id == undefined){
                        dp_last_row_id = 0;
                    }
                    $('#dp_update_tbody').append(`<tr class="added_dp_lines" id="${++dp_last_row_id}">
                        <td class="row-index dp_row_index">
                            <p class='form-control' id="dp_row_id" name="dp_row_id" >${dp_last_row_id}</p></td>
                            </input>
                        </td>
                        <td>
                            <input type="text" name="new_party_name_update_dp" placeholder="Maximum allowed characters 100" maxlength="100"
                            class='form-control equipment_reference' value="${party_name}" readonly="readonly" id="new_party_name_update_dp_${dp_last_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="new_tax_reference_1_update_dp" readonly="readonly" placeholder="Maximum allowed characters 20"
                            class='form-control tax_reference_1_dp' value="${tax_reference_1}"
                             id="new_tax_reference_1_update_dp_${dp_last_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="new_public_key_update_dp" placeholder="Maximum allowed characters 500"
                            class='form-control public_key_dp' value="${public_key}" readonly="readonly" id="new_public_key_update_dp_${dp_last_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="new_street_update_dp" placeholder="Maximum allowed characters 100"
                            class='form-control street_dp' value="${street}" readonly="readonly" id="new_street_update_dp_${dp_last_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="new_street_number_update_dp" placeholder="Maximum allowed characters 50"
                            class='form-control street_number_dp' value="${street_number}" readonly="readonly" id="new_street_number_update_dp_${dp_last_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="new_floor_update_dp" placeholder="Maximum allowed characters 50"
                            class='form-control floor_dp' value="${floor}" readonly="readonly" id="new_floor_update_dp_${dp_last_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="new_post_code_update_dp" placeholder="Maximum allowed characters 10"
                            class='form-control post_code_dp' value="${post_code}" readonly="readonly" id="new_post_code_update_dp_${dp_last_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="new_city_update_dp" placeholder="Maximum allowed characters 65"
                            class='form-control city_dp' value="${city}" readonly="readonly" id="new_city_update_dp_${dp_last_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="new_state_region_update_dp" placeholder="Maximum allowed characters 65"
                            class='form-control state_region_dp' value="${state_region}" readonly="readonly" id="new_state_region_update_dp_${dp_last_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="new_country_update_dp" placeholder="Maximum allowed characters 75"
                            class='form-control country_dp' value="${country}" readonly="readonly" id="new_country_update_dp_${dp_last_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="new_tax_reference_2_update_dp" placeholder="Maximum allowed characters 20"
                            class='form-control tax_reference_2_dp' value="${tax_reference_2}" readonly="readonly" id="new_tax_reference_2_update_dp_${dp_last_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="new_nmfta_code_update_dp" placeholder="Maximum allowed characters 4"
                            class='form-control nmfta_code_dp' value="${nmfta_code}" readonly="readonly" id="new_nmfta_code_update_dp_${dp_last_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="new_party_function_update_dp" placeholder="Maximum allowed characters 3"
                            class='form-control party_function_dp' value="${party_function}" readonly="readonly" id="new_party_function_update_dp_${dp_last_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="new_address_line_update_dp" placeholder="Maximum allowed characters 250"
                            class='form-control address_line_dp' value="${address_line}" readonly="readonly" id="new_address_line_update_dp_${dp_last_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="new_name_update_dp" placeholder="Maximum allowed characters 100"
                            class='form-control name_dp' value="${name}" readonly="readonly" id="new_name_update_dp_${dp_last_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="new_email_update_dp" placeholder="Maximum allowed characters 100"
                            class='form-control email_dp' value="${email}" readonly="readonly" id="new_email_update_dp_${dp_last_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="new_phone_update_dp" placeholder="Maximum allowed characters 30"
                            class='form-control phone_dp' value="${phone}" readonly="readonly" id="new_phone_update_dp_${dp_last_row_id}"/>
                        </td>
                        <td>
                            <input type="checkbox" name="new_is_to_be_notified_update_dp"
                            class='form-control to_be_notified' value="${is_to_be_notified_val}"
                            id="new_is_to_be_notified_update_dp_${dp_last_row_id}"/>
                        </td>
                        <td>
                            <input type="hidden" name="document_parties_array_created_by"
                            class='form-control dp_array_created_by' value="${dp_array_created_by}"
                             id="dp_array_created_by_${dp_last_row_id}"/>
                        </td>
                        <td>
                            <button class="btn btn-primary update_edit_dp" id="update_edit_dp"
                            type="button"><small><i class="fa fa-pencil"></i> </small></button>
                        </td>
                        <td>
                            <button class="btn btn-primary remove_dp_update" id="remove_dp_update"
                            type="button"><small><i class='fa fa-trash-o'></i></small></button>
                        </td>
                    </tr>`);
                    document.getElementById("new_is_to_be_notified_update_dp_"+dp_last_row_id).checked = is_to_be_notified_val;
                }
            }],
        });
        dialog.opened().then(function () {
            var update_formdp = document.getElementById('update_formdp');
            for(var i=0; i < update_formdp.elements.length; i++){
                if(update_formdp.elements[i].hasAttribute('required')){
                    update_formdp.elements[i].style.background='#ADD8E6';
                }
            }
            var dp_created_by = document.getElementById("si_updated_by").value;
            document.getElementById("dp_array_created_by_form").value = dp_created_by;
       });
        dialog.open();
            });

            // Add new line on Transport Equipment
            $('#shipping_instructions_update_form').on('click', '.update_add_tq_div', function (ev) {
                var self = this;
                var dialog = new Dialog(this, {
                title: _t("Shipping Instruction - Transport Equipment"),
                $content: $(qweb.render('freightbox.update_add_transport_eqipment_popup')),
                buttons: [{
                text: _t('Add'),
                classes: "btn-primary tq_add_new_line",
                close: false,
                click: function () {
                    var shipper_owned_tq = false;

                    var equipment_reference = document.getElementById("equipment_reference_tq_form").value;
                    var weight_unit_tq = document.getElementById("weight_unit_tq_form").value;
                    var cargo_gross_weight = document.getElementById("cargo_gross_weight_form").value;
                    var container_tare_weight = document.getElementById("container_tare_weight_form").value;
                    var iso_equipment_code = document.getElementById("iso_equipment_code_form").value;
                    var is_shipper_owned = document.getElementById("is_shipper_owned_form");
                        if(is_shipper_owned.checked == true){
                            shipper_owned_tq = true;
                        } else {
                            shipper_owned_tq = false;
                        }

                   // var is_shipper_owned = document.getElementById("is_shipper_owned_form").value;
                    var temperature_min = document.getElementById("temperature_min_form").value;
                    var temperature_max = document.getElementById("temperature_max_form").value;
                    var temperature_unit = document.getElementById("temperature_unit_form").value;
                    var humidity_min = document.getElementById("humidity_min_form").value;
                    var humidity_max = document.getElementById("humidity_max_form").value;
                    var ventilation_min = document.getElementById("ventilation_min_form").value;
                    var ventilation_max = document.getElementById("ventilation_max_form").value;
                    var seal_number = document.getElementById("seal_number_form").value;
                    var seal_source = document.getElementById("seal_source_form").value;
                    var seal_type = document.getElementById("seal_type_form").value;
                    var tq_array_created_by = document.getElementById("tq_array_created_by_form").value;

                    var update_formtq = document.getElementById('update_formtq');
                    for(var i=0; i < update_formtq.elements.length; i++){
                        if(update_formtq.elements[i].value === '' && update_formtq.elements[i].hasAttribute('required')){
                            if (equipment_reference == ""){
                                 document.getElementById("equipment_reference_tq_form").focus();
                                 document.getElementById("equipment_reference_div").innerHTML = "Please fill this field";
                                 document.getElementById("equipment_reference_div").style.color="Red";
                                 return;
                            } else {
                                document.getElementById("equipment_reference_div").innerHTML = "";
                            }
                            if (weight_unit_tq == ""){
                                 document.getElementById("weight_unit_tq_form").focus();
                                 document.getElementById("weight_unit_div").innerHTML = "Please fill this field";
                                 document.getElementById("weight_unit_div").style.color="Red";
                                 return;
                            } else {
                                document.getElementById("weight_unit_div").innerHTML = "";
                            }
                            if (cargo_gross_weight == ""){
                                 document.getElementById("cargo_gross_weight_form").focus();
                                 document.getElementById("cgw_unit_div").innerHTML = "Please fill this field";
                                 document.getElementById("cgw_unit_div").style.color="Red";
                                 return;
                            } else {
                                document.getElementById("cgw_unit_div").innerHTML = "";
                            }
                            if (container_tare_weight == ""){
                                if(is_shipper_owned.checked == true){
                                 document.getElementById("container_tare_weight_form").focus();
                                 document.getElementById("ctw_unit_div").innerHTML = "Please fill this field";
                                 document.getElementById("ctw_unit_div").style.color="Red";
                                 return;
                                 }
                            } else {
                                document.getElementById("ctw_unit_div").innerHTML = "";
                            }
                            if (iso_equipment_code == ""){
                                if(is_shipper_owned.checked == true){
                                 document.getElementById("iso_equipment_code_form").focus();
                                 document.getElementById("iso_equipment_code_div").innerHTML = "Please fill this field";
                                 document.getElementById("iso_equipment_code_div").style.color="Red";
                                 return;
                                 }
                            } else {
                                document.getElementById("iso_equipment_code_div").innerHTML = "";
                            }
                            if (seal_number == ""){
                                 document.getElementById("seal_number_form").focus();
                                 document.getElementById("seal_number_div").innerHTML = "Please fill this field";
                                 document.getElementById("seal_number_div").style.color="Red";
                                 return;
                            } else {
                                document.getElementById("seal_number_div").innerHTML = "";
                            }
                            if (seal_type == "") {
                                 document.getElementById("seal_type_form").focus();
                                 document.getElementById("seal_type_div").innerHTML = "Please fill this field";
                                 document.getElementById("seal_type_div").style.color="Red";
                                 return;
                            } else {
                                document.getElementById("seal_type_div").innerHTML = "";
                            }
                            if (tq_array_created_by == "") {
                                 document.getElementById("tq_array_created_by_form").focus();
                                 document.getElementById("tq_array_created_by_div").innerHTML = "Please fill this field";
                                 document.getElementById("tq_array_created_by_div").style.color="Red";
                                 return;
                            } else {
                                document.getElementById("tq_array_created_by_div").innerHTML = "";
                            }
                        }
                    }
                    var reg = /^[+-]?\d+(\.\d+)?$/;
                    if (reg.test(temperature_min)){
                        document.getElementById("temperature_min_div").innerHTML = "";
                    } else {
                             document.getElementById("temperature_min_form").focus();
                            document.getElementById("temperature_min_div").innerHTML = "Please enter a valid number or 0";
                            document.getElementById("temperature_min_div").style.color="Red";
                            return;
                    }
                    if (reg.test(temperature_max)){
                        document.getElementById("temperature_max_div").innerHTML = "";
                    } else {
                            document.getElementById("temperature_max_form").focus();
                            document.getElementById("temperature_max_div").innerHTML = "Please enter a valid number or 0";
                            document.getElementById("temperature_max_div").style.color="Red";
                            return;
                    }
                    if (reg.test(humidity_min)){
                        document.getElementById("humidity_min_div").innerHTML = "";
                    } else {
                                document.getElementById("humidity_min_form").focus();
                                document.getElementById("humidity_min_div").innerHTML = "Please enter a valid number or 0";
                                document.getElementById("humidity_min_div").style.color="Red";
                                return;
                    }
                    if (reg.test(humidity_max)){
                        document.getElementById("humidity_max_div").innerHTML = "";
                    } else {
                                document.getElementById("humidity_max_form").focus();
                                document.getElementById("humidity_max_div").innerHTML = "Please enter a valid number or 0";
                                document.getElementById("humidity_max_div").style.color="Red";
                                return;
                    }
                    if (reg.test(ventilation_min)){
                        document.getElementById("ventilation_min_div").innerHTML = "";
                    } else {
                                document.getElementById("ventilation_min_form").focus();
                                document.getElementById("ventilation_min_div").innerHTML = "Please enter a valid number or 0";
                                document.getElementById("ventilation_min_div").style.color="Red";
                                return;
                    }
                    if (reg.test(ventilation_max)){
                        document.getElementById("ventilation_max_div").innerHTML = "";
                    } else {
                                document.getElementById("ventilation_max_form").focus();
                                document.getElementById("ventilation_max_div").innerHTML = "Please enter a valid number or 0";
                                document.getElementById("ventilation_max_div").style.color="Red";
                                return;
                    }

                    dialog.close();
                    var tq_last_row_id = $('#tq_update_table tr:last').attr('id');
                    if (tq_last_row_id == undefined){
                        tq_last_row_id = 0;
                    }

                    $('#tq_update_tbody').append(`<tr class="added_tq_lines" id="${++tq_last_row_id}">
                      <td class="row-index tq_row_index">
                              <p class='form-control'  id="row_count_tq" name="tq_row_id" readonly="readonly" >${tq_last_row_id}</p></td>
                          </input>
                      </td>
                      <td>
                        <input type="text" name="equipment_reference" placeholder="Maximum allowed characters 15" maxlength="35"
                            class='form-control equipment_reference' value="${equipment_reference}" readonly="readonly" id="new_update_eq_id_${tq_last_row_id}"/>
                      </td>
                      <td>
                        <input type="text" name="new_wt_unit_update_tq" placeholder="Maximum allowed characters 3"
                            class='form-control weight_unit_tq' value="${weight_unit_tq}" readonly="readonly" id="new_wt_unit_update_tq_${tq_last_row_id}"/>
                      </td>
                      <td>
                        <input type="number" name="new_cgw_update_tq"
                            class='form-control cargo_gross_weight' value="${cargo_gross_weight}" readonly="readonly" id="new_cgw_update_tq_${tq_last_row_id}"/>
                      </td>
                      <td>
                        <input type="number" name="new_ctw_update_tq"
                            class='form-control container_tare_weight' value="${container_tare_weight}" readonly="readonly" id="new_ctw_update_tq_${tq_last_row_id}"/>
                      </td>
                      <td>
                        <input type="text" name="new_iso_eq_code_update_tq" placeholder="Maximum allowed characters 4"
                            class='form-control iso_equipment_code' value="${iso_equipment_code}" readonly="readonly" id="new_iso_eq_code_update_tq_${tq_last_row_id}"/>
                      </td>
                      <td>
                        <input type="checkbox" name="new_is_shipper_owned_update_tq" style="pointer-events: none;"
                          class='form-control shipper_owned' value="${shipper_owned_tq}" readonly="readonly" id="new_is_shipper_owned_update_tq_${tq_last_row_id}"/>
                      </td>
                      <td>
                        <input type="number" name="new_temp_min_update_tq"
                            class='form-control temperature_min' value="${temperature_min}" readonly="readonly" id="new_temp_min_update_tq_${tq_last_row_id}"/>
                      </td>
                      <td>
                        <input type="number" name="new_temp_max_update_tq"
                            class='form-control temperature_max' value="${temperature_max}" readonly="readonly" id="new_temp_max_update_tq_${tq_last_row_id}"/>
                      </td>
                      <td>
                        <input type="text" name="new_temp_unit_update_tq" placeholder="Maximum allowed characters 3"
                            class='form-control temperature_unit' value="${temperature_unit}"  readonly="readonly" id="new_temp_unit_update_tq_${tq_last_row_id}"/>
                      </td>
                      <td>
                        <input type="number" name="new_humidity_min_update_tq"
                         class='form-control humidity_min' value="${humidity_min}" readonly="readonly" id="new_humidity_min_update_tq_${tq_last_row_id}"/>
                      </td>
                      <td>
                        <input type="number" name="new_humidity_max_update_tq"
                         class='form-control humidity_max' value="${humidity_max}" readonly="readonly" id="new_humidity_max_update_tq_${tq_last_row_id}"/>
                      </td>
                      <td>
                        <input type="number" name="new_ventilation_min_update_tq"  readonly="readonly"
                         class='form-control ventilation_min' value="${ventilation_min}" id="new_ventilation_min_update_tq_${tq_last_row_id}"/>
                      </td>
                      <td>
                        <input type="number" name="new_ventilation_max_update_tq"  readonly="readonly"
                         class='form-control ventilation_max' value="${ventilation_max}" id="new_ventilation_max_update_tq_${tq_last_row_id}"/>
                      </td>
                      <td>
                        <input type="text" name="new_seal_no_update_tq" placeholder="Maximum allowed characters 15"
                            class='form-control seal_number' value="${seal_number}" readonly="readonly" id="new_seal_no_update_tq_${tq_last_row_id}"/>
                      </td>
                      <td>
                        <input type="text" name="new_seal_source_update_tq" placeholder="Maximum allowed characters 5"
                            class='form-control seal_source' value="${seal_source}" readonly="readonly" id="new_seal_source_update_tq_${tq_last_row_id}"/>
                      </td>
                      <td>
                        <input type="text" name="new_seal_type_update_tq" placeholder="Maximum allowed characters 5"
                            class='form-control seal_type' value="${seal_type}" readonly="readonly" id="new_seal_type_update_tq_${tq_last_row_id}"/>
                      </td>
                      <td>
                        <input type="hidden" name="transport_equipment_array_created_by"
                            class='form-control tq_array_created_by' value="${tq_array_created_by}"
                            id="tq_array_created_by_${tq_last_row_id}"/>
                      </td>
                      <td>
                        <button class="btn btn-primary edit_update_tq" id="edit_update_tq"
                            type="button"><small><i class="fa fa-pencil"></i> </small></button>
                      </td>
                      <td>
                        <button class="btn btn-primary remove_tq_update" id="remove_tq_update"
                            type="button"><small><i class='fa fa-trash-o'></i></small></button>
                      </td>
                   </tr>`);
                   document.getElementById("new_is_shipper_owned_update_tq_"+tq_last_row_id).checked = shipper_owned_tq;
                }
            }],
       });
       dialog.opened().then(function () {
            var update_formtq = document.getElementById('update_formtq');
            for(var i=0; i < update_formtq.elements.length; i++){
                if(update_formtq.elements[i].hasAttribute('required')){
                    update_formtq.elements[i].style.background='#ADD8E6';
                }
            }
            var tq_created_by = document.getElementById("si_updated_by").value;
            document.getElementById("tq_array_created_by_form").value = tq_created_by;

            var update_cont_id = document.getElementById("update_cont_id").value;
            document.getElementById("equipment_reference_tq_form").value = update_cont_id;
       });
       dialog.open();
            });

            // Add new line on Cargo Items
            $('#shipping_instructions_update_form .update_cargo_item_div')
                .off('click')
                .click(function (ev) {
                    var self = this;
                    var dialog = new Dialog(this, {
                    title: _t("Shipping Instruction - Cargo Items"),
                    $content: $(qweb.render('freightbox.update_cargo_item_popup')),
                    buttons: [{
                        text: _t('Add'),
                        classes: "btn-primary",
                        close: false,
                        click: function () {
                                var cargo_line_item_id = document.getElementById("cargo_line_item_id_form").value;
                                var cargo_shipping_marks = document.getElementById("shipping_marks_form").value;
                                var description_of_goods = document.getElementById("description_of_goods_form").value;
                                var carrier_booking_reference = document.getElementById("carrier_booking_reference_form").value;
                                var hs_code = document.getElementById("hs_code_form").value;
                                var no_of_packages = document.getElementById("no_of_packages_form").value;
                                var weight = document.getElementById("weight_form").value;
                                var volume = document.getElementById("volume_form").value;
                                var weight_unit = document.getElementById("weight_unit_form").value;
                                var volume_unit = document.getElementById("volume_unit_form").value;
                                var package_code = document.getElementById("package_code_form").value;
                                var equipment_reference = document.getElementById("equipment_reference_form").value;
                                var cargo_created_by = document.getElementById("cargo_array_created_by_form").value;

                                var add_ci_form = document.getElementById('add_ci_form');
                                    for(var i=0; i < add_ci_form.elements.length; i++){
                                        if(add_ci_form.elements[i].value === '' && add_ci_form.elements[i].hasAttribute('required')){
                                            if (cargo_line_item_id == ""){
                                                 document.getElementById("cargo_line_item_id_form").focus();
                                                 document.getElementById("cargo_line_item_id_div").innerHTML = "Please fill this field";
                                                 document.getElementById("cargo_line_item_id_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("cargo_line_item_id_div").innerHTML = "";
                                            }

                                            if (cargo_shipping_marks == ""){
                                                 document.getElementById("shipping_marks_form").focus();
                                                 document.getElementById("shipping_marks_div").innerHTML = "Please fill this field";
                                                 document.getElementById("shipping_marks_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("shipping_marks_div").innerHTML = "";
                                            }
                                            if (description_of_goods == ""){
                                                 document.getElementById("description_of_goods_form").focus();
                                                 document.getElementById("description_of_goods_div").innerHTML = "Please fill this field";
                                                 document.getElementById("description_of_goods_div").style.color="Red";
                                                 return;
                                            } else {
                                                 document.getElementById("description_of_goods_div").innerHTML = "";
                                            }
                                            if (hs_code == ""){
                                                 document.getElementById("hs_code_form").focus();
                                                 document.getElementById("hs_code_div").innerHTML = "Please fill this field";
                                                 document.getElementById("hs_code_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("hs_code_div").innerHTML = "";
                                            }
                                            if (no_of_packages == ""){
                                                 document.getElementById("no_of_packages_form").focus();
                                                 document.getElementById("no_of_packages_div").innerHTML = "Please fill this field";
                                                 document.getElementById("no_of_packages_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("no_of_packages_div").innerHTML = "";
                                            }
                                            if (weight == ""){
                                                 document.getElementById("weight_form").focus();
                                                 document.getElementById("weight_div").innerHTML = "Please enter number";
                                                 document.getElementById("weight_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("weight_div").innerHTML = "";
                                            }
                                            if (weight_unit == ""){
                                                 document.getElementById("weight_unit_form").focus();
                                                 document.getElementById("weight_unit_div").innerHTML = "Please fill this field";
                                                 document.getElementById("weight_unit_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("weight_unit_div").innerHTML = "";
                                            }
                                            if (package_code == ""){
                                                 document.getElementById("package_code_form").focus();
                                                 document.getElementById("package_code_div").innerHTML = "Please fill this field";
                                                 document.getElementById("package_code_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("package_code_div").innerHTML = "";
                                            }
                                            if (equipment_reference == ""){
                                                  document.getElementById("equipment_reference_form").focus();
                                                 document.getElementById("equipment_reference_div").innerHTML = "Please fill this field";
                                                 document.getElementById("equipment_reference_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("equipment_reference_div").innerHTML = "";
                                            }
                                            if (cargo_created_by == ""){
                                                  document.getElementById("cargo_array_created_by_form").focus();
                                                 document.getElementById("cargo_array_created_by_div").innerHTML = "Please fill this field";
                                                 document.getElementById("cargo_array_created_by_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("cargo_array_created_by_div").innerHTML = "";
                                            }
                                        }
                                    }
                                    if (no_of_packages != ""){
                                        var regex = /^\d*[]?\d*$/;
                                        if(regex.test(no_of_packages)){
                                            document.getElementById("no_of_packages_div").innerHTML = "";
                                        } else{
                                             document.getElementById("no_of_packages_form").focus();
                                             document.getElementById("no_of_packages_div").innerHTML = "Please enter a valid number";
                                             document.getElementById("no_of_packages_div").style.color="Red";
                                             return;
                                        }
                                    }
                                    dialog.close();
                                    var cargo_last_row_id = $('#cargo_table_update_si tr:last').attr('id');
                                    if (cargo_last_row_id == undefined){
                                        cargo_last_row_id = 0;
                                    }

                                    $('#cargo_tbody_update_si').append(`<tr class="added_cargo_update_si" id="${++cargo_last_row_id}">
                                          <td class="row-index">
                                                  <p class='form-control'  id="update_row_id_${cargo_last_row_id}" readonly="readonly"
                                                   name="row_count" >${cargo_last_row_id}</p></td>
                                              </input>
                                          </td>
                                          <td>
                                              <input type="text" name="cargo_line_items_id"  readonly="readonly"
                                              id="update_cargo_line_items_id_${cargo_last_row_id}"
                                              value="${cargo_line_item_id}" class='form-control cargo_line_item_id'  />
                                          </td>
                                          <td id="td3" style="border-right: 1px solid black;">
                                              <input type="text" name="shipping_marks" readonly="readonly"
                                                  id="update_shipping_marks_id_${cargo_last_row_id}"
                                                  value="${cargo_shipping_marks}"  class='form-control shipping_marks'/>
                                          </td>
                                          <td>
                                              <input type="text" name="carrier_booking_reference" readonly="readonly"
                                                 id="update_carrier_booking_reference_id_${cargo_last_row_id}" value="${carrier_booking_reference}"
                                                 maxlength="35" placeholder="Maximum allowed characters 35" class='form-control carrier_booking_reference'/>
                                          </td>
                                          <td>
                                              <input type="text" name="description_of_goods" readonly="readonly"
                                                 id="update_description_of_goods_id_${cargo_last_row_id}" maxlength="250"
                                                 value="${description_of_goods}"
                                                 placeholder="Maximum allowed characters 250"  class='form-control description_of_goods'/>
                                          </td>
                                          <td>
                                              <input type="text" name="hs_code"
                                                 id="update_hs_code_id_${cargo_last_row_id}" maxlength="10"
                                                 value="${hs_code}" readonly="readonly"
                                                 placeholder="Maximum allowed characters 10"  class='form-control hs_code'/>
                                          </td>
                                          <td>
                                              <input type="number" name="no_of_packages" readonly="readonly"
                                                 id="update_number_of_packages_id_${cargo_last_row_id}"
                                                 value="${no_of_packages}"  class='form-control no_of_packages'/>
                                          </td>
                                          <td>
                                              <input type="number" name="weight" readonly="readonly"
                                                 id="update_weight_id_${cargo_last_row_id}"
                                                 value="${weight}" class='form-control weight'/>
                                          </td>
                                          <td>
                                              <input type="number" name="volume" readonly="readonly"
                                                 id="update_volume_id_${cargo_last_row_id}" value="${volume}" class='form-control volume'/>
                                          </td>
                                          <td>
                                              <input type="text" name="weight_unit" readonly="readonly"
                                                 id="update_weight_unit_id_${cargo_last_row_id}" maxlength="3"
                                                 value="${weight_unit}"
                                                 placeholder="Maximum allowed characters 3" class='form-control weight_unit'/>
                                          </td>
                                          <td>
                                              <input type="text" name="volume_unit" readonly="readonly"
                                                 id="update_volume_unit_id_${cargo_last_row_id}" maxlength="3"
                                                 value="${volume_unit}"
                                                 placeholder="Maximum allowed characters 3"  class='form-control volume_unit'/>
                                          </td>
                                          <td>
                                              <input type="text" name="package_code" readonly="readonly"
                                                 id="update_package_code_id_${cargo_last_row_id}" maxlength="3"
                                                 value="${package_code}" placeholder="Maximum allowed characters 3" class='form-control package_code'/>
                                          </td>
                                          <td>
                                              <input type="text" name="equipment_reference" readonly="readonly"
                                                 id="update_equipment_reference_id_${cargo_last_row_id}" maxlength="15"
                                                 value="${equipment_reference}" readonly="readonly"
                                                 placeholder="Maximum allowed characters 15"  class='form-control equipment_reference'/>
                                          </td>
                                          <td>
                                              <input type="hidden" name="cargo_array_created_by"
                                                 id="cargo_array_created_by_${cargo_last_row_id}"
                                                 value="${cargo_created_by}"
                                                 class='form-control cargo_created_by'/>
                                          </td>
                                          <td>
                                            <button class="btn btn-primary edit_added_cargo_item" id="edit_added_cargo_item"
                                                type="button"><small><i class="fa fa-pencil"></i> </small></button>
                                          </td>
                                          <td>
                                            <button class="btn btn-primary remove_cargo_update" id="remove_cargo_update"
                                                type="button"><small><i class='fa fa-trash-o'></i></small></button>
                                          </td>

                                       </tr>`);
                                    }
                                }],
                            });
                            dialog.opened().then(function () {
                                var add_ci_form = document.getElementById('add_ci_form');
                                    for(var i=0; i < add_ci_form.elements.length; i++){
                                        if(add_ci_form.elements[i].hasAttribute('required')){
                                            add_ci_form.elements[i].style.background='#ADD8E6';
                                        }
                                    }
                                var si_created_by = document.getElementById("si_created_by").value;
                                document.getElementById("cargo_array_created_by_form").value = si_created_by;

                                var cbr = document.getElementById("carrier_booking_reference_update").value;
                                document.getElementById("carrier_booking_reference_form").value = cbr;

                                var update_cont_id = document.getElementById("update_cont_id").value;
                                document.getElementById("equipment_reference_form").value = update_cont_id;
                            });
                            dialog.open();

            });

            // Edit/view References
            $('#rc_update_tbody').on('click', '.rc_view_update', function () {
                var child = $(this).closest('tr');
                child.each(function () {
                    var id = $(this).attr('id');
                    var dialog = new Dialog(this, {
                        title: _t("Update Shipping Instruction - References"),
                        $content: $(qweb.render('freightbox.update_rc_values_popup')),
                        buttons: [{
                            text: _t('Update'),
                            classes: "btn-primary",
                            close: false,
                            click: function () {
                                // Update Reference Type
                                var reference_type_update_approved_form = document.getElementById("reference_type_update_approved_form");
                                var new_reference_type_form = document.getElementById("new_reference_type_form").value;
                                var old_reference_type_form = document.getElementById("old_reference_type_form").value;

                                if(reference_type_update_approved_form.checked == true){
                                    if(new_reference_type_form != "" && document.getElementById("new_reference_type_form").hasAttribute('required')){
                                        document.getElementById("new_reference_type_update_rc_"+id).value = new_reference_type_form;
                                        document.getElementById("reference_type_update_val_approved_"+id).value = true;
                                        document.getElementById("new_reference_type_update_rc_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_reference_type_form_div").innerHTML = "";
                                    } else {
                                        if (new_reference_type_form == "" && reference_type_update_approved_form.checked == true){
                                             document.getElementById("new_reference_type_form").focus();
                                             document.getElementById("new_reference_type_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_reference_type_form_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("new_reference_type_update_rc_"+id).value = old_reference_type_form;
                                        document.getElementById("reference_type_update_val_approved_"+id).value = false;
                                        document.getElementById("new_reference_type_update_rc_"+id).style.background='#FFFFFF';
                                        return;
                                    }
                                }

                                // Update Reference Value
                                var reference_value_update_approved_form = document.getElementById("reference_value_update_approved_form");
                                var new_reference_value_form = document.getElementById("new_reference_value_form").value;
                                var old_reference_value_form = document.getElementById("old_reference_value_form").value;

                                if(reference_value_update_approved_form.checked == true){
                                    if(new_reference_value_form != "" && document.getElementById("new_reference_value_form").hasAttribute('required')){
                                        document.getElementById("new_reference_value_update_rc_"+id).value = new_reference_value_form;
                                        document.getElementById("reference_value_update_val_approved_"+id).value = true;
                                        document.getElementById("new_reference_value_update_rc_"+id).style.background='#ADD8E6';
                                    } else {
                                        if (new_reference_value_form == "" && reference_value_update_approved_form.checked == true) {
                                            document.getElementById("new_reference_value_form").focus();
                                             document.getElementById("new_reference_value_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_reference_value_form_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("new_reference_value_update_rc_"+id).value = old_reference_value_form;
                                        document.getElementById("reference_value_update_val_approved_"+id).value = false;
                                        document.getElementById("new_reference_value_update_rc_"+id).style.background='#FFFFFF';
                                        return;
                                    }
                                }

                                var update_rc_form = document.getElementById('update_rc_form');
                                /*for(var i=0; i < update_rc_form.elements.length; i++){
                                    if(update_rc_form.elements[i].value === '' && update_rc_form.elements[i].hasAttribute('required')){
                                        if (new_reference_type_form == "" && reference_type_update_approved_form.checked == true){
                                             document.getElementById("new_reference_type_form").focus();
                                             document.getElementById("new_reference_type_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_reference_type_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_reference_type_form_div").innerHTML = "";
                                        }
                                        if (new_reference_value_form == "" && reference_value_update_approved_form.checked == true) {
                                            document.getElementById("new_reference_value_form").focus();
                                             document.getElementById("new_reference_value_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_reference_value_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_reference_value_form_div").innerHTML = "";
                                        }
                                    }
                                }*/
                                dialog.close();
                            }
                        }],
                    });
                    dialog.opened().then(function () {

                        var update_rc_form = document.getElementById('update_rc_form');
                        for(var i=0; i < update_rc_form.elements.length; i++){
                            if(update_rc_form.elements[i].hasAttribute('required')){
                                update_rc_form.elements[i].style.background='#ADD8E6';
                            }
                        }
                        var update_rc_row_id_form = document.getElementById("rc_update_row_id_"+id).value;
                        document.getElementById("update_rc_row_id_form").value = update_rc_row_id_form;



                        // Update Created By value
                        var si_created_by_val = document.getElementById("si_created_by").value;
                        document.getElementById("update_reference_type_created_by").value = si_created_by_val;
                        document.getElementById("update_reference_value_created_by").value = si_created_by_val;
                        // Set modified by - but still user can edit
                        document.getElementById("update_reference_type_modify_by").value = si_created_by_val;
                        document.getElementById("update_reference_value_modify_by").value = si_created_by_val;

                        // update Reference Type
                        // old value
                        var old_reference_type_form = document.getElementById("old_reference_type_update_rc_"+id).value;
                        document.getElementById("old_reference_type_form").value = old_reference_type_form;
                        // new value
                        var new_reference_type_form = document.getElementById("new_reference_type_update_rc_"+id).value;
                        if (old_reference_type_form === new_reference_type_form){
                            document.getElementById("new_reference_type_form").value = "";
                        } else{
                            document.getElementById("new_reference_type_form").value = new_reference_type_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var reference_type_update_val_approved = document.getElementById("reference_type_update_val_approved_"+id).value;
                        var reference_type_update_approved_form = document.getElementById("reference_type_update_approved_form");
                        if (reference_type_update_val_approved == "true"){
                            reference_type_update_approved_form.checked = true;
                        } else {
                            reference_type_update_approved_form.checked = false;
                        }

                        // update Reference Value
                        // old value
                        var old_reference_value_form = document.getElementById("old_reference_value_update_rc_"+id).value;
                        document.getElementById("old_reference_value_form").value = old_reference_value_form;
                        // new value
                        var new_reference_value_form = document.getElementById("new_reference_value_update_rc_"+id).value;
                        if (old_reference_value_form === new_reference_value_form){
                            document.getElementById("new_reference_value_form").value = "";
                        } else{
                            document.getElementById("new_reference_value_form").value = new_reference_value_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var reference_value_update_val_approved = document.getElementById("reference_value_update_val_approved_"+id).value;
                        var reference_value_update_approved_form = document.getElementById("reference_value_update_approved_form");
                        if (reference_value_update_val_approved == "true"){
                            reference_value_update_approved_form.checked = true;
                        } else {
                            reference_value_update_approved_form.checked = false;
                        }
                    });
                    dialog.open();
                });
            });

            // Edit/view Shipment Locations
            $('#sl_update_tbody').on('click', '.sl_view_update', function () {
                var child = $(this).closest('tr');
                child.each(function () {
                    var id = $(this).attr('id');
                    var dialog = new Dialog(this, {
                        title: _t("Update Shipping Instruction - Shipment Locations"),
                        $content: $(qweb.render('freightbox.update_sl_values_popup')),
                        buttons: [{
                            text: _t('Update'),
                            classes: "btn-primary",
                            close: false,
                            click: function () {
                                // Update Location Type
                                var location_type_update_approved_form = document.getElementById("location_type_update_approved_form");
                                var new_location_type_form = document.getElementById("new_location_type_form").value;
                                var old_location_type_form = document.getElementById("old_location_type_form").value;

                                if(location_type_update_approved_form.checked == true){
                                    if(new_location_type_form != "" && document.getElementById("new_location_type_form").hasAttribute('required')){
                                        document.getElementById("new_location_type_update_sl_"+id).value = new_location_type_form;
                                        document.getElementById("location_type_update_val_approved_"+id).value = true;
                                        document.getElementById("new_location_type_update_sl_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_location_type_form_div").innerHTML = "";
                                    } else {
                                        if (new_location_type_form == "" && location_type_update_approved_form.checked == true){
                                             document.getElementById("new_location_type_form").focus();
                                             document.getElementById("new_location_type_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_location_type_form_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("new_location_type_update_sl_"+id).value = old_location_type_form;
                                        document.getElementById("location_type_update_val_approved_"+id).value = false;
                                        document.getElementById("new_location_type_update_sl_"+id).style.background='#FFFFFF';
                                        return;
                                    }
                                }

                                // Update Location Name
                                var location_name_update_approved_form = document.getElementById("location_name_update_approved_form");
                                var new_location_name_form = document.getElementById("new_location_name_form").value;
                                var old_location_name_form = document.getElementById("old_location_name_form").value;

                                if(location_name_update_approved_form.checked == true){
                                     if(new_location_name_form != "" && document.getElementById("new_location_name_form").hasAttribute('required')){
                                        document.getElementById("new_location_name_update_sl_"+id).value = new_location_name_form;
                                        document.getElementById("location_name_update_val_approved_"+id).value = true;
                                        document.getElementById("new_location_name_update_sl_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_location_name_form_div").innerHTML = "";
                                    } else {
                                        if (new_location_name_form == "" && location_name_update_approved_form.checked == true) {
                                            if ( (new_location_type_form === "POL" || new_location_type_form === "POD") && location_name_update_approved_form.checked == true){
                                                 document.getElementById("new_location_name_form").focus();
                                                 document.getElementById("new_location_name_form_div").innerHTML = "Please fill this field";
                                                 document.getElementById("new_location_name_form_div").style.color="Red";
                                                 return;
                                                 }
                                            }
//                                        document.getElementById("new_location_name_update_sl_"+id).value = old_location_name_form;
//                                        document.getElementById("location_name_update_val_approved_"+id).value = false;
//                                        document.getElementById("new_location_name_update_sl_"+id).style.background='#FFFFFF';
//                                        return;
                                    }
                                }

                                // Update Latitude
                                var latitude_update_approved_form = document.getElementById("latitude_update_approved_form");
                                var new_latitude_form = document.getElementById("new_latitude_form").value;
                                var old_latitude_form = document.getElementById("old_latitude_form").value;

                                if(latitude_update_approved_form.checked == true){
                                    if(new_latitude_form != "" && document.getElementById("new_latitude_form").hasAttribute('required')){
                                        document.getElementById("new_latitude_update_sl_"+id).value = new_latitude_form;
                                        document.getElementById("latitude_update_val_approved_"+id).value = true;
                                        document.getElementById("new_latitude_update_sl_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_latitude_form_div").innerHTML = "";
                                    } else {
                                        if (new_latitude_form == "" && latitude_update_approved_form.checked == true) {
                                            if ( (new_location_type_form === "POL" || new_location_type_form === "POD") && latitude_update_approved_form.checked == true){
                                                 document.getElementById("new_latitude_form").focus();
                                                 document.getElementById("new_latitude_form_div").innerHTML = "Please fill this field";
                                                 document.getElementById("new_latitude_form_div").style.color="Red";
                                                 return;
                                             }
                                        }
//                                        document.getElementById("new_latitude_update_sl_"+id).value = old_latitude_form;
//                                        document.getElementById("latitude_update_val_approved_"+id).value = false;
//                                        document.getElementById("new_latitude_update_sl_"+id).style.background='#FFFFFF';
                                    }
                                }

                                // Update Longitude
                                var longitude_update_approved_form = document.getElementById("longitude_update_approved_form");
                                var new_longitude_form = document.getElementById("new_longitude_form").value;
                                var old_longitude_form = document.getElementById("old_longitude_form").value;

                                if(longitude_update_approved_form.checked == true){
                                    if(new_longitude_form != "" && document.getElementById("new_longitude_form").hasAttribute('required')){
                                        document.getElementById("new_longitude_update_sl_"+id).value = new_longitude_form;
                                        document.getElementById("longitude_update_val_approved_"+id).value = true;
                                        document.getElementById("new_longitude_update_sl_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_longitude_form_div").innerHTML = "";
                                    } else {
                                        if (new_longitude_form == "" && longitude_update_approved_form.checked == true) {
                                            if ( (new_location_type_form === "POL" || new_location_type_form === "POD") && longitude_update_approved_form.checked == true){
                                            document.getElementById("new_longitude_form").focus();
                                             document.getElementById("new_longitude_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_longitude_form_div").style.color="Red";
                                             return;
                                             }
                                        }
//                                        document.getElementById("new_longitude_update_sl_"+id).value = old_longitude_form;
//                                        document.getElementById("longitude_update_val_approved_"+id).value = false;
//                                        document.getElementById("new_longitude_update_sl_"+id).style.background='#FFFFFF';
                                    }
                                }

                                // Update UN Location Code
                                var un_location_code_update_approved_form = document.getElementById("un_location_code_update_approved_form");
                                var new_un_location_code_form = document.getElementById("new_un_location_code_form").value;
                                var old_un_location_code_form = document.getElementById("old_un_location_code_form").value;

                                if(un_location_code_update_approved_form.checked == true){
                                    if(new_un_location_code_form != "" && document.getElementById("new_un_location_code_form").hasAttribute('required')){
                                        document.getElementById("new_un_location_code_update_sl_"+id).value = new_un_location_code_form;
                                        document.getElementById("un_location_code_update_val_approved_"+id).value = true;
                                        document.getElementById("new_un_location_code_update_sl_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_un_location_code_form_div").innerHTML = "";
                                    } else {
                                        if (new_un_location_code_form == "" && un_location_code_update_approved_form.checked == true) {
                                            if ( (new_location_type_form === "POL" || new_location_type_form === "POD") && un_location_code_update_approved_form.checked == true){
                                            document.getElementById("new_un_location_code_form").focus();
                                             document.getElementById("new_un_location_code_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_un_location_code_form_div").style.color="Red";
                                             return;
                                             }
                                        }
//                                        document.getElementById("new_un_location_code_update_sl_"+id).value = old_un_location_code_form;
//                                        document.getElementById("un_location_code_update_val_approved_"+id).value = false;
//                                        document.getElementById("new_un_location_code_update_sl_"+id).style.background='#FFFFFF';
                                    }
                                }

                                // Update Street Name
                                var street_name_update_approved_form = document.getElementById("street_name_update_approved_form");
                                var new_street_name_form = document.getElementById("new_street_name_form").value;
                                var old_street_name_form = document.getElementById("old_street_name_form").value;

                                if(street_name_update_approved_form.checked == true){
                                    if(new_street_name_form != "" && document.getElementById("new_street_name_form").hasAttribute('required')){
                                        document.getElementById("new_street_name_code_update_sl_"+id).value = new_street_name_form;
                                        document.getElementById("street_name_update_val_approved_"+id).value = true;
                                        document.getElementById("new_street_name_code_update_sl_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_street_name_form_div").innerHTML = "";
                                    } else {
                                        if (new_street_name_form == "" && street_name_update_approved_form.checked == true) {
                                            if ( (new_location_type_form === "POL" || new_location_type_form === "POD") && street_name_update_approved_form.checked == true){
                                                 document.getElementById("new_street_name_form").focus();
                                                 document.getElementById("new_street_name_form_div").innerHTML = "Please fill this field";
                                                 document.getElementById("new_street_name_form_div").style.color="Red";
                                                 return;
                                             }
                                        }
//                                        document.getElementById("new_street_name_code_update_sl_"+id).value = old_street_name_form;
//                                        document.getElementById("street_name_update_val_approved_"+id).value = false;
//                                        document.getElementById("new_street_name_code_update_sl_"+id).style.background='#FFFFFF';
                                    }
                                }

                                // Update Street Number
                                var street_no_update_approved_form = document.getElementById("street_no_update_approved_form");
                                var new_street_no_form = document.getElementById("new_street_no_form").value;
                                var old_street_no_form = document.getElementById("old_street_no_form").value;

                                if(street_no_update_approved_form.checked == true){
                                    if(new_street_no_form != "" && document.getElementById("new_street_no_form").hasAttribute('required')){
                                        document.getElementById("new_street_number_code_update_sl_"+id).value = new_street_no_form;
                                        document.getElementById("street_number_update_val_approved_"+id).value = true;
                                        document.getElementById("new_street_number_code_update_sl_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_street_no_form_div").innerHTML = "";
                                    } else {
                                        if (new_street_no_form == "" && street_no_update_approved_form.checked == true) {
                                            if ( (new_location_type_form === "POL" || new_location_type_form === "POD") && street_no_update_approved_form.checked == true){
                                            document.getElementById("new_street_no_form").focus();
                                             document.getElementById("new_street_no_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_street_no_form_div").style.color="Red";
                                             return;
                                             }
                                        }
//                                        document.getElementById("new_street_number_code_update_sl_"+id).value = old_street_no_form;
//                                        document.getElementById("street_number_update_val_approved_"+id).value = false;
//                                        document.getElementById("new_street_number_code_update_sl_"+id).style.background='#FFFFFF';
                                    }
                                }

                                // Update Floor
                                var floor_update_approved_form = document.getElementById("floor_update_approved_form");
                                var new_floor_form = document.getElementById("new_floor_form").value;
                                var old_floor_form = document.getElementById("old_floor_form").value;

                                if(floor_update_approved_form.checked == true){
                                    if(new_floor_form != "" && document.getElementById("new_floor_form").hasAttribute('required')){
                                        document.getElementById("new_floor_update_sl_"+id).value = new_floor_form;
                                        document.getElementById("floor_update_val_approved_"+id).value = true;
                                        document.getElementById("new_floor_update_sl_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_floor_form_div").innerHTML = "";
                                    } else {
                                        if (new_floor_form == "" && floor_update_approved_form.checked == true) {
                                            if ( (new_location_type_form === "POL" || new_location_type_form === "POD") && floor_update_approved_form.checked == true){
                                             document.getElementById("new_floor_form").focus();
                                             document.getElementById("new_floor_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_floor_form_div").style.color="Red";
                                             return;
                                             }
                                        }
//                                        document.getElementById("new_floor_update_sl_"+id).value = old_floor_form;
//                                        document.getElementById("floor_update_val_approved_"+id).value = false;
//                                        document.getElementById("new_floor_update_sl_"+id).style.background='#FFFFFF';
                                    }
                                }

                                // Update Post Code
                                var post_code_update_approved_form = document.getElementById("post_code_update_approved_form");
                                var new_post_code_form = document.getElementById("new_post_code_form").value;
                                var old_post_code_form = document.getElementById("old_post_code_form").value;

                                if(post_code_update_approved_form.checked == true){
                                    if(new_post_code_form != "" && document.getElementById("new_post_code_form").hasAttribute('required')){
                                        document.getElementById("new_post_code_update_sl_"+id).value = new_post_code_form;
                                        document.getElementById("post_code_update_val_approved_"+id).value = true;
                                        document.getElementById("new_post_code_update_sl_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_post_code_form_div").innerHTML = "";
                                    } else {
                                        if (new_post_code_form == "" && post_code_update_approved_form.checked == true) {
                                            if ( (new_location_type_form === "POL" || new_location_type_form === "POD") && post_code_update_approved_form.checked == true){
                                             document.getElementById("new_post_code_form").focus();
                                             document.getElementById("new_post_code_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_post_code_form_div").style.color="Red";
                                             return;
                                             }
                                        }
//                                        document.getElementById("new_post_code_update_sl_"+id).value = old_post_code_form;
//                                        document.getElementById("post_code_update_val_approved_"+id).value = false;
//                                        document.getElementById("new_post_code_update_sl_"+id).style.background='#FFFFFF';
                                    }
                                }

                                // Update City
                                var city_update_approved_form = document.getElementById("city_update_approved_form");
                                var new_city_form = document.getElementById("new_city_form").value;
                                var old_city_form = document.getElementById("old_city_form").value;

                                if(city_update_approved_form.checked == true){
                                    if(new_city_form != "" && document.getElementById("new_city_form").hasAttribute('required')){
                                        document.getElementById("new_city_name_update_sl_"+id).value = new_city_form;
                                        document.getElementById("city_name_update_val_approved_"+id).value = true;
                                        document.getElementById("new_city_name_update_sl_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_city_form_div").innerHTML = "";
                                    } else {
                                        if (new_city_form == "" && city_update_approved_form.checked == true) {
                                            if ( (new_location_type_form === "POL" || new_location_type_form === "POD") && city_update_approved_form.checked == true){
                                             document.getElementById("new_city_form").focus();
                                             document.getElementById("new_city_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_city_form_div").style.color="Red";
                                             return;
                                             }
                                        }
//                                        document.getElementById("new_city_name_update_sl_"+id).value = old_city_form;
//                                        document.getElementById("city_name_update_val_approved_"+id).value = false;
//                                        document.getElementById("new_city_name_update_sl_"+id).style.background='#FFFFFF';
                                    }
                                }

                                // Update State Region
                                var state_region_update_approved_form = document.getElementById("state_region_update_approved_form");
                                var new_state_region_form = document.getElementById("new_state_region_form").value;
                                var old_state_region_form = document.getElementById("old_state_region_form").value;

                                if(state_region_update_approved_form.checked == true){
                                    if(new_state_region_form != "" && document.getElementById("new_state_region_form").hasAttribute('required')){
                                        document.getElementById("new_state_region_update_sl_"+id).value = new_state_region_form;
                                        document.getElementById("state_region_update_val_approved_"+id).value = true;
                                        document.getElementById("new_state_region_update_sl_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_state_region_form_div").innerHTML = "";
                                    } else {
                                        if (new_state_region_form == "" && state_region_update_approved_form.checked == true) {
                                            if ( (new_location_type_form === "POL" || new_location_type_form === "POD") && state_region_update_approved_form.checked == true){
                                             document.getElementById("new_state_region_form").focus();
                                             document.getElementById("new_state_region_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_state_region_form_div").style.color="Red";
                                             return;

                                             }
                                        }
//                                        document.getElementById("new_state_region_update_sl_"+id).value = old_state_region_form;
//                                        document.getElementById("state_region_update_val_approved_"+id).value = false;
//                                        document.getElementById("new_state_region_update_sl_"+id).style.background='#FFFFFF';
                                    }
                                }

                                // Update Country
                                var country_update_approved_form = document.getElementById("country_update_approved_form");
                                var new_country_form = document.getElementById("new_country_form").value;
                                var old_country_form = document.getElementById("old_country_form").value;

                                if(country_update_approved_form.checked == true){
                                    if(new_country_form != "" && document.getElementById("new_country_form").hasAttribute('required')){
                                        document.getElementById("new_country_update_sl_"+id).value = new_country_form;
                                        document.getElementById("country_update_val_approved_"+id).value = true;
                                        document.getElementById("new_country_update_sl_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_country_form_div").innerHTML = "";
                                    } else {
                                        if (new_country_form == "" && country_update_approved_form.checked == true) {
                                            if ( (new_location_type_form === "POL" || new_location_type_form === "POD") && country_update_approved_form.checked == true){
                                             document.getElementById("new_country_form").focus();
                                             document.getElementById("new_country_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_country_form_div").style.color="Red";
                                             return;
                                             }
                                        }
//                                        document.getElementById("new_country_update_sl_"+id).value = old_country_form;
//                                        document.getElementById("country_update_val_approved_"+id).value = false;
//                                        document.getElementById("new_country_update_sl_"+id).style.background='#FFFFFF';
                                    }
                                }

                                // Update Displayed Name
                                var displayed_name_update_approved_form = document.getElementById("displayed_name_update_approved_form");
                                var new_displayed_name_form = document.getElementById("new_displayed_name_form").value;
                                var old_displayed_name_form = document.getElementById("old_displayed_name_form").value;

                                if(displayed_name_update_approved_form.checked == true){
                                    document.getElementById("new_displayed_name_update_sl_"+id).value = new_displayed_name_form;
                                    document.getElementById("displayed_name_update_val_approved_"+id).value = true;
                                    document.getElementById("new_displayed_name_update_sl_"+id).style.background='#ADD8E6';
                                } else {
                                    document.getElementById("new_displayed_name_update_sl_"+id).value = old_displayed_name_form;
                                    document.getElementById("displayed_name_update_val_approved_"+id).value = false;
                                    document.getElementById("new_displayed_name_update_sl_"+id).style.background='#FFFFFF';
                                }

                                var update_sl_form = document.getElementById('update_sl_form');
                                /*for(var i=0; i < update_sl_form.elements.length; i++){
                                    if(update_sl_form.elements[i].value === '' && update_sl_form.elements[i].hasAttribute('required')){
                                        *//*if (new_location_type_form == "" && location_type_update_approved_form.checked == true){
                                             document.getElementById("new_location_type_form").focus();
                                             document.getElementById("new_location_type_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_location_type_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_location_type_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_location_name_form == "" && location_name_update_approved_form.checked == true) {
                                            if ( (new_location_type_form === "POL" || new_location_type_form === "POD") && location_name_update_approved_form.checked == true){
                                            document.getElementById("new_location_name_form").focus();
                                             document.getElementById("new_location_name_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_location_name_form_div").style.color="Red";
                                             return;
                                             }
                                        } else {
                                            document.getElementById("new_location_name_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_latitude_form == "" && latitude_update_approved_form.checked == true) {
                                            if ( (new_location_type_form === "POL" || new_location_type_form === "POD") && latitude_update_approved_form.checked == true){
                                            document.getElementById("new_latitude_form").focus();
                                             document.getElementById("new_latitude_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_latitude_form_div").style.color="Red";
                                             return;
                                             }
                                        } else {
                                            document.getElementById("new_latitude_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_longitude_form == "" && longitude_update_approved_form.checked == true) {
                                            if ( (new_location_type_form === "POL" || new_location_type_form === "POD") && longitude_update_approved_form.checked == true){
                                            document.getElementById("new_longitude_form").focus();
                                             document.getElementById("new_longitude_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_longitude_form_div").style.color="Red";
                                             return;
                                             }
                                        } else {
                                            document.getElementById("new_longitude_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_un_location_code_form == "" && un_location_code_update_approved_form.checked == true) {
                                            if ( (new_location_type_form === "POL" || new_location_type_form === "POD") && un_location_code_update_approved_form.checked == true){
                                            document.getElementById("new_un_location_code_form").focus();
                                             document.getElementById("new_un_location_code_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_un_location_code_form_div").style.color="Red";
                                             return;
                                             }
                                        } else {
                                            document.getElementById("new_un_location_code_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_street_name_form == "" && street_name_update_approved_form.checked == true) {
                                            if ( (new_location_type_form === "POL" || new_location_type_form === "POD") && street_name_update_approved_form.checked == true){
                                            document.getElementById("new_street_name_form").focus();
                                             document.getElementById("new_street_name_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_street_name_form_div").style.color="Red";
                                             return;
                                             }
                                        } else {
                                            document.getElementById("new_street_name_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_street_no_form == "" && street_no_update_approved_form.checked == true) {
                                            if ( (new_location_type_form === "POL" || new_location_type_form === "POD") && street_no_update_approved_form.checked == true){
                                            document.getElementById("new_street_no_form").focus();
                                             document.getElementById("new_street_no_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_street_no_form_div").style.color="Red";
                                             return;
                                             }
                                        } else {
                                            document.getElementById("new_street_no_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_floor_form == "" && floor_update_approved_form.checked == true) {
                                            if ( (new_location_type_form === "POL" || new_location_type_form === "POD") && floor_update_approved_form.checked == true){
                                             document.getElementById("new_floor_form").focus();
                                             document.getElementById("new_floor_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_floor_form_div").style.color="Red";
                                             return;
                                             }
                                        } else {
                                            document.getElementById("new_floor_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_post_code_form == "" && post_code_update_approved_form.checked == true) {
                                            if ( (new_location_type_form === "POL" || new_location_type_form === "POD") && post_code_update_approved_form.checked == true){
                                             document.getElementById("new_post_code_form").focus();
                                             document.getElementById("new_post_code_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_post_code_form_div").style.color="Red";
                                             return;
                                             }
                                        } else {
                                            document.getElementById("new_post_code_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_city_form == "" && city_update_approved_form.checked == true) {
                                            if ( (new_location_type_form === "POL" || new_location_type_form === "POD") && city_update_approved_form.checked == true){
                                             document.getElementById("new_city_form").focus();
                                             document.getElementById("new_city_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_city_form_div").style.color="Red";
                                             return;
                                             }
                                        } else {
                                            document.getElementById("new_city_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_state_region_form == "" && state_region_update_approved_form.checked == true) {
                                            if ( (new_location_type_form === "POL" || new_location_type_form === "POD") && state_region_update_approved_form.checked == true){
                                             document.getElementById("new_state_region_form").focus();
                                             document.getElementById("new_state_region_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_state_region_form_div").style.color="Red";
                                             return;

                                             }
                                        } else {
                                            document.getElementById("new_state_region_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_country_form == "" && country_update_approved_form.checked == true) {
                                            if ( (new_location_type_form === "POL" || new_location_type_form === "POD") && country_update_approved_form.checked == true){
                                             document.getElementById("new_country_form").focus();
                                             document.getElementById("new_country_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_country_form_div").style.color="Red";
                                             return;
                                             }
                                        } else {
                                            document.getElementById("new_country_form_div").innerHTML = "";
                                        }*//*
                                    }
                                }*/
                                if (location_type_update_approved_form.checked == true){

                                if ( (new_location_type_form === "PRE" ||
                                        new_location_type_form === "POL" ||
                                        new_location_type_form === "POD" ||
                                        new_location_type_form === "PDE" ||
                                        new_location_type_form === "PCF" ||
                                        new_location_type_form === "OIR" ||
                                        new_location_type_form === "PSR") && (location_type_update_approved_form.checked == true)) {
                                             document.getElementById("new_location_type_form_div").innerHTML = "";
                                        } else {
                                            document.getElementById("new_location_type_form").value = "";
                                             document.getElementById("new_location_type_form").focus();
                                             document.getElementById("new_location_type_form_div").innerHTML = "Please double click and select any from dropdown";
                                             document.getElementById("new_location_type_form_div").style.color="Red";
                                             return;
                                        }

                                        if ( (new_location_type_form === "POL" ||  new_location_type_form === "POD" ) && (location_type_update_approved_form.checked == true)) {
                                              if (new_location_name_form == ""){
                                                 document.getElementById("new_location_name_form").focus();
                                                 document.getElementById("new_location_name_form_div").innerHTML = "Please fill this field";
                                                 document.getElementById("new_location_name_form_div").style.color="Red";
                                                 document.getElementById("location_name_update_approved_form").checked = true;
                                                 return;
                                              } else {
                                                document.getElementById("new_location_name_form_div").innerHTML = "";
                                              }
                                              if (new_latitude_form == ""){
                                                 document.getElementById("new_latitude_form").focus();
                                                 document.getElementById("new_latitude_form_div").innerHTML = "Please fill this field";
                                                 document.getElementById("new_latitude_form_div").style.color="Red";
                                                 document.getElementById("latitude_update_approved_form").checked = true;
                                                 return;
                                              } else {
                                                document.getElementById("new_latitude_form_div").innerHTML = "";
                                              }
                                              if (new_latitude_form == ""){
                                                 document.getElementById("new_latitude_form").focus();
                                                 document.getElementById("new_latitude_form_div").innerHTML = "Please fill this field";
                                                 document.getElementById("new_latitude_form_div").style.color="Red";
                                                 document.getElementById("latitude_update_approved_form").checked = true;
                                                 return;
                                              } else {
                                                document.getElementById("new_latitude_form_div").innerHTML = "";
                                              }

                                              if (new_longitude_form == ""){
                                                 document.getElementById("new_longitude_form").focus();
                                                 document.getElementById("new_longitude_form_div").innerHTML = "Please fill this field";
                                                 document.getElementById("new_longitude_form_div").style.color="Red";
                                                 document.getElementById("longitude_update_approved_form").checked = true;
                                                 return;
                                              } else {
                                                document.getElementById("new_longitude_form_div").innerHTML = "";
                                              }
                                              if (new_un_location_code_form == ""){
                                                 document.getElementById("new_un_location_code_form").focus();
                                                 document.getElementById("new_un_location_code_form_div").innerHTML = "Please fill this field";
                                                 document.getElementById("new_un_location_code_form_div").style.color="Red";
                                                 document.getElementById("un_location_code_update_approved_form").checked = true;
                                                 return;
                                              } else {
                                                document.getElementById("new_un_location_code_form_div").innerHTML = "";
                                              }
                                              if (new_street_name_form == ""){
                                                 document.getElementById("new_street_name_form").focus();
                                                 document.getElementById("new_street_name_form_div").innerHTML = "Please fill this field";
                                                 document.getElementById("new_street_name_form_div").style.color="Red";
                                                 document.getElementById("street_name_update_approved_form").checked = true;
                                                 return;
                                              } else {
                                                document.getElementById("new_street_name_form_div").innerHTML = "";
                                              }
                                              if (new_street_no_form == ""){
                                                 document.getElementById("new_street_no_form").focus();
                                                 document.getElementById("new_street_no_form_div").innerHTML = "Please fill this field";
                                                 document.getElementById("new_street_no_form_div").style.color="Red";
                                                 document.getElementById("street_no_update_approved_form").checked = true;
                                                 return;
                                              } else {
                                                document.getElementById("new_street_no_form_div").innerHTML = "";
                                              }
                                              if (new_floor_form == ""){
                                                 document.getElementById("new_floor_form").focus();
                                                 document.getElementById("new_floor_form_div").innerHTML = "Please fill this field";
                                                 document.getElementById("new_floor_form_div").style.color="Red";
                                                 document.getElementById("floor_update_approved_form").checked = true;
                                                 return;
                                              } else {
                                                document.getElementById("new_floor_form_div").innerHTML = "";
                                              }
                                              if (new_post_code_form == ""){
                                                 document.getElementById("new_post_code_form").focus();
                                                 document.getElementById("new_post_code_form_div").innerHTML = "Please fill this field";
                                                 document.getElementById("new_post_code_form_div").style.color="Red";
                                                 document.getElementById("post_code_update_approved_form").checked = true;
                                                 return;
                                              } else {
                                                document.getElementById("new_post_code_form_div").innerHTML = "";
                                              }
                                              if (new_city_form == ""){
                                                 document.getElementById("new_city_form").focus();
                                                 document.getElementById("new_city_form_div").innerHTML = "Please fill this field";
                                                 document.getElementById("new_city_form_div").style.color="Red";
                                                 document.getElementById("city_update_approved_form").checked = true;
                                                 return;
                                              } else {
                                                document.getElementById("new_city_form_div").innerHTML = "";
                                              }
                                              if (new_state_region_form == ""){
                                                 document.getElementById("new_state_region_form").focus();
                                                 document.getElementById("new_state_region_form_div").innerHTML = "Please fill this field";
                                                 document.getElementById("new_state_region_form_div").style.color="Red";
                                                 document.getElementById("state_region_update_approved_form").checked = true;
                                                 return;
                                              } else {
                                                document.getElementById("new_state_region_form_div").innerHTML = "";
                                              }
                                              if (new_country_form == ""){
                                                 document.getElementById("new_country_form").focus();
                                                 document.getElementById("new_country_form_div").innerHTML = "Please fill this field";
                                                 document.getElementById("new_country_form_div").style.color="Red";
                                                 document.getElementById("country_update_approved_form").checked = true;
                                                 return;
                                              } else {
                                                document.getElementById("new_country_form_div").innerHTML = "";
                                              }
                                              }
                                        }
                                dialog.close();
                            },
                        }],
                    });
                    dialog.opened().then(function () {

                        var update_sl_form = document.getElementById('update_sl_form');
                        for(var i=0; i < update_sl_form.elements.length; i++){
                            if(update_sl_form.elements[i].hasAttribute('required')){
                                update_sl_form.elements[i].style.background='#ADD8E6';
                            }
                        }

                        $("#new_location_type_form").on('change', function() {
                var loc_type = document.getElementById("new_location_type_form").value;
                document.getElementById("new_location_type_form").value = loc_type;
                /*if (loc_type == "PRE") {
                    document.getElementById("new_location_type_form").value = "PRE";
                }
                if (loc_type == "POL") {
                    document.getElementById("new_location_type_form").value = "POL";
                }
                if (loc_type == "POD") {
                    document.getElementById("new_location_type_form").value = "POD";
                }
                if (loc_type == "PDE") {
                    document.getElementById("new_location_type_form").value = "PDE";
                }
                if (loc_type == "Pre-carriage from (PCF)") {
                    document.getElementById("new_location_type_form").value = "PCF";
                }
                if (loc_type == "Onward Inland Routing (OIR)"){
                    document.getElementById("new_location_type_form").value = "OIR";
                }*/
            });
                        var update_sl_row_id_form = document.getElementById("sl_update_row_id_"+id).value;
                        document.getElementById("update_sl_row_id_form").value = update_sl_row_id_form;

                        // Update Created By value
                        var si_created_by_val = document.getElementById("si_created_by").value;
                        document.getElementById("update_location_type_created_by").value = si_created_by_val;
                        document.getElementById("update_location_name_created_by").value = si_created_by_val;
                        document.getElementById("update_latitude_created_by").value = si_created_by_val;
                        document.getElementById("update_longitude_created_by").value = si_created_by_val;
                        document.getElementById("update_un_location_code_created_by").value = si_created_by_val;
                        document.getElementById("update_street_name_created_by").value = si_created_by_val;
                        document.getElementById("update_street_no_created_by").value = si_created_by_val;
                        document.getElementById("update_floor_created_by").value = si_created_by_val;
                        document.getElementById("update_post_code_created_by").value = si_created_by_val;
                        document.getElementById("update_city_created_by").value = si_created_by_val;
                        document.getElementById("update_state_region_created_by").value = si_created_by_val;
                        document.getElementById("update_country_created_by").value = si_created_by_val;
                        document.getElementById("update_displayed_name_created_by").value = si_created_by_val;

                        // Update modified By value
                        document.getElementById("update_location_type_modify_by").value = si_created_by_val;
                        document.getElementById("update_location_name_modify_by").value = si_created_by_val;
                        document.getElementById("update_latitude_modify_by").value = si_created_by_val;
                        document.getElementById("update_longitude_modify_by").value = si_created_by_val;
                        document.getElementById("update_un_location_code_modify_by").value = si_created_by_val;
                        document.getElementById("update_street_name_modify_by").value = si_created_by_val;
                        document.getElementById("update_street_no_modify_by").value = si_created_by_val;
                        document.getElementById("update_floor_modify_by").value = si_created_by_val;
                        document.getElementById("update_post_code_modify_by").value = si_created_by_val;
                        document.getElementById("update_city_modify_by").value = si_created_by_val;
                        document.getElementById("update_state_region_modify_by").value = si_created_by_val;
                        document.getElementById("update_country_modify_by").value = si_created_by_val;
                        document.getElementById("update_displayed_name_modify_by").value = si_created_by_val;

                        // update Location Type
                        // old value
                        var old_location_type_form = document.getElementById("old_location_type_update_sl_"+id).value;
                        document.getElementById("old_location_type_form").value = old_location_type_form;
                        // new value
                        var new_location_type_form = document.getElementById("new_location_type_update_sl_"+id).value;
                        if (old_location_type_form === new_location_type_form){
                            document.getElementById("new_location_type_form").value = "";
                        } else{
                            document.getElementById("new_location_type_form").value = new_location_type_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var location_type_update_val_approved = document.getElementById("location_type_update_val_approved_"+id).value;
                        var location_type_update_approved_form = document.getElementById("location_type_update_approved_form");
                        if (location_type_update_val_approved == "true"){
                            location_type_update_approved_form.checked = true;
                        } else {
                            location_type_update_approved_form.checked = false;
                        }

                        // update Location Name
                        // old value
                        var old_location_name_form = document.getElementById("old_location_name_update_sl_"+id).value;
                        document.getElementById("old_location_name_form").value = old_location_name_form;
                        // new value
                        var new_location_name_form = document.getElementById("new_location_name_update_sl_"+id).value;
                        if (old_location_name_form === new_location_name_form){
                            document.getElementById("new_location_name_form").value = "";
                        } else{
                            document.getElementById("new_location_name_form").value = new_location_name_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var location_name_update_val_approved = document.getElementById("location_name_update_val_approved_"+id).value;
                        var location_name_update_approved_form = document.getElementById("location_name_update_approved_form");
                        if (location_name_update_val_approved == "true"){
                            location_name_update_approved_form.checked = true;
                        } else {
                            location_name_update_approved_form.checked = false;
                        }

                        // update Latitude
                        // old value
                        var old_latitude_form = document.getElementById("old_latitude_update_sl_"+id).value;
                        document.getElementById("old_latitude_form").value = old_latitude_form;
                        // new value
                        var new_latitude_form = document.getElementById("new_latitude_update_sl_"+id).value;
                        if (old_latitude_form === new_latitude_form){
                            document.getElementById("new_latitude_form").value = "";
                        } else{
                            document.getElementById("new_latitude_form").value = new_latitude_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var latitude_update_val_approved = document.getElementById("latitude_update_val_approved_"+id).value;
                        var latitude_update_approved_form = document.getElementById("latitude_update_approved_form");
                        if (latitude_update_val_approved == "true"){
                            latitude_update_approved_form.checked = true;
                        } else {
                            latitude_update_approved_form.checked = false;
                        }

                        // update Longitude
                        // old value
                        var old_longitude_form = document.getElementById("old_longitude_update_sl_"+id).value;
                        document.getElementById("old_longitude_form").value = old_longitude_form;
                        // new value
                        var new_longitude_form = document.getElementById("new_longitude_update_sl_"+id).value;
                        if (old_longitude_form === new_longitude_form){
                            document.getElementById("new_longitude_form").value = "";
                        } else{
                            document.getElementById("new_longitude_form").value = new_longitude_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var longitude_update_val_approved = document.getElementById("longitude_update_val_approved_"+id).value;
                        var longitude_update_approved_form = document.getElementById("longitude_update_approved_form");
                        if (longitude_update_val_approved == "true"){
                            longitude_update_approved_form.checked = true;
                        } else {
                            longitude_update_approved_form.checked = false;
                        }

                        // update UN Location Code
                        // old value
                        var old_un_location_code_form = document.getElementById("old_un_location_code_update_sl_"+id).value;
                        document.getElementById("old_un_location_code_form").value = old_un_location_code_form;
                        // new value
                        var new_un_location_code_form = document.getElementById("new_un_location_code_update_sl_"+id).value;
                        if (old_un_location_code_form === new_un_location_code_form){
                            document.getElementById("new_un_location_code_form").value = "";
                        } else{
                            document.getElementById("new_un_location_code_form").value = new_un_location_code_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var un_location_code_update_val_approved = document.getElementById("un_location_code_update_val_approved_"+id).value;
                        var un_location_code_update_approved_form = document.getElementById("un_location_code_update_approved_form");
                        if (un_location_code_update_val_approved == "true"){
                            un_location_code_update_approved_form.checked = true;
                        } else {
                            un_location_code_update_approved_form.checked = false;
                        }

                        // update Street Name
                        // old value
                        var old_street_name_form = document.getElementById("old_street_name_update_sl_"+id).value;
                        document.getElementById("old_street_name_form").value = old_street_name_form;
                        // new value
                        var new_street_name_form = document.getElementById("new_street_name_code_update_sl_"+id).value;
                        if (old_street_name_form === new_street_name_form){
                            document.getElementById("new_street_name_form").value = "";
                        } else{
                            document.getElementById("new_street_name_form").value = new_street_name_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var street_name_update_val_approved = document.getElementById("street_name_update_val_approved_"+id).value;
                        var street_name_update_approved_form = document.getElementById("street_name_update_approved_form");
                        if (street_name_update_val_approved == "true"){
                            street_name_update_approved_form.checked = true;
                        } else {
                            street_name_update_approved_form.checked = false;
                        }

                        // update Street Number
                        // old value
                        var old_street_no_form = document.getElementById("old_street_number_update_sl_"+id).value;
                        document.getElementById("old_street_no_form").value = old_street_no_form;
                        // new value
                        var new_street_no_form = document.getElementById("new_street_number_code_update_sl_"+id).value;
                        if (old_street_no_form === new_street_no_form){
                            document.getElementById("new_street_no_form").value = "";
                        } else{
                            document.getElementById("new_street_no_form").value = new_street_no_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var street_number_update_val_approved = document.getElementById("street_number_update_val_approved_"+id).value;
                        var street_no_update_approved_form = document.getElementById("street_no_update_approved_form");
                        if (street_number_update_val_approved == "true"){
                            street_no_update_approved_form.checked = true;
                        } else {
                            street_no_update_approved_form.checked = false;
                        }

                        // update Floor
                        // old value
                        var old_floor_form = document.getElementById("old_floor_update_sl_"+id).value;
                        document.getElementById("old_floor_form").value = old_floor_form;
                        // new value
                        var new_floor_form = document.getElementById("new_floor_update_sl_"+id).value;
                        if (old_floor_form === new_floor_form){
                            document.getElementById("new_floor_form").value = "";
                        } else{
                            document.getElementById("new_floor_form").value = new_floor_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var floor_update_val_approved = document.getElementById("floor_update_val_approved_"+id).value;
                        var floor_update_approved_form = document.getElementById("floor_update_approved_form");
                        if (floor_update_val_approved == "true"){
                            floor_update_approved_form.checked = true;
                        } else {
                            floor_update_approved_form.checked = false;
                        }

                        // update Post Code
                        // old value
                        var old_post_code_form = document.getElementById("old_post_code_update_sl_"+id).value;
                        document.getElementById("old_post_code_form").value = old_post_code_form;
                        // new value
                        var new_post_code_form = document.getElementById("new_post_code_update_sl_"+id).value;
                        if (old_post_code_form === new_post_code_form){
                            document.getElementById("new_post_code_form").value = "";
                        } else{
                            document.getElementById("new_post_code_form").value = new_post_code_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var post_code_update_val_approved = document.getElementById("post_code_update_val_approved_"+id).value;
                        var post_code_update_approved_form = document.getElementById("post_code_update_approved_form");
                        if (post_code_update_val_approved == "true"){
                            post_code_update_approved_form.checked = true;
                        } else {
                            post_code_update_approved_form.checked = false;
                        }

                        // update City
                        // old value
                        var old_city_form = document.getElementById("old_city_name_update_sl_"+id).value;
                        document.getElementById("old_city_form").value = old_city_form;
                        // new value
                        var new_city_form = document.getElementById("new_city_name_update_sl_"+id).value;
                        if (old_city_form === new_city_form){
                            document.getElementById("new_city_form").value = "";
                        } else {
                            document.getElementById("new_city_form").value = new_city_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var city_name_update_val_approved = document.getElementById("city_name_update_val_approved_"+id).value;
                        var city_update_approved_form = document.getElementById("city_update_approved_form");
                        if (city_name_update_val_approved == "true"){
                            city_update_approved_form.checked = true;
                        } else {
                            city_update_approved_form.checked = false;
                        }

                        // update State Region
                        // old value
                        var old_state_region_form = document.getElementById("old_state_region_update_sl_"+id).value;
                        document.getElementById("old_state_region_form").value = old_state_region_form;
                        // new value
                        var new_state_region_form = document.getElementById("new_state_region_update_sl_"+id).value;
                        if (old_state_region_form === new_state_region_form){
                            document.getElementById("new_state_region_form").value = "";
                        } else{
                            document.getElementById("new_state_region_form").value = new_state_region_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var state_region_update_val_approved = document.getElementById("state_region_update_val_approved_"+id).value;
                        var state_region_update_approved_form = document.getElementById("state_region_update_approved_form");
                        if (state_region_update_val_approved == "true"){
                            state_region_update_approved_form.checked = true;
                        } else {
                            state_region_update_approved_form.checked = false;
                        }

                        // update Country
                        // old value
                        var old_country_form = document.getElementById("old_country_update_sl_"+id).value;
                        document.getElementById("old_country_form").value = old_country_form;
                        // new value
                        var new_country_form = document.getElementById("new_country_update_sl_"+id).value;
                        if (old_country_form === new_country_form){
                            document.getElementById("new_country_form").value = "";
                        } else{
                            document.getElementById("new_country_form").value = new_country_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var country_update_val_approved = document.getElementById("country_update_val_approved_"+id).value;
                        var country_update_approved_form = document.getElementById("country_update_approved_form");
                        if (country_update_val_approved == "true"){
                            country_update_approved_form.checked = true;
                        } else {
                            country_update_approved_form.checked = false;
                        }

                        // update Displayed Name
                        // old value
                        var old_displayed_name_form = document.getElementById("old_displayed_name_update_sl_"+id).value;
                        document.getElementById("old_displayed_name_form").value = old_displayed_name_form;
                        // new value
                        var new_displayed_name_form = document.getElementById("new_displayed_name_update_sl_"+id).value;
                        if (old_displayed_name_form === new_displayed_name_form){
                            document.getElementById("new_displayed_name_form").value = "";
                        } else{
                            document.getElementById("new_displayed_name_form").value = new_displayed_name_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var displayed_name_update_val_approved = document.getElementById("displayed_name_update_val_approved_"+id).value;
                        var displayed_name_update_approved_form = document.getElementById("displayed_name_update_approved_form");
                        if (displayed_name_update_val_approved == "true"){
                            displayed_name_update_approved_form.checked = true;
                        } else {
                            displayed_name_update_approved_form.checked = false;
                        }



                    });
                    dialog.open();
                });
            });

            // Edit/view Transport Equipment
            $('#dp_update_tbody').on('click', '.dp_view_update', function () {
                var child = $(this).closest('tr');
                child.each(function () {
                    var id = $(this).attr('id');
                    var dialog = new Dialog(this, {
                        title: _t("Update Shipping Instruction - Document Parties"),
                        $content: $(qweb.render('freightbox.update_dp_values_popup')),
                        buttons: [{
                            text: _t('Update'),
                            classes: "btn-primary",
                            close: false,
                            click: function () {
                                // Update Party Name
                                var party_name_update_approved_form = document.getElementById("party_name_update_approved_form");
                                var new_party_name_form = document.getElementById("new_party_name_form").value;
                                var old_party_name_form = document.getElementById("old_party_name_form").value;

                                if(party_name_update_approved_form.checked == true){
                                    if(new_party_name_form != "" && document.getElementById("new_party_name_form").hasAttribute('required')){
                                        document.getElementById("new_party_name_update_dp_"+id).value = new_party_name_form;
                                        document.getElementById("party_name_update_val_approved_"+id).value = true;
                                        document.getElementById("new_party_name_update_dp_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_party_name_form_div").innerHTML = "";
                                    } else {
                                        if (new_party_name_form == "" && party_name_update_approved_form.checked == true){
                                             document.getElementById("new_party_name_form").focus();
                                             document.getElementById("new_party_name_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_party_name_form_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("new_party_name_update_dp_"+id).value = old_party_name_form;
                                        document.getElementById("party_name_update_val_approved_"+id).value = false;
                                        document.getElementById("new_party_name_update_dp_"+id).style.background='#FFFFFF';
                                        return;
                                    }
                                }

                                // Update Tax Ref 1
                                var tax_reference_1_update_approved_form = document.getElementById("tax_reference_1_update_approved_form");
                                var new_tax_reference_1_form = document.getElementById("new_tax_reference_1_form").value;
                                var old_tax_reference_1_form = document.getElementById("old_tax_reference_1_form").value;

                                if(tax_reference_1_update_approved_form.checked == true){
                                    if(new_tax_reference_1_form != "" && document.getElementById("new_tax_reference_1_form").hasAttribute('required')){
                                        document.getElementById("new_tax_reference_1_update_dp_"+id).value = new_tax_reference_1_form;
                                        document.getElementById("tax_reference_1_update_val_approved_"+id).value = true;
                                        document.getElementById("new_tax_reference_1_update_dp_"+id).style.background='#ADD8E6';
                                    } else {
                                        if (new_tax_reference_1_form == "" && tax_reference_1_update_approved_form.checked == true) {
                                            document.getElementById("new_tax_reference_1_form").focus();
                                             document.getElementById("new_tax_reference_1_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_tax_reference_1_form_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("new_tax_reference_1_update_dp_"+id).value = old_tax_reference_1_form;
                                        document.getElementById("tax_reference_1_update_val_approved_"+id).value = false;
                                        document.getElementById("new_tax_reference_1_update_dp_"+id).style.background='#FFFFFF';
                                        return;
                                    }
                                }

                                // Update public_key
                                var public_key_update_approved_form = document.getElementById("public_key_update_approved_form");
                                var new_public_key_form = document.getElementById("new_public_key_form").value;
                                var old_public_key_form = document.getElementById("old_public_key_form").value;

                                if(public_key_update_approved_form.checked == true){
                                    if(new_public_key_form != "" && document.getElementById("new_public_key_form").hasAttribute('required')){
                                        document.getElementById("new_public_key_update_dp_"+id).value = new_public_key_form;
                                        document.getElementById("public_key_update_val_approved_"+id).value = true;
                                        document.getElementById("new_public_key_update_dp_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_public_key_form_div").innerHTML = "";
                                    } else {
                                        if (new_public_key_form == "" && public_key_update_approved_form.checked == true) {
                                             document.getElementById("new_public_key_form").focus();
                                             document.getElementById("new_public_key_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_public_key_form_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("new_public_key_update_dp_"+id).value = old_public_key_form;
                                        document.getElementById("public_key_update_val_approved_"+id).value = false;
                                        document.getElementById("new_public_key_update_dp_"+id).style.background='#FFFFFF';
                                        return;
                                    }
                                }

                                // Update street
                                var street_update_approved_form = document.getElementById("street_update_approved_form");
                                var new_street_form = document.getElementById("new_street_form").value;
                                var old_street_form = document.getElementById("old_street_form").value;

                                if(street_update_approved_form.checked == true){
                                    if(new_street_form != "" && document.getElementById("new_street_form").hasAttribute('required')){
                                        document.getElementById("new_street_update_dp_"+id).value = new_street_form;
                                        document.getElementById("street_update_val_approved_"+id).value = true;
                                        document.getElementById("new_street_update_dp_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_street_form_div").innerHTML = "";
                                    } else {
                                        if (new_street_form == "" && street_update_approved_form.checked == true) {
                                             document.getElementById("new_street_form").focus();
                                             document.getElementById("new_street_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_street_form_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("new_street_update_dp_"+id).value = old_street_form;
                                        document.getElementById("street_update_val_approved_"+id).value = false;
                                        document.getElementById("new_street_update_dp_"+id).style.background='#FFFFFF';
                                        return;
                                    }
                                }
                                // Update street_number
                                var street_no_update_approved_form = document.getElementById("street_no_update_approved_form");
                                var new_street_no_form = document.getElementById("new_street_no_form").value;
                                var old_street_no_form = document.getElementById("old_street_no_form").value;

                                if(street_no_update_approved_form.checked == true){
                                    if(new_street_no_form != "" && document.getElementById("new_street_no_form").hasAttribute('required')){
                                        document.getElementById("new_street_number_update_dp_"+id).value = new_street_no_form;
                                        document.getElementById("street_number_update_val_approved_"+id).value = true;
                                        document.getElementById("new_street_number_update_dp_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_street_no_form_div").innerHTML = "";
                                    } else {
                                        if (new_street_no_form == "" && street_no_update_approved_form.checked == true) {
                                            document.getElementById("new_street_no_form").focus();
                                             document.getElementById("new_street_no_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_street_no_form_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("new_street_number_update_dp_"+id).value = old_street_no_form;
                                        document.getElementById("street_number_update_val_approved_"+id).value = false;
                                        document.getElementById("new_street_number_update_dp_"+id).style.background='#FFFFFF';
                                        return;
                                    }
                                }

                                // Update floor
                                var floor_update_approved_form = document.getElementById("floor_update_approved_form");
                                var new_floor_form = document.getElementById("new_floor_form").value;
                                var old_floor_form = document.getElementById("old_floor_form").value;

                                if(floor_update_approved_form.checked == true){
                                    if(new_floor_form != "" && document.getElementById("new_floor_form").hasAttribute('required')){
                                        document.getElementById("new_floor_update_dp_"+id).value = new_floor_form;
                                        document.getElementById("floor_update_val_approved_"+id).value = true;
                                        document.getElementById("new_floor_update_dp_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_floor_form_div").innerHTML = "";
                                    } else {
                                        if (new_floor_form == "" && floor_update_approved_form.checked == true) {
                                            document.getElementById("new_floor_form").focus();
                                             document.getElementById("new_floor_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_floor_form_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("new_floor_update_dp_"+id).value = old_floor_form;
                                        document.getElementById("floor_update_val_approved_"+id).value = false;
                                        document.getElementById("new_floor_update_dp_"+id).style.background='#FFFFFF';
                                        return;
                                    }
                                }

                                // Update post_code
                                var floor_post_code_approved_form = document.getElementById("floor_post_code_approved_form");
                                var new_post_code_form = document.getElementById("new_post_code_form").value;
                                var old_post_code_form = document.getElementById("old_post_code_form").value;

                                if(floor_post_code_approved_form.checked == true){
                                    if(new_post_code_form != "" && document.getElementById("new_post_code_form").hasAttribute('required')){
                                        document.getElementById("new_post_code_update_dp_"+id).value = new_post_code_form;
                                        document.getElementById("post_code_update_val_approved_"+id).value = true;
                                        document.getElementById("new_post_code_update_dp_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_post_code_form_div").innerHTML = "";
                                    } else {
                                        if (new_post_code_form == "" && floor_post_code_approved_form.checked == true) {
                                             document.getElementById("new_post_code_form").focus();
                                             document.getElementById("new_post_code_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_post_code_form_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("new_post_code_update_dp_"+id).value = old_post_code_form;
                                        document.getElementById("post_code_update_val_approved_"+id).value = false;
                                        document.getElementById("new_post_code_update_dp_"+id).style.background='#FFFFFF';
                                        return;
                                    }
                                }

                                // Update city
                                var city_approved_form = document.getElementById("city_approved_form");
                                var new_city_form = document.getElementById("new_city_form").value;
                                var old_city_form = document.getElementById("old_city_form").value;

                                if(city_approved_form.checked == true){
                                    if(new_city_form != "" && document.getElementById("new_city_form").hasAttribute('required')){
                                        document.getElementById("new_city_update_dp_"+id).value = new_city_form;
                                        document.getElementById("city_update_val_approved_"+id).value = true;
                                        document.getElementById("new_city_update_dp_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_city_form_div").innerHTML = "";
                                    } else {
                                        if (new_city_form == "" && city_approved_form.checked == true) {
                                             document.getElementById("new_city_form").focus();
                                             document.getElementById("new_city_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_city_form_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("new_city_update_dp_"+id).value = old_city_form;
                                        document.getElementById("city_update_val_approved_"+id).value = false;
                                        document.getElementById("new_city_update_dp_"+id).style.background='#FFFFFF';
                                        return;
                                    }
                                }

                                // Update state region
                                var state_region_approved_form = document.getElementById("state_region_approved_form");
                                var new_state_region_form = document.getElementById("new_state_region_form").value;
                                var old_state_region_form = document.getElementById("old_state_region_form").value;

                                if(state_region_approved_form.checked == true){
                                    if(new_state_region_form != "" && document.getElementById("new_state_region_form").hasAttribute('required')){
                                        document.getElementById("new_state_region_update_dp_"+id).value = new_state_region_form;
                                        document.getElementById("state_region_update_val_approved_"+id).value = true;
                                        document.getElementById("new_state_region_update_dp_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_state_region_form_div").innerHTML = "";
                                    } else {
                                        if (new_state_region_form == "" && state_region_approved_form.checked == true) {
                                             document.getElementById("new_state_region_form").focus();
                                             document.getElementById("new_state_region_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_state_region_form_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("new_state_region_update_dp_"+id).value = old_state_region_form;
                                        document.getElementById("state_region_update_val_approved_"+id).value = false;
                                        document.getElementById("new_state_region_update_dp_"+id).style.background='#FFFFFF';
                                        return;
                                    }
                                }

                                // Update country
                                var country_approved_form = document.getElementById("country_approved_form");
                                var new_country_form = document.getElementById("new_country_form").value;
                                var old_country_form = document.getElementById("old_country_form").value;

                                if(country_approved_form.checked == true){
                                    if(new_country_form != "" && document.getElementById("new_country_form").hasAttribute('required')){
                                        document.getElementById("new_country_update_dp_"+id).value = new_country_form;
                                        document.getElementById("country_update_val_approved_"+id).value = true;
                                        document.getElementById("new_country_update_dp_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_country_form_div").innerHTML = "";
                                    } else {
                                        if (new_country_form == "" && country_approved_form.checked == true) {
                                             document.getElementById("new_country_form").focus();
                                             document.getElementById("new_country_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_country_form_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("new_country_update_dp_"+id).value = old_country_form;
                                        document.getElementById("country_update_val_approved_"+id).value = false;
                                        document.getElementById("new_country_update_dp_"+id).style.background='#FFFFFF';
                                        return;
                                    }
                                }

                                // Update Tax Reference 2
                                var tax_reference_2_approved_form = document.getElementById("tax_reference_2_approved_form");
                                var new_tax_reference_2_form = document.getElementById("new_tax_reference_2_form").value;
                                var old_tax_reference_2_form = document.getElementById("old_tax_reference_2_form").value;

                                if(tax_reference_2_approved_form.checked == true){
                                    if(new_tax_reference_2_form != "" && document.getElementById("new_tax_reference_2_form").hasAttribute('required')){
                                        document.getElementById("new_tax_reference_2_update_dp_"+id).value = new_tax_reference_2_form;
                                        document.getElementById("tax_reference_2_update_val_approved_"+id).value = true;
                                        document.getElementById("new_tax_reference_2_update_dp_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_tax_reference_2_form_div").innerHTML = "";
                                    } else {
                                        if (new_tax_reference_2_form == "" && tax_reference_2_approved_form.checked == true) {
                                             document.getElementById("new_tax_reference_2_form").focus();
                                             document.getElementById("new_tax_reference_2_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_tax_reference_2_form_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("new_tax_reference_2_update_dp_"+id).value = old_tax_reference_2_form;
                                        document.getElementById("tax_reference_2_update_val_approved_"+id).value = false;
                                        document.getElementById("new_tax_reference_2_update_dp_"+id).style.background='#FFFFFF';
                                        return;
                                    }
                                }

                                // Update NMFTA code
                                var nmfta_code_approved_form = document.getElementById("nmfta_code_approved_form");
                                var new_nmfta_code_form = document.getElementById("new_nmfta_code_form").value;
                                var old_nmfta_code_form = document.getElementById("old_nmfta_code_form").value;

                                if(nmfta_code_approved_form.checked == true){
                                    if(new_nmfta_code_form != "" && document.getElementById("new_nmfta_code_form").hasAttribute('required')){
                                        document.getElementById("new_nmfta_code_update_dp_"+id).value = new_nmfta_code_form;
                                        document.getElementById("nmfta_code_update_val_approved_"+id).value = true;
                                        document.getElementById("new_nmfta_code_update_dp_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_nmfta_code_form_div").innerHTML = "";
                                    } else {
                                        if (new_nmfta_code_form == "" && nmfta_code_approved_form.checked == true) {
                                             document.getElementById("new_nmfta_code_form").focus();
                                             document.getElementById("new_nmfta_code_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_nmfta_code_form_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("new_nmfta_code_update_dp_"+id).value = old_nmfta_code_form;
                                        document.getElementById("nmfta_code_update_val_approved_"+id).value = false;
                                        document.getElementById("new_nmfta_code_update_dp_"+id).style.background='#FFFFFF';
                                        return;
                                    }
                                }

                                // Update Party Function
                                var party_function_approved_form = document.getElementById("party_function_approved_form");
                                var new_party_function_form = document.getElementById("new_party_function_form").value;
                                var old_party_function_form = document.getElementById("old_party_function_form").value;

                                if(party_function_approved_form.checked == true){
                                    if(new_party_function_form != "" && document.getElementById("new_party_function_form").hasAttribute('required')){
                                        document.getElementById("new_party_function_update_dp_"+id).value = new_party_function_form;
                                        document.getElementById("party_function_update_val_approved_"+id).value = true;
                                        document.getElementById("new_party_function_update_dp_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_party_function_form_div").innerHTML = "";
                                    } else {
                                        if (new_party_function_form == "" && party_function_approved_form.checked == true) {
                                             document.getElementById("new_party_function_form").focus();
                                             document.getElementById("new_party_function_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_party_function_form_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("new_party_function_update_dp_"+id).value = old_party_function_form;
                                        document.getElementById("party_function_update_val_approved_"+id).value = false;
                                        document.getElementById("new_party_function_update_dp_"+id).style.background='#FFFFFF';
                                        return;
                                    }
                                }

                                // Update Address line
                                var address_line_approved_form = document.getElementById("address_line_approved_form");
                                var new_address_line_form = document.getElementById("new_address_line_form").value;
                                var old_address_line_form = document.getElementById("old_address_line_form").value;

                                if(address_line_approved_form.checked == true){
                                    document.getElementById("new_address_line_update_dp_"+id).value = new_address_line_form;
                                    document.getElementById("address_line_update_val_approved_"+id).value = true;
                                    document.getElementById("new_address_line_update_dp_"+id).style.background='#ADD8E6';
                                } else {
                                    document.getElementById("new_address_line_update_dp_"+id).value = old_address_line_form;
                                    document.getElementById("address_line_update_val_approved_"+id).value = false;
                                    document.getElementById("new_address_line_update_dp_"+id).style.background='#FFFFFF';
                                }

                                // Update Name
                                var name_approved_form = document.getElementById("name_approved_form");
                                var new_name_form = document.getElementById("new_name_form").value;
                                var old_name_form = document.getElementById("old_name_form").value;

                                if(name_approved_form.checked == true){
                                    if(new_name_form != "" && document.getElementById("new_name_form").hasAttribute('required')){
                                        document.getElementById("new_name_update_dp_"+id).value = new_name_form;
                                        document.getElementById("name_update_val_approved_"+id).value = true;
                                        document.getElementById("new_name_update_dp_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_name_form_div").innerHTML = "";
                                    } else {
                                        if (new_name_form == "" && name_approved_form.checked == true) {
                                             document.getElementById("new_name_form").focus();
                                             document.getElementById("new_name_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_name_form_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("new_name_update_dp_"+id).value = old_name_form;
                                        document.getElementById("name_update_val_approved_"+id).value = false;
                                        document.getElementById("new_name_update_dp_"+id).style.background='#FFFFFF';
                                        return;
                                    }
                                }

                                // Update Email
                                var email_approved_form = document.getElementById("email_approved_form");
                                var new_email_form = document.getElementById("new_email_form").value;
                                var old_email_form = document.getElementById("old_email_form").value;

                                if(email_approved_form.checked == true){
                                    if(new_email_form != "" && document.getElementById("new_email_form").hasAttribute('required')){
                                        document.getElementById("new_email_update_dp_"+id).value = new_email_form;
                                        document.getElementById("email_update_val_approved_"+id).value = true;
                                        document.getElementById("new_email_update_dp_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_email_form_div").innerHTML = "";
                                    } else {
                                        if (new_email_form == "" && email_approved_form.checked == true) {
                                             document.getElementById("new_email_form").focus();
                                             document.getElementById("new_email_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_email_form_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("new_email_update_dp_"+id).value = old_email_form;
                                        document.getElementById("email_update_val_approved_"+id).value = false;
                                        document.getElementById("new_email_update_dp_"+id).style.background='#FFFFFF';
                                        return;
                                    }
                                }

                                // Update Phone
                                var phone_approved_form = document.getElementById("phone_approved_form");
                                var new_phone_form = document.getElementById("new_phone_form").value;
                                var old_phone_form = document.getElementById("old_phone_form").value;

                                if(phone_approved_form.checked == true){
                                    if(new_phone_form != "" && document.getElementById("new_phone_form").hasAttribute('required')){
                                        document.getElementById("new_phone_update_dp_"+id).value = new_phone_form;
                                        document.getElementById("phone_update_val_approved_"+id).value = true;
                                        document.getElementById("new_phone_update_dp_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_phone_form_div").innerHTML = "";
                                    } else {
                                        if (new_phone_form == "" && phone_approved_form.checked == true) {
                                             document.getElementById("new_phone_form").focus();
                                             document.getElementById("new_phone_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_phone_form_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("new_phone_update_dp_"+id).value = old_phone_form;
                                        document.getElementById("phone_update_val_approved_"+id).value = false;
                                        document.getElementById("new_phone_update_dp_"+id).style.background='#FFFFFF';
                                        return;
                                    }
                                }


                                // Update Is To Be Notified
                                var notified_approved_form = document.getElementById("notified_approved_form");
                                var new_notified_form = document.getElementById("new_notified_form");
                                var old_notified_form = document.getElementById("old_notified_form");
                                if(notified_approved_form.checked == true){
//                                    alert("ccccccccc"+ new_notified_form.checked);
                                    if(new_notified_form.checked != true){
                                        document.getElementById("new_is_to_be_notified_update_dp_"+id).checked = new_notified_form.checked;
                                        document.getElementById("is_to_be_notified_update_val_approved_"+id).checked = true;
                                        document.getElementById("new_is_to_be_notified_update_dp_"+id).style.background='#ADD8E6';
                                    } else {
                                        document.getElementById("new_is_to_be_notified_update_dp_"+id).checked = new_notified_form.checked;
                                        document.getElementById("is_to_be_notified_update_val_approved_"+id).checked = true;
                                        document.getElementById("new_is_to_be_notified_update_dp_"+id).style.background='#FFFFFF';
                                    }
                                }

                                var update_dp_form = document.getElementById('update_dp_form');
                                /*for(var i=0; i < update_dp_form.elements.length; i++){
                                    if(update_dp_form.elements[i].value === '' && update_dp_form.elements[i].hasAttribute('required')){
                                        *//*if (new_party_name_form == "" && party_name_update_approved_form.checked == true){
                                             document.getElementById("new_party_name_form").focus();
                                             document.getElementById("new_party_name_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_party_name_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_party_name_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_tax_reference_1_form == "" && tax_reference_1_update_approved_form.checked == true) {
                                            document.getElementById("new_tax_reference_1_form").focus();
                                             document.getElementById("new_tax_reference_1_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_tax_reference_1_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_tax_reference_1_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_public_key_form == "" && public_key_update_approved_form.checked == true) {
                                            document.getElementById("new_public_key_form").focus();
                                             document.getElementById("new_public_key_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_public_key_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_public_key_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_street_form == "" && street_update_approved_form.checked == true) {
                                            document.getElementById("new_street_form").focus();
                                             document.getElementById("new_street_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_street_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_street_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_street_form == "" && street_update_approved_form.checked == true) {
                                            document.getElementById("new_street_form").focus();
                                             document.getElementById("new_street_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_street_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_street_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_street_no_form == "" && street_no_update_approved_form.checked == true) {
                                            document.getElementById("new_street_no_form").focus();
                                             document.getElementById("new_street_no_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_street_no_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_street_no_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_floor_form == "" && floor_update_approved_form.checked == true) {
                                            document.getElementById("new_floor_form").focus();
                                             document.getElementById("new_floor_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_floor_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_floor_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_post_code_form == "" && floor_post_code_approved_form.checked == true) {
                                             document.getElementById("new_post_code_form").focus();
                                             document.getElementById("new_post_code_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_post_code_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_post_code_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_city_form == "" && city_approved_form.checked == true) {
                                             document.getElementById("new_city_form").focus();
                                             document.getElementById("new_city_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_city_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_city_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_state_region_form == "" && state_region_approved_form.checked == true) {
                                             document.getElementById("new_state_region_form").focus();
                                             document.getElementById("new_state_region_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_state_region_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_state_region_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_country_form == "" && country_approved_form.checked == true) {
                                             document.getElementById("new_country_form").focus();
                                             document.getElementById("new_country_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_country_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_country_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_tax_reference_2_form == "" && tax_reference_2_approved_form.checked == true) {
                                             document.getElementById("new_tax_reference_2_form").focus();
                                             document.getElementById("new_tax_reference_2_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_tax_reference_2_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_tax_reference_2_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_tax_reference_2_form == "" && tax_reference_2_approved_form.checked == true) {
                                             document.getElementById("new_tax_reference_2_form").focus();
                                             document.getElementById("new_tax_reference_2_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_tax_reference_2_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_tax_reference_2_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_nmfta_code_form == "" && nmfta_code_approved_form.checked == true) {
                                             document.getElementById("new_nmfta_code_form").focus();
                                             document.getElementById("new_nmfta_code_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_nmfta_code_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_nmfta_code_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_party_function_form == "" && party_function_approved_form.checked == true) {
                                             document.getElementById("new_party_function_form").focus();
                                             document.getElementById("new_party_function_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_party_function_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_party_function_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_name_form == "" && name_approved_form.checked == true) {
                                             document.getElementById("new_name_form").focus();
                                             document.getElementById("new_name_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_name_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_name_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_email_form == "" && email_approved_form.checked == true) {
                                             document.getElementById("new_email_form").focus();
                                             document.getElementById("new_email_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_email_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_email_form_div").innerHTML = "";
                                        }
                                        if (new_phone_form == "" && phone_approved_form.checked == true) {
                                             document.getElementById("new_phone_form").focus();
                                             document.getElementById("new_phone_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_phone_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_phone_form_div").innerHTML = "";
                                        }*//*
                                    }
                                }*/

                                if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(new_email_form) && email_approved_form.checked == true) {
                                    document.getElementById("new_email_form_div").innerHTML = "";
                                } else {
                                if (email_approved_form.checked == true) {
                                    document.getElementById("new_email_form").focus();
                                    document.getElementById("new_email_form_div").innerHTML = "Please Enter a valid email";
                                    document.getElementById("new_email_form_div").style.color="Red";
                                    return;
                                    }
                                }

                                    /*if(notified_approved_form.checked == true){
                                        document.getElementById("new_notified_form").focus();
                                        document.getElementById("new_notified_form_div").innerHTML = "Please fill this field";
                                        document.getElementById("new_notified_form_div").style.color="Red";
                                        return;
                                    }*/

                                /*var re = /^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$/im;
                                 if (re.test(phone_approved_form) == true && phone_approved_form.checked == true){
                                     document.getElementById("new_phone_form_div").innerHTML = "";
                                 } else {
                                    if(phone_approved_form.checked == true){
                                     document.getElementById("new_phone_form").focus();
                                     document.getElementById("new_phone_form_div").innerHTML = "Please fill this field";
                                     document.getElementById("new_phone_form_div").style.color="Red";
                                     return;
                                     }
                                 }*/

                                dialog.close();


                            }
                        }],
                    });
                    dialog.opened().then(function () {

                        var update_dp_form = document.getElementById('update_dp_form');
                        for(var i=0; i < update_dp_form.elements.length; i++){
                            if(update_dp_form.elements[i].hasAttribute('required')){
                                update_dp_form.elements[i].style.background='#ADD8E6';
                            }
                        }
                        var update_dp_row_id_form = document.getElementById("dp_update_row_id_"+id).value;
                        document.getElementById("update_dp_row_id_form").value = update_dp_row_id_form;

                        // Update Created By value
                        var si_created_by_val = document.getElementById("si_created_by").value;
                        document.getElementById("update_party_name_created_by").value = si_created_by_val;
                        document.getElementById("update_tax_reference_1_created_by").value = si_created_by_val;
                        document.getElementById("update_public_key_created_by").value = si_created_by_val;
                        document.getElementById("update_street_created_by").value = si_created_by_val;
                        document.getElementById("update_street_no_created_by").value = si_created_by_val;
                        document.getElementById("update_floor_created_by").value = si_created_by_val;
                        document.getElementById("update_post_code_created_by").value = si_created_by_val;
                        document.getElementById("update_city_created_by").value = si_created_by_val;
                        document.getElementById("update_state_region_created_by").value = si_created_by_val;
                        document.getElementById("update_country_created_by").value = si_created_by_val;
                        document.getElementById("update_tax_reference_2_created_by").value = si_created_by_val;
                        document.getElementById("update_nmfta_code_created_by").value = si_created_by_val;
                        document.getElementById("update_party_function_created_by").value = si_created_by_val;
                        document.getElementById("update_address_line_created_by").value = si_created_by_val;
                        document.getElementById("update_name_created_by").value = si_created_by_val;
                        document.getElementById("update_email_created_by").value = si_created_by_val;
                        document.getElementById("update_phone_created_by").value = si_created_by_val;
                        document.getElementById("update_notified_created_by").value = si_created_by_val;

                        // Update Modified By value
                        document.getElementById("update_party_name_modify_by").value = si_created_by_val;
                        document.getElementById("update_tax_reference_1_modify_by").value = si_created_by_val;
                        document.getElementById("update_public_key_modify_by").value = si_created_by_val;
                        document.getElementById("update_street_modify_by").value = si_created_by_val;
                        document.getElementById("update_street_no_modify_by").value = si_created_by_val;
                        document.getElementById("update_floor_modify_by").value = si_created_by_val;
                        document.getElementById("update_post_code_modify_by").value = si_created_by_val;
                        document.getElementById("update_city_modify_by").value = si_created_by_val;
                        document.getElementById("update_state_region_modify_by").value = si_created_by_val;
                        document.getElementById("update_country_modify_by").value = si_created_by_val;
                        document.getElementById("update_tax_reference_2_modify_by").value = si_created_by_val;
                        document.getElementById("update_nmfta_code_modify_by").value = si_created_by_val;
                        document.getElementById("update_party_function_modify_by").value = si_created_by_val;
                        document.getElementById("update_address_line_modify_by").value = si_created_by_val;
                        document.getElementById("update_name_modify_by").value = si_created_by_val;
                        document.getElementById("update_email_modify_by").value = si_created_by_val;
                        document.getElementById("update_phone_modify_by").value = si_created_by_val;
                        document.getElementById("update_notified_modify_by").value = si_created_by_val;

                        // update Party Name
                        // old value
                        var old_party_name_form = document.getElementById("old_party_name_update_dp_"+id).value;
                        document.getElementById("old_party_name_form").value = old_party_name_form;
                        // new value
                        var new_party_name_form = document.getElementById("new_party_name_update_dp_"+id).value;
                        if (old_party_name_form === new_party_name_form){
                            document.getElementById("new_party_name_form").value = "";
                        } else{
                            document.getElementById("new_party_name_form").value = new_party_name_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var party_name_update_val_approved = document.getElementById("party_name_update_val_approved_"+id).value;
                        var party_name_update_approved_form = document.getElementById("party_name_update_approved_form");
                        if (party_name_update_val_approved == "true"){
                            party_name_update_approved_form.checked = true;
                        } else {
                            party_name_update_approved_form.checked = false;
                        }

                        // update tax_reference_1
                        // old value
                        var old_tax_reference_1_form = document.getElementById("old_tax_reference_1_update_dp_"+id).value;
                        document.getElementById("old_tax_reference_1_form").value = old_tax_reference_1_form;
                        // new value
                        var new_tax_reference_1_form = document.getElementById("new_tax_reference_1_update_dp_"+id).value;
                        if (old_tax_reference_1_form === new_tax_reference_1_form){
                            document.getElementById("new_tax_reference_1_form").value = "";
                        } else{
                            document.getElementById("new_tax_reference_1_form").value = new_tax_reference_1_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var tax_reference_1_update_val_approved = document.getElementById("tax_reference_1_update_val_approved_"+id).value;
                        var tax_reference_1_update_approved_form = document.getElementById("tax_reference_1_update_approved_form");
                        if (tax_reference_1_update_val_approved == "true"){
                            tax_reference_1_update_approved_form.checked = true;
                        } else {
                            tax_reference_1_update_approved_form.checked = false;
                        }

                        // update public_key
                        // old value
                        var old_public_key_form = document.getElementById("old_public_key_update_dp_"+id).value;
                        document.getElementById("old_public_key_form").value = old_public_key_form;
                        // new value
                        var new_public_key_form = document.getElementById("new_public_key_update_dp_"+id).value;
                        if (old_public_key_form === new_public_key_form){
                            document.getElementById("new_public_key_form").value = "";
                        } else{
                            document.getElementById("new_public_key_form").value = new_public_key_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var public_key_update_val_approved = document.getElementById("public_key_update_val_approved_"+id).value;
                        var public_key_update_approved_form = document.getElementById("public_key_update_approved_form");
                        if (public_key_update_val_approved == "true"){
                            public_key_update_approved_form.checked = true;
                        } else {
                            public_key_update_approved_form.checked = false;
                        }

                        // update public_key
                        // old value
                        /*var old_public_key_form = document.getElementById("old_public_key_update_dp_"+id).value;
                        document.getElementById("old_public_key_form").value = old_public_key_form;
                        // new value
                        var new_public_key_form = document.getElementById("new_public_key_update_dp_"+id).value;
                        if (old_public_key_form === new_public_key_form){
                            document.getElementById("new_public_key_form").value = "";
                        } else{
                            document.getElementById("new_public_key_form").value = new_public_key_form;
                        }*/

                        // update Street
                        // old value
                        var old_street_form = document.getElementById("old_street_update_dp_"+id).value;
                        document.getElementById("old_street_form").value = old_street_form;
                        // new value
                        var new_street_form = document.getElementById("new_street_update_dp_"+id).value;
                        if (old_street_form === new_street_form){
                            document.getElementById("new_street_form").value = "";
                        } else{
                            document.getElementById("new_street_form").value = new_street_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var street_update_val_approved = document.getElementById("street_update_val_approved_"+id).value;
                        var street_update_approved_form = document.getElementById("street_update_approved_form");
                        if (street_update_val_approved == "true"){
                            street_update_approved_form.checked = true;
                        } else {
                            street_update_approved_form.checked = false;
                        }

                        // update Street number
                        // old value
                        var old_street_no_form = document.getElementById("old_street_number_update_dp_"+id).value;
                        document.getElementById("old_street_no_form").value = old_street_no_form;
                        // new value
                        var new_street_no_form = document.getElementById("new_street_number_update_dp_"+id).value;
                        if (old_street_no_form === new_street_no_form){
                            document.getElementById("new_street_no_form").value = "";
                        } else{
                            document.getElementById("new_street_no_form").value = new_street_no_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var street_number_update_val_approved = document.getElementById("street_number_update_val_approved_"+id).value;
                        var street_no_update_approved_form = document.getElementById("street_no_update_approved_form");
                        if (street_number_update_val_approved == "true"){
                            street_no_update_approved_form.checked = true;
                        } else {
                            street_no_update_approved_form.checked = false;
                        }

                        // update Floorr
                        // old value
                        var old_floor_form = document.getElementById("old_floor_update_dp_"+id).value;
                        document.getElementById("old_floor_form").value = old_floor_form;
                        // new value
                        var new_floor_form = document.getElementById("new_floor_update_dp_"+id).value;
                        if (old_floor_form === new_floor_form){
                            document.getElementById("new_floor_form").value = "";
                        } else{
                            document.getElementById("new_floor_form").value = new_floor_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var floor_update_val_approved = document.getElementById("floor_update_val_approved_"+id).value;
                        var floor_update_approved_form = document.getElementById("floor_update_approved_form");
                        if (floor_update_val_approved == "true"){
                            floor_update_approved_form.checked = true;
                        } else {
                            floor_update_approved_form.checked = false;
                        }

                        // update post_code
                        // old value
                        var old_post_code_form = document.getElementById("old_city_update_dp_"+id).value;
                        document.getElementById("old_post_code_form").value = old_post_code_form;
                        // new value
                        var new_post_code_form = document.getElementById("new_city_update_dp_"+id).value;
                        if (old_post_code_form === new_post_code_form){
                            document.getElementById("new_post_code_form").value = "";
                        } else{
                            document.getElementById("new_post_code_form").value = new_post_code_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var post_code_update_val_approved = document.getElementById("post_code_update_val_approved_"+id).value;
                        var floor_post_code_approved_form = document.getElementById("floor_post_code_approved_form");
                        if (post_code_update_val_approved == "true"){
                            floor_post_code_approved_form.checked = true;
                        } else {
                            floor_post_code_approved_form.checked = false;
                        }

                        // update city
                        // old value
                        var old_city_form = document.getElementById("old_city_update_dp_"+id).value;
                        document.getElementById("old_city_form").value = old_city_form;
                        // new value
                        var new_city_form = document.getElementById("new_city_update_dp_"+id).value;
                        if (old_city_form === new_city_form){
                            document.getElementById("new_city_form").value = "";
                        } else{
                            document.getElementById("new_city_form").value = new_city_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var city_update_val_approved = document.getElementById("city_update_val_approved_"+id).value;
                        var city_approved_form = document.getElementById("city_approved_form");
                        if (city_update_val_approved == "true"){
                            city_approved_form.checked = true;
                        } else {
                            city_approved_form.checked = false;
                        }

                        // update state_region
                        // old value
                        var old_state_region_form = document.getElementById("old_state_region_update_dp_"+id).value;
                        document.getElementById("old_state_region_form").value = old_state_region_form;
                        // new value
                        var new_state_region_form = document.getElementById("new_state_region_update_dp_"+id).value;
                        if (old_state_region_form === new_state_region_form){
                            document.getElementById("new_state_region_form").value = "";
                        } else{
                            document.getElementById("new_state_region_form").value = new_state_region_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var state_region_update_val_approved = document.getElementById("state_region_update_val_approved_"+id).value;
                        var state_region_approved_form = document.getElementById("state_region_approved_form");
                        if (state_region_update_val_approved == "true"){
                            state_region_approved_form.checked = true;
                        } else {
                            state_region_approved_form.checked = false;
                        }

                        // update country
                        // old value
                        var old_country_form = document.getElementById("old_country_update_dp_"+id).value;
                        document.getElementById("old_country_form").value = old_country_form;
                        // new value
                        var new_country_form = document.getElementById("new_country_update_dp_"+id).value;
                        if (old_country_form === new_country_form){
                            document.getElementById("new_country_form").value = "";
                        } else{
                            document.getElementById("new_country_form").value = new_country_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var country_update_val_approved = document.getElementById("country_update_val_approved_"+id).value;
                        var country_approved_form = document.getElementById("country_approved_form");
                        if (country_update_val_approved == "true"){
                            country_approved_form.checked = true;
                        } else {
                            country_approved_form.checked = false;
                        }

                        // update Tax Reference 2
                        // old value
                        var old_tax_reference_2_form = document.getElementById("old_tax_reference_2_update_dp_"+id).value;
                        document.getElementById("old_tax_reference_2_form").value = old_tax_reference_2_form;
                        // new value
                        var new_tax_reference_2_form = document.getElementById("new_tax_reference_2_update_dp_"+id).value;
                        if (old_tax_reference_2_form === new_tax_reference_2_form){
                            document.getElementById("new_tax_reference_2_form").value = "";
                        } else{
                            document.getElementById("new_tax_reference_2_form").value = new_tax_reference_2_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var tax_reference_2_update_val_approved = document.getElementById("tax_reference_2_update_val_approved_"+id).value;
                        var tax_reference_2_approved_form = document.getElementById("tax_reference_2_approved_form");
                        if (tax_reference_2_update_val_approved == "true"){
                            tax_reference_2_approved_form.checked = true;
                        } else {
                            tax_reference_2_approved_form.checked = false;
                        }

                        // update NMFTA code
                        // old value
                        var old_nmfta_code_form = document.getElementById("old_nmfta_code_update_dp_"+id).value;
                        document.getElementById("old_nmfta_code_form").value = old_nmfta_code_form;
                        // new value
                        var new_nmfta_code_form = document.getElementById("new_nmfta_code_update_dp_"+id).value;
                        if (old_nmfta_code_form === new_nmfta_code_form){
                            document.getElementById("new_nmfta_code_form").value = "";
                        } else{
                            document.getElementById("new_nmfta_code_form").value = new_nmfta_code_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var nmfta_code_update_val_approved = document.getElementById("nmfta_code_update_val_approved_"+id).value;
                        var nmfta_code_approved_form = document.getElementById("nmfta_code_approved_form");
                        if (nmfta_code_update_val_approved == "true"){
                            nmfta_code_approved_form.checked = true;
                        } else {
                            nmfta_code_approved_form.checked = false;
                        }


                        // update Party Function
                        // old value
                        var old_party_function_form = document.getElementById("old_party_function_update_dp_"+id).value;
                        document.getElementById("old_party_function_form").value = old_party_function_form;
                        // new value
                        var new_party_function_form = document.getElementById("new_party_function_update_dp_"+id).value;
                        if (old_party_function_form === new_party_function_form){
                            document.getElementById("new_party_function_form").value = "";
                        } else{
                            document.getElementById("new_party_function_form").value = new_party_function_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var party_function_update_val_approved = document.getElementById("party_function_update_val_approved_"+id).value;
                        var party_function_approved_form = document.getElementById("party_function_approved_form");
                        if (party_function_update_val_approved == "true"){
                            party_function_approved_form.checked = true;
                        } else {
                            party_function_approved_form.checked = false;
                        }

                        // update Address line
                        // old value
                        var old_address_line_form = document.getElementById("old_address_line_update_dp_"+id).value;
                        document.getElementById("old_address_line_form").value = old_address_line_form;
                        // new value
                        var new_address_line_form = document.getElementById("new_address_line_update_dp_"+id).value;
                        if (old_address_line_form === new_address_line_form){
                            document.getElementById("new_address_line_form").value = "";
                        } else{
                            document.getElementById("new_address_line_form").value = new_address_line_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var address_line_update_val_approved = document.getElementById("address_line_update_val_approved_"+id).value;
                        var address_line_approved_form = document.getElementById("address_line_approved_form");
                        if (address_line_update_val_approved == "true"){
                            address_line_approved_form.checked = true;
                        } else {
                            address_line_approved_form.checked = false;
                        }

                        // update Name
                        // old value
                        var old_name_form = document.getElementById("old_name_update_dp_"+id).value;
                        document.getElementById("old_name_form").value = old_name_form;
                        // new value
                        var new_name_form = document.getElementById("new_name_update_dp_"+id).value;
                        if (old_name_form === new_name_form){
                            document.getElementById("new_name_form").value = "";
                        } else{
                            document.getElementById("new_name_form").value = new_name_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var name_update_val_approved = document.getElementById("name_update_val_approved_"+id).value;
                        var name_approved_form = document.getElementById("name_approved_form");
                        if (name_update_val_approved == "true"){
                            name_approved_form.checked = true;
                        } else {
                            name_approved_form.checked = false;
                        }

                        // update Email
                        // old value
                        var old_email_form = document.getElementById("old_email_update_dp_"+id).value;
                        document.getElementById("old_email_form").value = old_email_form;
                        // new value
                        var new_email_form = document.getElementById("new_email_update_dp_"+id).value;
                        if (old_email_form === new_email_form){
                            document.getElementById("new_email_form").value = "";
                        } else{
                            document.getElementById("new_email_form").value = new_email_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var email_update_val_approved = document.getElementById("email_update_val_approved_"+id).value;
                        var email_approved_form = document.getElementById("email_approved_form");
                        if (email_update_val_approved == "true"){
                            email_approved_form.checked = true;
                        } else {
                            email_approved_form.checked = false;
                        }

                        // update Phone
                        // old value
                        var old_phone_form = document.getElementById("old_phone_update_dp_"+id).value;
                        document.getElementById("old_phone_form").value = old_phone_form;
                        // new value
                        var new_phone_form = document.getElementById("new_phone_update_dp_"+id).value;
                        if (old_phone_form === new_phone_form){
                            document.getElementById("new_phone_form").value = "";
                        } else{
                            document.getElementById("new_phone_form").value = new_phone_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var phone_update_val_approved = document.getElementById("phone_update_val_approved_"+id).value;
                        var phone_approved_form = document.getElementById("phone_approved_form");
                        if (phone_update_val_approved == "true"){
                            phone_approved_form.checked = true;
                        } else {
                            phone_approved_form.checked = false;
                        }


                        // update Is To Be Notified
                        // old value
                        var old_notified_form = document.getElementById("old_is_to_be_notified_update_dp_"+id);
//                        document.getElementById("old_notified_form").checked = old_notified_form.checked;
                        if (old_notified_form.checked === true){
                            document.getElementById("old_notified_form").checked = true;
                        } else{
                            document.getElementById("old_notified_form").checked = false;
                        }
                        // new value
                        var new_notified_form = document.getElementById("new_is_to_be_notified_update_dp_"+id);
                        if (new_notified_form.checked === true){
                            document.getElementById("new_notified_form").checked = true;
                        } else{
                            document.getElementById("new_notified_form").checked = false;
                        }

                        // To make approve check box checked by default if it is approved once
                        var is_to_be_notified_update_val_approved = document.getElementById("is_to_be_notified_update_val_approved_"+id).checked;
                        var notified_approved_form = document.getElementById("notified_approved_form");
//                        alert("is_to_be_notified_update_val_approved"+ is_to_be_notified_update_val_approved);
                        if (is_to_be_notified_update_val_approved == true){
                            notified_approved_form.checked = true;
                        } else {
                            notified_approved_form.checked = false;
                        }
                    });
                    dialog.open();
                });
            });

            // Edit/view Transport Equipment
            $('#tq_update_tbody').on('click', '.tq_view_update', function () {
                var child = $(this).closest('tr');
                child.each(function () {
                    var id = $(this).attr('id');
                    var dialog = new Dialog(this, {
                        title: _t("Update Shipping Instruction - Transport Equipment"),
                        $content: $(qweb.render('freightbox.update_tq_values_popup')),
                        buttons: [{
                            text: _t('Update'),
                            classes: "btn-primary",
                            close: false,
                            click: function () {
                                // Update Container ID
                                var eq_ref_update_approved_form = document.getElementById("eq_ref_update_approved_form");
                                var new_update_eq_ref_form = document.getElementById("new_update_eq_ref_form").value;
                                var old_update_eq_ref_form = document.getElementById("old_update_eq_ref_form").value;

                                if(eq_ref_update_approved_form.checked == true){
                                    if(new_update_eq_ref_form != "" && document.getElementById("new_update_eq_ref_form").hasAttribute('required')){
                                        document.getElementById("new_update_eq_id_"+id).value = new_update_eq_ref_form;
                                        document.getElementById("eq_update_val_approved_"+id).value = true;
                                        document.getElementById("new_update_eq_id_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_update_eq_ref_form_div").innerHTML = "";
                                    } else {
                                        /*if (new_update_eq_ref_form == "" && eq_ref_update_approved_form.checked == true){
                                             document.getElementById("new_update_eq_ref_form").focus();
                                             document.getElementById("new_update_eq_ref_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_update_eq_ref_form_div").style.color="Red";
                                             return;
//                                        }*/
                                        document.getElementById("eq_update_val_approved_"+id).value = true;
                                        document.getElementById("new_update_eq_id_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_update_eq_ref_form_div").innerHTML = "";
                                    }
                                }

                                // Update Weight Unit
                                var wt_unit_update_approved_form = document.getElementById("wt_unit_update_approved_form");
                                var new_update_wt_unit_form = document.getElementById("new_update_wt_unit_form").value;
                                var old_update_wt_unit_form = document.getElementById("old_update_wt_unit_form").value;

                                if(wt_unit_update_approved_form.checked == true){
                                    if(new_update_wt_unit_form != "" && document.getElementById("new_update_wt_unit_form").hasAttribute('required')){
                                        document.getElementById("new_wt_unit_update_tq_"+id).value = new_update_wt_unit_form;
                                        document.getElementById("wt_unit_update_val_approved_"+id).value = true;
                                        document.getElementById("new_wt_unit_update_tq_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_update_wt_unit_form_div").innerHTML = "";
                                    } else {
                                        if (new_update_wt_unit_form == "" && wt_unit_update_approved_form.checked == true) {
                                             document.getElementById("new_update_wt_unit_form").focus();
                                             document.getElementById("new_update_wt_unit_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_update_wt_unit_form_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("new_wt_unit_update_tq_"+id).value = old_update_wt_unit_form;
                                        document.getElementById("wt_unit_update_val_approved_"+id).value = false;
                                        document.getElementById("new_wt_unit_update_tq_"+id).style.background='#FFFFFF';
                                        return;
                                    }
                                }

                                // Update Cargo Gross Weight
                                var cgw_update_approved_form = document.getElementById("cgw_update_approved_form");
                                var new_update_cgw_form = document.getElementById("new_update_cgw_form").value;
                                var old_update_cgw_form = document.getElementById("old_update_cgw_form").value;

                                if(cgw_update_approved_form.checked == true){
                                    if(new_update_cgw_form != "" && document.getElementById("new_update_cgw_form").hasAttribute('required')){
                                        document.getElementById("new_cgw_update_tq_"+id).value = new_update_cgw_form;
                                        document.getElementById("cgw_update_update_val_approved_"+id).value = true;
                                        document.getElementById("new_cgw_update_tq_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_update_cgw_form_div").innerHTML = "";
                                    } else {
                                        if (new_update_cgw_form == "" && cgw_update_approved_form.checked == true){
                                             document.getElementById("new_update_cgw_form").focus();
                                             document.getElementById("new_update_cgw_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_update_cgw_form_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("new_cgw_update_tq_"+id).value = old_update_cgw_form;
                                        document.getElementById("cgw_update_update_val_approved_"+id).value = false;
                                        document.getElementById("new_cgw_update_tq_"+id).style.background='#FFFFFF';
                                        return;
                                    }
                                }
                                var new_update_shipper_form = document.getElementById("new_update_shipper_form");

                                // Update Container tare weight
                                var ctw_update_approved_form = document.getElementById("ctw_update_approved_form");
                                var new_update_ctw_form = document.getElementById("new_update_ctw_form").value;
                                var old_update_ctw_form = document.getElementById("old_update_ctw_form").value;

                                if(ctw_update_approved_form.checked == true){
                                    if(new_update_ctw_form != "" && document.getElementById("new_update_ctw_form").hasAttribute('required')){
                                        document.getElementById("new_ctw_update_tq_"+id).value = new_update_ctw_form;
                                        document.getElementById("ctw_update_val_approved_"+id).value = true;
                                        document.getElementById("new_ctw_update_tq_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_update_ctw_form_div").innerHTML = "";
                                    } else {
                                        if (new_update_ctw_form == "" && ctw_update_approved_form.checked == true){
                                            if (new_update_shipper_form.checked == true && ctw_update_approved_form.checked == true){
                                                 document.getElementById("new_update_ctw_form").focus();
                                                 document.getElementById("new_update_ctw_form_div").innerHTML = "Please fill this field";
                                                 document.getElementById("new_update_ctw_form_div").style.color="Red";
                                                 return;
                                             }
                                        }
//                                        document.getElementById("new_ctw_update_tq_"+id).value = old_update_ctw_form;
//                                        document.getElementById("ctw_update_val_approved_"+id).value = false;
//                                        document.getElementById("new_ctw_update_tq_"+id).style.background='#FFFFFF';
//                                        return;
                                    }
                                }
                                // Update ISO equipment code
                                var iso_eq_update_approved_form = document.getElementById("iso_eq_update_approved_form");
                                var new_update_iso_eq_form = document.getElementById("new_update_iso_eq_form").value;
                                var old_update_iso_eq_form = document.getElementById("old_update_iso_eq_form").value;

                                if(iso_eq_update_approved_form.checked == true){
                                    if(new_update_iso_eq_form != "" && document.getElementById("new_update_iso_eq_form").hasAttribute('required')){
                                        document.getElementById("new_iso_eq_code_update_tq_"+id).value = new_update_iso_eq_form;
                                        document.getElementById("iso_eq_code_update_val_approved_"+id).value = true;
                                        document.getElementById("new_iso_eq_code_update_tq_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_update_iso_eq_form_div").innerHTML = "";
                                    } else {
                                        if (new_update_iso_eq_form == "" && iso_eq_update_approved_form.checked == true){
                                         //   alert("aaaaaaaaaaaaaaaaaaaa");
                                            if (new_update_shipper_form.checked == true && iso_eq_update_approved_form.checked == true){
                                             //   alert("bbbbbbbbbbbbbbbbbbb");
                                                document.getElementById("new_update_iso_eq_form").focus();
                                                document.getElementById("new_update_iso_eq_form_div").innerHTML = "Please fill this field";
                                                document.getElementById("new_update_iso_eq_form_div").style.color="Red";
                                                return;
                                             }
                                        }
                                       // alert("ffffffffffffffffffffffffff");
                                        //document.getElementById("new_iso_eq_code_update_tq_"+id).value = old_update_iso_eq_form;
                                        //document.getElementById("iso_eq_code_update_val_approved_"+id).value = false;
                                        //document.getElementById("new_iso_eq_code_update_tq_"+id).style.background='#FFFFFF';

                                    }
                                }

                                // Shipper owned

                                var shipper_update_approved_form = document.getElementById("shipper_update_approved_form");
//                                var new_update_shipper_form = document.getElementById("new_update_shipper_form");
                                var old_update_shipper_form = document.getElementById("old_update_shipper_form");
                     //           document.getElementById("new_is_shipper_owned_update_tq_"+id).checked = new_update_shipper_form.checked;
                                if (shipper_update_approved_form.checked == true){
                                    document.getElementById("new_is_shipper_owned_update_tq_"+id).checked = new_update_shipper_form.checked;
                                } /*else {
                                    document.getElementById("new_is_shipper_owned_update_tq_"+id).checked = old_update_shipper_form.checked;
                                }*/

                                // Update Temperature Min
                                var temp_min_update_approved_form = document.getElementById("temp_min_update_approved_form");
                                var new_update_temp_min_form = document.getElementById("new_update_temp_min_form").value;
                                var old_update_temp_min_form = document.getElementById("old_update_temp_min_form").value;

                                if(temp_min_update_approved_form.checked == true){
                                    document.getElementById("new_temp_min_update_tq_"+id).value = new_update_temp_min_form;
                                    document.getElementById("temp_min_update_val_approved_"+id).value = true;
                                    document.getElementById("new_temp_min_update_tq_"+id).style.background='#ADD8E6';
                                } /*else {
                                    document.getElementById("new_temp_min_update_tq_"+id).value = old_update_temp_min_form;
                                    document.getElementById("temp_min_update_val_approved_"+id).value = false;
                                    document.getElementById("new_temp_min_update_tq_"+id).style.background='#FFFFFF';
                                }*/

                                // Update Temperature Max
                                var temp_max_update_approved_form = document.getElementById("temp_max_update_approved_form");
                                var new_update_temp_max_form = document.getElementById("new_update_temp_max_form").value;
                                var old_update_temp_max_form = document.getElementById("old_update_temp_max_form").value;

                                if(temp_max_update_approved_form.checked == true){
                                    document.getElementById("new_temp_max_update_tq_"+id).value = new_update_temp_max_form;
                                    document.getElementById("temp_max_update_val_approved_"+id).value = true;
                                    document.getElementById("new_temp_max_update_tq_"+id).style.background='#ADD8E6';
                                } /*else {
                                    document.getElementById("new_temp_max_update_tq_"+id).value = old_update_temp_max_form;
                                    document.getElementById("temp_max_update_val_approved_"+id).value = false;
                                    document.getElementById("new_temp_max_update_tq_"+id).style.background='#FFFFFF';
                                }*/

                                // Update Temperature Unit
                                var temp_unit_update_approved_form = document.getElementById("temp_unit_update_approved_form");
                                var new_update_temp_unit_form = document.getElementById("new_update_temp_unit_form").value;
                                var old_update_temp_unit_form = document.getElementById("old_update_temp_unit_form").value;

                                if(temp_unit_update_approved_form.checked == true){
                                    document.getElementById("new_temp_unit_update_tq_"+id).value = new_update_temp_unit_form;
                                    document.getElementById("temp_unit_update_val_approved_"+id).value = true;
                                    document.getElementById("new_temp_unit_update_tq_"+id).style.background='#ADD8E6';
                                } /*else {
                                    document.getElementById("new_temp_unit_update_tq_"+id).value = old_update_temp_unit_form;
                                    document.getElementById("temp_unit_update_val_approved_"+id).value = false;
                                    document.getElementById("new_temp_unit_update_tq_"+id).style.background='#FFFFFF';
                                }*/

                                // Update Humidity Min
                                var humidity_min_update_approved_form = document.getElementById("humidity_min_update_approved_form");
                                var new_update_hum_min_form = document.getElementById("new_update_hum_min_form").value;
                                var old_update_hum_min_form = document.getElementById("old_update_hum_min_form").value;

                                if(humidity_min_update_approved_form.checked == true){
                                    document.getElementById("new_humidity_min_update_tq_"+id).value = new_update_hum_min_form;
                                    document.getElementById("humidity_min_update_val_approved_"+id).value = true;
                                    document.getElementById("new_humidity_min_update_tq_"+id).style.background='#ADD8E6';
                                } /*else {
                                    document.getElementById("new_humidity_min_update_tq_"+id).value = old_update_hum_min_form;
                                    document.getElementById("humidity_min_update_val_approved_"+id).value = false;
                                    document.getElementById("new_humidity_min_update_tq_"+id).style.background='#FFFFFF';
                                }*/

                                // Update Humidity Max
                                var humidity_max_update_approved_form = document.getElementById("humidity_max_update_approved_form");
                                var new_update_hum_max_form = document.getElementById("new_update_hum_max_form").value;
                                var old_update_hum_max_form = document.getElementById("old_update_hum_max_form").value;

                                if(humidity_max_update_approved_form.checked == true){
                                    document.getElementById("new_humidity_max_update_tq_"+id).value = new_update_hum_max_form;
                                    document.getElementById("humidity_max_update_val_approved_"+id).value = true;
                                    document.getElementById("new_humidity_max_update_tq_"+id).style.background='#ADD8E6';
                                } /*else {
                                    document.getElementById("new_humidity_max_update_tq_"+id).value = old_update_hum_max_form;
                                    document.getElementById("humidity_max_update_val_approved_"+id).value = false;
                                    document.getElementById("new_humidity_max_update_tq_"+id).style.background='#FFFFFF';
                                }*/

                                // Update Ventilation Min
                                var ven_min_update_approved_form = document.getElementById("ven_min_update_approved_form");
                                var new_update_ven_min_form = document.getElementById("new_update_ven_min_form").value;
                                var old_update_ven_min_form = document.getElementById("old_update_ven_min_form").value;

                                if(ven_min_update_approved_form.checked == true){
                                    document.getElementById("new_ventilation_min_update_tq_"+id).value = new_update_ven_min_form;
                                    document.getElementById("ventilation_min_update_val_approved_"+id).value = true;
                                    document.getElementById("new_ventilation_min_update_tq_"+id).style.background='#ADD8E6';
                                } /*else {
                                    document.getElementById("new_ventilation_min_update_tq_"+id).value = old_update_ven_min_form;
                                    document.getElementById("ventilation_min_update_val_approved_"+id).value = false;
                                    document.getElementById("new_ventilation_min_update_tq_"+id).style.background='#FFFFFF';
                                }*/

                                // Update Ventilation Max
                                var ven_max_update_approved_form = document.getElementById("ven_max_update_approved_form");
                                var new_update_ven_max_form = document.getElementById("new_update_ven_max_form").value;
                                var old_update_ven_max_form = document.getElementById("old_update_ven_max_form").value;

                                if(ven_max_update_approved_form.checked == true){
                                    document.getElementById("new_ventilation_max_update_tq_"+id).value = new_update_ven_max_form;
                                    document.getElementById("ventilation_max_update_val_approved_"+id).value = true;
                                    document.getElementById("new_ventilation_max_update_tq_"+id).style.background='#ADD8E6';
                                } /*else {
                                    document.getElementById("new_ventilation_max_update_tq_"+id).value = old_update_ven_max_form;
                                    document.getElementById("ventilation_max_update_val_approved_"+id).value = false;
                                    document.getElementById("new_ventilation_max_update_tq_"+id).style.background='#FFFFFF';
                                }*/

                                // Update Seal Number
                                var seal_no_update_approved_form = document.getElementById("seal_no_update_approved_form");
                                var new_update_seal_no_form = document.getElementById("new_update_seal_no_form").value;
                                var old_update_seal_no_form = document.getElementById("old_update_seal_no_form").value;

                                if(seal_no_update_approved_form.checked == true){
                                    if(new_update_seal_no_form != "" && document.getElementById("new_update_seal_no_form").hasAttribute('required')){
                                        document.getElementById("new_seal_no_update_tq_"+id).value = new_update_seal_no_form;
                                        document.getElementById("seal_no_update_val_approved_"+id).value = true;
                                        document.getElementById("new_seal_no_update_tq_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_update_seal_no_form_div").innerHTML = "";
                                    } else {
                                        if (new_update_seal_no_form == "" && seal_no_update_approved_form.checked == true){
                                             document.getElementById("new_update_seal_no_form").focus();
                                             document.getElementById("new_update_seal_no_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_update_seal_no_form_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("new_seal_no_update_tq_"+id).value = old_update_seal_no_form;
                                        document.getElementById("seal_no_update_val_approved_"+id).value = false;
                                        document.getElementById("new_seal_no_update_tq_"+id).style.background='#FFFFFF';
                                        return;
                                    }
                                }

                                // Update Seal Source
                                var seal_src_update_approved_form = document.getElementById("seal_src_update_approved_form");
                                var new_update_seal_src_form = document.getElementById("new_update_seal_src_form").value;
                                var old_update_seal_src_form = document.getElementById("old_update_seal_src_form").value;

                                if(seal_src_update_approved_form.checked == true){
                                    document.getElementById("new_seal_source_update_tq_"+id).value = new_update_seal_src_form;
                                    document.getElementById("seal_source_update_val_approved_"+id).value = true;
                                    document.getElementById("new_seal_source_update_tq_"+id).style.background='#ADD8E6';
                                } /*else {
                                    document.getElementById("new_seal_source_update_tq_"+id).value = old_update_seal_src_form;
                                    document.getElementById("seal_source_update_val_approved_"+id).value = false;
                                    document.getElementById("new_seal_source_update_tq_"+id).style.background='#FFFFFF';
                                }*/

                                // Update Seal Type
                                var seal_type_update_approved_form = document.getElementById("seal_type_update_approved_form");
                                var new_update_seal_type_form = document.getElementById("new_update_seal_type_form").value;
                                var old_update_seal_type_form = document.getElementById("old_update_seal_type_form").value;

                                if(seal_type_update_approved_form.checked == true){
                                    if(new_update_seal_type_form != "" && document.getElementById("new_update_seal_type_form").hasAttribute('required')){
                                        document.getElementById("new_seal_type_update_tq_"+id).value = new_update_seal_type_form;
                                        document.getElementById("seal_type_update_val_approved_"+id).value = true;
                                        document.getElementById("new_seal_type_update_tq_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_update_seal_type_form_div").innerHTML = "";
                                    }
                                    else {
                                        if (new_update_seal_type_form == "" && seal_type_update_approved_form.checked == true){
                                             document.getElementById("new_update_seal_type_form").focus();
                                             document.getElementById("new_update_seal_type_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_update_seal_type_form_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("new_seal_type_update_tq_"+id).value = old_update_seal_type_form;
                                        document.getElementById("seal_type_update_val_approved_"+id).value = false;
                                        document.getElementById("new_seal_type_update_tq_"+id).style.background='#FFFFFF';
                                        return;
                                    }
                                }

                                var update_tq_form = document.getElementById('update_tq_form');
                                /*for(var i=0; i < update_tq_form.elements.length; i++){
                                    if(update_tq_form.elements[i].value === '' && update_tq_form.elements[i].hasAttribute('required')){
                                        *//*if (new_update_eq_ref_form == "" && eq_ref_update_approved_form.checked == true){
                                             document.getElementById("new_update_eq_ref_form").focus();
                                             document.getElementById("new_update_eq_ref_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_update_eq_ref_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_update_eq_ref_form_div").innerHTML = "";
                                        }*//*

                                        *//*if (new_update_wt_unit_form == "" && wt_unit_update_approved_form.checked == true) {
                                            document.getElementById("new_update_wt_unit_form").focus();
                                             document.getElementById("new_update_wt_unit_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_update_wt_unit_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_update_wt_unit_form_div").innerHTML = "";
                                        }*//*
                                       *//* if (new_update_cgw_form == "" && cgw_update_approved_form.checked == true) {
                                            document.getElementById("new_update_cgw_form").focus();
                                             document.getElementById("new_update_cgw_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_update_cgw_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_update_cgw_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_update_ctw_form == "" && ctw_update_approved_form.checked == true) {

                                            if (new_update_shipper_form.checked == true && ctw_update_approved_form.checked == true){
                                            document.getElementById("new_update_ctw_form").focus();
                                             document.getElementById("new_update_ctw_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_update_ctw_form_div").style.color="Red";
                                             return;
                                             }
                                        } else {
                                            document.getElementById("new_update_ctw_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_update_iso_eq_form == "" && iso_eq_update_approved_form.checked == true) {
                                            if (new_update_shipper_form.checked == true && iso_eq_update_approved_form.checked == true){
                                            document.getElementById("new_update_iso_eq_form").focus();
                                             document.getElementById("new_update_iso_eq_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_update_iso_eq_form_div").style.color="Red";
                                             return;
                                             }
                                        } else {
                                            document.getElementById("new_update_iso_eq_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_update_seal_no_form == "" && seal_no_update_approved_form.checked == true) {
                                            document.getElementById("new_update_seal_no_form").focus();
                                             document.getElementById("new_update_seal_no_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_update_seal_no_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_update_seal_no_form_div").innerHTML = "";
                                        }*//*
                                        *//*if (new_update_seal_type_form == "" && seal_type_update_approved_form.checked == true) {
                                            document.getElementById("new_update_seal_type_form").focus();
                                             document.getElementById("new_update_seal_type_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_update_seal_type_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_update_seal_type_form_div").innerHTML = "";
                                        }*//*
                                    }
                                }*/
                                var reg = /^[+-]?\d+(\.\d+)?$/;
                                if(reg.test(new_update_temp_min_form)  && temp_min_update_approved_form.checked == true){
                                    document.getElementById("new_update_temp_min_form_div").innerHTML = "";
                                } else {
                                if(temp_min_update_approved_form.checked == true){
                                    document.getElementById("new_update_temp_min_form").focus();
                                    document.getElementById("new_update_temp_min_form_div").innerHTML = "Please enter a valid number or 0";
                                    document.getElementById("new_update_temp_min_form_div").style.color="Red";
                                    return;
                                    }
                                }

                                if (reg.test(new_update_temp_max_form) && temp_max_update_approved_form.checked == true){
                                    document.getElementById("new_update_temp_max_form_div").innerHTML = "";
                                } else {
                                    if(temp_max_update_approved_form.checked == true){
                                    document.getElementById("new_update_temp_max_form").focus();
                                    document.getElementById("new_update_temp_max_form_div").innerHTML = "Please enter number";
                                    document.getElementById("new_update_temp_max_form_div").style.color="Red";
                                    return;
                                    }

                                }
                                 if (reg.test(new_update_hum_min_form) && humidity_min_update_approved_form.checked == true){
                                    document.getElementById("new_update_hum_min_form_div").innerHTML = "";
                                } else {
                                    if(humidity_min_update_approved_form.checked == true){
                                    document.getElementById("new_update_hum_min_form").focus();
                                    document.getElementById("new_update_hum_min_form_div").innerHTML = "Please enter number";
                                    document.getElementById("new_update_hum_min_form_div").style.color="Red";
                                    return;
                                    }
                                }
                                if (reg.test(new_update_hum_max_form) && humidity_max_update_approved_form.checked == true){
                                    document.getElementById("new_update_hum_max_form_div").innerHTML = "";
                                } else {
                                    if (humidity_max_update_approved_form.checked == true){
                                    document.getElementById("new_update_hum_max_form").focus();
                                    document.getElementById("new_update_hum_max_form_div").innerHTML = "Please enter number";
                                    document.getElementById("new_update_hum_max_form_div").style.color="Red";
                                    return;
                                    }
                                }
                                if (reg.test(new_update_ven_min_form ) && ven_min_update_approved_form.checked == true){
                                    document.getElementById("new_update_ven_min_form_div").innerHTML = "";
                                } else {
                                    if (ven_min_update_approved_form.checked == true){
                                    document.getElementById("new_update_ven_min_form").focus();
                                    document.getElementById("new_update_ven_min_form_div").innerHTML = "Please enter number";
                                    document.getElementById("new_update_ven_min_form_div").style.color="Red";
                                    return;
                                    }
                                }

                                if (reg.test(new_update_ven_max_form) && ven_max_update_approved_form.checked == true){
                                    document.getElementById("new_update_ven_max_form_div").innerHTML = "";
                                } else {
                                    if(ven_max_update_approved_form.checked == true) {
                                    document.getElementById("new_update_ven_max_form").focus();
                                    document.getElementById("new_update_ven_max_form_div").innerHTML = "Please enter number";
                                    document.getElementById("new_update_ven_max_form_div").style.color="Red";
                                    return;
                                    }
                                }

                                dialog.close();

                            }
                        }]
                    });
                    dialog.opened().then(function () {
//                        $(".close").hide();

                        var update_tq_form = document.getElementById('update_tq_form');
                        for(var i=0; i < update_tq_form.elements.length; i++){
                            if(update_tq_form.elements[i].hasAttribute('required')){
                                update_tq_form.elements[i].style.background='#ADD8E6';
                            }
                        }
                        var update_tq_row_id_form = document.getElementById("tq_update_row_id_"+id).value;
                        document.getElementById("update_tq_row_id_form").value = update_tq_row_id_form;

                        // Update Created By value
                        var si_created_by_val = document.getElementById("si_created_by").value;
                        document.getElementById("update_eq_ref_created_by").value = si_created_by_val;
                        document.getElementById("update_wt_unit_created_by").value = si_created_by_val;
                        document.getElementById("update_cgw_created_by").value = si_created_by_val;
                        document.getElementById("update_ctw_created_by").value = si_created_by_val;
                        document.getElementById("update_iso_eq_created_by").value = si_created_by_val;
                        document.getElementById("update_shipper_created_by").value = si_created_by_val;
                        document.getElementById("update_temp_min_created_by").value = si_created_by_val;
                        document.getElementById("update_temp_max_created_by").value = si_created_by_val;
                        document.getElementById("update_temp_unit_created_by").value = si_created_by_val;
                        document.getElementById("update_humidity_min_created_by").value = si_created_by_val;
                        document.getElementById("update_humidity_max_created_by").value = si_created_by_val;
                        document.getElementById("update_ven_min_created_by").value = si_created_by_val;
                        document.getElementById("update_ven_max_created_by").value = si_created_by_val;
                        document.getElementById("update_seal_no_created_by").value = si_created_by_val;
                        document.getElementById("update_seal_src_created_by").value = si_created_by_val;
                        document.getElementById("update_seal_type_created_by").value = si_created_by_val;

                        // By default set modified by - but still user can edit
                        document.getElementById("update_eq_ref_modify_by").value = si_created_by_val;
                        document.getElementById("update_wt_unit_modify_by").value = si_created_by_val;
                        document.getElementById("update_cgw_modify_by").value = si_created_by_val;
                        document.getElementById("update_ctw_modify_by").value = si_created_by_val;
                        document.getElementById("update_iso_eq_modify_by").value = si_created_by_val;
                        document.getElementById("update_shipper_modify_by").value = si_created_by_val;
                        document.getElementById("update_temp_min_modify_by").value = si_created_by_val;
                        document.getElementById("update_temp_max_modify_by").value = si_created_by_val;
                        document.getElementById("update_temp_unit_modify_by").value = si_created_by_val;
                        document.getElementById("update_humidity_min_modify_by").value = si_created_by_val;
                        document.getElementById("update_humidity_max_modify_by").value = si_created_by_val;
                        document.getElementById("update_ven_min_modify_by").value = si_created_by_val;
                        document.getElementById("update_ven_max_modify_by").value = si_created_by_val;
                        document.getElementById("update_seal_no_modify_by").value = si_created_by_val;
                        document.getElementById("update_seal_src_modify_by").value = si_created_by_val;
                        document.getElementById("update_seal_type_modify_by").value = si_created_by_val;


                        // update Container ID
                        // old value
                        var update_old_eq_ref_form = document.getElementById("old_update_eq_id_"+id).value;
                        document.getElementById("old_update_eq_ref_form").value = update_old_eq_ref_form;
                        document.getElementById("new_update_eq_ref_form").value = update_old_eq_ref_form;
                        // new value
                        /*var update_new_eq_ref_form = document.getElementById("new_update_eq_id_"+id).value;
                        if (update_old_eq_ref_form === update_new_eq_ref_form){
                            document.getElementById("new_update_eq_ref_form").value = "";
                        } else{
                            document.getElementById("new_update_eq_ref_form").value = update_new_eq_ref_form;
                        }*/
                        // To make approve check box checked by default if it is approved once
                        var eq_update_val_approved = document.getElementById("eq_update_val_approved_"+id).value;
                        var eq_ref_update_approved_form = document.getElementById("eq_ref_update_approved_form");
                        if (eq_update_val_approved == "true"){
                            eq_ref_update_approved_form.checked = true;
                        } else {
                            eq_ref_update_approved_form.checked = false;
                        }

                        // update Weight Unit
                        // old value
                        var update_old_wt_unit_form = document.getElementById("old_wt_unit_update_tq_"+id).value;
                        document.getElementById("old_update_wt_unit_form").value = update_old_wt_unit_form;
                        // new value
                        var update_new_wt_unit_form = document.getElementById("new_wt_unit_update_tq_"+id).value;
                        if (update_old_wt_unit_form === update_new_wt_unit_form){
                            document.getElementById("new_update_wt_unit_form").value = "";
                        } else{
                            document.getElementById("new_update_wt_unit_form").value = update_new_wt_unit_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var wt_unit_update_val_approved = document.getElementById("wt_unit_update_val_approved_"+id).value;
                        var wt_unit_update_approved_form = document.getElementById("wt_unit_update_approved_form");
                        if (wt_unit_update_val_approved == "true"){
                            wt_unit_update_approved_form.checked = true;
                        } else {
                            wt_unit_update_approved_form.checked = false;
                        }

                        // update Cargo Gross Weight
                        // old value
                        var old_update_cgw_form = document.getElementById("old_cgw_update_tq_"+id).value;
                        document.getElementById("old_update_cgw_form").value = old_update_cgw_form;
                        // new value
                        var new_update_cgw_form = document.getElementById("new_cgw_update_tq_"+id).value;
                        if (old_update_cgw_form === new_update_cgw_form){
                            document.getElementById("new_update_cgw_form").value = "";
                        } else{
                            document.getElementById("new_update_cgw_form").value = new_update_cgw_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var cgw_update_update_val_approved = document.getElementById("cgw_update_update_val_approved_"+id).value;
                        var cgw_update_approved_form = document.getElementById("cgw_update_approved_form");
                        if (cgw_update_update_val_approved == "true"){
                            cgw_update_approved_form.checked = true;
                        } else {
                            cgw_update_approved_form.checked = false;
                        }

                        // update Container tare weight
                        // old value
                        var old_update_ctw_form = document.getElementById("old_ctw_update_tq_"+id).value;
                        document.getElementById("old_update_ctw_form").value = old_update_ctw_form;
                        // new value
                        var new_update_ctw_form = document.getElementById("new_ctw_update_tq_"+id).value;
                        if (old_update_ctw_form === new_update_ctw_form){
                            document.getElementById("new_update_ctw_form").value = "";
                        } else{
                            document.getElementById("new_update_ctw_form").value = new_update_ctw_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var ctw_update_val_approved = document.getElementById("ctw_update_val_approved_"+id).value;
                        var ctw_update_approved_form = document.getElementById("ctw_update_approved_form");
                        if (ctw_update_val_approved == "true"){
                            ctw_update_approved_form.checked = true;
                        } else {
                            ctw_update_approved_form.checked = false;
                        }

                        // update ISO equipment code
                        // old value
                        var old_update_iso_eq_form = document.getElementById("old_iso_eq_code_update_tq_"+id).value;
                        document.getElementById("old_update_iso_eq_form").value = old_update_iso_eq_form;
                        // new value
                        var new_update_iso_eq_form = document.getElementById("new_iso_eq_code_update_tq_"+id).value;
                        if (old_update_iso_eq_form === new_update_iso_eq_form){
                            document.getElementById("new_update_iso_eq_form").value = "";
                        } else{
                            document.getElementById("new_update_iso_eq_form").value = new_update_iso_eq_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var iso_eq_code_update_val_approved = document.getElementById("iso_eq_code_update_val_approved_"+id).value;
                        var iso_eq_update_approved_form = document.getElementById("iso_eq_update_approved_form");
                        if (iso_eq_code_update_val_approved == "true"){
                            iso_eq_update_approved_form.checked = true;
                        } else {
                            iso_eq_update_approved_form.checked = false;
                        }

                        // update Is shipper owned
                        // old value
                        var old_update_shipper_form = document.getElementById("old_is_shipper_owned_update_tq_"+id);
                        if(old_update_shipper_form.checked == true){
                            document.getElementById("old_update_shipper_form").checked = true;
                        } else {
                            document.getElementById("old_update_shipper_form").checked = false;
                        }
                        // new value
                        var new_update_shipper_form = document.getElementById("new_is_shipper_owned_update_tq_"+id);

                            if(new_update_shipper_form.checked == true){
                                document.getElementById("new_update_shipper_form").checked = true;
                            } else {
                                document.getElementById("new_update_shipper_form").checked = false;
                            }
                        // To make approve check box checked by default if it is approved once
                        var is_shipper_owned_update_val_approved = document.getElementById("is_shipper_owned_update_val_approved_"+id).value;
                        var shipper_update_approved_form = document.getElementById("shipper_update_approved_form");
                        if (is_shipper_owned_update_val_approved == "true"){
                            shipper_update_approved_form.checked = true;
                        } else {
                            shipper_update_approved_form.checked = false;
                        }

                        var  new_update_temp_min_form = 0;
                        var new_update_temp_max_form = 0;

                        // update Temperature Min
                        // old value
                        var old_update_temp_min_form = document.getElementById("old_temp_min_update_tq_"+id).value;
                        document.getElementById("old_update_temp_min_form").value = old_update_temp_min_form;
                        // new value
                        var new_update_temp_min_form = document.getElementById("new_temp_min_update_tq_"+id).value;
                        if (old_update_temp_min_form === new_update_temp_min_form){
                            document.getElementById("new_update_temp_min_form").value = 0;
                        } else{
                            document.getElementById("new_update_temp_min_form").value = new_update_temp_min_form;
                        }

                        // To make approve check box checked by default if it is approved once
                        var temp_min_update_val_approved = document.getElementById("temp_min_update_val_approved_"+id).value;
                        var temp_min_update_approved_form = document.getElementById("temp_min_update_approved_form");
                        if (temp_min_update_val_approved == "true"){
                            temp_min_update_approved_form.checked = true;
                        } else {
                            temp_min_update_approved_form.checked = false;
                        }

                        // update Temperature Max
                        // old value
                        var old_update_temp_max_form = document.getElementById("old_temp_max_update_tq_"+id).value;
                        document.getElementById("old_update_temp_max_form").value = old_update_temp_max_form;
                        // new value
                        var new_update_temp_max_form = document.getElementById("new_temp_max_update_tq_"+id).value;
                        if (old_update_temp_max_form === new_update_temp_max_form){
                            document.getElementById("new_update_temp_max_form").value = 0;
                        } else{
                            document.getElementById("new_update_temp_max_form").value = new_update_temp_max_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var temp_max_update_val_approved = document.getElementById("temp_max_update_val_approved_"+id).value;
                        var temp_max_update_approved_form = document.getElementById("temp_max_update_approved_form");
                        if (temp_max_update_val_approved == "true"){
                            temp_max_update_approved_form.checked = true;
                        } else {
                            temp_max_update_approved_form.checked = false;
                        }

                        // update Temperature Unit
                        // old value
                        var old_update_temp_unit_form = document.getElementById("old_temp_unit_update_tq_"+id).value;
                        document.getElementById("old_update_temp_unit_form").value = old_update_temp_unit_form;
                        // new value
                        var new_update_temp_unit_form = document.getElementById("new_temp_unit_update_tq_"+id).value;
                        if (old_update_temp_unit_form === new_update_temp_unit_form){
                            document.getElementById("new_update_temp_unit_form").value = "";
                        } else{
                            document.getElementById("new_update_temp_unit_form").value = new_update_temp_unit_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var temp_unit_update_val_approved = document.getElementById("temp_unit_update_val_approved_"+id).value;
                        var temp_unit_update_approved_form = document.getElementById("temp_unit_update_approved_form");
                        if (temp_unit_update_val_approved == "true"){
                            temp_unit_update_approved_form.checked = true;
                        } else {
                            temp_unit_update_approved_form.checked = false;
                        }

                        var new_update_hum_min_form = 0;
                        var new_update_hum_max_form = 0;

                        // update Humidity Min
                        // old value
                        var old_update_hum_min_form = document.getElementById("old_humidity_min_update_tq_"+id).value;
                        document.getElementById("old_update_hum_min_form").value = old_update_hum_min_form;
                        // new value
                        var new_update_hum_min_form = document.getElementById("new_humidity_min_update_tq_"+id).value;
                        if (old_update_hum_min_form === new_update_hum_min_form){
                            document.getElementById("new_update_hum_min_form").value = 0;
                        } else{
                            document.getElementById("new_update_hum_min_form").value = new_update_hum_min_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var humidity_min_update_val_approved = document.getElementById("humidity_min_update_val_approved_"+id).value;
                        var humidity_min_update_approved_form = document.getElementById("humidity_min_update_approved_form");
                        if (humidity_min_update_val_approved == "true"){
                            humidity_min_update_approved_form.checked = true;
                        } else {
                            humidity_min_update_approved_form.checked = false;
                        }

                        // update Humidity Max
                        // old value
                        var old_update_hum_max_form = document.getElementById("old_humidity_max_update_tq_"+id).value;
                        document.getElementById("old_update_hum_max_form").value = old_update_hum_max_form;
                        // new value
                        var new_update_hum_max_form = document.getElementById("new_humidity_max_update_tq_"+id).value;
                        if (old_update_hum_max_form === new_update_hum_max_form){
                            document.getElementById("new_update_hum_max_form").value = 0;
                        } else{
                            document.getElementById("new_update_hum_max_form").value = new_update_hum_max_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var humidity_max_update_val_approved = document.getElementById("humidity_max_update_val_approved_"+id).value;
                        var humidity_max_update_approved_form = document.getElementById("humidity_max_update_approved_form");
                        if (humidity_max_update_val_approved == "true"){
                            humidity_max_update_approved_form.checked = true;
                        } else {
                            humidity_max_update_approved_form.checked = false;
                        }

                        var new_update_ven_min_form = 0;
                        var new_update_ven_max_form = 0;
                        // update Ventilation Min
                        // old value
                        var old_update_ven_min_form = document.getElementById("old_ventilation_min_update_tq_"+id).value;
                        document.getElementById("old_update_ven_min_form").value = old_update_ven_min_form;
                        // new value
                        var new_update_ven_min_form = document.getElementById("new_ventilation_min_update_tq_"+id).value;
                        if (old_update_ven_min_form === new_update_ven_min_form){
                            document.getElementById("new_update_ven_min_form").value = 0;
                        } else{
                            document.getElementById("new_update_ven_min_form").value = new_update_ven_min_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var ventilation_min_update_val_approved = document.getElementById("ventilation_min_update_val_approved_"+id).value;
                        var ven_min_update_approved_form = document.getElementById("ven_min_update_approved_form");
                        if (ventilation_min_update_val_approved == "true"){
                            ven_min_update_approved_form.checked = true;
                        } else {
                            ven_min_update_approved_form.checked = false;
                        }

                        // update Ventilation Max
                        // old value
                        var old_update_ven_max_form = document.getElementById("old_ventilation_max_update_tq_"+id).value;
                        document.getElementById("old_update_ven_max_form").value = old_update_ven_max_form;
                        // new value
                        var new_update_ven_max_form = document.getElementById("new_ventilation_max_update_tq_"+id).value;
                        if (old_update_ven_max_form === new_update_ven_max_form){
                            document.getElementById("new_update_ven_max_form").value = 0;
                        } else{
                            document.getElementById("new_update_ven_max_form").value = new_update_ven_max_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var ventilation_max_update_val_approved = document.getElementById("ventilation_max_update_val_approved_"+id).value;
                        var ven_max_update_approved_form = document.getElementById("ven_max_update_approved_form");
                        if (ventilation_max_update_val_approved == "true"){
                            ven_max_update_approved_form.checked = true;
                        } else {
                            ven_max_update_approved_form.checked = false;
                        }

                        // update Seal Number
                        // old value
                        var old_update_seal_no_form = document.getElementById("old_seal_no_update_tq_"+id).value;
                        document.getElementById("old_update_seal_no_form").value = old_update_seal_no_form;
                        // new value
                        var new_update_seal_no_form = document.getElementById("new_seal_no_update_tq_"+id).value;
                        if (old_update_seal_no_form === new_update_seal_no_form){
                            document.getElementById("new_update_seal_no_form").value = "";
                        } else{
                            document.getElementById("new_update_seal_no_form").value = new_update_seal_no_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var seal_no_update_val_approved = document.getElementById("seal_no_update_val_approved_"+id).value;
                        var seal_no_update_approved_form = document.getElementById("seal_no_update_approved_form");
                        if (seal_no_update_val_approved == "true"){
                            seal_no_update_approved_form.checked = true;
                        } else {
                            seal_no_update_approved_form.checked = false;
                        }

                        // update Seal Source
                        // old value
                        var old_update_seal_src_form = document.getElementById("old_seal_source_update_tq_"+id).value;
                        document.getElementById("old_update_seal_src_form").value = old_update_seal_src_form;
                        // new value
                        var new_update_seal_src_form = document.getElementById("new_seal_source_update_tq_"+id).value;
                        if (old_update_seal_src_form === new_update_seal_src_form){
                            document.getElementById("new_update_seal_src_form").value = "";
                        } else{
                            document.getElementById("new_update_seal_src_form").value = new_update_seal_src_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var seal_source_update_val_approved = document.getElementById("seal_source_update_val_approved_"+id).value;
                        var seal_src_update_approved_form = document.getElementById("seal_src_update_approved_form");
                        if (seal_source_update_val_approved == "true"){
                            seal_src_update_approved_form.checked = true;
                        } else {
                            seal_src_update_approved_form.checked = false;
                        }

                        // update Seal Type
                        // old value
                        var old_update_seal_type_form = document.getElementById("old_seal_type_update_tq_"+id).value;
                        document.getElementById("old_update_seal_type_form").value = old_update_seal_type_form;
                        // new value
                        var new_update_seal_type_form = document.getElementById("new_seal_type_update_tq_"+id).value;
                        if (old_update_seal_type_form === new_update_seal_type_form){
                            document.getElementById("new_update_seal_type_form").value = "";
                        } else{
                            document.getElementById("new_update_seal_type_form").value = new_update_seal_type_form;
                        }
                        // To make approve check box checked by default if it is approved once
                        var seal_type_update_val_approved = document.getElementById("seal_type_update_val_approved_"+id).value;
                        var seal_type_update_approved_form = document.getElementById("seal_type_update_approved_form");
                        if (seal_type_update_val_approved == "true"){
                            seal_type_update_approved_form.checked = true;
                        } else {
                            seal_type_update_approved_form.checked = false;
                        }

                    });
                    dialog.open();

                });
            });

            // Edit/View Cargo Item Popup
            $('#cargo_tbody_update_si').on('click', '.cargo_view_update', function () {
                var child = $(this).closest('tr');
                child.each(function () {
                    var id = $(this).attr('id');
                    var dialog = new Dialog(this, {
                        title: _t("Update Shipping Instruction - Cargo Items"),
                        $content: $(qweb.render('freightbox.update_cargo_item_values_popup')),
                        buttons: [{
                            text: _t('Update'),
                            classes: "btn-primary",
                            close: false,
                            click: function () {
                                /*var update_row_id_form = document.getElementById("update_popup_approve_all_form");
                                if(update_row_id_form.checked == true){
                                    document.getElementById("update_row_id_"+id).style.background='#ADD8E6';
                                    document.getElementById("update_cargo_line_items_id_"+id).style.background='#ADD8E6';
                                    document.getElementById("update_shipping_marks_id_"+id).style.background='#ADD8E6';
                                    document.getElementById("update_carrier_booking_reference_id_"+id).style.background='#ADD8E6';
                                    document.getElementById("update_description_of_goods_id_"+id).style.background='#ADD8E6';
                                    document.getElementById("update_hs_code_id_"+id).style.background='#ADD8E6';
                                    document.getElementById("update_number_of_packages_id_"+id).style.background='#ADD8E6';
                                    document.getElementById("update_weight_id_"+id).style.background='#ADD8E6';
                                    document.getElementById("update_volume_id_"+id).style.background='#ADD8E6';
                                    document.getElementById("update_weight_unit_id_"+id).style.background='#ADD8E6';
                                    document.getElementById("update_volume_unit_id_"+id).style.background='#ADD8E6';
                                    document.getElementById("update_package_code_id_"+id).style.background='#ADD8E6';
                                    document.getElementById("update_equipment_reference_id_"+id).style.background='#ADD8E6';
                                }*/

                                // Update Cargo Lie Item ID
                                var new_cargo_line_item_id_form = document.getElementById("new_update_cargo_line_item_id_form");
                                var cargo_line_approved_form = document.getElementById("cargo_line_approved_form");
                                var update_cargo_line_item_id_form = document.getElementById("new_update_cargo_line_item_id_form").value;
                                var update_old_cargo_line_item_id_form = document.getElementById("old_update_cargo_line_item_id_form").value;

                                if(cargo_line_approved_form.checked == true) {
                                    if(update_cargo_line_item_id_form != "" && new_cargo_line_item_id_form.hasAttribute('required')){
                                        document.getElementById("update_cargo_line_items_id_"+id).value = update_cargo_line_item_id_form;
                                        document.getElementById("cl_val_approved_"+id).value = true;
                                        document.getElementById("update_cargo_line_items_id_"+id).style.background='#ADD8E6';
                                        document.getElementById("cargo_line_item_id_div").innerHTML = "";
                                    } else {
                                        if (update_cargo_line_item_id_form == "" && cargo_line_approved_form.checked == true){
                                             document.getElementById("new_update_cargo_line_item_id_form").focus();
                                             document.getElementById("cargo_line_item_id_div").innerHTML = "Please fill this field";
                                             document.getElementById("cargo_line_item_id_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("update_cargo_line_items_id_"+id).value = update_old_cargo_line_item_id_form;
                                        document.getElementById("cl_val_approved_"+id).value = false;
                                        document.getElementById("update_cargo_line_items_id_"+id).style.background='#FFFFFF';
                                        return;
                                    }
                                }

                                // Shipping Marks
                                var update_new_shipping_marks_form = document.getElementById("new_update_shipping_marks_form").value;
                                var update_old_shipping_marks_form = document.getElementById("old_update_shipping_marks_form").value;
                                var update_shipping_marks_form_approved_form = document.getElementById("update_shipping_marks_form_approved_form");
                                if(update_shipping_marks_form_approved_form.checked == true){
                                    if(update_new_shipping_marks_form != "" && document.getElementById("new_update_shipping_marks_form").hasAttribute('required')){
                                        document.getElementById("update_shipping_marks_id_"+id).value = update_new_shipping_marks_form;
                                        document.getElementById("sm_val_approved_"+id).value = true;
                                        document.getElementById("update_shipping_marks_id_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_update_shipping_marks_form_div").innerHTML = "";
                                    } else {
                                        if (update_new_shipping_marks_form == "" && update_shipping_marks_form_approved_form.checked == true){
                                             document.getElementById("new_update_shipping_marks_form").focus();
                                             document.getElementById("new_update_shipping_marks_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_update_shipping_marks_form_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("update_shipping_marks_id_"+id).value = update_old_shipping_marks_form;
                                        document.getElementById("sm_val_approved_"+id).value = false;
                                        document.getElementById("update_shipping_marks_id_"+id).style.background='#FFFFFF';
                                        return;
                                    }
                                }

                                // carrier_booking_reference
                                var update_cbr_approved = document.getElementById("update_cbr_approved");
                                var update_new_cbr_form = document.getElementById("new_update_carrier_booking_reference").value;
                                var update_old_cbr_form = document.getElementById("old_update_carrier_booking_reference_form").value;
                                if(update_cbr_approved.checked == true){
                                        document.getElementById("update_carrier_booking_reference_id_"+id).value = update_old_cbr_form;
                                        document.getElementById("cbr_val_approved_"+id).value = true;
                                        document.getElementById("update_carrier_booking_reference_id_"+id).style.background='#ADD8E6';
                                } /*else {

                                        document.getElementById("update_carrier_booking_reference_id_"+id).value = update_old_cbr_form;
                                        document.getElementById("cbr_val_approved_"+id).value = false;
                                        document.getElementById("update_carrier_booking_reference_id_"+id).style.background='#FFFFFF';
                                }*/


                                // description_of_goods
                                var update_new_dog_form = document.getElementById("new_update_description_of_goods_form").value;
                                var update_old_dog_form = document.getElementById("old_update_description_of_goods_form").value;
                                var update_dog_form_approved = document.getElementById("update_description_of_goods_form_approved");
                                if(update_dog_form_approved.checked == true){
                                    if(update_new_dog_form != "" && document.getElementById("new_update_description_of_goods_form").hasAttribute('required')){
//                                        alert("ifff");
                                        document.getElementById("update_description_of_goods_id_"+id).value = update_new_dog_form;
                                        document.getElementById("dog_val_approved_"+id).value = true;
                                        document.getElementById("update_description_of_goods_id_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_update_dog_form_div").innerHTML = "";
                                    }
                                    else {
                                        if (update_new_dog_form == "" && update_dog_form_approved.checked == true){
                                             document.getElementById("new_update_description_of_goods_form").focus();
                                             document.getElementById("new_update_dog_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_update_dog_form_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("update_description_of_goods_id_"+id).value = update_old_dog_form;
                                        document.getElementById("dog_val_approved_"+id).value = false;
                                        document.getElementById("update_description_of_goods_id_"+id).style.background='#FFFFFF';
                                        return;
                                }
                            }

                                // HS code
                                var update_new_hscode_form = document.getElementById("new_update_hs_code_form").value;
                                var update_old_hscode_form = document.getElementById("old_update_hs_code_form").value;
                                var update_hs_code_form_approved = document.getElementById("update_hs_code_form_approved");
                                if(update_hs_code_form_approved.checked == true){
                                    if(update_new_hscode_form != "" && document.getElementById("new_update_hs_code_form").hasAttribute('required')){
                                        document.getElementById("update_hs_code_id_"+id).value = update_new_hscode_form ;
                                        document.getElementById("hs_val_approved_"+id).value = true;
                                        document.getElementById("update_hs_code_id_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_update_hs_code_form_div").innerHTML = "";
                                    }
                                    else {
                                        if (update_new_hscode_form == "" && update_hs_code_form_approved.checked == true){
                                             document.getElementById("new_update_hs_code_form").focus();
                                             document.getElementById("new_update_hs_code_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_update_hs_code_form_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("update_hs_code_id_"+id).value = update_old_hscode_form ;
                                        document.getElementById("hs_val_approved_"+id).value = false;
                                        document.getElementById("update_hs_code_id_"+id).style.background='#FFFFFF';
                                        return;
                                    }
                                }

                                // no_of_packages
                                var update_new_no_of_packages = document.getElementById("update_new_no_of_packages").value;
                                var update_old_no_of_packages = document.getElementById("update_old_no_of_packages").value;
                                var update_no_of_packages_form_approved = document.getElementById("update_no_of_packages_form_approved");
                                if(update_no_of_packages_form_approved.checked == true){
                                    if(update_new_no_of_packages != "" && document.getElementById("update_new_no_of_packages").hasAttribute('required')){
                                        document.getElementById("update_number_of_packages_id_"+id).value = update_new_no_of_packages;
                                        document.getElementById("nop_val_approved_"+id).value = true;
                                        document.getElementById("update_number_of_packages_id_"+id).style.background='#ADD8E6';
                                        document.getElementById("update_new_no_of_packages_div").innerHTML = "";
                                    }
                                    else {
                                        if (update_new_no_of_packages == "" && update_no_of_packages_form_approved.checked == true){
                                             document.getElementById("update_new_no_of_packages").focus();
                                             document.getElementById("update_new_no_of_packages_div").innerHTML = "Please fill this field";
                                             document.getElementById("update_new_no_of_packages_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("update_number_of_packages_id_"+id).value = update_old_no_of_packages;
                                        document.getElementById("nop_val_approved_"+id).value = false;
                                        document.getElementById("update_number_of_packages_id_"+id).style.background='#FFFFFF';
                                        return;
                                    }
                                }

                                // weight
                                var update_new_wt_form = document.getElementById("new_update_weight_form").value;
                                var update_old_wt_form = document.getElementById("old_update_weight_form").value;
                                var update_weight_form_approved = document.getElementById("update_weight_form_approved");
                                if(update_weight_form_approved.checked == true){
                                    if(update_new_wt_form != "" && document.getElementById("new_update_weight_form").hasAttribute('required')){
                                        document.getElementById("update_weight_id_"+id).value = update_new_wt_form;
                                        document.getElementById("wt_val_approved_"+id).value = true;
                                        document.getElementById("update_weight_id_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_update_weight_form_div").innerHTML = "";
                                    }
                                    else {
                                        if (update_new_wt_form == "" && update_weight_form_approved.checked == true){
                                             document.getElementById("new_update_weight_form").focus();
                                             document.getElementById("new_update_weight_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_update_weight_form_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("update_weight_id_"+id).value = update_old_wt_form;
                                        document.getElementById("wt_val_approved_"+id).value = false;
                                        document.getElementById("update_weight_id_"+id).style.background='#FFFFFF';
                                        return;
                                    }
                                }
                                // volume
                                var update_new_volume_form = document.getElementById("new_update_volume_form").value;
                                var update_old_volume_form = document.getElementById("old_update_volume_form").value;
                                var update_volume_form_approved = document.getElementById("update_volume_form_approved");
                                if(update_volume_form_approved.checked == true){
                                        document.getElementById("update_volume_id_"+id).value = update_new_volume_form;
                                        document.getElementById("vl_val_approved_"+id).value = true;
                                        document.getElementById("update_volume_id_"+id).style.background='#ADD8E6';
                                } /*else {
                                    document.getElementById("update_volume_id_"+id).value = update_old_volume_form;
                                    document.getElementById("vl_val_approved_"+id).value = false;
                                    document.getElementById("update_volume_id_"+id).style.background='#FFFFFF';
                                }*/

                                // wt_unit
                                var update_new_wt_unit_form = document.getElementById("new_update_wt_unit_form").value;
                                var update_old_wt_unit_form = document.getElementById("old_update_wt_unit_form").value;
                                var update_wt_unit_form_approved = document.getElementById("update_wt_unit_form_approved");
                                if(update_wt_unit_form_approved.checked == true){
                                    if(update_new_wt_unit_form != "" && document.getElementById("new_update_wt_unit_form").hasAttribute('required')){
                                        document.getElementById("update_weight_unit_id_"+id).value = update_new_wt_unit_form;
                                        document.getElementById("wt_unit_val_approved_"+id).value = true;
                                        document.getElementById("update_weight_unit_id_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_update_wt_unit_form_div").innerHTML = "";
                                    }
                                    else {
                                        if (update_new_wt_unit_form == "" && update_wt_unit_form_approved.checked == true){
                                             document.getElementById("new_update_wt_unit_form").focus();
                                             document.getElementById("new_update_wt_unit_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_update_wt_unit_form_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("update_weight_unit_id_"+id).value = update_old_wt_unit_form;
                                        document.getElementById("wt_unit_val_approved_"+id).value = false;
                                        document.getElementById("update_weight_unit_id_"+id).style.background='#FFFFFF';
                                        return;
                                    }
                                }

                                //  volume_unit
                                var update_new_volume_unit_form = document.getElementById("new_update_volume_unit_form").value;
                                var update_old_volume_unit_form = document.getElementById("old_update_volume_unit_form").value;
                                var update_volume_unit_form_approved = document.getElementById("update_volume_unit_form_approved");
                                if(update_volume_unit_form_approved.checked == true){
                                    document.getElementById("update_volume_unit_id_"+id).value = update_new_volume_unit_form;
                                    document.getElementById("vl_unit_val_approved_"+id).value = true;
                                    document.getElementById("update_volume_unit_id_"+id).style.background='#ADD8E6';
                                } /*else {
                                    document.getElementById("update_volume_unit_id_"+id).value = update_old_volume_unit_form;
                                    document.getElementById("vl_unit_val_approved_"+id).value = false;
                                    document.getElementById("update_volume_unit_id_"+id).style.background='#FFFFFF';
                                }*/

                                // package_code
                                var update_new_pc_form = document.getElementById("new_update_package_code_form").value;
                                var update_old_pc_form = document.getElementById("old_update_package_code_form").value;
                                var update_package_code_form_approved = document.getElementById("update_package_code_form_approved");
                                if(update_package_code_form_approved.checked == true){
                                    if(update_new_pc_form != "" && document.getElementById("new_update_package_code_form").hasAttribute('required')){
                                        document.getElementById("update_package_code_id_"+id).value = update_new_pc_form;
                                        document.getElementById("pc_val_approved_"+id).value = true;
                                        document.getElementById("update_package_code_id_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_update_package_code_form_div").innerHTML = "";
                                    }
                                    else {
                                        if (update_new_pc_form == "" && update_package_code_form_approved.checked == true){
                                             document.getElementById("new_update_package_code_form").focus();
                                             document.getElementById("new_update_package_code_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_update_package_code_form_div").style.color="Red";
                                             return;
                                        }
                                        document.getElementById("update_package_code_id_"+id).value = update_old_pc_form;
                                        document.getElementById("pc_val_approved_"+id).value = false;
                                        document.getElementById("update_package_code_id_"+id).style.background='#FFFFFF';
                                        return;
                                    }
                                }

                                // container_id
                                var update_new_container_id_form = document.getElementById("new_update_container_id_form").value;
                                var update_old_container_id_form = document.getElementById("old_update_container_id_form").value;
                                var update_container_id_form_approved = document.getElementById("update_container_id_form_approved");
                                if(update_container_id_form_approved.checked == true){
                                    if(update_new_container_id_form != "" && document.getElementById("new_update_container_id_form").hasAttribute('required')){
                                        document.getElementById("update_equipment_reference_id_"+id).value = update_old_container_id_form;
                                        document.getElementById("eq_val_approved_"+id).value = true;
                                        document.getElementById("update_equipment_reference_id_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_update_container_id_form_div").innerHTML = "";
                                    }
                                    else {
                                        /*if (update_new_container_id_form == "" && update_container_id_form_approved.checked == true){
                                             document.getElementById("new_update_container_id_form").focus();
                                             document.getElementById("new_update_container_id_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_update_container_id_form_div").style.color="Red";
                                             return;
                                        }*/
                                        document.getElementById("update_equipment_reference_id_"+id).value = update_old_container_id_form;
                                        document.getElementById("eq_val_approved_"+id).value = true;
                                        document.getElementById("update_equipment_reference_id_"+id).style.background='#ADD8E6';
                                        document.getElementById("new_update_container_id_form_div").innerHTML = "";
                                    }
                                }
                                //var form_cargo_items = document.getElementById('form_cargo_items');
                                /*for(var i=0; i < form_cargo_items.elements.length; i++){
                                    if(form_cargo_items.elements[i].value === '' && form_cargo_items.elements[i].hasAttribute('required')){
                                        if (update_cargo_line_item_id_form == "" && cargo_line_approved_form.checked == true){
                                             document.getElementById("new_update_cargo_line_item_id_form").focus();
                                             document.getElementById("cargo_line_item_id_div").innerHTML = "Please fill this field";
                                             document.getElementById("cargo_line_item_id_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("cargo_line_item_id_div").innerHTML = "";
                                        }
                                        if (update_new_shipping_marks_form == "" && update_shipping_marks_form_approved_form.checked == true) {
                                            document.getElementById("new_update_shipping_marks_form").focus();
                                             document.getElementById("new_update_shipping_marks_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_update_shipping_marks_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_update_shipping_marks_form_div").innerHTML = "";
                                        }
                                        if (update_new_dog_form == "" && update_dog_form_approved.checked == true) {
                                            document.getElementById("new_update_description_of_goods_form").focus();
                                             document.getElementById("new_update_dog_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_update_dog_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_update_dog_form_div").innerHTML = "";
                                        }
                                        if (update_new_hscode_form == "" && update_hs_code_form_approved.checked == true) {
                                            document.getElementById("new_update_hs_code_form").focus();
                                             document.getElementById("new_update_hs_code_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_update_hs_code_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_update_hs_code_form_div").innerHTML = "";
                                        }
                                        if (update_new_no_of_packages == "" && update_no_of_packages_form_approved.checked == true) {
                                            document.getElementById("update_new_no_of_packages").focus();
                                             document.getElementById("update_new_no_of_packages_div").innerHTML = "Please fill this field";
                                             document.getElementById("update_new_no_of_packages_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("update_new_no_of_packages_div").innerHTML = "";
                                        }
                                        if (update_new_wt_form == "" && update_weight_form_approved.checked == true) {
                                            document.getElementById("new_update_weight_form").focus();
                                             document.getElementById("new_update_weight_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_update_weight_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_update_weight_form_div").innerHTML = "";
                                        }
                                        if (update_new_wt_unit_form == "" && update_wt_unit_form_approved.checked == true) {
                                            document.getElementById("new_update_wt_unit_form").focus();
                                             document.getElementById("new_update_wt_unit_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_update_wt_unit_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_update_wt_unit_form_div").innerHTML = "";
                                        }
                                        if (update_new_pc_form == "" && update_package_code_form_approved.checked == true) {
                                            document.getElementById("new_update_package_code_form").focus();
                                             document.getElementById("new_update_package_code_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_update_package_code_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_update_package_code_form_div").innerHTML = "";
                                        }
                                        if (update_new_container_id_form == "" && update_container_id_form_approved.checked == true) {
                                            document.getElementById("new_update_container_id_form").focus();
                                             document.getElementById("new_update_container_id_form_div").innerHTML = "Please fill this field";
                                             document.getElementById("new_update_container_id_form_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("new_update_container_id_form_div").innerHTML = "";
                                        }
                                    }
                                }*/
                                if (update_new_no_of_packages != "" && update_no_of_packages_form_approved.checked == true) {
                                    var regex = /^\d*[]?\d*$/;
                                    if(regex.test(update_new_no_of_packages)){
                                         document.getElementById("update_new_no_of_packages_div").innerHTML = "";
                                    } else {
                                         document.getElementById("update_new_no_of_packages").focus();
                                         document.getElementById("update_new_no_of_packages_div").innerHTML = "Please enter a valid number";
                                         document.getElementById("update_new_no_of_packages_div").style.color="Red";
                                         return;
                                    }
                                }
                                dialog.close();
                            }
                        }]
                    });
                    dialog.opened().then(function () {
//                        $(".close").hide();
                        var form_cargo_items = document.getElementById('form_cargo_items');
                        for(var i=0; i < form_cargo_items.elements.length; i++){
                            if(form_cargo_items.elements[i].hasAttribute('required')){
                                form_cargo_items.elements[i].style.background='#ADD8E6';
                            }
                        }
                        var update_row_id_form = document.getElementById("update_row_id_"+id).value;
                        document.getElementById("update_row_id_form").value = update_row_id_form;

                        // update Cargo Line Item ID
                        // old value
                        var update_cargo_line_item_id_form = document.getElementById("old_cargo_line_items_id_val_"+id).value;
                        document.getElementById("old_update_cargo_line_item_id_form").value = update_cargo_line_item_id_form;
                        // new value
                        var update_new_val_cl_id_form = document.getElementById("update_cargo_line_items_id_"+id).value;
                        if (update_cargo_line_item_id_form === update_new_val_cl_id_form){
                            document.getElementById("new_update_cargo_line_item_id_form").value = "";
                        } else{
                            document.getElementById("new_update_cargo_line_item_id_form").value = update_new_val_cl_id_form;
                        }
//                        cl_val_approved_
                        var cl_val_approved = document.getElementById("cl_val_approved_"+id).value;
                        if (cl_val_approved == "true"){
                            document.getElementById("cargo_line_approved_form").checked = true;
                        } else {
                            document.getElementById("cargo_line_approved_form").checked = false;
                        }

                        // Shipping Marks
                        // old value
                        var update_shipping_marks_form = document.getElementById("old_update_shipping_marks_val_id_"+id).value;
                        document.getElementById("old_update_shipping_marks_form").value = update_shipping_marks_form;
                        // new value
                        var update_new_val_sm_form = document.getElementById("update_shipping_marks_id_"+id).value;
                        if (update_shipping_marks_form === update_new_val_sm_form){
                            document.getElementById("new_update_shipping_marks_form").value = "";
                        } else{
                            document.getElementById("new_update_shipping_marks_form").value = update_new_val_sm_form;
                        }
                        // sm_val_approved
                        var sm_val_approved = document.getElementById("sm_val_approved_"+id).value;
                        if (sm_val_approved == "true"){
                            document.getElementById("update_shipping_marks_form_approved_form").checked = true;
                        } else {
                            document.getElementById("update_shipping_marks_form_approved_form").checked = false;
                        }


                        // carrier_booking_reference
                        // old value
                        var update_carrier_booking_reference_form = document.getElementById("old_carrier_booking_reference_id_"+id).value;
                        document.getElementById("old_update_carrier_booking_reference_form").value = update_carrier_booking_reference_form;
                        // new value
                        var update_cbr_form = document.getElementById("update_carrier_booking_reference_id_"+id).value;
                        document.getElementById("new_update_carrier_booking_reference").value = update_carrier_booking_reference_form;

                        /*if (update_carrier_booking_reference_form === update_cbr_form){
                            document.getElementById("new_update_carrier_booking_reference").value = "";
                        } else{
                            document.getElementById("new_update_carrier_booking_reference").value = update_cbr_form;
                        }*/
                        // cbr_val_approved
                        var cbr_val_approved = document.getElementById("cbr_val_approved_"+id).value;
                        if (cbr_val_approved == "true"){
                            document.getElementById("update_cbr_approved").checked = true;
                        } else {
                            document.getElementById("update_cbr_approved").checked = false;
                        }

                        // description_of_goods
                        // old value
                        var update_description_of_goods_form = document.getElementById("old_update_description_of_goods_id_"+id).value;
                        document.getElementById("old_update_description_of_goods_form").value = update_description_of_goods_form;
                        // new value
                        var update_new_val_dog_form = document.getElementById("update_description_of_goods_id_"+id).value;
                        // if old value and new value are same then - new value should be blank
                        if (update_description_of_goods_form === update_new_val_dog_form){
                            document.getElementById("new_update_description_of_goods_form").value = ""
                        } else {
                            document.getElementById("new_update_description_of_goods_form").value = update_new_val_dog_form;
                        }
                        // dog_val_approved
                        var dog_val_approved = document.getElementById("dog_val_approved_"+id).value;
                        if (dog_val_approved == "true"){
                            document.getElementById("update_description_of_goods_form_approved").checked = true;
                        } else {
                            document.getElementById("update_description_of_goods_form_approved").checked = false;
                        }

                        // hs_code
                        // old value
                        var update_hs_code_form = document.getElementById("old_update_hs_code_id_"+id).value;
                        document.getElementById("old_update_hs_code_form").value = update_hs_code_form;
                        // new value
                        var update_new_hs_code_form = document.getElementById("update_hs_code_id_"+id).value;
                        if (update_hs_code_form === update_new_hs_code_form){
                            document.getElementById("new_update_hs_code_form").value = "";
                        } else {
                            document.getElementById("new_update_hs_code_form").value = update_new_hs_code_form;
                        }
                        // hs_val_approved
                        var hs_val_approved = document.getElementById("hs_val_approved_"+id).value;
                        if (hs_val_approved == "true"){
                            document.getElementById("update_hs_code_form_approved").checked = true;
                        } else {
                            document.getElementById("update_hs_code_form_approved").checked = false;
                        }


                        // no_of_packages
                        // old value
                        var update_no_of_packages_form = document.getElementById("old_update_number_of_packages_id_"+id).value;
                        document.getElementById("update_old_no_of_packages").value = update_no_of_packages_form;
                        // new value
                        var new_update_no_of_packages_form = document.getElementById("update_number_of_packages_id_"+id).value;
                        if(update_no_of_packages_form === new_update_no_of_packages_form){
                            document.getElementById("update_new_no_of_packages").value = "";
                        } else{
                            document.getElementById("update_new_no_of_packages").value = new_update_no_of_packages_form;
                        }
                        // nop_val_approved
                        var nop_val_approved = document.getElementById("nop_val_approved_"+id).value;
                        if (nop_val_approved == "true"){
                            document.getElementById("update_no_of_packages_form_approved").checked = true;
                        } else {
                            document.getElementById("update_no_of_packages_form_approved").checked = false;
                        }


                        // weight
                        // old value
                        var update_weight_form = document.getElementById("old_update_weight_id_"+id).value;
                        document.getElementById("old_update_weight_form").value = update_weight_form;
                        // new value
                        var update_new_weight_form = document.getElementById("update_weight_id_"+id).value;
                        if (update_weight_form === update_new_weight_form){
                            document.getElementById("new_update_weight_form").value = "";
                        } else {
                            document.getElementById("new_update_weight_form").value = update_new_weight_form;
                        }
                        // wt_val_approved
                        var wt_val_approved = document.getElementById("wt_val_approved_"+id).value;
                        if (wt_val_approved == "true"){
                            document.getElementById("update_weight_form_approved").checked = true;
                        } else {
                            document.getElementById("update_weight_form_approved").checked = false;
                        }


                        // volume
                        // old value
                        var update_volume_form = document.getElementById("old_update_volume_id_"+id).value;
                        document.getElementById("old_update_volume_form").value = update_volume_form;
                        // new value
                        var update_new_volume_form = document.getElementById("update_volume_id_"+id).value;
                        if (update_volume_form === update_new_volume_form){
                            document.getElementById("new_update_volume_form").value = "";
                        } else {
                            document.getElementById("new_update_volume_form").value = update_new_volume_form;
                        }
                        // vl_val_approved
                        var vl_val_approved = document.getElementById("vl_val_approved_"+id).value;
                        if (vl_val_approved == "true"){
                            document.getElementById("update_volume_form_approved").checked = true;
                        } else {
                            document.getElementById("update_volume_form_approved").checked = false;
                        }


                        // wt_unit
                        // old value
                        var update_wt_unit_form = document.getElementById("old_update_weight_unit_id_"+id).value;
                        document.getElementById("old_update_wt_unit_form").value = update_wt_unit_form;
                        // new value
                        var update_new_wt_unit_form = document.getElementById("update_weight_unit_id_"+id).value;

                        if(update_wt_unit_form === update_new_wt_unit_form){
                            document.getElementById("new_update_wt_unit_form").value = "";
                        } else {
                            document.getElementById("new_update_wt_unit_form").value = update_new_wt_unit_form;
                        }
                        // wt_unit_val_approved
                        var wt_unit_val_approved = document.getElementById("wt_unit_val_approved_"+id).value;
                        if (wt_unit_val_approved == "true"){
                            document.getElementById("update_wt_unit_form_approved").checked = true;
                        } else {
                            document.getElementById("update_wt_unit_form_approved").checked = false;
                        }

                        // volume_unit
                        // old value
                        var update_volume_unit_form = document.getElementById("old_update_volume_unit_id_"+id).value;
                        document.getElementById("old_update_volume_unit_form").value = update_volume_unit_form;
                        // new value
                        var update_new_volume_unit_form = document.getElementById("update_volume_unit_id_"+id).value;
                        if(update_volume_unit_form === update_new_volume_unit_form){
                            document.getElementById("new_update_volume_unit_form").value = "";
                        } else {
                            document.getElementById("new_update_volume_unit_form").value = update_new_volume_unit_form;
                        }
                        // vl_unit_val_approved
                        var vl_unit_val_approved = document.getElementById("vl_unit_val_approved_"+id).value;
                        if (vl_unit_val_approved == "true"){
                            document.getElementById("update_volume_unit_form_approved").checked = true;
                        } else {
                            document.getElementById("update_volume_unit_form_approved").checked = false;
                        }


                        // package_code
                        // old value
                        var update_package_code_form = document.getElementById("old_update_package_code_id_"+id).value;
                        document.getElementById("old_update_package_code_form").value = update_package_code_form;
                        // new value
                        var update_new_package_code_form = document.getElementById("update_package_code_id_"+id).value;
                        if (update_package_code_form === update_new_package_code_form){
                            document.getElementById("new_update_package_code_form").value = "";
                        } else {
                            document.getElementById("new_update_package_code_form").value = update_new_package_code_form;
                        }
                        // pc_val_approved
                        var pc_val_approved = document.getElementById("pc_val_approved_"+id).value;
                        if (pc_val_approved == "true"){
                            document.getElementById("update_package_code_form_approved").checked = true;
                        } else {
                            document.getElementById("update_package_code_form_approved").checked = false;
                        }


                        // container_id
                        // old value
                        var update_container_id_form = document.getElementById("old_update_equipment_reference_id_"+id).value;
                        document.getElementById("old_update_container_id_form").value = update_container_id_form;
                        document.getElementById("new_update_container_id_form").value = update_container_id_form;
                        // new value
                        /*var update_new_container_id_form = document.getElementById("update_equipment_reference_id_"+id).value;
                        if (update_container_id_form === update_new_container_id_form){
                            document.getElementById("new_update_container_id_form").value = "";
                        } else {
                            document.getElementById("new_update_container_id_form").value = update_new_container_id_form;
                        }*/
                        // eq_val_approved
                        var eq_val_approved = document.getElementById("eq_val_approved_"+id).value;
                        if (eq_val_approved == "true"){
                            document.getElementById("update_container_id_form_approved").checked = true;
                        } else {
                            document.getElementById("update_container_id_form_approved").checked = false;
                        }

                        // update Created by field by default
                        var si_created_by_val = document.getElementById("si_created_by").value;
                        document.getElementById("update_cargo_line_created_by_form").value = si_created_by_val;
                        document.getElementById("update_shipping_marks_form_created_by").value = si_created_by_val;
                        document.getElementById("update_cbr_created_by").value = si_created_by_val;
                        document.getElementById("update_created_by_dog").value = si_created_by_val;
                        document.getElementById("update_created_by_hs_code").value = si_created_by_val;
                        document.getElementById("update_created_by_no_of_packages").value = si_created_by_val;
                        document.getElementById("update_created_by_weight").value = si_created_by_val;
                        document.getElementById("update_created_by_volume").value = si_created_by_val;
                        document.getElementById("update_created_by_wt_unit").value = si_created_by_val;
                        document.getElementById("update_created_by_volume_unit").value = si_created_by_val;
                        document.getElementById("update_created_by_package_code").value = si_created_by_val;
                        document.getElementById("update_created_by_container_id").value = si_created_by_val;

                        // Update modified field by default - but still user can edit
                        document.getElementById("update_cargo_line_modified_by_form").value = si_created_by_val;
                        document.getElementById("update_shipping_marks_form_modified_by").value = si_created_by_val;
                        document.getElementById("update_cbr_modified_by").value = si_created_by_val;
                        document.getElementById("update_dog_modified_by").value = si_created_by_val;
                        document.getElementById("update_modified_by_hs_code").value = si_created_by_val;
                        document.getElementById("update_modified_by_no_of_packages").value = si_created_by_val;
                        document.getElementById("update_modified_by_weight").value = si_created_by_val;
                        document.getElementById("update_modified_by_volume").value = si_created_by_val;
                        document.getElementById("update_modified_by_wt_unit").value = si_created_by_val;
                        document.getElementById("update_modified_by_volume_unit").value = si_created_by_val;
                        document.getElementById("update_modified_by_package_code").value = si_created_by_val;
                        document.getElementById("update_modified_by_container_id").value = si_created_by_val;
                    });
                    dialog.open();
                });
            });

            // Update SI values to backend
            $('#shipping_instructions_update_form').on('click', '.update_si_submit', function (ev) {
                // Parent column values
                var update_parent_vals = [];
                var cargo_update_tbl = document.getElementById("cargo_tbody_update_si");
                var cargo_table_update_count = cargo_update_tbl.rows.length;
                var tq_update_tbl = document.getElementById("tq_update_tbody");
                var tq_table_update_count = tq_update_tbl.rows.length;
                var dp_update_tbl = document.getElementById("dp_update_tbody");
                var dp_table_update_count = dp_update_tbl.rows.length;
                var sl_update_tbl = document.getElementById("sl_update_tbody");
                var sl_table_update_count = sl_update_tbl.rows.length;
                var rc_update_tbl = document.getElementById("rc_update_tbody");
                var rc_table_update_count = rc_update_tbl.rows.length;




                var si_rec = document.getElementById("current_si_rec").value;

                var update_si_created_by = document.getElementById("si_updated_by").value;
                if (update_si_created_by == "") {
                    document.getElementById("si_updated_by_div").innerHTML="Please fill this field";
                    document.getElementById("si_updated_by_div").style.color="Red";
                    document.getElementById("si_updated_by").focus();
                    return false;
                }
                else
                {
                    document.getElementById("si_updated_by_div").innerHTML="";
                }

                var transport_document_type_code_update = document.getElementById("transport_document_type_code_update").value;
                if (transport_document_type_code_update == "") {
                    document.getElementById("transport_document_type_code_update_div").innerHTML="Please fill this field";
                    document.getElementById("transport_document_type_code_update_div").style.color="Red";
                    document.getElementById("transport_document_type_code_update").focus();
                    return false;
                }
                else
                {
                    document.getElementById("transport_document_type_code_update_div").innerHTML="";
                }

                if (transport_document_type_code_update === "BOL" || transport_document_type_code_update === "bol" || transport_document_type_code_update === "swb" || transport_document_type_code_update === "SWB"){
                    document.getElementById("transport_document_type_code_update_div").innerHTML= "";
                }
                else {
                    document.getElementById("transport_document_type_code_update_div").innerHTML= "Please enter BOL or SWB";
                    document.getElementById("transport_document_type_code_update_div").style.color="Red";
                    document.getElementById("transport_document_type_code_update").focus();
                    return false;
                }

                var is_shipper_owned_update = document.getElementById("is_shipped_onboard_type_update");
                var shipper_owned_tq;
                if(is_shipper_owned_update.checked == true){
                    shipper_owned_tq = true;
                } else {
                    shipper_owned_tq = false;
                }
                var is_electronic_update = document.getElementById("is_electronic_update");
                var is_electronic_update_val;
                if(is_electronic_update.checked == true){
                    is_electronic_update_val = true;
                } else {
                    is_electronic_update_val = false;
                }
                var is_charges_displayed_update = document.getElementById("is_charges_displayed_update");
                var is_charges_displayed_update_val;
                if(is_charges_displayed_update.checked == true){
                    is_charges_displayed_update_val = true;
                } else {
                    is_charges_displayed_update_val = false;
                }
                var number_of_copies_update = document.getElementById("number_of_copies_update").value;
                var number_of_originals_update = document.getElementById("number_of_originals_update").value;
                var carrier_booking_reference_update = document.getElementById("carrier_booking_reference_update").value;
                if (carrier_booking_reference_update == "") {
                    document.getElementById("carrier_booking_reference_update_div").innerHTML="Please fill this field";
                    document.getElementById("carrier_booking_reference_update_div").style.color="Red";
                    document.getElementById("carrier_booking_reference_update").focus();
                    return false;
                }
                else
                {
                    document.getElementById("carrier_booking_reference_update_div").innerHTML="";
                }
                var pre_carriage_under_shippers_responsibility_update = document.getElementById("pre_carriage_under_shippers_responsibility_update").value;
                // Invoice Payable at fields
                var inv_payable_location_name_update = document.getElementById("inv_payable_location_name_update").value;
                if (inv_payable_location_name_update == "") {
                    document.getElementById("inv_payable_location_name_update_div").innerHTML="Please fill this field";
                    document.getElementById("inv_payable_location_name_update_div").style.color="Red";
                    document.getElementById("inv_payable_location_name_update").focus();
                    return false;
                }
                else
                {
                    document.getElementById("inv_payable_location_name_update_div").innerHTML="";
                }

                var inv_payable_un_location_code_update = document.getElementById("inv_payable_un_location_code_update").value;
                if (inv_payable_un_location_code_update == "") {
                    document.getElementById("inv_payable_un_location_code_update_div").innerHTML="Please fill this field";
                    document.getElementById("inv_payable_un_location_code_update_div").style.color="Red";
                    document.getElementById("inv_payable_un_location_code_update").focus();
                    return false;
                }
                else
                {
                    document.getElementById("inv_payable_un_location_code_update_div").innerHTML="";
                }

                var inv_payable_city_name_update = document.getElementById("inv_payable_city_name_update").value;
                if (inv_payable_city_name_update == "") {
                    document.getElementById("inv_payable_city_name_update_div").innerHTML="Please fill this field";
                    document.getElementById("inv_payable_city_name_update_div").style.color="Red";
                    document.getElementById("inv_payable_city_name_update").focus();
                    return false;
                }
                else
                {
                    document.getElementById("inv_payable_city_name_update_div").innerHTML="";
                }

                var inv_payable_state_region_update = document.getElementById("inv_payable_state_region_update").value;
                if (inv_payable_state_region_update == "") {
                    document.getElementById("inv_payable_state_region_update_div").innerHTML="Please fill this field";
                    document.getElementById("inv_payable_state_region_update_div").style.color="Red";
                    document.getElementById("inv_payable_state_region_update").focus();
                    return false;
                }
                else
                {
                    document.getElementById("inv_payable_state_region_update_div").innerHTML="";
                }

                var inv_payable_country_update = document.getElementById("inv_payable_country_update").value;
                if (inv_payable_country_update == "") {
                    document.getElementById("inv_payable_country_update_div").innerHTML="Please fill this field";
                    document.getElementById("inv_payable_country_update_div").style.color="Red";
                    document.getElementById("inv_payable_country_update").focus();
                    return false;
                }
                else
                {
                    document.getElementById("inv_payable_country_update_div").innerHTML="";
                }

                // If cargo items are not added then give user warning
                if (cargo_table_update_count == 0){
                    Dialog.alert(this, _t('Please Add Cargo Item'));
//                    document.getElementById("add_cargo_item_div").focus();
                    return;
                }
                // If Transport eq. are not added then give user warning
                if (tq_table_update_count == 0){
                    Dialog.alert(this, _t('Please Add Transport Equipment'));
                    return;
                }
                // If document parties are not added then give user warning
                if (dp_table_update_count == 0){
                    Dialog.alert(this, _t('Please Add Document Parties'));
                    return;
                }
                // If shipment location are not added then give user warning
                if (sl_table_update_count == 0){
                    Dialog.alert(this, _t('Please Add Shipment Location'));
                    return;
                }
                // If references are not added then give user warning
                if (rc_table_update_count == 0){
                    Dialog.alert(this, _t('Please Add References'));
                    return;
                }

                update_parent_vals.push({
                    'current_si_id': si_rec,
                    'transport_document_type_code': transport_document_type_code_update,
                    'is_shipper_owned': shipper_owned_tq,
                    'is_electronic': is_electronic_update_val,
                    'is_charges_displayed': is_charges_displayed_update_val,
                    'number_of_originals': number_of_originals_update,
                    'number_of_copies': number_of_copies_update,
                    'carrier_booking_reference': carrier_booking_reference_update,
                    'pre_carriage_under_shippers_responsibility': pre_carriage_under_shippers_responsibility_update,
                    'inv_payable_location_name': inv_payable_location_name_update,
                    'inv_payable_un_location_code': inv_payable_un_location_code_update,
                    'inv_payable_city_name_update': inv_payable_city_name_update,
                    'inv_payable_state_region_update': inv_payable_state_region_update,
                    'inv_payable_country_update': inv_payable_country_update,
                    'cargo_table_update_count': cargo_table_update_count,
                    'tq_table_update_count': tq_table_update_count,
                    'dp_table_update_count': dp_table_update_count,
                    'sl_table_update_count': sl_table_update_count,
                    'rc_table_update_count': rc_table_update_count,
                    'update_si_created_by': update_si_created_by,
                });

                // Child column values - Cargo Items Update
                var CargoTableColUpdateData = new Array();
                for(var ct=0;ct<cargo_table_update_count;ct++){
                    var cargo_update_tds = cargo_update_tbl.rows.item(ct).cells;
                    for (var ct_td = 0; ct_td < cargo_update_tds.length; ct_td++) {
                       // var ct_row_count = (cargo_update_tbl.rows[ct].cells[0].textContent.trim());
                        var column_name = cargo_update_tbl.rows[ct].cells[ct_td].children[0].name;
//                        alert("column_name"+ column_name);
                        if (column_name === "cargo_line_items_id") {
                            var cargo_line_item_id = cargo_update_tbl.rows[ct].cells[ct_td].children[0].value;
                        }
                        else if (column_name === "shipping_marks"){
                            var shipping_marks = cargo_update_tbl.rows[ct].cells[ct_td].children[0].value;
                        }
                        else if (column_name === "carrier_booking_reference"){
                            var carrier_booking_reference = cargo_update_tbl.rows[ct].cells[ct_td].children[0].value;
                        }
                        else if (column_name === "description_of_goods"){
                            var description_of_goods = cargo_update_tbl.rows[ct].cells[ct_td].children[0].value;
                        }
                        else if (column_name === "hs_code"){
                            var hs_code = cargo_update_tbl.rows[ct].cells[ct_td].children[0].value;
                        }
                        else if (column_name === "no_of_packages"){
                            var no_of_packages = cargo_update_tbl.rows[ct].cells[ct_td].children[0].value;
                        }
                        else if (column_name === "weight"){
                            var weight = cargo_update_tbl.rows[ct].cells[ct_td].children[0].value;
                        }
                        else if (column_name === "volume"){
                            var volume = cargo_update_tbl.rows[ct].cells[ct_td].children[0].value;
                        }
                        else if (column_name === "weight_unit"){
                            var weight_unit = cargo_update_tbl.rows[ct].cells[ct_td].children[0].value;
                        }
                        else if (column_name === "volume_unit"){
                            var volume_unit = cargo_update_tbl.rows[ct].cells[ct_td].children[0].value;
                        }
                        else if (column_name === "package_code"){
                            var package_code = cargo_update_tbl.rows[ct].cells[ct_td].children[0].value;
                        }
                        else if (column_name === "equipment_reference"){
                            var equipment_reference = cargo_update_tbl.rows[ct].cells[ct_td].children[0].value;
                        }
                        else if (column_name === "cargo_array_created_by"){
                            var cargo_array_created_by = cargo_update_tbl.rows[ct].cells[ct_td].children[0].value;
                        }
                        CargoTableColUpdateData[ct] = {
                            "cargo_line_item_id": cargo_line_item_id,
                            "shipping_marks": shipping_marks,
                            "carrier_booking_reference": carrier_booking_reference,
                            "description_of_goods": description_of_goods,
                            "hs_code": hs_code,
                            "no_of_packages": no_of_packages,
                            "weight": weight,
                            "volume": volume,
                            "weight_unit": weight_unit,
                            "volume_unit": volume_unit,
                            "package_code": package_code,
                            "equipment_reference": equipment_reference,
                            "cargo_array_created_by": cargo_array_created_by,
                        }

                    }
                }

                // Child column values - Transport Equipment Update
                var TqTableColUpdateData = new Array();
                for(var tq=0;tq<tq_table_update_count;tq++){
                    var tq_update_tds = tq_update_tbl.rows.item(tq).cells;
                    for (var tq_td = 0; tq_td < tq_update_tds.length; tq_td++) {
                        var tq_column_name = tq_update_tbl.rows[tq].cells[tq_td].children[0].name;
                        if (tq_column_name === "equipment_reference") {
                            var equipment_reference = tq_update_tbl.rows[tq].cells[tq_td].children[0].value;
                        }
                        else if (tq_column_name === "new_wt_unit_update_tq"){
                            var new_wt_unit_update_tq = tq_update_tbl.rows[tq].cells[tq_td].children[0].value;
                        }
                        else if (tq_column_name === "new_cgw_update_tq"){
                            var new_cgw_update_tq = tq_update_tbl.rows[tq].cells[tq_td].children[0].value;
                        }
                        else if (tq_column_name === "new_ctw_update_tq"){
                            var new_ctw_update_tq = tq_update_tbl.rows[tq].cells[tq_td].children[0].value;
                        }
                        else if (tq_column_name === "new_iso_eq_code_update_tq"){
                            var new_iso_eq_code_update_tq = tq_update_tbl.rows[tq].cells[tq_td].children[0].value;
                        }
                        else if (tq_column_name === "new_is_shipper_owned_update_tq"){
                            var new_is_shipper_owned_update_tq = tq_update_tbl.rows[tq].cells[tq_td].children[0].checked;
                        }
                        else if (tq_column_name === "new_temp_min_update_tq"){
                            var new_temp_min_update_tq = tq_update_tbl.rows[tq].cells[tq_td].children[0].value;
                        }
                        else if (tq_column_name === "new_temp_min_update_tq"){
                            var new_temp_min_update_tq = tq_update_tbl.rows[tq].cells[tq_td].children[0].value;
                        }
                        else if (tq_column_name === "new_temp_max_update_tq"){
                            var new_temp_max_update_tq = tq_update_tbl.rows[tq].cells[tq_td].children[0].value;
                        }
                        else if (tq_column_name === "new_temp_unit_update_tq"){
                            var new_temp_unit_update_tq = tq_update_tbl.rows[tq].cells[tq_td].children[0].value;
                        }
                        else if (tq_column_name === "new_humidity_min_update_tq"){
                            var new_humidity_min_update_tq = tq_update_tbl.rows[tq].cells[tq_td].children[0].value;
                        }
                        else if (tq_column_name === "new_humidity_max_update_tq"){
                            var new_humidity_max_update_tq = tq_update_tbl.rows[tq].cells[tq_td].children[0].value;
                        }
                        else if (tq_column_name === "new_ventilation_min_update_tq"){
                            var new_ventilation_min_update_tq = tq_update_tbl.rows[tq].cells[tq_td].children[0].value;
                        }
                        else if (tq_column_name === "new_ventilation_max_update_tq"){
                            var new_ventilation_max_update_tq = tq_update_tbl.rows[tq].cells[tq_td].children[0].value;
                        }
                        else if (tq_column_name === "new_seal_no_update_tq"){
                            var new_seal_no_update_tq = tq_update_tbl.rows[tq].cells[tq_td].children[0].value;
                        }
                        else if (tq_column_name === "new_seal_source_update_tq"){
                            var new_seal_source_update_tq = tq_update_tbl.rows[tq].cells[tq_td].children[0].value;
                        }
                        else if (tq_column_name === "new_seal_type_update_tq"){
                            var new_seal_type_update_tq = tq_update_tbl.rows[tq].cells[tq_td].children[0].value;
                        }
                        else if (tq_column_name === "transport_equipment_array_created_by"){
                            var transport_equipment_array_created_by = tq_update_tbl.rows[tq].cells[tq_td].children[0].value;
                        }
                        TqTableColUpdateData[tq] = {
                            "equipment_reference": equipment_reference,
                            "new_wt_unit_update_tq": new_wt_unit_update_tq,
                            "new_cgw_update_tq": new_cgw_update_tq,
                            "new_ctw_update_tq": new_ctw_update_tq,
                            "new_iso_eq_code_update_tq": new_iso_eq_code_update_tq,
                            "new_is_shipper_owned_update_tq": new_is_shipper_owned_update_tq,
                            "new_temp_min_update_tq": new_temp_min_update_tq,
                            "new_temp_max_update_tq": new_temp_max_update_tq,
                            "new_temp_unit_update_tq": new_temp_unit_update_tq,
                            "new_humidity_min_update_tq": new_humidity_min_update_tq,
                            "new_humidity_max_update_tq": new_humidity_max_update_tq,
                            "new_ventilation_min_update_tq": new_ventilation_min_update_tq,
                            "new_ventilation_max_update_tq": new_ventilation_max_update_tq,
                            "new_seal_no_update_tq": new_seal_no_update_tq,
                            "new_seal_source_update_tq": new_seal_source_update_tq,
                            "new_seal_type_update_tq": new_seal_type_update_tq,
                            "transport_equipment_array_created_by": transport_equipment_array_created_by,
                        }
                    }
                }

                // Child column values - Document Praties Update
                var DocumentPartiesColUpdateData = new Array();
                for(var dp=0;dp<dp_table_update_count;dp++){
                    var dp_update_tds = dp_update_tbl.rows.item(dp).cells;
                    for (var dp_td = 0; dp_td < dp_update_tds.length; dp_td++) {
                       // var ct_row_count = (cargo_update_tbl.rows[ct].cells[0].textContent.trim());
                        var column_name = dp_update_tbl.rows[dp].cells[dp_td].children[0].name;
                        if (column_name === "new_party_name_update_dp") {
                            var new_party_name_update_dp = dp_update_tbl.rows[dp].cells[dp_td].children[0].value;
                        }
                        else if (column_name === "new_tax_reference_1_update_dp"){
                            var new_tax_reference_1_update_dp = dp_update_tbl.rows[dp].cells[dp_td].children[0].value;
                        }
                        else if (column_name === "new_public_key_update_dp"){
                            var new_public_key_update_dp = dp_update_tbl.rows[dp].cells[dp_td].children[0].value;
                        }
                        else if (column_name === "new_street_update_dp"){
                            var new_street_update_dp = dp_update_tbl.rows[dp].cells[dp_td].children[0].value;
                        }
                        else if (column_name === "new_street_number_update_dp"){
                            var new_street_number_update_dp = dp_update_tbl.rows[dp].cells[dp_td].children[0].value;
                        }
                        else if (column_name === "new_floor_update_dp"){
                            var new_floor_update_dp = dp_update_tbl.rows[dp].cells[dp_td].children[0].value;
                        }
                        else if (column_name === "new_post_code_update_dp"){
                            var new_post_code_update_dp = dp_update_tbl.rows[dp].cells[dp_td].children[0].value;
                        }
                        else if (column_name === "new_city_update_dp"){
                            var new_city_update_dp = dp_update_tbl.rows[dp].cells[dp_td].children[0].value;
                        }
                        else if (column_name === "new_state_region_update_dp"){
                            var new_state_region_update_dp = dp_update_tbl.rows[dp].cells[dp_td].children[0].value;
                        }
                        else if (column_name === "new_country_update_dp"){
                            var new_country_update_dp = dp_update_tbl.rows[dp].cells[dp_td].children[0].value;
                        }
                        else if (column_name === "new_tax_reference_2_update_dp"){
                            var new_tax_reference_2_update_dp = dp_update_tbl.rows[dp].cells[dp_td].children[0].value;
                        }
                        else if (column_name === "new_nmfta_code_update_dp"){
                            var new_nmfta_code_update_dp = dp_update_tbl.rows[dp].cells[dp_td].children[0].value;
                        }
                        else if (column_name === "new_party_function_update_dp"){
                            var new_party_function_update_dp = dp_update_tbl.rows[dp].cells[dp_td].children[0].value;
                        }
                        else if (column_name === "new_address_line_update_dp"){
                            var new_address_line_update_dp = dp_update_tbl.rows[dp].cells[dp_td].children[0].value;
                        }
                        else if (column_name === "new_name_update_dp"){
                            var new_name_update_dp = dp_update_tbl.rows[dp].cells[dp_td].children[0].value;
                        }
                        else if (column_name === "new_email_update_dp"){
                            var new_email_update_dp = dp_update_tbl.rows[dp].cells[dp_td].children[0].value;
                        }
                        else if (column_name === "new_phone_update_dp"){
                            var new_phone_update_dp = dp_update_tbl.rows[dp].cells[dp_td].children[0].value;
                        }
                        else if (column_name === "new_is_to_be_notified_update_dp"){
                            var new_is_to_be_notified_update_dp = dp_update_tbl.rows[dp].cells[dp_td].children[0].checked;
                        }
                        else if (column_name === "document_parties_array_created_by"){
                            var document_parties_array_created_by = dp_update_tbl.rows[dp].cells[dp_td].children[0].value;
                        }
                        DocumentPartiesColUpdateData[dp] = {
                            "new_party_name_update_dp": new_party_name_update_dp,
                            "new_tax_reference_1_update_dp": new_tax_reference_1_update_dp,
                            "new_public_key_update_dp": new_public_key_update_dp,
                            "new_street_update_dp": new_street_update_dp,
                            "new_street_number_update_dp": new_street_number_update_dp,
                            "new_floor_update_dp": new_floor_update_dp,
                            "new_post_code_update_dp": new_post_code_update_dp,
                            "new_city_update_dp": new_city_update_dp,
                            "new_state_region_update_dp": new_state_region_update_dp,
                            "new_country_update_dp": new_country_update_dp,
                            "new_tax_reference_2_update_dp": new_tax_reference_2_update_dp,
                            "new_nmfta_code_update_dp": new_nmfta_code_update_dp,
                            "new_party_function_update_dp": new_party_function_update_dp,
                            "new_address_line_update_dp": new_address_line_update_dp,
                            "new_name_update_dp": new_name_update_dp,
                            "new_email_update_dp": new_email_update_dp,
                            "new_phone_update_dp": new_phone_update_dp,
                            "new_is_to_be_notified_update_dp": new_is_to_be_notified_update_dp,
                            "document_parties_array_created_by": document_parties_array_created_by,
                        }
                    }
                }

                // Child column values - Shipment Location
                var ShipmentLocationColUpdateData = new Array();
                for(var sl=0;sl<sl_table_update_count;sl++){
                    var sl_update_tds = sl_update_tbl.rows.item(sl).cells;
                    for (var sl_td = 0; sl_td < sl_update_tds.length; sl_td++) {
                       // var ct_row_count = (cargo_update_tbl.rows[ct].cells[0].textContent.trim());
                        var column_name = sl_update_tbl.rows[sl].cells[sl_td].children[0].name;
                        if (column_name === "new_location_type_update_sl") {
                            var new_location_type_update_sl = sl_update_tbl.rows[sl].cells[sl_td].children[0].value;
                        }
                        else if (column_name === "new_location_name_update_sl"){
                            var new_location_name_update_sl = sl_update_tbl.rows[sl].cells[sl_td].children[0].value;
                        }
                        else if (column_name === "new_latitude_update_sl"){
                            var new_latitude_update_sl = sl_update_tbl.rows[sl].cells[sl_td].children[0].value;
                        }
                        else if (column_name === "new_longitude_update_sl"){
                            var new_longitude_update_sl = sl_update_tbl.rows[sl].cells[sl_td].children[0].value;
                        }
                        else if (column_name === "new_un_location_code_update_sl"){
                            var new_un_location_code_update_sl = sl_update_tbl.rows[sl].cells[sl_td].children[0].value;
                        }
                        else if (column_name === "new_street_name_code_update_sl"){
                            var new_street_name_code_update_sl = sl_update_tbl.rows[sl].cells[sl_td].children[0].value;
                        }
                        else if (column_name === "new_street_number_code_update_sl"){
                            var new_street_number_code_update_sl = sl_update_tbl.rows[sl].cells[sl_td].children[0].value;
                        }
                        else if (column_name === "new_floor_update_sl"){
                            var new_floor_update_sl = sl_update_tbl.rows[sl].cells[sl_td].children[0].value;
                        }
                        else if (column_name === "new_post_code_update_sl"){
                            var new_post_code_update_sl = sl_update_tbl.rows[sl].cells[sl_td].children[0].value;
                        }
                        else if (column_name === "new_city_name_update_sl"){
                            var new_city_name_update_sl = sl_update_tbl.rows[sl].cells[sl_td].children[0].value;
                        }
                        else if (column_name === "new_state_region_update_sl"){
                            var new_state_region_update_sl = sl_update_tbl.rows[sl].cells[sl_td].children[0].value;
                        }
                        else if (column_name === "new_country_update_sl"){
                            var new_country_update_sl = sl_update_tbl.rows[sl].cells[sl_td].children[0].value;
                        }
                        else if (column_name === "new_displayed_name_update_sl"){
                            var new_displayed_name_update_sl = sl_update_tbl.rows[sl].cells[sl_td].children[0].value;
                        }
                        else if (column_name === "shipment_location_array_created_by"){
                            var shipment_location_array_created_by = sl_update_tbl.rows[sl].cells[sl_td].children[0].value;
                        }
                        ShipmentLocationColUpdateData[sl] = {
                            "new_location_type_update_sl": new_location_type_update_sl,
                            "new_location_name_update_sl": new_location_name_update_sl,
                            "new_latitude_update_sl": new_latitude_update_sl,
                            "new_longitude_update_sl": new_longitude_update_sl,
                            "new_un_location_code_update_sl": new_un_location_code_update_sl,
                            "new_street_name_code_update_sl": new_street_name_code_update_sl,
                            "new_street_number_code_update_sl": new_street_number_code_update_sl,
                            "new_floor_update_sl": new_floor_update_sl,
                            "new_post_code_update_sl": new_post_code_update_sl,
                            "new_city_name_update_sl": new_city_name_update_sl,
                            "new_state_region_update_sl": new_state_region_update_sl,
                            "new_country_update_sl": new_country_update_sl,
                            "new_displayed_name_update_sl": new_displayed_name_update_sl,
                            "shipment_location_array_created_by": shipment_location_array_created_by,
                        }
                    }
                }

                // Child column values - References
                var ReferencesColUpdateData = new Array();
                for(var rc=0;rc<rc_table_update_count;rc++){
                    var rc_update_tds = rc_update_tbl.rows.item(rc).cells;
                    for (var rc_td = 0; rc_td < rc_update_tds.length; rc_td++) {
                       // var ct_row_count = (cargo_update_tbl.rows[ct].cells[0].textContent.trim());
                        var column_name = rc_update_tbl.rows[rc].cells[rc_td].children[0].name;
                        if (column_name === "new_reference_type_update_rc") {
                            var new_reference_type_update_rc = rc_update_tbl.rows[rc].cells[rc_td].children[0].value;
                        }
                        else if (column_name === "new_reference_value_update_rc"){
                            var new_reference_value_update_rc = rc_update_tbl.rows[rc].cells[rc_td].children[0].value;
                        }
                        else if (column_name === "references_array_created_by"){
                            var references_array_created_by = rc_update_tbl.rows[rc].cells[rc_td].children[0].value;
                        }
                        ReferencesColUpdateData[rc] = {
                            "new_reference_type_update_rc": new_reference_type_update_rc,
                            "new_reference_value_update_rc": new_reference_value_update_rc,
                            "references_array_created_by": references_array_created_by,
                        }
                    }
                }
                 // RPC call to update shippi    `ng instructions with its childs
                rpc.query({
                    route: '/si_update_vals',
                    params: {
                        update_parent_vals: update_parent_vals,
                        updated_cargo_vals: CargoTableColUpdateData,
                        updated_tq_vals: TqTableColUpdateData,
                        updated_dp_vals: DocumentPartiesColUpdateData,
                        updated_sl_vals: ShipmentLocationColUpdateData,
                        updated_rc_vals: ReferencesColUpdateData,
                    }
               }).then(function (res) {
                    window.location.href = '/shippinginstrunction_update';
               });
            });
        });
    },
});


publicWidget.registry.WebsiteShippingInstructionsUpdateInstance = publicWidget.Widget.extend({
    selector: '#shipping_instructions_update_form',

    /**
     * @override
     */
    start: function () {
        var def = this._super.apply(this, arguments);
        this.instance = new WebsiteShippingInstructionsUpdate(this);
        return Promise.all([def, this.instance.attachTo(this.$el)]);
    },
    /**
     * @override
     */
    destroy: function () {
        this.instance.setElement(null);
        this._super.apply(this, arguments);
        this.instance.setElement(this.$el);
    },
});

return WebsiteShippingInstructionsUpdate;
});

