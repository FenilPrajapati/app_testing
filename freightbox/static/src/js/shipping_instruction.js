odoo.define('freightbox.shipping_instruction', function (require) {
'use strict';
var publicWidget = require('web.public.widget');
var core = require('web.core');
var Widget = require('web.Widget');
var publicWidget = require('web.public.widget');
var rowIdx = 0;
var rpc = require('web.rpc');


    const Dialog = require('web.Dialog');
    const { qweb, _t } = require('web.core');

var WebsiteShippingInstructions = Widget.extend({
        xmlDependencies: ['/freightbox/static/src/xml/SiPopup.xml'],
       
    start: function () {
        var self = this;
        var res = this._super.apply(this.arguments).then(function () {

            // Update Create SI field values based on SI template
            $('#shipping_instructions_form').on('click', '.get_si_template_values', function (ev) {
                // To avoid duplicate lines we need to clear and update the table
                var cargo_table = document.getElementById("cargo_tbody");
                cargo_table.innerHTML = "";
                var tq_table = document.getElementById("tq_tbody");
                tq_table.innerHTML = "";
                var dp_table = document.getElementById("dp_tbody");
                dp_table.innerHTML = "";
                var sl_table = document.getElementById("sl_tbody");
                sl_table.innerHTML = "";
                var rc_table = document.getElementById("rc_tbody");
                rc_table.innerHTML = "";
                // Apply action starts
                self.on_click_apply_si_template_values(ev);
            });

            // $('#modal-body').on('keydown', '.oe_search_box', function (ev) {
            //     console.log('------------------- Call From --------------')
            //     var cargo_table = document.getElementById("oe_search_box");
                
            // });

              // Edit/View Popup of References
            $('#rc_tbody').on('click', '.references_view', function () {
                var child = $(this).closest('tr');
                child.each(function () {
                    var id = $(this).attr('id');
                    var dialog = new Dialog(this, {
                        title: _t("Shipping Instruction - References"),
                        $content: $(qweb.render('freightbox.add_references_values_popup')),
                            buttons: [{
                                text: _t('Edit'),
                                classes: "btn-primary",
                                close: false,
                                click: function () {
                                    var reference_type = document.getElementById("reference_type_rc_form").value;
                                    document.getElementById("reference_type_rc_id_"+id).value = reference_type;

                                    var reference_value = document.getElementById("reference_value_rc_form").value;
                                    document.getElementById("reference_value_rc_id_"+id).value = reference_value;

                                    var rc_created_by = document.getElementById("ref_array_created_by_form").value
                                    document.getElementById("ref_array_created_by_"+id).value = rc_created_by;

                                    var formrc = document.getElementById('formrc');
                                    for(var i=0; i < formrc.elements.length; i++){
                                        if(formrc.elements[i].value === '' && formrc.elements[i].hasAttribute('required')){
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
                            var formrc = document.getElementById('formrc');
                            for(var i=0; i < formrc.elements.length; i++){
                                if(formrc.elements[i].hasAttribute('required')){
                                    formrc.elements[i].style.background='#ADD8E6';
                                }
                            }

                         //   var view_row_count = document.getElementById("row_count").innerHTML;
                            var reference_type = document.getElementById("reference_type_rc_id_"+id).value;
                            document.getElementById("reference_type_rc_form").value = reference_type;

                            var reference_value = document.getElementById("reference_value_rc_id_"+id).value;
                            document.getElementById("reference_value_rc_form").value = reference_value;

                            var rc_created_by = document.getElementById("ref_array_created_by_"+id).value;
                            document.getElementById("ref_array_created_by_form").value = rc_created_by;

                    });
                    dialog.open();
                });
            }),

            // Edit/View Popup of shipment locations
             $('#sl_tbody').on('click', '.shipment_view', function () {
                var child = $(this).closest('tr');
                child.each(function () {
                    var id = $(this).attr('id');
                    var dialog = new Dialog(this, {
                        title: _t("Shipping Instruction - Edit Shipment Locations"),
                        $content: $(qweb.render('freightbox.add_shipment_locations_values_popup')),
                            buttons: [{
                                text: _t('Edit'),
                                classes: "btn-primary",
                                close: false,
                                click: function () {
                                   
                                    var location_type = document.getElementById("location_type_form").value;
//                                    alert("location_type edit"+ location_type);
                                    document.getElementById("location_type_id_"+id).value = location_type;

                                    var location_name = document.getElementById("location_name_form").value;
                                    document.getElementById("location_name_id_"+id).value = location_name;

                                    var latitude = document.getElementById("latitude_form").value;
                                    document.getElementById("latitude_id_"+id).value = latitude;

                                    var longitude = document.getElementById("longitude_form").value;
                                    document.getElementById("longitude_id_"+id).value = longitude;

                                    var un_location_code = document.getElementById("un_location_code_form").value;
                                    document.getElementById("un_location_code_id_"+id).value = un_location_code;

                                    var street_name = document.getElementById("street_name_form").value;
                                    document.getElementById("street_name_id_"+id).value = street_name;

                                    var street_number = document.getElementById("street_number_form").value;
                                    document.getElementById("street_number_id_"+id).value = street_number;

                                    var floor = document.getElementById("floor_form").value;
                                    document.getElementById("floor_id_"+id).value = floor;

                                    var post_code = document.getElementById("post_code_form").value;
                                    document.getElementById("post_code_id_"+id).value = post_code;

                                    var city_name = document.getElementById("city_name_form").value;
                                    document.getElementById("city_name_id_"+id).value = city_name;

                                    var state_region = document.getElementById("state_region_form").value;
                                    document.getElementById("state_region_id_"+id).value = state_region;

                                    var country = document.getElementById("country_form").value;
                                    document.getElementById("country_id_"+id).value = country;

                                    var displayed_name = document.getElementById("displayed_name_form").value;
                                    document.getElementById("displayed_name_id_"+id).value = displayed_name;

                                    var sl_created_by = document.getElementById("sl_array_created_by_form").value;
                                    document.getElementById("sl_array_created_by_"+id).value = sl_created_by;


                                    var formsl = document.getElementById('formsl');
                                    for(var i=0; i < formsl.elements.length; i++){
                                        if(formsl.elements[i].value === '' && formsl.elements[i].hasAttribute('required')){
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
                        var formsl = document.getElementById('formsl');
                        for(var i=0; i < formsl.elements.length; i++){
                            if(formsl.elements[i].hasAttribute('required')){
                                formsl.elements[i].style.background='#ADD8E6';
                            }
                        }

                        $("#location_type_form").on('change', function() {
//                alert("sdf");
//                var opts = document.getElementById('location-type-list').childNodes;
//                opts.show();
                var loc_type = document.getElementById("location_type_form").value;
                if (loc_type == "PRE" ||
                        location_type === "PDE" ||
                        location_type === "PCF" ||
                        location_type === "OIR" ||
                        location_type === "PSR") {
                    document.getElementById("location_type_form").value = loc_type;
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
                else {
                    document.getElementById("location_type_form").value = loc_type;
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
                /*if (loc_type == "Port of Discharge (POD)") {
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
                }*/
               /* if (loc_type == "POL" || loc_type == "POD"){

                }*/
            });


                            //   var view_row_count = document.getElementById("row_count").innerHTML;

                            var location_type = document.getElementById("location_type_id_"+id).value;
                            document.getElementById("location_type_form").value = location_type;

                            var location_name = document.getElementById("location_name_id_"+id).value;
                            document.getElementById("location_name_form").value = location_name;

                            var latitude = document.getElementById("latitude_id_"+id).value;
                            document.getElementById("latitude_form").value = latitude;

                            var longitude = document.getElementById("longitude_id_"+id).value;
                            document.getElementById("longitude_form").value = longitude;

                            var un_location_code = document.getElementById("un_location_code_id_"+id).value;
                            document.getElementById("un_location_code_form").value = un_location_code;

                            var street_name = document.getElementById("street_name_id_"+id).value;
                            document.getElementById("street_name_form").value = street_name;

                            var street_number = document.getElementById("street_number_id_"+id).value;
                            document.getElementById("street_number_form").value = street_number;

                            var floor = document.getElementById("floor_id_"+id).value;
                            document.getElementById("floor_form").value = floor;

                            var post_code = document.getElementById("post_code_id_"+id).value;
                            document.getElementById("post_code_form").value = post_code;

                            var city_name = document.getElementById("city_name_id_"+id).value;
                            document.getElementById("city_name_form").value = city_name;

                            var state_region = document.getElementById("state_region_id_"+id).value;
                            document.getElementById("state_region_form").value = state_region;

                            var country = document.getElementById("country_id_"+id).value;
                            document.getElementById("country_form").value = country;

                            var displayed_name = document.getElementById("displayed_name_id_"+id).value;
                            document.getElementById("displayed_name_form").value = displayed_name;

                            var sl_created_by = document.getElementById("sl_array_created_by_"+id).value;
                            document.getElementById("sl_array_created_by_form").value = sl_created_by;

                    });
                    dialog.open();
                });

            }),

             // Edit/View Popup of document parties
             $('#dp_tbody').on('click', '.document_view', function () {
                var child = $(this).closest('tr');
                child.each(function () {
                    var id = $(this).attr('id');
                    var dialog = new Dialog(this, {
                        title: _t("Shipping Instruction - Edit Document View"),
                        $content: $(qweb.render('freightbox.add_document_parties_values_popup')),
                            buttons: [{
                                text: _t('Edit'),
                                classes: "btn-primary",
                                close: false,
                                click: function () {
                                    var party_name = document.getElementById("party_name_dp_form").value;
                                    document.getElementById("party_name_dp_id_"+id).value = party_name;

                                    var tax_reference_1 = document.getElementById("tax_reference_1_dp_form").value;
                                    document.getElementById("tax_reference_1_dp_id_"+id).value = tax_reference_1;

                                    var public_key = document.getElementById("public_key_form").value;
                                    document.getElementById("public_key_dp_id_"+id).value = public_key;

                                    var street = document.getElementById("street_form").value;
                                    document.getElementById("street_id_"+id).value = street;

                                    var street_number = document.getElementById("street_number_form").value;
                                    document.getElementById("street_number_id_"+id).value = street_number;

                                    var floor = document.getElementById("floor_form").value;
                                    document.getElementById("floor_id_"+id).value = floor;

                                    var post_code = document.getElementById("post_code_form").value;
                                     document.getElementById("post_code_id_"+id).value = post_code;

                                    var city = document.getElementById("city_form").value;
                                    document.getElementById("city_id_"+id).value = city;

                                    var state_region = document.getElementById("state_region_form").value;
                                    document.getElementById("state_region_id_"+id).value = state_region;

                                    var country = document.getElementById("country_form").value;
                                    document.getElementById("country_id_"+id).value = country;

                                    var tax_reference_2 = document.getElementById("tax_reference_2_form").value;
                                     document.getElementById("tax_reference_2_id_"+id).value = tax_reference_2;

                                    var nmfta_code = document.getElementById("nmfta_code_form").value;
                                    document.getElementById("nmfta_code_id_"+id).value = nmfta_code;

                                    var party_function = document.getElementById("party_function_form").value;
                                    document.getElementById("party_function_id_"+id).value = party_function;

                                    var address_line = document.getElementById("address_line_form").value;
                                    document.getElementById("address_line_id_"+id).value = address_line;

                                    var name = document.getElementById("name_form").value;
                                    document.getElementById("name_id_"+id).value = name;

                                    var email = document.getElementById("email_form").value;
                                    document.getElementById("email_id_"+id).value = email;

                                    var phone = document.getElementById("phone_form").value;
                                    document.getElementById("phone_id_"+id).value = phone;

                                    var dp_modified_by = document.getElementById("dp_array_created_by_form").value;
                                    document.getElementById("dp_array_created_by_"+id).value = dp_modified_by;

                                    var is_to_be_notified = document.getElementById("is_to_be_notified_form");
                                    if(is_to_be_notified.checked == true){
                                        document.getElementById("to_be_notified_id_"+id).checked = true;
                                    } else {
                                        document.getElementById("to_be_notified_id_"+id).checked = false;
                                    }

                                    var formdp = document.getElementById('formdp');
                                    for(var i=0; i < formdp.elements.length; i++){
                                        if(formdp.elements[i].value === '' && formdp.elements[i].hasAttribute('required')){
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

//                                      var is_to_be_notified = document.getElementById("is_to_be_notified_form");
                                    if(is_to_be_notified.checked != true){
                                        is_to_be_notified.checked = true;
                                    }

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

                                }
                            }],
                    });
                    dialog.opened().then(function () {

                    var formdp = document.getElementById('formdp');
                    for(var i=0; i < formdp.elements.length; i++){
                        if(formdp.elements[i].hasAttribute('required')){
                            formdp.elements[i].style.background='#ADD8E6';
                        }
                    }
                         //   var view_row_count = document.getElementById("row_count").innerHTML;
                            var party_name = document.getElementById("party_name_dp_id_"+id).value;
                            document.getElementById("party_name_dp_form").value = party_name;

                            var tax_reference_1 = document.getElementById("tax_reference_1_dp_id_"+id).value;
                            document.getElementById("tax_reference_1_dp_form").value = tax_reference_1;

                            var public_key = document.getElementById("public_key_dp_id_"+id).value;
                            document.getElementById("public_key_form").value = public_key;

                            var street = document.getElementById("street_id_"+id).value;
                            document.getElementById("street_form").value = street;

                            var street_number = document.getElementById("street_number_id_"+id).value;
                            document.getElementById("street_number_form").value = street_number;

                            var floor = document.getElementById("floor_id_"+id).value;
                            document.getElementById("floor_form").value = floor;

                            var post_code = document.getElementById("post_code_id_"+id).value;
                            document.getElementById("post_code_form").value = post_code;

                            var city = document.getElementById("city_id_"+id).value;
                            document.getElementById("city_form").value = city;

                            var state_region = document.getElementById("state_region_id_"+id).value;
                            document.getElementById("state_region_form").value = state_region;

                            var country = document.getElementById("country_id_"+id).value;
                            document.getElementById("country_form").value = country;

                            var tax_reference_2 = document.getElementById("tax_reference_2_id_"+id).value;
                            document.getElementById("tax_reference_2_form").value = tax_reference_2;

                            var nmfta_code = document.getElementById("nmfta_code_id_"+id).value;
                            document.getElementById("nmfta_code_form").value = nmfta_code;

                            var party_function = document.getElementById("party_function_id_"+id).value;
                            document.getElementById("party_function_form").value = party_function;

                            var address_line = document.getElementById("address_line_id_"+id).value;
                            document.getElementById("address_line_form").value = address_line;

                            var name = document.getElementById("name_id_"+id).value;
                            document.getElementById("name_form").value = name;

                            var email = document.getElementById("email_id_"+id).value;
                            document.getElementById("email_form").value = email;

                            var phone = document.getElementById("phone_id_"+id).value;
                            document.getElementById("phone_form").value = phone;

                            var dp_created_by = document.getElementById("dp_array_created_by_"+id).value;
                            document.getElementById("dp_array_created_by_form").value = dp_created_by;


                            var is_to_be_notified = document.getElementById("to_be_notified_id_"+id);
                            if(is_to_be_notified.checked == true){
                                document.getElementById("is_to_be_notified_form").checked = true;
                            } else {
                                document.getElementById("is_to_be_notified_form").checked = false;
                            }
                    });
                    dialog.open();
                });

            }),

            // Edit/View Transport Equipment Popup
            $('#tq_tbody').on('click', '.tq_view', function () {
                var child = $(this).closest('tr');
                child.each(function () {
                    var id = $(this).attr('id');
                    var dialog = new Dialog(this, {
                        title: _t("Shipping Instruction - Edit Transport Equipment"),
                        $content: $(qweb.render('freightbox.add_transport_eqipment_values_popup')),
                        buttons: [{
                            text: _t('Edit'),
                            classes: "btn-primary",
                            close: false,
                            click: function () {
                                // field 1
                                var equipment_reference_tq = document.getElementById("equipment_reference_tq_form").value;
                                document.getElementById("equipment_reference_id_"+id).value  = equipment_reference_tq;

                                // field 2
                                var weight_unit_tq = document.getElementById("weight_unit_tq_form").value;
                                document.getElementById("weight_unit_tq_id_"+id).value  = weight_unit_tq;

                                // field 3
                                var cargo_gross_weight = document.getElementById("cargo_gross_weight_form").value;
                                document.getElementById("cargo_gross_weight_id_"+id).value = cargo_gross_weight;

                                // field 4
                                var container_tare_weight = document.getElementById("container_tare_weight_form").value;
                                document.getElementById("container_tare_weight_id_"+id).value = container_tare_weight;

                                // field 5
                                var iso_equipment_code = document.getElementById("iso_equipment_code_form").value;
                                document.getElementById("iso_equipment_code_id_"+id).value = iso_equipment_code;

                                // field 6
                                var is_shipper_owned = document.getElementById("is_shipper_owned_form");
                                if(is_shipper_owned.checked == true){
                                    document.getElementById("shipper_owned_id_"+id).checked = true;
                                } else {
                                    document.getElementById("shipper_owned_id_"+id).checked = false;
                                }
                                // field 7
                                var temperature_min = document.getElementById("temperature_min_form").value;
                                document.getElementById("temperature_min_id_"+id).value = temperature_min;

                                // field 8
                                var temperature_max = document.getElementById("temperature_max_form").value;
                                document.getElementById("temperature_max_id_"+id).value = temperature_max;

                                // field 9
                                var temperature_unit = document.getElementById("temperature_unit_form").value;
                                document.getElementById("temperature_unit_id_"+id).value = temperature_unit;

                                // field 10
                                var humidity_min = document.getElementById("humidity_min_form").value;
                                document.getElementById("humidity_min_id_"+id).value = humidity_min;

                                // field 11
                                var humidity_max = document.getElementById("humidity_max_form").value;
                                document.getElementById("humidity_max_id_"+id).value = humidity_max;

                                // field 12
                                var ventilation_min = document.getElementById("ventilation_min_form").value;
                                document.getElementById("ventilation_min_id_"+id).value = ventilation_min;

                                // field 13
                                var ventilation_max = document.getElementById("ventilation_max_form").value;
                                document.getElementById("ventilation_max_id_"+id).value = ventilation_max;

                                // field 14
                                var seal_number = document.getElementById("seal_number_form").value;
                                document.getElementById("seal_number_id_"+id).value = seal_number;

                                // field 15
                                var seal_source = document.getElementById("seal_source_form").value;
                                document.getElementById("seal_source_id_"+id).value = seal_source;

                                // field 16
                                var seal_type = document.getElementById("seal_type_form").value;
                                document.getElementById("seal_type_id_"+id).value = seal_type;

                                // field 17
                                var tq_array_created_by = document.getElementById("tq_array_created_by_form").value;
                                document.getElementById("tq_array_created_by_"+id).value = tq_array_created_by;

                                var formtq = document.getElementById('formtq');
                                for(var i=0; i < formtq.elements.length; i++){

                                    if(formtq.elements[i].value === '' && formtq.elements[i].hasAttribute('required')){
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
                                             document.getElementById("cgw_unit_div").innerHTML = "Please enter number";
                                             document.getElementById("cgw_unit_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("cgw_unit_div").innerHTML = "";
                                        }
                                        if (container_tare_weight == ""){

                                            if(is_shipper_owned.checked == true){
                                             document.getElementById("container_tare_weight_form").focus();
                                             document.getElementById("ctw_unit_div").innerHTML = "Please enter number";
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
                                        if (seal_type == ""){
                                             document.getElementById("seal_type_form").focus();
                                             document.getElementById("seal_type_div").innerHTML = "Please fill this field";
                                             document.getElementById("seal_type_div").style.color="Red";
                                             return;
                                        } else {
                                            document.getElementById("seal_type_div").innerHTML = "";
                                        }
                                        if (tq_array_created_by == ""){
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

                        var formtq = document.getElementById('formtq');
                        for(var i=0; i < formtq.elements.length; i++){
                            if(formtq.elements[i].hasAttribute('required')){
                                formtq.elements[i].style.background='#ADD8E6';
                            }
                        }
                        // Update each field values from main row
                        // field 1
                        var equipment_reference_tq = document.getElementById("equipment_reference_id_"+id).value;
                        document.getElementById("equipment_reference_tq_form").value = equipment_reference_tq;

                        // field 2
                        var weight_unit_tq = document.getElementById("weight_unit_tq_id_"+id).value;
                        document.getElementById("weight_unit_tq_form").value = weight_unit_tq;

                        // field 3
                        var cargo_gross_weight = document.getElementById("cargo_gross_weight_id_"+id).value;
                        document.getElementById("cargo_gross_weight_form").value = cargo_gross_weight;

                        // field 4
                        var container_tare_weight = document.getElementById("container_tare_weight_id_"+id).value;
                        document.getElementById("container_tare_weight_form").value = container_tare_weight;

                        // field 5
                        var iso_equipment_code = document.getElementById("iso_equipment_code_id_"+id).value;
                        document.getElementById("iso_equipment_code_form").value = iso_equipment_code;

                        // field 6
                        var is_shipper_owned = document.getElementById("shipper_owned_id_"+id);
                        if(is_shipper_owned.checked == true){
                            document.getElementById("is_shipper_owned_form").checked = true;
                        } else {
                            document.getElementById("is_shipper_owned_form").checked = false;
                        }

                        // field 7
                        var temperature_min = document.getElementById("temperature_min_id_"+id).value;
                        document.getElementById("temperature_min_form").value = temperature_min;

                        // field 8
                        var temperature_max = document.getElementById("temperature_max_id_"+id).value;
                        document.getElementById("temperature_max_form").value = temperature_max;

                        // field 9
                        var temperature_unit = document.getElementById("temperature_unit_id_"+id).value;
                        document.getElementById("temperature_unit_form").value = temperature_unit;

                        // field 10
                        var humidity_min = document.getElementById("humidity_min_id_"+id).value;
                        document.getElementById("humidity_min_form").value = humidity_min;

                        // field 11
                        var humidity_max = document.getElementById("humidity_max_id_"+id).value;
                        document.getElementById("humidity_max_form").value = humidity_max;

                        // field 12
                        var ventilation_max = document.getElementById("ventilation_min_id_"+id).value;
                        document.getElementById("ventilation_min_form").value = ventilation_max;

                        // field 13
                        var ventilation_max = document.getElementById("ventilation_max_id_"+id).value;
                        document.getElementById("ventilation_max_form").value = ventilation_max;

                        // field 14
                        var seal_number = document.getElementById("seal_number_id_"+id).value;
                        document.getElementById("seal_number_form").value = seal_number;

                        // field 15
                        var seal_source = document.getElementById("seal_source_id_"+id).value;
                        document.getElementById("seal_source_form").value = seal_source;

                        // field 16
                        var seal_type = document.getElementById("seal_type_id_"+id).value;
                        document.getElementById("seal_type_form").value = seal_type;

                        var tq_array_created_by = document.getElementById("tq_array_created_by_"+id).value;
                        document.getElementById("tq_array_created_by_form").value = tq_array_created_by;

                    });
                    dialog.open();
                });
            });

            // Edit/View Cargo Item Popup
            $('#cargo_tbody').on('click', '.cargo_view', function () {
                var child = $(this).closest('tr');
                child.each(function () {
                    var id = $(this).attr('id');
                    var dialog = new Dialog(this, {
                        title: _t("Shipping Instruction - Edit Cargo Items"),
                        $content: $(qweb.render('freightbox.add_cargo_item_values_popup')),
                        buttons: [{
                                text: _t('Edit'),
                                classes: "btn-primary",
                                close: false,
                                click: function () {
                                    var view_cargo_line_item_id = document.getElementById("cargo_line_item_id_form").value;
                                    document.getElementById("cargo_line_item_id_"+id).value = view_cargo_line_item_id;

                                    var shipping_marks = document.getElementById("shipping_marks_form").value;
                                    document.getElementById("shipping_marks_"+id).value = shipping_marks;

                                    var carrier_booking_reference = document.getElementById("carrier_booking_reference_form").value;
                                    document.getElementById("carrier_booking_reference_"+id).value = carrier_booking_reference;

                                    var description_of_goods = document.getElementById("description_of_goods_form").value;
                                    document.getElementById("description_of_goods_"+id).value = description_of_goods;

                                    var hs_code = document.getElementById("hs_code_form").value;
                                    document.getElementById("hs_code_"+id).value = hs_code;

                                    var no_of_packages = document.getElementById("no_of_packages_form").value;
                                    document.getElementById("no_of_packages_"+id).value = no_of_packages;

                                    var weight = document.getElementById("weight_form").value;
                                    document.getElementById("weight_"+id).value = weight;

                                    var volume = document.getElementById("volume_form").value;
                                    document.getElementById("volume_"+id).value = volume;

                                    var weight_unit = document.getElementById("weight_unit_form").value;
                                    document.getElementById("weight_unit_"+id).value = weight_unit;

                                    var volume_unit = document.getElementById("volume_unit_form").value;
                                    document.getElementById("volume_unit_"+id).value = volume_unit;

                                    var package_code = document.getElementById("package_code_form").value;
                                    document.getElementById("package_code_"+id).value = package_code;

                                    var equipment_reference = document.getElementById("equipment_reference_form").value;
                                    document.getElementById("equipment_reference_"+id).value = equipment_reference;

                                    var cargo_edited_by = document.getElementById("cargo_array_created_by_form").value;
                                    document.getElementById("cargo_array_created_by_"+id).value = cargo_edited_by;


                                    var edit_form = document.getElementById('theForm');
                                    for(var e=0; e < edit_form.elements.length; e++){
                                        if(edit_form.elements[e].value === '' && edit_form.elements[e].hasAttribute('required')){
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
                                                 document.getElementById("no_of_packages_div").innerHTML = "Please enter number";
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
                                            if (equipment_reference == "") {
                                                document.getElementById("equipment_reference_form").focus();
                                                 document.getElementById("equipment_reference_div").innerHTML = "Please fill this field";
                                                 document.getElementById("equipment_reference_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("equipment_reference_div").innerHTML = "";
                                            } if (cargo_edited_by == "") {
                                                document.getElementById("cargo_array_created_by_form").focus();
                                                 document.getElementById("cargo_array_created_by_div").innerHTML = "Please fill this field";
                                                 document.getElementById("cargo_array_created_by_div").style.color="Red";
                                                 return;
                                            } else {
                                                document.getElementById("cargo_array_created_by_div").innerHTML =  "";
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
                        var edit_form = document.getElementById('theForm');
                        for(var e=0; e < edit_form.elements.length; e++){
                            if(edit_form.elements[e].hasAttribute('required')){
                                edit_form.elements[e].style.background='#ADD8E6';
                            }
                        }
                            var view_cargo_line_item_id = document.getElementById("cargo_line_item_id_"+id).value;
                            document.getElementById("cargo_line_item_id_form").value = view_cargo_line_item_id;

                            var shipping_marks = document.getElementById("shipping_marks_"+id).value;
                            document.getElementById("shipping_marks_form").value = shipping_marks;

                            var carrier_booking_reference = document.getElementById("carrier_booking_reference_"+id).value;
                            document.getElementById("carrier_booking_reference_form").value = carrier_booking_reference;

                            var description_of_goods = document.getElementById("description_of_goods_"+id).value;
                            document.getElementById("description_of_goods_form").value = description_of_goods;

                            var hs_code = document.getElementById("hs_code_"+id).value;
                            document.getElementById("hs_code_form").value = hs_code;

                            var no_of_packages = document.getElementById("no_of_packages_"+id).value;
                            document.getElementById("no_of_packages_form").value = no_of_packages;

                            var weight = document.getElementById("weight_"+id).value;
                            document.getElementById("weight_form").value = weight;

                            var volume = document.getElementById("volume_"+id).value;
                            document.getElementById("volume_form").value = volume;

                            var weight_unit = document.getElementById("weight_unit_"+id).value;
                            document.getElementById("weight_unit_form").value = weight_unit;

                            var volume_unit = document.getElementById("volume_unit_"+id).value;
                            document.getElementById("volume_unit_form").value = volume_unit;

                            var package_code = document.getElementById("package_code_"+id).value;
                            document.getElementById("package_code_form").value = package_code;

                            var equipment_reference = document.getElementById("equipment_reference_"+id).value;
                            document.getElementById("equipment_reference_form").value = equipment_reference;

                            var cargo_created_by = document.getElementById("cargo_array_created_by_"+id).value;
                            document.getElementById("cargo_array_created_by_form").value = cargo_created_by;
                    });
                    dialog.open();
                });
            });

            // To delete current row -References
            $('#rc_tbody').on('click', '.remove_rc', function () {
                var child = $(this).closest('tr').nextAll();
                $(this).closest('tr').remove();
            });

            // To delete current row -Shipment Locations
            $('#sl_tbody').on('click', '.remove_sl', function () {
                var child = $(this).closest('tr').nextAll();
                $(this).closest('tr').remove();
            });

             // To delete current row -Document parties
            $('#dp_tbody').on('click', '.remove_dp', function () {
                var child = $(this).closest('tr').nextAll();
                $(this).closest('tr').remove();
            });

            // To delete current row - Transport Equipment
            $('#tq_tbody').on('click', '.remove_tq', function () {
                var child = $(this).closest('tr').nextAll();
                $(this).closest('tr').remove();
            });

            // To delete current row - cargo items
            $('#cargo_tbody').on('click', '.remove', function () {
                var child = $(this).closest('tr').nextAll();
                // Removing the current row.
                $(this).closest('tr').remove();
            });

            // Create SI save action for Parent Values action
            $('#shipping_instructions_form').on('click', '.create_si_save_parent_values', function (ev) {
                self.on_click_create_si_save_parent_values(ev);

            });

            // Create SI save action for Child Values action
            $('#shipping_instructions_form').on('click', '.create_si_save_child_values', function (ev) {
                var saved_si_id = document.getElementById("saved_si_id").value;
                if (saved_si_id == ""){
                    self.on_click_create_si_save_parent_values(ev);
                }else {
                    self.on_click_create_si_save_child_values(ev);
                }

            });


            // SI Template Create action
            $('#shipping_instructions_form').on('click', '.si_template_create', function (ev) {
                self.on_click_si_template_create(ev);
            });

              // Add new line on References
            $('#shipping_instructions_form').on('click', '.add_references_div', function (ev) {
                self.on_click_add_references(ev);
            });

            // Add new line on Shipment Locations
            $('#shipping_instructions_form').on('click', '.add_shipment_locations_div', function (ev) {
                self.on_click_add_shipment_locations(ev);
            });

            // Add new line on Document Parties
               $('#shipping_instructions_form').on('click', '.add_document_parties_div', function (ev) {
                self.on_click_add_document_parties(ev);
            });

            // Add new line on Transport Equipment
            $('#shipping_instructions_form').on('click', '.add_transport_equipment_div', function (ev) {
                self.on_click_add_transport_equipment(ev);
            });

            // Add new line on Cargo Items
            $('#shipping_instructions_form .add_cargo_item_div')
                .off('click')
                .click(function (ev) {
                    self.on_click(ev);
                });
            });

          // Create SI submit action
          $('#shipping_instructions_form').on('click', '.create_si_submit', function (ev) {
                var cargo_tbl = document.getElementById("cargo_tbody");
                var tq_tbl = document.getElementById("tq_tbody");
                var dp_tbl = document.getElementById("dp_tbody");
                var sl_tbl = document.getElementById("sl_tbody");
                var rc_tbl = document.getElementById("rc_tbody");
//                var filePath = document.getElementById("input").value;
//                var filepath = filePath.replace(/C:\\fakepath\\/i, '/home/')
//                var fr = new FileReader();
//                fr.readAsDataURL(document.getElementById("input").files[0]);
//                var test_pdf = document.getElementById("input").files[0];
//                alert("fr:"+ JSON.stringify(fr));
//                alert("test_pdf:"+ test_pdf)
//                document.getElementById('upload').src = "/home/indra/tt.pdf";


//                inputNode.value = filePath.replace("C:\\fakepath\\", "");
//                console.log(filePath);
//                var file_name = document.getElementById("input").files[0].name;
//                alert("filePath:"+ filePath);
//                alert("nnnn"+ filepath);
//                alert("5555 filePath:"+ JSON.stringify(filePath));
                // destination will be created or overwritten by default.
               /* fs.copyFile(filePath, '/opt/odoo14/odoo/custom_addons', (err) => {
                  if (err) throw err;
                  console.log('File was copied to destination');
                  alert("copied");
                });*/


                // Parent column values
                var parent_vals = [];
//                var attachments = []
                var rc_table_count = rc_tbl.rows.length;
                var sl_table_count = sl_tbl.rows.length;
                var dp_table_count = dp_tbl.rows.length;
                var tq_table_count = tq_tbl.rows.length;
                var cargo_table_count = cargo_tbl.rows.length;



                var new_si_created_by = document.getElementById("new_si_created_by").value;
                if (new_si_created_by == "") {
                    document.getElementById("new_si_created_by_div").innerHTML="Please fill this field";
                    document.getElementById("new_si_created_by_div").style.color="Red";
                    document.getElementById("new_si_created_by").focus();
                    return false;
                }
                else
                {
                    document.getElementById("new_si_created_by_div").innerHTML="";
                }

                var transport_document_type_code = document.getElementById("transport_document_type_code").value;
                if (transport_document_type_code == "") {
                    document.getElementById("transport_document_type_code_div").innerHTML="Please fill this field";
                    document.getElementById("transport_document_type_code_div").style.color="Red";
                    document.getElementById("transport_document_type_code").focus();
                    return false;
                }
                else
                {
                    document.getElementById("transport_document_type_code_div").innerHTML="";
                }

                if (transport_document_type_code === "BOL" || transport_document_type_code === "bol" || transport_document_type_code === "swb" || transport_document_type_code === "SWB"){
                    document.getElementById("transport_document_type_code_div").innerHTML= "";
                }
                else {
                    document.getElementById("transport_document_type_code_div").innerHTML= "Please enter BOL or SWB";
                    document.getElementById("transport_document_type_code_div").style.color="Red";
                    document.getElementById("transport_document_type_code").focus();
                    return false;
                }
                var is_shipper_owned = document.getElementById("is_shipped_onboard_type");
                var shipper_owned_tq;
                if(is_shipper_owned.checked == true){
                    shipper_owned_tq = true;
                } else {
                    shipper_owned_tq = false;
                }
                var is_electronic = document.getElementById("is_electronic");
                var is_electronic_val;
                if(is_electronic.checked == true){
                    is_electronic_val = true;
                } else {
                    is_electronic_val = false;
                }
                var is_charges_displayed = document.getElementById("is_charges_displayed");
                var is_charges_displayed_val;
                if(is_charges_displayed.checked == true){
                    is_charges_displayed_val = true;
                } else {
                    is_charges_displayed_val = false;
                }
                var number_of_copies = document.getElementById("number_of_copies").value;
                var number_of_originals = document.getElementById("number_of_originals").value;
                var carrier_booking_reference = document.getElementById("carrier_booking_reference").value;
                if (carrier_booking_reference == "") {
                    document.getElementById("carrier_booking_reference_div").innerHTML="Please fill this field";
                    document.getElementById("carrier_booking_reference_div").style.color="Red";
                    document.getElementById("carrier_booking_reference").focus();
                    return false;
                }
                else
                {
                    document.getElementById("carrier_booking_reference_div").innerHTML="";
                }
                var pre_carriage_under_shippers_responsibility = document.getElementById("pre_carriage_under_shippers_responsibility").value;

//                var upload_si = document.getElementById("upload_si").value;
//                if (upload_si == "") {
//                    document.getElementById("upload_si_div").innerHTML="Please fill this field";
//                    document.getElementById("upload_si_div").style.color="Red";
//                    document.getElementById("upload_si").focus();
//                    return false;
//                }
//                else
//                {
//                    document.getElementById("upload_si_div").innerHTML="";
//                }

                // Invoice Payable At - vals
                var inv_payable_location_name = document.getElementById("inv_payable_location_name").value;
                if (inv_payable_location_name == "") {
                    document.getElementById("inv_payable_location_name_div").innerHTML="Please fill this field";
                    document.getElementById("inv_payable_location_name_div").style.color="Red";
                    document.getElementById("inv_payable_location_name").focus();
                    return false;
                }
                else
                {
                    document.getElementById("inv_payable_location_name_div").innerHTML="";
                }

                var inv_payable_un_location_code = document.getElementById("inv_payable_un_location_code").value;
                if (inv_payable_un_location_code == "") {
                    document.getElementById("inv_payable_un_location_code_div").innerHTML="Please fill this field";
                    document.getElementById("inv_payable_un_location_code_div").style.color="Red";
                    document.getElementById("inv_payable_un_location_code").focus();
                    return false;
                }
                else
                {
                    document.getElementById("inv_payable_un_location_code_div").innerHTML="";
                }


                var inv_payable_city_name = document.getElementById("inv_payable_city_name").value;
                if (inv_payable_city_name == "") {
                    document.getElementById("inv_payable_city_name_div").innerHTML="Please fill this field";
                    document.getElementById("inv_payable_city_name_div").style.color="Red";
                    document.getElementById("inv_payable_city_name").focus();
                    return false;
                }
                else
                {
                    document.getElementById("inv_payable_city_name_div").innerHTML="";
                }

                var inv_payable_state_region = document.getElementById("inv_payable_state_region").value;
                if (inv_payable_state_region == "") {
                    document.getElementById("inv_payable_state_region_div").innerHTML="Please fill this field";
                    document.getElementById("inv_payable_state_region_div").style.color="Red";
                    document.getElementById("inv_payable_state_region").focus();
                    return false;
                }
                else
                {
                    document.getElementById("inv_payable_state_region_div").innerHTML="";
                }

                var inv_payable_country = document.getElementById("inv_payable_country").value;
                if (inv_payable_country == "") {
                    document.getElementById("inv_payable_country_div").innerHTML="Please fill this field";
                    document.getElementById("inv_payable_country_div").style.color="Red";
                    document.getElementById("inv_payable_country").focus();
                    return false;
                }
                else
                {
                    document.getElementById("inv_payable_country_div").innerHTML="";
                }

                var si_created_by_parent_val = document.getElementById("new_si_created_by").value;
                var si_create_inquiry_no = document.getElementById("si_create_inquiry_no").value;
                var si_create_job_id = document.getElementById("new_si_job_id").value;
                var si_create_transport_id = document.getElementById("new_si_transport_id").value;
                var saved_si_id = document.getElementById("saved_si_id").value;
                var saved_si_name = document.getElementById("saved_si_name").value;
                var saved_cont_id = document.getElementById("transport_container_id").value;

                // If cargo items are not added then give user warning
                if (cargo_table_count == 0){
                    Dialog.alert(this, _t('Please Add Cargo Item'));
                    return;
                }
                // If Transport eq. are not added then give user warning
                if (tq_table_count == 0){
                    Dialog.alert(this, _t('Please Add Transport Equipment'));
                    return;
                }
                // If document parties are not added then give user warning
                if (dp_table_count == 0){
                    Dialog.alert(this, _t('Please Add Document Parties'));
                    return;
                }
                // If shipment location are not added then give user warning
                if (sl_table_count == 0){
                    Dialog.alert(this, _t('Please Add Shipment Location'));
                    return;
                }
                // If references are not added then give user warning
                if (rc_table_count == 0){
                    Dialog.alert(this, _t('Please Add References'));
                    return;
                }

                parent_vals.push({
                    'transport_document_type_code': transport_document_type_code,
                    'is_shipper_owned': shipper_owned_tq,
                    'is_electronic': is_electronic_val,
                    'is_charges_displayed': is_charges_displayed_val,
                    'carrier_booking_reference': carrier_booking_reference,
                    'pre_carriage_under_shippers_responsibility': pre_carriage_under_shippers_responsibility,
                    'number_of_originals': number_of_originals,
                    'number_of_copies': number_of_copies,
                    'inv_payable_location_name': inv_payable_location_name,
                    'inv_payable_un_location_code': inv_payable_un_location_code,
                    'inv_payable_city_name': inv_payable_city_name,
                    'inv_payable_state_region': inv_payable_state_region,
                    'inv_payable_country': inv_payable_country,
                    'cargo_table_count': cargo_table_count,
                    'tq_table_count': tq_table_count,
                    'dp_table_count': dp_table_count,
                    'sl_table_count': sl_table_count,
                    'rc_table_count': rc_table_count,
                    'si_created_by_parent_val': si_created_by_parent_val,
                    'si_create_inquiry_no': si_create_inquiry_no,
                    'si_create_job_id': si_create_job_id,
                    'si_create_transport_id': si_create_transport_id,
                    'saved_si_id': saved_si_id,
                    'state': "draft",
                    'is_saved': false,
                    'saved_si_name': saved_si_name,
                    'saved_cont_id': saved_cont_id,
//                    'file_name': file_name,
//                    'filepath': filepath,
//                    'test_pdf': test_pdf,
//                    'upload_si': upload_si,
                });
//                attachments.push({'upload_si': upload_si,});

               // Child column values - Cargo Items
                var CargoTableColData = new Array();

                for(var i=0;i<cargo_table_count;i++){
                    var cargo_tds = cargo_tbl.rows.item(i).cells;
                    for (var j = 0; j < cargo_tds.length; j++) {
                        var row_count = (cargo_tbl.rows[i].cells[0].textContent.trim());
                        var column_name = cargo_tbl.rows[i].cells[j].children[0].name;
                     //   alert("column_name:"+column_name);

                        if (column_name === "row_count_id") {
                            var row_count_cargo = cargo_tbl.rows[i].cells[j].children[0].value;
                        //    alert("row_count"+ row_count);
                        }
                        else if (column_name === "cargo_line_item_id") {
                            var cargo_line_item_id = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "shipping_marks") {
                            var shipping_marks = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "carrier_booking_reference") {
                            var carrier_booking_reference = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "description_of_goods") {
                            var description_of_goods = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "hs_code") {
                            var hs_code = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "no_of_packages") {
                            var no_of_packages = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "weight") {
                            var weight = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "volume") {
                            var volume = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "weight_unit") {
                            var weight_unit = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "volume_unit") {
                            var volume_unit = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "package_code") {
                            var package_code = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if(column_name === "equipment_reference") {
                            var equipment_reference = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if(column_name === "cargo_array_created_by") {
                            var cargo_array_created_by = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        CargoTableColData[i] = {
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
                            "row_count_cargo": row_count_cargo,
                        }
                    }
                }
                // Child column values - Transport Equipment
                var TransportEquipmentTableColData = new Array();

                for(var m=0;m<tq_table_count;m++){
                    var transport_eq_tds = tq_tbl.rows.item(m).cells;
                    for (var k = 0; k < transport_eq_tds.length; k++) {
                        var tq_row_count = (tq_tbl.rows[m].cells[0].textContent.trim());
                        var tq_column_name = tq_tbl.rows[m].cells[k].children[0].name;
                        if (tq_column_name === "row_count_tq") {
                            var row_count_tq = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "equipment_reference") {
                            var equipment_reference = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "weight_unit_tq") {
                            var weight_unit_tq = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "cargo_gross_weight") {
                            var cargo_gross_weight = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "container_tare_weight") {
                            var container_tare_weight = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "iso_equipment_code") {
                            var iso_equipment_code = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "is_shipper_owned") {
                            var is_shipper_owned = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "temperature_min") {
                            var temperature_min = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "temperature_max") {
                            var temperature_max = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "temperature_unit") {
                            var temperature_unit = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "humidity_min") {
                            var humidity_min = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "humidity_min") {
                            var humidity_min = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "humidity_max") {
                            var humidity_max = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "ventilation_min") {
                            var ventilation_min = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "ventilation_min") {
                            var ventilation_min = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "ventilation_max") {
                            var ventilation_max = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "seal_number") {
                            var seal_number = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "seal_source") {
                            var seal_source = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "seal_type") {
                            var seal_type = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "tq_array_created_by") {
                            var tq_array_created_by = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        TransportEquipmentTableColData[m] = {
                            "equipment_reference": equipment_reference,
                            "weight_unit_tq": weight_unit_tq,
                            "cargo_gross_weight": cargo_gross_weight,
                            "container_tare_weight": container_tare_weight,
                            "iso_equipment_code": iso_equipment_code,
                            "is_shipper_owned": is_shipper_owned,
                            "temperature_min": temperature_min,
                            "temperature_max": temperature_max,
                            "temperature_unit": temperature_unit,
                            "humidity_min": humidity_min,
                            "humidity_max": humidity_max,
                            "ventilation_min": ventilation_min,
                            "ventilation_max": ventilation_max,
                            "seal_number": seal_number,
                            "seal_source": seal_source,
                            "seal_type": seal_type,
                            "tq_array_created_by": tq_array_created_by,
                            "row_count_tq": row_count_tq,
                        }
                    }
                }

                // Child column values - Document Parties
                var DocumentPartiesTableColData = new Array();
                for(var z=0; z<dp_table_count; z++){
                    var document_parties_tds = dp_tbl.rows.item(z).cells;
                    for (var l = 0; l < document_parties_tds.length; l++) {
                        var dp_row_count = (dp_tbl.rows[z].cells[0].textContent.trim());
                        var dp_column_name = dp_tbl.rows[z].cells[l].children[0].name;

                        if (dp_column_name === "row_count_dp") {
                            var row_count_dp = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "party_name") {
                            var party_name = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "tax_reference_1_dp") {
                            var tax_reference_1_dp = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "public_key") {
                            var public_key = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "street") {
                            var street = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "street_number") {
                            var street_number = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "floor") {
                            var floor = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "post_code") {
                            var post_code = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "city") {
                            var city = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "state_region") {
                            var state_region = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "country") {
                            var country = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "tax_reference_2") {
                            var tax_reference_2 = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "nmfta_code") {
                            var nmfta_code = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "party_function") {
                            var party_function = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "address_line") {
                            var address_line = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "name") {
                            var name = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "email") {
                            var email = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "phone") {
                            var phone = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "is_to_be_notified") {
                            var is_to_be_notified = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "dp_array_created_by") {
                            var dp_array_created_by = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        DocumentPartiesTableColData[z] = {
                            "party_name": party_name,
                            "tax_reference_1_dp": tax_reference_1_dp,
                            "public_key": public_key,
                            "street": street,
                            "street_number": street_number,
                            "floor": floor,
                            "post_code": post_code,
                            "city": city,
                            "state_region": state_region,
                            "country": country,
                            "tax_reference_2": tax_reference_2,
                            "nmfta_code": nmfta_code,
                            "party_function": party_function,
                            "address_line": address_line,
                            "name": name,
                            "email": email,
                            "phone": phone,
                            "is_to_be_notified": is_to_be_notified,
                            "dp_array_created_by": dp_array_created_by,
                            "row_count_dp": row_count_dp,
                        }
                    }
                }
                // Child column values - Shipment Locations
                var ShipmentLocationsTableColData = new Array();
                for(var d=0; d<sl_table_count; d++){
                    var shipment_location_tds = sl_tbl.rows.item(d).cells;
                    for (var p = 0; p < shipment_location_tds.length; p++) {
                        var sl_row_count = (sl_tbl.rows[d].cells[0].textContent.trim());
                        var sl_column_name = sl_tbl.rows[d].cells[p].children[0].name;
                        if (sl_column_name === "row_count_sl") {
                            var row_count_sl = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "location_type") {
                            var location_type = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "location_name") {
                            var location_name = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "latitude") {
                            var latitude = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "longitude") {
                            var longitude = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "un_location_code") {
                            var un_location_code = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "street_name") {
                            var street_name = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "street_number") {
                            var street_number = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "floor") {
                            var floor = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "post_code") {
                            var post_code = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "city_name") {
                            var city_name = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "state_region") {
                            var state_region = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "country") {
                            var country = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "displayed_name") {
                            var displayed_name = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "displayed_name") {
                            var displayed_name = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "sl_array_created_by") {
                            var sl_array_created_by = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        ShipmentLocationsTableColData[d] = {
                            "location_type": location_type,
                            "location_name": location_name,
                            "latitude": latitude,
                            "longitude": longitude,
                            "un_location_code": un_location_code,
                            "street_name": street_name,
                            "street_number": street_number,
                            "floor": floor,
                            "post_code": post_code,
                            "city_name": city_name,
                            "state_region": state_region,
                            "country": country,
                            "displayed_name": displayed_name,
                            "sl_array_created_by": sl_array_created_by,
                            "row_count_sl": row_count_sl,
                        }
                    }
                }
                // Child column values - References
                var ReferencesTableColData = new Array();
                for(var q=0; q<rc_table_count; q++){
                    var references_tds = rc_tbl.rows.item(q).cells;
                    for (var r = 0; r < references_tds.length; r++) {
                        var rc_row_count = (rc_tbl.rows[q].cells[0].textContent.trim());
                        var rc_column_name = rc_tbl.rows[q].cells[r].children[0].name;
                        if (rc_column_name === "row_count_rc") {
                            var row_count_rc = rc_tbl.rows[q].cells[r].children[0].value;
                        }
                        else if (rc_column_name === "reference_type") {
                            var reference_type = rc_tbl.rows[q].cells[r].children[0].value;
                        }
                        else if (rc_column_name === "reference_value") {
                            var reference_value = rc_tbl.rows[q].cells[r].children[0].value;
                        }
                        else if (rc_column_name === "ref_array_created_by") {
                            var ref_array_created_by = rc_tbl.rows[q].cells[r].children[0].value;
                        }
                        ReferencesTableColData[q] = {
                            "reference_type": reference_type,
                            "reference_value": reference_value,
                            "ref_array_created_by": ref_array_created_by,
                            "row_count_rc": row_count_rc
                        }
                    }
                }

                // RPC call to create shipping instructions with its childs
                rpc.query({
                    route: '/si_vals',
                    params: {
                        parent_vals: parent_vals,
//                        attachments: attachments,
                        cargo_vals: CargoTableColData,
                        tq_vals: TransportEquipmentTableColData,
                        dp_vals: DocumentPartiesTableColData,
                        sl_vals: ShipmentLocationsTableColData,
                        rc_vals: ReferencesTableColData,
                    }
               }).then(function (res) {
                    window.location.href = '/shippinginstrunction_created';
               });

            });
        return res;
    },

    // From SI Template Get values and update on Create SI
    on_click_apply_si_template_values: function(ev) {
        // SI template backend ID
        var si_template = document.getElementById("si_template").value;

        var transport_cont_id = document.getElementById("transport_container_id").value;
        var carrier_booking_reference = document.getElementById("carrier_booking_reference").value;

        if (si_template == "") {
            Dialog.alert(this, _t('Please select SI Template'));
            return;
        } else {
             rpc.query({
                    route: '/si_template_values',
                    params: {
                        si_template: si_template,
                    }
             }).then(function (data) {
                // Get Parent Values  and update
                var pcusr;
                var pre_carriage_under_shippers_responsibility = data["pre_carriage_under_shippers_responsibility"];
                if (pre_carriage_under_shippers_responsibility == false) {
                   pcusr = ""
                } else {
                    pcusr = pre_carriage_under_shippers_responsibility;
                }

                document.getElementById("transport_document_type_code").value = data["transport_document_type_code"];
                document.getElementById("number_of_originals").value = data["number_of_originals"];
                document.getElementById("number_of_copies").value = data["number_of_copies"];
                document.getElementById("pre_carriage_under_shippers_responsibility").value = pcusr;
//                document.getElementById("carrier_booking_reference").value = data["carrier_booking_reference"];
                document.getElementById("inv_payable_location_name").value = data["location_name"];
                document.getElementById("inv_payable_un_location_code").value = data["un_location_code"];
                document.getElementById("inv_payable_city_name").value = data["city_name"];
                document.getElementById("inv_payable_state_region").value = data["state_region"];
                document.getElementById("inv_payable_country").value = data["country"];

                // Fetch Cargo Items - child values and update
                var count_cargo_items = data["count_cargo_items"]
                if (count_cargo_items > 0) {
                    var cargo_line_values = data["cargo_line_values"];
                    for(var i=0; i < cargo_line_values.length; i++){
                            var get_row_id = i+1;
                            var cl_item_id = cargo_line_values[i]["cargo_line_items_id"];
                            var shipping_marks = cargo_line_values[i]["shipping_marks"];
//                            var carrier_booking_reference = cargo_line_values[i]["carrier_booking_reference"];
//                            if (carrier_booking_reference == false ) {
//                                carrier_booking_reference = "";
//                            }
                            var description_of_goods = cargo_line_values[i]["description_of_goods"];
                            var hs_code = cargo_line_values[i]["hs_code"];
                            var no_of_packages = cargo_line_values[i]["number_of_packages"];
                            var weight = cargo_line_values[i]["weight"];
                            var volume = cargo_line_values[i]["volume"];
                            var weight_unit = cargo_line_values[i]["weight_unit"];
                            var volume_unit = cargo_line_values[i]["volume_unit"];
                            if (volume_unit == false){
                                volume_unit = "";
                            }
                            var equipment_reference = transport_cont_id;
                            var package_code = cargo_line_values[i]["package_code"];
                            var cargo_created_by = document.getElementById("new_si_created_by").value;

                            $('#cargo_tbody').append(`<tr class="added_cargo" id="${get_row_id}">
                              <td class="row-index">
                                      <p class='form-control' readonly="readonly"  id="row_count" name="row_count" >${get_row_id}</p>
                              </td>
                              <td style="display:none">
                                  <input type="text" name="row_count_id"
                                  id="row_count_id" value="${get_row_id}" class='form-control row_count_id'  />
                              </td>
                              <td>
                                  <input type="text" name="cargo_line_item_id" readonly="readonly"
                                  id="cargo_line_item_id_${get_row_id}" value="${cl_item_id}" title="${cl_item_id}" class='form-control cargo_line_item_id'  />
                              </td>
                              <td style="border-right: 1px solid black;">
                                   <input type="text" name="shipping_marks" readonly="readonly"
                                      id="shipping_marks_${get_row_id}" value="${shipping_marks}" title="${shipping_marks}"  class='form-control shipping_marks'/>
                              </td>
                              <td>
                                  <input type="text" name="carrier_booking_reference" readonly="readonly"
                                     id="carrier_booking_reference_${get_row_id}" value="${carrier_booking_reference}" title="${carrier_booking_reference}"
                                     maxlength="35" placeholder="Maximum allowed characters 35" class='form-control carrier_booking_reference'/>
                              </td>
                              <td>
                                  <input type="text" name="description_of_goods" readonly="readonly"
                                     id="description_of_goods_${get_row_id}" maxlength="250"
                                     value="${description_of_goods}" title="${description_of_goods}"
                                     placeholder="Maximum allowed characters 250"  class='form-control description_of_goods'/>
                              </td>
                              <td>
                                  <input type="text" name="hs_code" readonly="readonly"
                                     id="hs_code_${get_row_id}" maxlength="10"
                                     value="${hs_code}" title="${hs_code}"
                                     placeholder="Maximum allowed characters 10"  class='form-control hs_code'/>
                              </td>
                              <td>
                                  <input type="number" name="no_of_packages" readonly="readonly"
                                     id="no_of_packages_${get_row_id}" value="${no_of_packages}" title="${no_of_packages}"  class='form-control no_of_packages'/>
                              </td>
                              <td>
                                  <input type="number" name="weight" readonly="readonly"
                                     id="weight_${get_row_id}" value="${weight}" title="${weight}" class='form-control weight'/>
                              </td>
                              <td>
                                  <input type="number" name="volume" readonly="readonly"
                                     id="volume_${get_row_id}" value="${volume}" title="${volume}" class='form-control volume'/>
                              </td>
                              <td>
                                  <input type="text" name="weight_unit" readonly="readonly"
                                     id="weight_unit_${get_row_id}" maxlength="3"
                                     value="${weight_unit}" title="${weight_unit}"
                                     placeholder="Maximum allowed characters 3" class='form-control weight_unit'/>
                              </td>
                              <td>
                                  <input type="text" name="volume_unit" readonly="readonly"
                                     id="volume_unit_${get_row_id}" maxlength="3"
                                     value="${volume_unit}" title="${volume_unit}"
                                     placeholder="Maximum allowed characters 3"  class='form-control volume_unit'/>
                              </td>
                              <td>
                                  <input type="text" name="package_code" readonly="readonly"
                                     id="package_code_${get_row_id}" maxlength="3"
                                     value="${package_code}" title="${package_code}" placeholder="Maximum allowed characters 3" class='form-control package_code'/>
                              </td>
                              <td>
                                  <input type="text" name="equipment_reference" readonly="readonly"
                                     id="equipment_reference_${get_row_id}" maxlength="15"
                                     value="${equipment_reference}" title="${equipment_reference}"
                                     placeholder="Maximum allowed characters 15"  class='form-control equipment_reference'/>
                              </td>
                              <td>
                                  <input type="hidden" name="cargo_array_created_by" readonly="readonly"
                                     id="cargo_array_created_by_${get_row_id}"
                                     value="${cargo_created_by}" title="${cargo_created_by}"
                                     class='form-control cargo_created_by'/>
                              </td>
                              <td>
                                <button class="btn btn-primary cargo_view" id="cargo_view"
                                    type="button"><small><i class="fa fa-pencil"></i> </small></button>
                              </td>
                              <td>
                                <button class="btn btn-primary remove" id="cargo_remove"
                                    type="button"><small><i class='fa fa-trash-o'></i></small></button>
                              </td>
                            </tr>`);
                    }
                }
                // Fetch Transport Equipment - child values and update
                var count_tq_items = data["count_tq_items"]
                if (count_tq_items > 0) {
                    var tq_line_values = data["tq_line_values"];
                    for(var tq=0; tq < tq_line_values.length; tq++) {
                        var get_tq_row_id = tq+1;
                        var tq_vals = tq_line_values[tq];
                        var equipment_reference = transport_cont_id;
                        var weight_unit_tq = tq_vals["weight_unit"];
                        var cargo_gross_weight = tq_vals["cargo_gross_weight"];
                        var container_tare_weight = tq_vals["container_tare_weight"];
                        var iso_equipment_code = tq_vals["iso_equipment_code"];
                        if (iso_equipment_code == false){
                            iso_equipment_code = "";
                        }
                        var shipper_owned_tq = tq_vals["is_shipper_owned"];
                        var temperature_min = tq_vals["temperature_min"];
                        var temperature_max = tq_vals["temperature_max"];
                        var temperature_unit = tq_vals["temperature_unit"];
                        if (temperature_unit == false){
                            temperature_unit = "";
                        }
                        var humidity_min = tq_vals["humidity_min"];
                        var humidity_max = tq_vals["humidity_max"];
                        var ventilation_min = tq_vals["ventilation_min"];
                        var ventilation_max = tq_vals["ventilation_max"];
                        var seal_number = tq_vals["seal_number"];
                        var seal_source = tq_vals["seal_source"];
                        if (seal_source == false){
                            seal_source = "";
                        }
                        var seal_type = tq_vals["seal_type"];
                        var tq_array_created_by = tq_vals["transport_equipment_array_created_by"];


                        $('#tq_tbody').append(`<tr class="added_tq_lines" id="${get_tq_row_id}">
                              <td class="row-index tq_row_index">
                                  <p class='form-control' readonly="readonly"  id="tqrow_count" name="tqrow_count" >${get_tq_row_id}</p>
                              </td>
                              <td style="display:none">
                                  <input type="text" name="row_count_tq" readonly="readonly"
                                  id="row_count_tq" value="${get_tq_row_id}" class='form-control get_tq_row_id'  />
                              </td>
                              <td>
                                <input type="text" name="equipment_reference"
                                    readonly="readonly" placeholder="Maximum allowed characters 15" maxlength="15"
                                    class='form-control equipment_reference' value="${equipment_reference}" id="equipment_reference_id_${get_tq_row_id}"/>
                              </td>
                              <td>
                                <input type="text" name="weight_unit_tq" readonly="readonly" placeholder="Maximum allowed characters 3" maxlength="3"
                                    class='form-control weight_unit_tq' value="${weight_unit_tq}" id="weight_unit_tq_id_${get_tq_row_id}"/>
                              </td>
                              <td>
                                <input type="number" name="cargo_gross_weight" readonly="readonly" placeholder="Maximum allowed numbers 9"
                                    class='form-control cargo_gross_weight' value="${cargo_gross_weight}" id="cargo_gross_weight_id_${get_tq_row_id}"/>
                              </td>
                              <td>
                                <input type="number" name="container_tare_weight" readonly="readonly" placeholder="Maximum allowed numbers 9"
                                    class='form-control container_tare_weight' value="${container_tare_weight}"
                                    id="container_tare_weight_id_${get_tq_row_id}"/>
                              </td>
                              <td>
                                <input type="text" name="iso_equipment_code" readonly="readonly" placeholder="Maximum allowed characters 4" maxlength="4"
                                    class='form-control iso_equipment_code' value="${iso_equipment_code}"
                                    id="iso_equipment_code_id_${get_tq_row_id}"/>
                              </td>
                              <td>
                                <input type="checkbox" name="is_shipper_owned" readonly="readonly" style="pointer-events: none;"
                                  class='form-control shipper_owned' value="${shipper_owned_tq}" id="shipper_owned_id_${get_tq_row_id}"/>
                              </td>
                              <td>
                                <input type="number" name="temperature_min" placeholder="Max. allowed numbers 9" readonly="readonly"
                                    class='form-control temperature_min' value="${temperature_min}" id="temperature_min_id_${get_tq_row_id}"/>
                              </td>
                              <td>
                                <input type="number" name="temperature_max" placeholder="Max. allowed numbers 9" readonly="readonly"
                                    class='form-control temperature_max' value="${temperature_max}" id="temperature_max_id_${get_tq_row_id}"/>
                              </td>
                              <td>
                                <input type="text" name="temperature_unit" placeholder="Maximum allowed characters 3" maxlength="3" readonly="readonly"
                                    class='form-control temperature_unit' value="${temperature_unit}" id="temperature_unit_id_${get_tq_row_id}"/>
                              </td>
                              <td>
                                <input type="number" name="humidity_min" placeholder="Max. allowed numbers 9" readonly="readonly"
                                 class='form-control humidity_min' value="${humidity_min}" id="humidity_min_id_${get_tq_row_id}"/>
                              </td>
                              <td>
                                <input type="number" name="humidity_max" placeholder="Max. allowed numbers 9" readonly="readonly"
                                 class='form-control humidity_max' value="${humidity_max}" id="humidity_max_id_${get_tq_row_id}"/>
                              </td>
                              <td>
                                <input type="number" name="ventilation_min" placeholder="Max. allowed numbers 9" readonly="readonly"
                                 class='form-control ventilation_min' value="${ventilation_min}" id="ventilation_min_id_${get_tq_row_id}"/>
                              </td>
                              <td>
                                <input type="number" name="ventilation_max" placeholder="Max. allowed numbers 9" readonly="readonly"
                                 class='form-control ventilation_max' value="${ventilation_max}" id="ventilation_max_id_${get_tq_row_id}"/>
                              </td>
                              <td>
                                <input type="text" name="seal_number" placeholder="Maximum allowed characters 15" maxlength="15" readonly="readonly"
                                    class='form-control seal_number' value="${seal_number}" id="seal_number_id_${get_tq_row_id}"/>
                              </td>
                              <td>
                                <input type="text" name="seal_source" placeholder="Maximum allowed characters 5" maxlength="5" readonly="readonly"
                                    class='form-control seal_source' value="${seal_source}" id="seal_source_id_${get_tq_row_id}"/>
                              </td>
                              <td>
                                <input type="text" name="seal_type" placeholder="Maximum allowed characters 5" maxlength="5" readonly="readonly"
                                    class='form-control seal_type' value="${seal_type}" id="seal_type_id_${get_tq_row_id}"/>
                              </td>
                              <td>
                                <input type="hidden" name="tq_array_created_by"
                                    class='form-control tq_array_created_by' value="${tq_array_created_by}"
                                    id="tq_array_created_by_${get_tq_row_id}"/>
                              </td>

                              <td>
                                <button class="btn btn-primary tq_view" id="tq_view"
                                    type="button"><small><i class="fa fa-pencil"></i> </small></button>
                              </td>
                              <td>
                                <button class="btn btn-primary remove_tq" id="tq_remove"
                                    type="button"><small><i class='fa fa-trash-o'></i></small></button>
                              </td>
                           </tr>`);
                        document.getElementById("shipper_owned_id_"+get_tq_row_id).checked = shipper_owned_tq;
                    }
                }
                // Fetch Document Parties - child values and update
                var count_dp_items = data["count_dp_items"]
                if (count_dp_items > 0) {
                    var dp_line_values = data["dp_line_values"];
                    for(var dp=0; dp < dp_line_values.length; dp++) {
                        var get_dp_row_id = dp+1;
                        var dp_vals = dp_line_values[dp];

                        var party_name = dp_vals["party_name_id"];
                        var tax_reference_1 = dp_vals["tax_reference_1"];
                        var public_key = dp_vals["public_key"];
                        var street = dp_vals["street"];
                        var street_number = dp_vals["street_number"];
                        var floor = dp_vals["floor"];
                        var post_code = dp_vals["post_code"];
                        var city = dp_vals["city"];
                        var state_region = dp_vals["state_region"];
                        var country = dp_vals["country"];
                        var tax_reference_2 = dp_vals["tax_reference_2"];
                        var nmfta_code = dp_vals["nmfta_code"];
                        var party_function = dp_vals["party_function"];
                        var address_line = dp_vals["address_line"];
                        if (address_line == false){
                            address_line = "";
                        }
                        var name = dp_vals["name"];
                        var email = dp_vals["email"];
                        var phone = dp_vals["phone"];
                        var is_to_be_notified_val = dp_vals["is_to_be_notified"];
                        var dp_array_created_by = dp_vals["document_parties_array_created_by"];

                        $('#dp_tbody').append(`<tr class="added_dp_lines" id="${get_dp_row_id}">
                        <td class="row-index dp_row_index">
                            <p class='form-control' readonly="readonly" id="dprow_count" name="dprow_count" >${get_dp_row_id}</p>
                        </td>
                        <td style="display:none">
                            <input type="text" name="row_count_dp" readonly="readonly"
                            id="row_count_dp" value="${get_dp_row_id}" class='form-control get_dp_row_id'  />
                        </td>
                        <td>
                            <input type="text" name="party_name" placeholder="Maximum allowed characters 100" maxlength="100" readonly="readonly"
                            class='form-control party_name_dp' value="${party_name}" id="party_name_dp_id_${get_dp_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="tax_reference_1_dp" placeholder="Maximum allowed characters 20" readonly="readonly"
                            class='form-control tax_reference_1_dp' value="${tax_reference_1}" id="tax_reference_1_dp_id_${get_dp_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="public_key" placeholder="Maximum allowed characters 500" readonly="readonly"
                            class='form-control public_key_dp' value="${public_key}" id="public_key_dp_id_${get_dp_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="street" placeholder="Maximum allowed characters 100" readonly="readonly"
                            class='form-control street_dp' value="${street}" id="street_id_${get_dp_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="street_number" placeholder="Maximum allowed characters 50" readonly="readonly"
                            class='form-control street_number_dp' value="${street_number}" id="street_number_id_${get_dp_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="floor" placeholder="Maximum allowed characters 50" readonly="readonly"
                            class='form-control floor_dp' value="${floor}" id="floor_id_${get_dp_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="post_code" placeholder="Maximum allowed characters 10" readonly="readonly"
                            class='form-control post_code_dp' value="${post_code}" id="post_code_id_${get_dp_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="city" placeholder="Maximum allowed characters 65" readonly="readonly"
                            class='form-control city_dp' value="${city}" id="city_id_${get_dp_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="state_region" placeholder="Maximum allowed characters 65" readonly="readonly"
                            class='form-control state_region_dp' value="${state_region}" id="state_region_id_${get_dp_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="country" placeholder="Maximum allowed characters 75" readonly="readonly"
                            class='form-control country_dp' value="${country}" id="country_id_${get_dp_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="tax_reference_2" placeholder="Maximum allowed characters 20" readonly="readonly"
                            class='form-control tax_reference_2_dp' value="${tax_reference_2}" id="tax_reference_2_id_${get_dp_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="nmfta_code" placeholder="Maximum allowed characters 4" readonly="readonly"
                            class='form-control nmfta_code_dp' value="${nmfta_code}" id="nmfta_code_id_${get_dp_row_id}"/>
                        </td>

                        <td>
                            <input type="text" name="party_function" placeholder="Maximum allowed characters 3" readonly="readonly"
                            class='form-control party_function_dp' value="${party_function}" id="party_function_id_${get_dp_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="address_line" placeholder="Maximum allowed characters 250" readonly="readonly"
                            class='form-control address_line_dp' value="${address_line}" id="address_line_id_${get_dp_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="name" placeholder="Maximum allowed characters 100" readonly="readonly"
                            class='form-control name_dp' value="${name}" id="name_id_${get_dp_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="email" placeholder="Maximum allowed characters 100" readonly="readonly"
                            class='form-control email_dp' value="${email}" id="email_id_${get_dp_row_id}"/>
                        </td>
                        <td>
                            <input type="text" name="phone" placeholder="Maximum allowed characters 30" readonly="readonly"
                            class='form-control phone_dp' value="${phone}" id="phone_id_${get_dp_row_id}"/>
                        </td>
                        <td>
                            <input type="checkbox" name="is_to_be_notified" readonly="readonly" style="pointer-events: none;"
                            class='form-control to_be_notified' value="${is_to_be_notified_val}" id="to_be_notified_id_${get_dp_row_id}"/>
                        </td>
                        <td>
                            <input type="hidden" name="dp_array_created_by" readonly="readonly"
                            class='form-control dp_array_created_by' value="${dp_array_created_by}"
                             id="dp_array_created_by_${get_dp_row_id}"/>
                        </td>
                        <td>
                            <button class="btn btn-primary document_view" id="document_view"
                            type="button"><small><i class="fa fa-pencil"></i> </small></button>
                        </td>
                        <td>
                            <button class="btn btn-primary remove_dp" id="dp_remove"
                            type="button"><small><i class='fa fa-trash-o'></i></small></button>
                        </td>
                    </tr>`);
                    document.getElementById("to_be_notified_id_"+get_dp_row_id).checked = is_to_be_notified_val;

                    }
                }
                // Fetch Shipment Location - child values and update
                var count_sl_items = data["count_sl_items"]
                if (count_sl_items > 0) {
                    var sl_line_values = data["sl_line_values"];
                    for(var sl=0; sl < sl_line_values.length; sl++) {
                        var get_sl_row_id = sl+1;
                        var sl_vals = sl_line_values[sl];
                        var location_type = sl_vals["location_type"];
//                        alert("location_type:"+ location_type);
                        var location_name = sl_vals["location_name"];
                        if (location_name == ""){
                            location_name = "";
                        }
                        var latitude = sl_vals["latitude"];
                        if (latitude == ""){
                            latitude = "";
                        }
                        var longitude = sl_vals["longitude"];
                        if (longitude == ""){
                            longitude = "";
                        }
                        var un_location_code = sl_vals["un_location_code"];
                        if (un_location_code == ""){
                            un_location_code = "";
                        }
                        var street_name = sl_vals["street_name"];
                        if (street_name == ""){
                            street_name = "";
                        }
                        var street_number = sl_vals["street_number"];
                        if (street_number == ""){
                            street_number = "";
                        }
                        var floor = sl_vals["floor"];
                        if (floor == ""){
                            floor = "";
                        }
                        var post_code = sl_vals["post_code"];
                        if (post_code == ""){
                            post_code = "";
                        }
                        var city_name = sl_vals["city_name"];
                        if (city_name == ""){
                            city_name = "";
                        }
                        var state_region = sl_vals["state_region"];
                        if (state_region == ""){
                            state_region = "";
                        }
                        var country = sl_vals["country"];
                        if (country == ""){
                            country = "";
                        }
                        var displayed_name = sl_vals["displayed_name"];
                        if (displayed_name == false){
                            displayed_name = "";
                        }
                        var sl_array_created_by = sl_vals["shipment_location_array_created_by"];

                        $('#sl_tbody').append(`<tr class="added_sl_lines" id="${get_sl_row_id}">
                            <td class="row-index sl_row_index">
                                <p class='form-control' readonly="readonly" id="slrow_count" name="slrow_count" >${get_sl_row_id}</p>
                            </td>
                            <td style="display:none">
                                <input type="text" name="row_count_sl" readonly="readonly"
                                id="row_count_sl" value="${get_sl_row_id}" class='form-control get_sl_row_id'  />
                            </td>
                            <td>
                                <input type="text" name="location_type" placeholder="Maximum allowed characters 3" readonly="readonly"
                                    class='form-control location_type_sl' value="${location_type}" id="location_type_id_${get_sl_row_id}"/>
                            </td>

                            <td>
                                <input type="text" name="location_name" placeholder="Maximum allowed characters 100" readonly="readonly"
                                class='form-control location_name_sl' value="${location_name}" id="location_name_id_${get_sl_row_id}"/>
                            </td>
                            <td>
                                <input type="text" name="latitude" placeholder="Maximum allowed characters 10" readonly="readonly"
                                class='form-control latitude_sl' value="${latitude}" id="latitude_id_${get_sl_row_id}"/>
                            </td>
                            <td>
                                <input type="text" name="longitude" placeholder="Maximum allowed characters 11" readonly="readonly"
                                class='form-control longitude_sl' value="${longitude}" id="longitude_id_${get_sl_row_id}"/>
                            </td>
                            <td>
                                <input type="text" name="un_location_code" placeholder="Maximum allowed characters 5" readonly="readonly"
                                class='form-control un_location_code_sl' value="${un_location_code}" id="un_location_code_id_${get_sl_row_id}"/>
                            </td>
                            <td>
                                <input type="text" name="street_name" placeholder="Maximum allowed characters 100" readonly="readonly"
                                class='form-control street_name_sl' value="${street_name}" id="street_name_id_${get_sl_row_id}"/>
                            </td>
                            <td>
                                <input type="text" name="street_number" placeholder="Maximum allowed characters 50" readonly="readonly"
                                class='form-control street_number_sl' value="${street_number}" id="street_number_id_${get_sl_row_id}"/>
                            </td>
                            <td>
                                <input type="text" name="floor" placeholder="Maximum allowed characters 50" readonly="readonly"
                                class='form-control floor_sl' value="${floor}" id="floor_id_${get_sl_row_id}"/>
                            </td>
                            <td>
                                <input type="text" name="post_code" placeholder="Maximum allowed characters 10" readonly="readonly"
                                class='form-control post_code_sl' value="${post_code}" id="post_code_id_${get_sl_row_id}"/>
                            </td>
                            <td>
                                <input type="text" name="city_name" placeholder="Maximum allowed characters 65" readonly="readonly"
                                class='form-control city_name_sl' value="${city_name}" id="city_name_id_${get_sl_row_id}"/>
                            </td>
                            <td>
                                <input type="text" name="state_region" placeholder="Maximum allowed characters 65" readonly="readonly"
                                class='form-control state_region_sl' value="${state_region}" id="state_region_id_${get_sl_row_id}"/>
                            </td>
                            <td>
                                <input type="text" name="country" placeholder="Maximum allowed characters 75" readonly="readonly"
                                class='form-control country_sl' value="${country}" id="country_id_${get_sl_row_id}"/>
                            </td>
                            <td>
                                <input type="text" name="displayed_name" placeholder="Maximum allowed characters 250" readonly="readonly"
                                class='form-control displayed_name_sl' value="${displayed_name}" id="displayed_name_id_${get_sl_row_id}"/>
                            </td>
                            <td>
                                <input type="hidden" name="sl_array_created_by" readonly="readonly"
                                class='form-control sl_array_created_by' value="${sl_array_created_by}"
                                id="sl_array_created_by_${get_sl_row_id}"/>
                            </td>
                            <td>
                                <button class="btn btn-primary shipment_view" id="shipment_view"
                                type="button"><small><i class="fa fa-pencil"></i> </small></button>
                            </td>
                            <td>
                                <button class="btn btn-primary remove_sl" id="sl_remove"
                                type="button"><small><i class='fa fa-trash-o'></i></small></button>
                            </td>
                        </tr>`);
                    }
                }
                // Fetch References - child values and update
                var count_rc_items = data["count_rc_items"]
                if (count_rc_items > 0) {
                    var rc_line_values = data["rc_line_values"];
                    for(var rc=0; rc < rc_line_values.length; rc++) {
                        var get_rc_row_id = rc+1;
                        var rc_vals = rc_line_values[rc];

                        var reference_type = rc_vals["reference_type"];
                        var reference_value = rc_vals["reference_value"];
                        var ref_array_created_by = rc_vals["references_array_created_by"];

                        $('#rc_tbody').append(`<tr class="added_rc_lines" id="${get_rc_row_id}">
                            <td class="row-index rc_row_index">
                                <p class='form-control' readonly="readonly" id="rcrow_count" name="rcrow_count" >${get_rc_row_id}</p>
                            </td>
                            <td style="display:none">
                                <input type="text" name="row_count_rc" readonly="readonly"
                                id="row_count_rc" value="${get_rc_row_id}" class='form-control get_rc_row_id'  />
                            </td>
                            <td>
                                <input type="text" name="reference_type" placeholder="Maximum allowed characters 3" maxlength="3" readonly="readonly"
                                class='form-control reference_type_rc' value="${reference_type}" id="reference_type_rc_id_${get_rc_row_id}"/>
                            </td>
                            <td>
                                <input type="text" name="reference_value" placeholder="Maximum allowed characters 100" maxlength="100" readonly="readonly"
                                class='form-control reference_value_rc' value="${reference_value}" id="reference_value_rc_id_${get_rc_row_id}"/>
                            </td>
                            <td>
                                <input type="hidden" name="ref_array_created_by" readonly="readonly"
                                  class='form-control ref_array_created_by' value="${ref_array_created_by}"
                                  id="ref_array_created_by_${get_rc_row_id}"/>
                            </td>
                            <td>
                                <button class="btn btn-primary references_view" id="references_view"
                                type="button"><small><i class="fa fa-pencil"></i> </small></button>
                            </td>
                            <td>
                                <button class="btn btn-primary remove_rc" id="rc_remove"
                                type="button"><small><i class='fa fa-trash-o'></i></small></button>
                            </td>
                        </tr>`);
                    }
                }
           });
        }
    },

    on_click_si_template_create: function (ev) {
        var self = this;
        var dialog = new Dialog(this, {
            title: _t("Create SI Template"),
            $content: $(qweb.render('freightbox.si_template_create_popup')),
            buttons: [{
                text: _t('Create SI Template'),
                classes: "btn-primary",
                close: true,
                click: function () {
                var cargo_tbl = document.getElementById("cargo_tbody");
                var tq_tbl = document.getElementById("tq_tbody");
                var dp_tbl = document.getElementById("dp_tbody");
                var sl_tbl = document.getElementById("sl_tbody");
                var rc_tbl = document.getElementById("rc_tbody");


                // Parent column values
                var parent_vals = [];
//                var attachments = []
                var rc_table_count = rc_tbl.rows.length;
                var sl_table_count = sl_tbl.rows.length;
                var dp_table_count = dp_tbl.rows.length;
                var tq_table_count = tq_tbl.rows.length;
                var cargo_table_count = cargo_tbl.rows.length;

                var si_template_name = document.getElementById("si_template_create_name").value;
                var transport_document_type_code = document.getElementById("transport_document_type_code").value;
                /*if (transport_document_type_code == "") {
                    document.getElementById("transport_document_type_code_div").innerHTML="Please fill this field";
                    document.getElementById("transport_document_type_code_div").style.color="Red";
                    document.getElementById("transport_document_type_code").focus();
                    return false;
                }
                else
                {
                    document.getElementById("transport_document_type_code_div").innerHTML="";
                }*/
                if (transport_document_type_code == "") {
                    document.getElementById("transport_document_type_code_div").innerHTML="Please fill this field";
                    document.getElementById("transport_document_type_code_div").style.color="Red";
                    document.getElementById("transport_document_type_code").focus();
                    return false;
                }
                else
                {
                    document.getElementById("transport_document_type_code_div").innerHTML="";
                }

                if (transport_document_type_code === "BOL" || transport_document_type_code === "bol" || transport_document_type_code === "swb" || transport_document_type_code === "SWB"){
                    document.getElementById("transport_document_type_code_div").innerHTML= "";
                }
                else {
                    document.getElementById("transport_document_type_code_div").innerHTML= "Please enter BOL or SWB";
                    document.getElementById("transport_document_type_code_div").style.color="Red";
                    document.getElementById("transport_document_type_code").focus();
                    return false;
                }

                var is_shipper_owned = document.getElementById("is_shipped_onboard_type");
                var shipper_owned_tq;
                if(is_shipper_owned.checked == true){
                    shipper_owned_tq = true;
                } else {
                    shipper_owned_tq = false;
                }
                var is_electronic = document.getElementById("is_electronic");
                var is_electronic_val;
                if(is_electronic.checked == true){
                    is_electronic_val = true;
                } else {
                    is_electronic_val = false;
                }
                var is_charges_displayed = document.getElementById("is_charges_displayed");
                var is_charges_displayed_val;
                if(is_charges_displayed.checked == true){
                    is_charges_displayed_val = true;
                } else {
                    is_charges_displayed_val = false;
                }
                var number_of_copies = document.getElementById("number_of_copies").value;
                var number_of_originals = document.getElementById("number_of_originals").value;
                var carrier_booking_reference = document.getElementById("carrier_booking_reference").value;
                if (carrier_booking_reference == "") {
                    document.getElementById("carrier_booking_reference_div").innerHTML="Please fill this field";
                    document.getElementById("carrier_booking_reference_div").style.color="Red";
                    document.getElementById("carrier_booking_reference").focus();
                    return false;
                }
                else
                {
                    document.getElementById("carrier_booking_reference_div").innerHTML="";
                }
                var pre_carriage_under_shippers_responsibility = document.getElementById("pre_carriage_under_shippers_responsibility").value;

                // Invoice Payable At - vals
                var inv_payable_location_name = document.getElementById("inv_payable_location_name").value;
                if (inv_payable_location_name == "") {
                    document.getElementById("inv_payable_location_name_div").innerHTML="Please fill this field";
                    document.getElementById("inv_payable_location_name_div").style.color="Red";
                    document.getElementById("inv_payable_location_name").focus();
//                    alert('Please fill Location Name');
                    return false;

                }
                else
                {
                    document.getElementById("inv_payable_location_name_div").innerHTML="";
                }
                var inv_payable_un_location_code = document.getElementById("inv_payable_un_location_code").value;
                if (inv_payable_un_location_code == "") {
                    document.getElementById("inv_payable_un_location_code_div").innerHTML="Please fill this field";
                    document.getElementById("inv_payable_un_location_code_div").style.color="Red";
                    document.getElementById("inv_payable_un_location_code").focus();
                    return false;
                }
                else
                {
                    document.getElementById("inv_payable_un_location_code_div").innerHTML="";
                }


                var inv_payable_city_name = document.getElementById("inv_payable_city_name").value;
                if (inv_payable_city_name == "") {
                    document.getElementById("inv_payable_city_name_div").innerHTML="Please fill this field";
                    document.getElementById("inv_payable_city_name_div").style.color="Red";
                    document.getElementById("inv_payable_city_name").focus();
                    return false;
                }
                else
                {
                    document.getElementById("inv_payable_city_name_div").innerHTML="";
                }

                var inv_payable_state_region = document.getElementById("inv_payable_state_region").value;
                if (inv_payable_state_region == "") {
                    document.getElementById("inv_payable_state_region_div").innerHTML="Please fill this field";
                    document.getElementById("inv_payable_state_region_div").style.color="Red";
                    document.getElementById("inv_payable_state_region").focus();
                    return false;
                }
                else
                {
                    document.getElementById("inv_payable_state_region_div").innerHTML="";
                }

                var inv_payable_country = document.getElementById("inv_payable_country").value;
                if (inv_payable_country == "") {
                    document.getElementById("inv_payable_country_div").innerHTML="Please fill this field";
                    document.getElementById("inv_payable_country_div").style.color="Red";
                    document.getElementById("inv_payable_country").focus();
                    return false;
                }
                else
                {
                    document.getElementById("inv_payable_country_div").innerHTML="";
                }

                var si_created_by_parent_val = document.getElementById("new_si_created_by").value;
                var si_create_inquiry_no = document.getElementById("si_create_inquiry_no").value;
                var si_create_job_id = document.getElementById("new_si_job_id").value;
                var new_si_created_by_user_id = document.getElementById("new_si_created_by_user_id").value;

                parent_vals.push({
                    'si_template_name': si_template_name,
                    'transport_document_type_code': transport_document_type_code,
                    'is_shipper_owned': shipper_owned_tq,
                    'is_electronic': is_electronic_val,
                    'is_charges_displayed': is_charges_displayed_val,
                    'carrier_booking_reference': carrier_booking_reference,
                    'pre_carriage_under_shippers_responsibility': pre_carriage_under_shippers_responsibility,
                    'number_of_originals': number_of_originals,
                    'number_of_copies': number_of_copies,
                    'inv_payable_location_name': inv_payable_location_name,
                    'inv_payable_un_location_code': inv_payable_un_location_code,
                    'inv_payable_city_name': inv_payable_city_name,
                    'inv_payable_state_region': inv_payable_state_region,
                    'inv_payable_country': inv_payable_country,
                    'cargo_table_count': cargo_table_count,
                    'tq_table_count': tq_table_count,
                    'dp_table_count': dp_table_count,
                    'sl_table_count': sl_table_count,
                    'rc_table_count': rc_table_count,
                    'si_created_by_parent_val': si_created_by_parent_val,
                    'si_create_inquiry_no': si_create_inquiry_no,
                    'si_create_job_id': si_create_job_id,
                    'new_si_created_by_user_id': new_si_created_by_user_id,
//                    'upload_si': upload_si,
                });
//                attachments.push({'upload_si': upload_si,});

               // Child column values - Cargo Items
                var CargoTableColData = new Array();

                for(var i=0;i<cargo_table_count;i++){
                    var cargo_tds = cargo_tbl.rows.item(i).cells;
                    for (var j = 0; j < cargo_tds.length; j++) {
                        var row_count = (cargo_tbl.rows[i].cells[0].textContent.trim());
                        var column_name = cargo_tbl.rows[i].cells[j].children[0].name;

                        if (column_name === "row_count_id") {
                            var row_count_cargo = cargo_tbl.rows[i].cells[j].children[0].value;
//                            alert("row_count:"+ cargo_row_count_id);
                        }
                        else if (column_name === "cargo_line_item_id") {
                            var cargo_line_item_id = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "shipping_marks") {
                            var shipping_marks = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "carrier_booking_reference") {
                            var carrier_booking_reference = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "description_of_goods") {
                            var description_of_goods = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "hs_code") {
                            var hs_code = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "no_of_packages") {
                            var no_of_packages = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "weight") {
                            var weight = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "volume") {
                            var volume = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "weight_unit") {
                            var weight_unit = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "volume_unit") {
                            var volume_unit = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "package_code") {
                            var package_code = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if(column_name === "equipment_reference") {
                            var equipment_reference = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if(column_name === "cargo_array_created_by") {
                            var cargo_array_created_by = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        CargoTableColData[i] = {
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
                            "row_count_cargo": row_count_cargo,
                        }
                    }
                }
                // Child column values - Transport Equipment
                var TransportEquipmentTableColData = new Array();

                for(var m=0;m<tq_table_count;m++){
                    var transport_eq_tds = tq_tbl.rows.item(m).cells;
                    for (var k = 0; k < transport_eq_tds.length; k++) {
                        var tq_row_count = (tq_tbl.rows[m].cells[0].textContent.trim());
                        var tq_column_name = tq_tbl.rows[m].cells[k].children[0].name;
                        if (tq_column_name === "equipment_reference") {
                            var equipment_reference = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "weight_unit_tq") {
                            var weight_unit_tq = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "cargo_gross_weight") {
                            var cargo_gross_weight = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "container_tare_weight") {
                            var container_tare_weight = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "iso_equipment_code") {
                            var iso_equipment_code = tq_tbl.rows[m].cells[k].children[0].value;
                        }

                        else if (tq_column_name === "is_shipper_owned") {
                            var is_shipper_owned = tq_tbl.rows[m].cells[k].children[0].checked;
                        }
                        else if (tq_column_name === "temperature_min") {
                            var temperature_min = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "temperature_max") {
                            var temperature_max = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "temperature_unit") {
                            var temperature_unit = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "humidity_min") {
                            var humidity_min = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "humidity_min") {
                            var humidity_min = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "humidity_max") {
                            var humidity_max = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "ventilation_min") {
                            var ventilation_min = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "ventilation_min") {
                            var ventilation_min = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "ventilation_max") {
                            var ventilation_max = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "seal_number") {
                            var seal_number = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "seal_source") {
                            var seal_source = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "seal_type") {
                            var seal_type = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "tq_array_created_by") {
                            var tq_array_created_by = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        TransportEquipmentTableColData[m] = {
                            "equipment_reference": equipment_reference,
                            "weight_unit_tq": weight_unit_tq,
                            "cargo_gross_weight": cargo_gross_weight,
                            "container_tare_weight": container_tare_weight,
                            "iso_equipment_code": iso_equipment_code,
                            "is_shipper_owned": is_shipper_owned,
                            "temperature_min": temperature_min,
                            "temperature_max": temperature_max,
                            "temperature_unit": temperature_unit,
                            "humidity_min": humidity_min,
                            "humidity_max": humidity_max,
                            "ventilation_min": ventilation_min,
                            "ventilation_max": ventilation_max,
                            "seal_number": seal_number,
                            "seal_source": seal_source,
                            "seal_type": seal_type,
                            "tq_array_created_by": tq_array_created_by,
                        }
                    }
                }

                // Child column values - Document Parties
                var DocumentPartiesTableColData = new Array();
                for(var z=0; z<dp_table_count; z++){
                    var document_parties_tds = dp_tbl.rows.item(z).cells;
                    for (var l = 0; l < document_parties_tds.length; l++) {
                        var dp_row_count = (dp_tbl.rows[z].cells[0].textContent.trim());
                        var dp_column_name = dp_tbl.rows[z].cells[l].children[0].name;

                        if (dp_column_name === "row_count_dp") {
                            var row_count_dp = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "party_name") {
                            var party_name = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "tax_reference_1_dp") {
                            var tax_reference_1_dp = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "public_key") {
                            var public_key = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "street") {
                            var street = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "street_number") {
                            var street_number = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "floor") {
                            var floor = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "post_code") {
                            var post_code = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "city") {
                            var city = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "state_region") {
                            var state_region = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "country") {
                            var country = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "tax_reference_2") {
                            var tax_reference_2 = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "nmfta_code") {
                            var nmfta_code = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "party_function") {
                            var party_function = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "address_line") {
                            var address_line = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "name") {
                            var name = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "email") {
                            var email = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "phone") {
                            var phone = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "is_to_be_notified") {
                            var is_to_be_notified = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "dp_array_created_by") {
                            var dp_array_created_by = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        DocumentPartiesTableColData[z] = {
                            "party_name": party_name,
                            "tax_reference_1_dp": tax_reference_1_dp,
                            "public_key": public_key,
                            "street": street,
                            "street_number": street_number,
                            "floor": floor,
                            "post_code": post_code,
                            "city": city,
                            "state_region": state_region,
                            "country": country,
                            "tax_reference_2": tax_reference_2,
                            "nmfta_code": nmfta_code,
                            "party_function": party_function,
                            "address_line": address_line,
                            "name": name,
                            "email": email,
                            "phone": phone,
                            "is_to_be_notified": is_to_be_notified,
                            "dp_array_created_by": dp_array_created_by,
                            "row_count_dp": row_count_dp,
                        }
                    }
                }
                // Child column values - Shipment Locations
                var ShipmentLocationsTableColData = new Array();
                for(var d=0; d<sl_table_count; d++){
                    var shipment_location_tds = sl_tbl.rows.item(d).cells;
                    for (var p = 0; p < shipment_location_tds.length; p++) {
                        var sl_row_count = (sl_tbl.rows[d].cells[0].textContent.trim());
                        var sl_column_name = sl_tbl.rows[d].cells[p].children[0].name;

                        if (sl_column_name === "row_count_sl") {
                            var row_count_sl = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "location_type") {
                            var location_type = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "location_name") {
                            var location_name = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "latitude") {
                            var latitude = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "longitude") {
                            var longitude = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "un_location_code") {
                            var un_location_code = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "street_name") {
                            var street_name = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "street_number") {
                            var street_number = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "floor") {
                            var floor = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "post_code") {
                            var post_code = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "city_name") {
                            var city_name = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "state_region") {
                            var state_region = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "country") {
                            var country = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "displayed_name") {
                            var displayed_name = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "displayed_name") {
                            var displayed_name = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "sl_array_created_by") {
                            var sl_array_created_by = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        ShipmentLocationsTableColData[d] = {
                            "location_type": location_type,
                            "location_name": location_name,
                            "latitude": latitude,
                            "longitude": longitude,
                            "un_location_code": un_location_code,
                            "street_name": street_name,
                            "street_number": street_number,
                            "floor": floor,
                            "post_code": post_code,
                            "city_name": city_name,
                            "state_region": state_region,
                            "country": country,
                            "displayed_name": displayed_name,
                            "sl_array_created_by": sl_array_created_by,
                            "row_count_sl": row_count_sl,
                        }
                    }
                }
                // Child column values - References
                var ReferencesTableColData = new Array();
                for(var q=0; q<rc_table_count; q++){
                    var references_tds = rc_tbl.rows.item(q).cells;
                    for (var r = 0; r < references_tds.length; r++) {
                        var rc_row_count = (rc_tbl.rows[q].cells[0].textContent.trim());
                        var rc_column_name = rc_tbl.rows[q].cells[r].children[0].name;

                        if (rc_column_name === "row_count_rc") {
                            var row_count_rc = rc_tbl.rows[q].cells[r].children[0].value;
                        }
                        else if (rc_column_name === "reference_type") {
                            var reference_type = rc_tbl.rows[q].cells[r].children[0].value;
                        }
                        else if (rc_column_name === "reference_value") {
                            var reference_value = rc_tbl.rows[q].cells[r].children[0].value;
                        }
                        else if (rc_column_name === "ref_array_created_by") {
                            var ref_array_created_by = rc_tbl.rows[q].cells[r].children[0].value;
                        }
                        ReferencesTableColData[q] = {
                            "reference_type": reference_type,
                            "reference_value": reference_value,
                            "ref_array_created_by": ref_array_created_by,
                            "row_count_rc": row_count_rc
                        }
                    }
                }

                // RPC call to create shipping instructions with its childs
                rpc.query({
                    route: '/si_template_values_for_create',
                    params: {
                        parent_vals: parent_vals,
//                        attachments: attachments,
                        cargo_vals: CargoTableColData,
                        tq_vals: TransportEquipmentTableColData,
                        dp_vals: DocumentPartiesTableColData,
                        sl_vals: ShipmentLocationsTableColData,
                        rc_vals: ReferencesTableColData,
                    }
               }).then(function (res) {
                    Dialog.alert(this, _t('Successfully Created SI Template'));

               });

                }
            }],
        });
        dialog.opened().then(function () {
           // var ref_created_by = document.getElementById("new_si_created_by").value;
//            document.getElementById("ref_array_created_by_form").value = ref_created_by;
       });
        dialog.open();
    },


    on_click_add_references: function (ev) {
        var self = this;
        var dialog = new Dialog(this, {
            title: _t("Shipping Instruction - References"),
            $content: $(qweb.render('freightbox.add_references_values_popup')),
            buttons: [{
                text: _t('Add'),
                classes: "btn-primary",
                close: false,
                click: function () {
                    var reference_type = document.getElementById("reference_type_rc_form").value;
                    var reference_value = document.getElementById("reference_value_rc_form").value;
                    var ref_array_created_by = document.getElementById("ref_array_created_by_form").value;

                    var formrc = document.getElementById('formrc');
                    for(var i=0; i < formrc.elements.length; i++){
                        if(formrc.elements[i].value === '' && formrc.elements[i].hasAttribute('required')){
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
                    var rc_rowIdx = $('#rc_tbody tr:last').attr('id');
                    if (rc_rowIdx == undefined){
                        rc_rowIdx = 0;
                    }

                    $('#rc_tbody').append(`<tr class="added_rc_lines" id="${++rc_rowIdx}">
                    <td class="row-index rc_row_index">
                        <p class='form-control' id="rcrow_count" name="rcrow_count" readonly="readonly" >${rc_rowIdx}</p>
                    </td>
                    <td style="display:none">
                        <input type="text" name="row_count_rc"
                        id="row_count_rc" value="${rc_rowIdx}" title="${rc_rowIdx}" class='form-control get_rc_row_id'  />
                    </td>
                    <td>
                        <input type="text" name="reference_type" placeholder="Maximum allowed characters 3" maxlength="3" readonly="readonly"
                        class='form-control reference_type_rc' value="${reference_type}" title="${reference_type}" id="reference_type_rc_id_${rc_rowIdx}"/>
                    </td>
                    <td>
                        <input type="text" name="reference_value" placeholder="Maximum allowed characters 100" maxlength="100" readonly="readonly"
                        class='form-control reference_value_rc' value="${reference_value}" title="${reference_value}" id="reference_value_rc_id_${rc_rowIdx}"/>
                    </td>
                    <td>
                        <input type="hidden" name="ref_array_created_by" readonly="readonly"
                          class='form-control ref_array_created_by' value="${ref_array_created_by}"
                          id="ref_array_created_by_${rc_rowIdx}"/>
                    </td>
                    <td>
                        <button class="btn btn-primary references_view" id="references_view"
                        type="button"><small><i class="fa fa-pencil"></i> </small></button>
                    </td>
                    <td>
                        <button class="btn btn-primary remove_rc" id="rc_remove"
                        type="button"><small><i class='fa fa-trash-o'></i></small></button>
                    </td>
                </tr>`);
                }
            }],
        });
        dialog.opened().then(function () {
            var ref_created_by = document.getElementById("new_si_created_by").value;
            document.getElementById("ref_array_created_by_form").value = ref_created_by;
            var formrc = document.getElementById('formrc');
            for(var i=0; i < formrc.elements.length; i++){
                if(formrc.elements[i].hasAttribute('required')){
                     formrc.elements[i].style.background='#ADD8E6';
                }
            }
       });
        dialog.open();
    },

    on_click_add_shipment_locations: function (ev) {
        var self = this;
        var dialog = new Dialog(this, {
            title: _t("Shipping Instruction - Shipment Locations"),
            $content: $(qweb.render('freightbox.add_shipment_locations_values_popup')),
            buttons: [{
                text: _t('Add'),
                classes: "btn-primary",
                close: false,
                click: function () {
                    var location_type = document.getElementById("location_type_form").value;
//                    alert("location_type:"+ location_type);
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

                    var formsl = document.getElementById('formsl');
                    for(var i=0; i < formsl.elements.length; i++){
                        if(formsl.elements[i].value === '' && formsl.elements[i].hasAttribute('required')){
                            if (location_type == ""){
                                 document.getElementById("location_type_form").focus();
                                 document.getElementById("loc_type_div").innerHTML = "Please fill this field";
                                 document.getElementById("loc_type_div").style.color="Red";
                                 return;
                            } else {
                                document.getElementById("loc_type_div").innerHTML = "";
                            }
                            if (location_name == ""){
                                if (location_type === "POL" || location_type === "POD") {
                                     document.getElementById("location_name_form").focus();
                                     document.getElementById("loc_div").innerHTML = "Please fill this field";
                                     document.getElementById("loc_div").style.color="Red";
                                return;
                                }

                            } else {
                                document.getElementById("loc_div").innerHTML = "";
                            }
                            if (latitude == ""){
                                if (location_type === "POL" || location_type === "POD") {
                                     document.getElementById("latitude_form").focus();
                                     document.getElementById("lat_div").innerHTML = "Please fill this field";
                                     document.getElementById("lat_div").style.color="Red";
                                     return;
                                 }
                            } else {
                                document.getElementById("lat_div").innerHTML = "";
                            }
                            if (longitude == ""){
                                if (location_type === "POL" || location_type === "POD") {
                                 document.getElementById("longitude_form").focus();
                                 document.getElementById("long_div").innerHTML = "Please fill this field";
                                 document.getElementById("long_div").style.color="Red";
                                 return;
                                 }
                            } else {
                                document.getElementById("long_div").innerHTML = "";
                            }
                            if (un_location_code == ""){
                                if (location_type === "POL" || location_type === "POD") {
                                 document.getElementById("un_location_code_form").focus();
                                 document.getElementById("un_loc_code_div").innerHTML = "Please fill this field";
                                 document.getElementById("un_loc_code_div").style.color="Red";
                                 return;
                                 }
                            } else {
                                document.getElementById("un_loc_code_div").innerHTML = "";
                            }
                            if (street_name == ""){
                                if (location_type === "POL" || location_type === "POD") {
                                 document.getElementById("street_name_form").focus();
                                 document.getElementById("st_name_div").innerHTML = "Please fill this field";
                                 document.getElementById("st_name_div").style.color="Red";
                                 return;
                                 }
                            } else {
                                document.getElementById("st_name_div").innerHTML = "";
                            }
                            if (street_number == ""){
                                if (location_type === "POL" || location_type === "POD") {
                                 document.getElementById("street_number_form").focus();
                                 document.getElementById("st_no_div").innerHTML = "Please fill this field";
                                 document.getElementById("st_no_div").style.color="Red";
                                 return;
                                 }
                            } else {
                                document.getElementById("st_no_div").innerHTML = "";
                            }
                            if (floor == ""){
                                if (location_type === "POL" || location_type === "POD") {
                                 document.getElementById("floor_form").focus();
                                 document.getElementById("floor_div").innerHTML = "Please fill this field";
                                 document.getElementById("floor_div").style.color="Red";
                                 return;
                                 }
                            } else {
                                document.getElementById("floor_div").innerHTML = "";
                            }
                            if (post_code == ""){
                            if (location_type === "POL" || location_type === "POD") {
                                 document.getElementById("post_code_form").focus();
                                 document.getElementById("post_code_div").innerHTML = "Please fill this field";
                                 document.getElementById("post_code_div").style.color="Red";
                                 return;
                                 }
                            } else {
                                document.getElementById("post_code_div").innerHTML = "";
                            }
                            if (city_name == ""){
                                if (location_type === "POL" || location_type === "POD") {
                                 document.getElementById("city_name_form").focus();
                                 document.getElementById("city_div").innerHTML = "Please fill this field";
                                 document.getElementById("city_div").style.color="Red";
                                 return;
                                 }
                            } else {
                                document.getElementById("city_div").innerHTML = "";
                            }
                            if (state_region == ""){
                                if (location_type === "POL" || location_type === "POD") {
                                 document.getElementById("state_region_form").focus();
                                 document.getElementById("st_reg_div").innerHTML = "Please fill this field";
                                 document.getElementById("st_reg_div").style.color="Red";
                                 return;
                                 }
                            } else {
                                document.getElementById("st_reg_div").innerHTML = "";
                            }
                            if (country == ""){
                                if (location_type === "POL" || location_type === "POD") {
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
                    var sl_rowIdx = $('#sl_tbody tr:last').attr('id');
                    if (sl_rowIdx == undefined){
                        sl_rowIdx = 0;
                    }

                    $('#sl_tbody').append(`<tr class="added_sl_lines" id="${++sl_rowIdx}">
                    <td class="row-index sl_row_index">
                        <p class='form-control' id="slrow_count" name="slrow_count" readonly="readonly">${sl_rowIdx}</p>
                    </td>
                    <td style="display:none">
                        <input type="text" name="row_count_sl"
                        id="row_count_sl" value="${sl_rowIdx}" title="${sl_rowIdx}" class='form-control row_count_sl'  />
                    </td>
                    <td>
                        <input type="text" name="location_type" placeholder="Maximum allowed characters 3" readonly="readonly"
                                id="location_type_id_${sl_rowIdx}" value="${location_type}" title="${location_type}"
                                class='form-control location_type_sl'/>
                    </td>
                    <td>
                        <input type="text" name="location_name" placeholder="Maximum allowed characters 100" readonly="readonly"
                        class='form-control location_name_sl' value="${location_name}" title="${location_name}" id="location_name_id_${sl_rowIdx}"/>
                    </td>
                    <td>
                        <input type="text" name="latitude" placeholder="Maximum allowed characters 10" readonly="readonly"
                        class='form-control latitude_sl' value="${latitude}" title="${latitude}" id="latitude_id_${sl_rowIdx}"/>
                    </td>
                    <td>
                        <input type="text" name="longitude" placeholder="Maximum allowed characters 11" readonly="readonly"
                        class='form-control longitude_sl' value="${longitude}" title="${longitude}" id="longitude_id_${sl_rowIdx}"/>
                    </td>
                    <td>
                        <input type="text" name="un_location_code" placeholder="Maximum allowed characters 5" readonly="readonly"
                        class='form-control un_location_code_sl' value="${un_location_code}" title="${un_location_code}" id="un_location_code_id_${sl_rowIdx}"/>
                    </td>
                    <td>
                        <input type="text" name="street_name" placeholder="Maximum allowed characters 100" readonly="readonly"
                        class='form-control street_name_sl' value="${street_name}" title="${street_name}" id="street_name_id_${sl_rowIdx}"/>
                    </td>
                    <td>
                        <input type="text" name="street_number" placeholder="Maximum allowed characters 50" readonly="readonly"
                        class='form-control street_number_sl' value="${street_number}" title="${street_number}" id="street_number_id_${sl_rowIdx}"/>
                    </td>
                    <td>
                        <input type="text" name="floor" placeholder="Maximum allowed characters 50" readonly="readonly"
                        class='form-control floor_sl' value="${floor}" title="${floor}" id="floor_id_${sl_rowIdx}"/>
                    </td>
                    <td>
                        <input type="text" name="post_code" placeholder="Maximum allowed characters 10" readonly="readonly"
                        class='form-control post_code_sl' value="${post_code}" title="${post_code}" id="post_code_id_${sl_rowIdx}"/>
                    </td>
                    <td>
                        <input type="text" name="city_name" placeholder="Maximum allowed characters 65" readonly="readonly"
                        class='form-control city_name_sl' value="${city_name}" title="${city_name}" id="city_name_id_${sl_rowIdx}"/>
                    </td>
                    <td>
                        <input type="text" name="state_region" placeholder="Maximum allowed characters 65" readonly="readonly"
                        class='form-control state_region_sl' value="${state_region}" title="${state_region}" id="state_region_id_${sl_rowIdx}"/>
                    </td>
                    <td>
                        <input type="text" name="country" placeholder="Maximum allowed characters 75" readonly="readonly"
                        class='form-control country_sl' value="${country}" title="${country}" id="country_id_${sl_rowIdx}"/>
                    </td>
                    <td>
                        <input type="text" name="displayed_name" placeholder="Maximum allowed characters 250" readonly="readonly"
                        class='form-control displayed_name_sl' value="${displayed_name}" title="${displayed_name}" id="displayed_name_id_${sl_rowIdx}"/>
                    </td>
                    <td>
                        <input type="hidden" name="sl_array_created_by" readonly="readonly"
                        class='form-control sl_array_created_by' value="${sl_array_created_by}"
                        id="sl_array_created_by_${sl_rowIdx}"/>
                    </td>
                    <td>
                        <button class="btn btn-primary shipment_view" id="shipment_view"
                        type="button"><small><i class="fa fa-pencil"></i> </small></button>
                    </td>
                    <td>
                        <button class="btn btn-primary remove_sl" id="sl_remove"
                        type="button"><small><i class='fa fa-trash-o'></i></small></button>
                    </td>
                </tr>`);
                }
            }],
        });
        dialog.opened().then(function () {
            var sl_created_by = document.getElementById("new_si_created_by").value;
            document.getElementById("sl_array_created_by_form").value = sl_created_by;
            var transport_fpod_unloc_code = document.getElementById("transport_fpod_unloc_code").value;
            document.getElementById("un_location_code_form").value = transport_fpod_unloc_code;
            var transport_fpod_longitude = document.getElementById("transport_fpod_longitude").value;
            document.getElementById("longitude_form").value = transport_fpod_longitude;
            var transport_fpod_latitude = document.getElementById("transport_fpod_latitude").value;
            document.getElementById("latitude_form").value = transport_fpod_latitude;
            var transport_fpod_state = document.getElementById("transport_fpod_state").value;
            document.getElementById("state_region_form").value = transport_fpod_state;
            var transport_fpod_country = document.getElementById("transport_fpod_country").value;
            document.getElementById("country_form").value = transport_fpod_country;

//            $('#location_type_form').change(function(){
            $("#location_type_form").on('change', function(e) {
//                alert("sdf");
//                var opts = document.getElementById('location-type-list').childNodes;
//                opts.show();
                var loc_type = document.getElementById("location_type_form").value;
//                alert("loc_type:"+ loc_type);
                if (loc_type === "PRE" ||
                        loc_type === "PDE" ||
                        loc_type === "PCF" ||
                        loc_type === "OIR" ||
                        loc_type === "PSR") {
                    document.getElementById("location_type_form").value = loc_type;
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
                } // (loc_type === "POL" || "POD")
                else  {
                    document.getElementById("location_type_form").value = loc_type;
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
                /*if (loc_type == "POD") {
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
                if (loc_type == "PDE") {
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
                if (loc_type == "PCF") {
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
                if (loc_type == "OIR"){
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
                }*/
               /* if (loc_type == "POL" || loc_type == "POD"){

                }*/
            });

            var formsl = document.getElementById('formsl');
            for(var i=0; i < formsl.elements.length; i++){
                if(formsl.elements[i].hasAttribute('required')){
                    formsl.elements[i].style.background='#ADD8E6';
                }
            }
       });
        dialog.open();
    },

    on_click_add_document_parties: function (ev) {
        var self = this;
        var dialog = new Dialog(this, {
            title: _t("Shipping Instruction - Document Parties"),
            $content: $(qweb.render('freightbox.add_document_parties_values_popup')),
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

                    var formdp = document.getElementById('formdp');
                    for(var i=0; i < formdp.elements.length; i++){
                        if(formdp.elements[i].value === '' && formdp.elements[i].hasAttribute('required')){
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

                    var dp_rowIdx = $('#dp_tbody tr:last').attr('id');
                    if (dp_rowIdx == undefined){
                        dp_rowIdx = 0;
                    }


                    $('#dp_tbody').append(`<tr class="added_dp_lines" id="${++dp_rowIdx}">
                        <td class="row-index dp_row_index">
                            <p class='form-control' id="dprow_count" name="dprow_count" readonly="readonly">${dp_rowIdx}</p>
                        </td>
                        <td style="display:none">
                            <input type="text" name="row_count_dp"
                            id="row_count_dp" value="${dp_rowIdx}" title="${dp_rowIdx}" class='form-control get_dp_row_id'  />
                        </td>
                        <td>
                            <input type="text" name="party_name" placeholder="Maximum allowed characters 100" maxlength="100" readonly="readonly"
                            class='form-control party_name_dp' value="${party_name}" title=""${party_name}" id="party_name_dp_id_${dp_rowIdx}"/>
                        </td>
                        <td>
                            <input type="text" name="tax_reference_1_dp" placeholder="Maximum allowed characters 20" readonly="readonly"
                            class='form-control tax_reference_1_dp' value="${tax_reference_1}" title="${tax_reference_1}" id="tax_reference_1_dp_id_${dp_rowIdx}"/>
                        </td>
                        <td>
                            <input type="text" name="public_key" placeholder="Maximum allowed characters 500" readonly="readonly"
                            class='form-control public_key_dp' value="${public_key}" title="${public_key}" id="public_key_dp_id_${dp_rowIdx}"/>
                        </td>
                        <td>
                            <input type="text" name="street" placeholder="Maximum allowed characters 100" readonly="readonly"
                            class='form-control street_dp' value="${street}" title="${street}" id="street_id_${dp_rowIdx}"/>
                        </td>
                        <td>
                            <input type="text" name="street_number" placeholder="Maximum allowed characters 50" readonly="readonly"
                            class='form-control street_number_dp' value="${street_number}" title="${street_number}" id="street_number_id_${dp_rowIdx}"/>
                        </td>
                        <td>
                            <input type="text" name="floor" placeholder="Maximum allowed characters 50" readonly="readonly"
                            class='form-control floor_dp' value="${floor}" title="${floor}" id="floor_id_${dp_rowIdx}"/>
                        </td>
                        <td>
                            <input type="text" name="post_code" placeholder="Maximum allowed characters 10" readonly="readonly"
                            class='form-control post_code_dp' value="${post_code}" title="${post_code}" id="post_code_id_${dp_rowIdx}"/>
                        </td>
                        <td>
                            <input type="text" name="city" placeholder="Maximum allowed characters 65" readonly="readonly"
                            class='form-control city_dp' value="${city}" title="${city}" id="city_id_${dp_rowIdx}"/>
                        </td>
                        <td>
                            <input type="text" name="state_region" placeholder="Maximum allowed characters 65" readonly="readonly"
                            class='form-control state_region_dp' value="${state_region}" title="${state_region}" id="state_region_id_${dp_rowIdx}"/>
                        </td>
                        <td>
                            <input type="text" name="country" placeholder="Maximum allowed characters 75" readonly="readonly"
                            class='form-control country_dp' value="${country}" title="${country}" id="country_id_${dp_rowIdx}"/>
                        </td>
                        <td>
                            <input type="text" name="tax_reference_2" placeholder="Maximum allowed characters 20" readonly="readonly"
                            class='form-control tax_reference_2_dp' value="${tax_reference_2}" title="${tax_reference_2}" id="tax_reference_2_id_${dp_rowIdx}"/>
                        </td>
                        <td>
                            <input type="text" name="nmfta_code" placeholder="Maximum allowed characters 4" readonly="readonly"
                            class='form-control nmfta_code_dp' value="${nmfta_code}" title="${nmfta_code}" id="nmfta_code_id_${dp_rowIdx}"/>
                        </td>

                        <td>
                            <input type="text" name="party_function" placeholder="Maximum allowed characters 3" readonly="readonly"
                            class='form-control party_function_dp' value="${party_function}" title="${party_function}" id="party_function_id_${dp_rowIdx}"/>
                        </td>
                        <td>
                            <input type="text" name="address_line" placeholder="Maximum allowed characters 250" readonly="readonly"
                            class='form-control address_line_dp' value="${address_line}" title="${address_line}" id="address_line_id_${dp_rowIdx}"/>
                        </td>
                        <td>
                            <input type="text" name="name" placeholder="Maximum allowed characters 100" readonly="readonly"
                            class='form-control name_dp' value="${name}" title="${name}" id="name_id_${dp_rowIdx}"/>
                        </td>
                        <td>
                            <input type="text" name="email" placeholder="Maximum allowed characters 100" readonly="readonly"
                            class='form-control email_dp' value="${email}" title="${email}" id="email_id_${dp_rowIdx}"/>
                        </td>
                        <td>
                            <input type="text" name="phone" placeholder="Maximum allowed characters 30" readonly="readonly"
                            class='form-control phone_dp' value="${phone}" title="${phone}" id="phone_id_${dp_rowIdx}"/>
                        </td>
                        <td>
                            <input type="checkbox" name="is_to_be_notified" readonly="readonly"
                            class='form-control to_be_notified' value="${is_to_be_notified_val}" title="${is_to_be_notified_val}" id="to_be_notified_id_${dp_rowIdx}"/>
                        </td>
                        <td>
                            <input type="hidden" name="dp_array_created_by" readonly="readonly"
                            class='form-control dp_array_created_by' value="${dp_array_created_by}"
                             id="dp_array_created_by_${dp_rowIdx}"/>
                        </td>
                        <td>
                            <button class="btn btn-primary document_view" id="document_view"
                            type="button"><small><i class="fa fa-pencil"></i> </small></button>
                        </td>
                        <td>
                            <button class="btn btn-primary remove_dp" id="dp_remove"
                            type="button"><small><i class='fa fa-trash-o'></i></small></button>
                        </td>
                    </tr>`);
                    document.getElementById("to_be_notified_id_"+dp_rowIdx).checked = is_to_be_notified_val;
                }
            }],
        });
        dialog.opened().then(function () {
            var dp_created_by = document.getElementById("new_si_created_by").value;
            document.getElementById("dp_array_created_by_form").value = dp_created_by;
            var formdp = document.getElementById('formdp');
            for(var i=0; i < formdp.elements.length; i++){
                if(formdp.elements[i].hasAttribute('required')){
                    formdp.elements[i].style.background='#ADD8E6';
                }
            }
       });
        dialog.open();
    },

    on_click_add_transport_equipment: function (ev) {
        var self = this;
        var isEmpty;
        var dialog = new Dialog(this, {
            title: _t("Shipping Instruction - Transport Equipment"),
            $content: $(qweb.render('freightbox.add_transport_eqipment_values_popup')),
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

                    var si_container_type_is_reefer = document.getElementById("si_container_type_is_reefer_form").value;
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

                    isEmpty = false;
                   var formtq = document.getElementById('formtq');
                    for(var i=0; i < formtq.elements.length; i++){
                        if(formtq.elements[i].value === '' && formtq.elements[i].hasAttribute('required')){
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
                                 document.getElementById("cgw_unit_div").innerHTML = "Please enter number";
                                 document.getElementById("cgw_unit_div").style.color="Red";
                                 return;
                            } else {
                                document.getElementById("cgw_unit_div").innerHTML = "";
                            }
                            if (container_tare_weight == ""){
                                if(is_shipper_owned.checked == true){
                                    document.getElementById("container_tare_weight_form").focus();
                                     document.getElementById("ctw_unit_div").innerHTML = "Please enter number";
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
                            if (temperature_min == 0){
                                if(si_container_type_is_reefer == "True"){
                                    document.getElementById("temperature_min_form").focus();
                                     document.getElementById("temperature_min_div").innerHTML = "Please enter number";
                                     document.getElementById("temperature_min_div").style.color="Red";
                                     return;
                                }
                            } else {
                                document.getElementById("temperature_min_div").innerHTML = "";
                            }
                            if (temperature_max == 0){
                                if(si_container_type_is_reefer == "True"){
                                    document.getElementById("temperature_max_form").focus();
                                     document.getElementById("temperature_max_div").innerHTML = "Please enter number";
                                     document.getElementById("temperature_max_div").style.color="Red";
                                     return;
                                }
                            } else {
                                document.getElementById("temperature_max_div").innerHTML = "";
                            }
                            if (temperature_unit == ""){
                                if(si_container_type_is_reefer == "True"){
                                    document.getElementById("temperature_unit_form").focus();
                                     document.getElementById("temperature_unit_div").innerHTML = "Please enter number";
                                     document.getElementById("temperature_unit_div").style.color="Red";
                                     return;
                                }
                            } else {
                                document.getElementById("temperature_unit_div").innerHTML = "";
                            }
                            if (humidity_min == 0){
                                if(si_container_type_is_reefer == "True"){
                                    document.getElementById("humidity_min_form").focus();
                                     document.getElementById("humidity_min_div").innerHTML = "Please enter number";
                                     document.getElementById("humidity_min_div").style.color="Red";
                                     return;
                                }
                            } else {
                                document.getElementById("humidity_min_div").innerHTML = "";
                            }
                            if (humidity_max == 0){
                                if(si_container_type_is_reefer == "True"){
                                    document.getElementById("humidity_max_form").focus();
                                     document.getElementById("humidity_max_div").innerHTML = "Please enter number";
                                     document.getElementById("humidity_max_div").style.color="Red";
                                     return;
                                }
                            } else {
                                document.getElementById("humidity_max_div").innerHTML = "";
                            }
                            if (ventilation_min == 0){
                                if(si_container_type_is_reefer == "True"){
                                    document.getElementById("ventilation_min_form").focus();
                                     document.getElementById("ventilation_min_div").innerHTML = "Please enter number";
                                     document.getElementById("ventilation_min_div").style.color="Red";
                                     return;
                                }
                            } else {
                                document.getElementById("ventilation_min_div").innerHTML = "";
                            }
                            if (ventilation_max == 0){
                                if(si_container_type_is_reefer == "True"){
                                    document.getElementById("ventilation_max_form").focus();
                                     document.getElementById("ventilation_max_div").innerHTML = "Please enter number";
                                     document.getElementById("ventilation_max_div").style.color="Red";
                                     return;
                                }
                            } else {
                                document.getElementById("ventilation_max_div").innerHTML = "";
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
                    var tq_rowIdx = $('#tq_tbody tr:last').attr('id');
                    if (tq_rowIdx == undefined){
                        tq_rowIdx = 0;
                    }

                    $('#tq_tbody').append(`<tr class="added_tq_lines" id="${++tq_rowIdx}">
                      <td class="row-index tq_row_index">
                          <p class='form-control'  id="tqrow_count" name="tqrow_count" readonly="readonly">${tq_rowIdx}</p>
                      </td>
                      <td style="display:none">
                          <input type="text" name="row_count_tq"
                          id="row_count_tq" value="${tq_rowIdx}" class='form-control get_tq_row_id'  />
                      </td>
                      <td>
                        <input type="text" name="equipment_reference" placeholder="Maximum allowed characters 15" maxlength="15" readonly="readonly"
                            class='form-control equipment_reference' value="${equipment_reference}" title="${equipment_reference}" id="equipment_reference_id_${tq_rowIdx}"/>
                      </td>
                      <td>
                        <input type="text" name="weight_unit_tq" placeholder="Maximum allowed characters 3" maxlength="3" readonly="readonly"
                            class='form-control weight_unit_tq' value="${weight_unit_tq}" title="${weight_unit_tq}" id="weight_unit_tq_id_${tq_rowIdx}"/>
                      </td>
                      <td>
                        <input type="number" name="cargo_gross_weight" placeholder="Maximum allowed characters 9" maxlength="9" readonly="readonly"
                            class='form-control cargo_gross_weight' value="${cargo_gross_weight}" title="${cargo_gross_weight}" id="cargo_gross_weight_id_${tq_rowIdx}"/>
                      </td>
                      <td>
                        <input type="number" name="container_tare_weight" placeholder="Maximum allowed characters 9" maxlength="9" readonly="readonly"
                            class='form-control container_tare_weight' value="${container_tare_weight}" title="${container_tare_weight}" id="container_tare_weight_id_${tq_rowIdx}"/>
                      </td>
                      <td>
                        <input type="text" name="iso_equipment_code" placeholder="Maximum allowed characters 4" maxlength="4" readonly="readonly"
                            class='form-control iso_equipment_code' value="${iso_equipment_code}" title="${iso_equipment_code}" id="iso_equipment_code_id_${tq_rowIdx}"/>
                      </td>
                      <td>
                        <input type="checkbox" name="is_shipper_owned" readonly="readonly"
                          class='form-control shipper_owned' value="${shipper_owned_tq}" title="${shipper_owned_tq}" id="shipper_owned_id_${tq_rowIdx}"/>
                      </td>
                      <td>
                        <input type="number" name="temperature_min" placeholder="Maximum allowed characters 9" maxlength="9" readonly="readonly"
                            class='form-control temperature_min' value="${temperature_min}" title="${temperature_min}" id="temperature_min_id_${tq_rowIdx}"/>
                      </td>
                      <td>
                        <input type="number" name="temperature_max" placeholder="Maximum allowed characters 9" maxlength="9" readonly="readonly"
                            class='form-control temperature_max' value="${temperature_max}" title="${temperature_max}" id="temperature_max_id_${tq_rowIdx}"/>
                      </td>
                      <td>
                        <input type="text" name="temperature_unit" placeholder="Maximum allowed characters 3" maxlength="3" readonly="readonly"
                            class='form-control temperature_unit' value="${temperature_unit}" title="${temperature_unit}" id="temperature_unit_id_${tq_rowIdx}"/>
                      </td>
                      <td>
                        <input type="number" name="humidity_min" placeholder="Maximum allowed characters 9" maxlength="9" readonly="readonly"
                         class='form-control humidity_min' value="${humidity_min}" title="${humidity_min}" id="humidity_min_id_${tq_rowIdx}"/>
                      </td>
                      <td>
                        <input type="number" name="humidity_max" placeholder="Maximum allowed characters 9" maxlength="9" readonly="readonly"
                         class='form-control humidity_max' value="${humidity_max}" title="${humidity_max}" id="humidity_max_id_${tq_rowIdx}"/>
                      </td>
                      <td>
                        <input type="number" name="ventilation_min" placeholder="Maximum allowed characters 9" maxlength="9" readonly="readonly"
                         class='form-control ventilation_min' value="${ventilation_min}" title="${ventilation_min}" id="ventilation_min_id_${tq_rowIdx}"/>
                      </td>
                      <td>
                        <input type="number" name="ventilation_max" placeholder="Maximum allowed characters 9" maxlength="9" readonly="readonly"
                         class='form-control ventilation_max' value="${ventilation_max}" title="${ventilation_max}" id="ventilation_max_id_${tq_rowIdx}"/>
                      </td>
                      <td>
                        <input type="text" name="seal_number" placeholder="Maximum allowed characters 15" maxlength="15" readonly="readonly"
                            class='form-control seal_number' value="${seal_number}" title="${seal_number}" id="seal_number_id_${tq_rowIdx}"/>
                      </td>
                      <td>
                        <input type="text" name="seal_source" placeholder="Maximum allowed characters 5" readonly="readonly"
                            class='form-control seal_source' value="${seal_source}" title="${seal_source}" id="seal_source_id_${tq_rowIdx}"/>
                      </td>
                      <td>
                        <input type="text" name="seal_type" placeholder="Maximum allowed characters 5" readonly="readonly"
                            class='form-control seal_type' value="${seal_type}" title="${seal_type}" id="seal_type_id_${tq_rowIdx}"/>
                      </td>
                      <td>
                        <input type="hidden" name="tq_array_created_by" readonly="readonly"
                            class='form-control tq_array_created_by' value="${tq_array_created_by}"
                            id="tq_array_created_by_${tq_rowIdx}"/>
                      </td>

                      <td>
                        <button class="btn btn-primary tq_view" id="tq_view"
                            type="button"><small><i class="fa fa-pencil"></i> </small></button>
                      </td>
                      <td>
                        <button class="btn btn-primary remove_tq" id="tq_remove"
                            type="button"><small><i class='fa fa-trash-o'></i></small></button>
                      </td>

                   </tr>`);
                   document.getElementById("shipper_owned_id_"+tq_rowIdx).checked = shipper_owned_tq;

                }
            }],
       });
       dialog.opened().then(function () {
            var tq_created_by = document.getElementById("new_si_created_by").value;
            document.getElementById("tq_array_created_by_form").value = tq_created_by;

            var transport_cont_id = document.getElementById("transport_container_id").value;
            document.getElementById("equipment_reference_tq_form").value = transport_cont_id;

            var si_container_type_is_reefer = document.getElementById("transport_cont_type").value;
            document.getElementById("si_container_type_is_reefer_form").value = si_container_type_is_reefer;
            if (si_container_type_is_reefer == "True"){
                $("#temperature_min_form").attr('required',"required");
                $("#temperature_max_form").attr('required',"required");
                $("#temperature_unit_form").attr('required',"required");
                $("#humidity_min_form").attr('required',"required");
                $("#humidity_max_form").attr('required',"required");
                $("#ventilation_min_form").attr('required',"required");
                $("#ventilation_max_form").attr('required',"required");
            }
            var formtq = document.getElementById('formtq');
            for(var i=0; i < formtq.elements.length; i++){
                if(formtq.elements[i].hasAttribute('required')){
                    formtq.elements[i].style.background='#ADD8E6';
                }
            }

            /*$("#is_shipper_owned_form").on('change', function() {
                alert("change");
                var is_shipper_owned = document.getElementById("is_shipper_owned_form");
                if(is_shipper_owned.checked == true){
                    if ($("#container_tare_weight_form").attr('required')) {
                        alert("ifff");
                        $("#container_tare_weight_form").removeAttr('required');
                    }
                    else {
                        alert("else");
                        $("#container_tare_weight_form").attr('required','required');
                    }
                }


            });*/
       });
       dialog.open();
    },

    on_click: function (ev) {
       var self = this;
       var isEmpty;
       isEmpty = false;
        var dialog = new Dialog(this, {
            title: _t("Shipping Instruction - Cargo Items"),
            $content: $(qweb.render('freightbox.add_cargo_item_values_popup')),
            buttons: [{
                text: _t('Add'),
                classes: "btn-primary cargo_add_new_line",
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


                    var form = document.getElementById('theForm');
                    for(var i=0; i < form.elements.length; i++){
                        if(form.elements[i].value === '' && form.elements[i].hasAttribute('required')){
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
                                 document.getElementById("no_of_packages_div").innerHTML = "Please enter number";
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
                    var cargo_last_row_id = $('#cargo_tbody tr:last').attr('id');
                    if (cargo_last_row_id == undefined){
                        cargo_last_row_id = 0;
                    }
                    $('#cargo_tbody').append(`<tr class="added_cargo" id="${++cargo_last_row_id}">
                      <td class="row-index">
                              <p class='form-control'  id="row_count" name="row_count" readonly="readonly" >${cargo_last_row_id}</p>
                      </td>
                      <td style="display:none">
                          <input type="text" name="row_count_id"
                          id="row_count_id" value="${cargo_last_row_id}" class='form-control cargo_last_row_id'  />
                      </td>
                      <td>
                          <input type="text" name="cargo_line_item_id" readonly="readonly"
                          id="cargo_line_item_id_${cargo_last_row_id}" title="${cargo_line_item_id}" value="${cargo_line_item_id}" class='form-control cargo_line_item_id'  />
                      </td>
                      <td style="border-right: 1px solid black;">
                          <input type="text" name="shipping_marks" readonly="readonly"
                              id="shipping_marks_${cargo_last_row_id}" value="${cargo_shipping_marks}" title="${cargo_shipping_marks}" class='form-control shipping_marks'/>
                      </td>
                      <td>
                          <input type="text" name="carrier_booking_reference" readonly="readonly"
                             id="carrier_booking_reference_${cargo_last_row_id}" value="${carrier_booking_reference}" title="${carrier_booking_reference}"
                             maxlength="35" placeholder="Maximum allowed characters 35" class='form-control carrier_booking_reference'/>
                      </td>
                      <td>
                          <input type="text" name="description_of_goods" readonly="readonly"
                             id="description_of_goods_${cargo_last_row_id}" maxlength="250"
                             value="${description_of_goods}" title="${description_of_goods}"
                             placeholder="Maximum allowed characters 250"  class='form-control description_of_goods'/>
                      </td>
                      <td>
                          <input type="text" name="hs_code" readonly="readonly"
                             id="hs_code_${cargo_last_row_id}" maxlength="10"
                             value="${hs_code}" title="${hs_code}"
                             placeholder="Maximum allowed characters 10"  class='form-control hs_code'/>
                      </td>
                      <td>
                          <input type="number" name="no_of_packages" readonly="readonly"
                             id="no_of_packages_${cargo_last_row_id}" value="${no_of_packages}" title="${no_of_packages}"  class='form-control no_of_packages'/>
                      </td>
                      <td>
                          <input type="number" name="weight" readonly="readonly"
                             id="weight_${cargo_last_row_id}" value="${weight}" title="${weight}" class='form-control weight'/>
                      </td>
                      <td>
                          <input type="number" name="volume" readonly="readonly"
                             id="volume_${cargo_last_row_id}" value="${volume}" title="${volume}" class='form-control volume'/>
                      </td>
                      <td>
                          <input type="text" name="weight_unit" readonly="readonly"
                             id="weight_unit_${cargo_last_row_id}" maxlength="3"
                             value="${weight_unit}" title="${weight_unit}"
                             placeholder="Maximum allowed characters 3" class='form-control weight_unit'/>
                      </td>
                      <td>
                          <input type="text" name="volume_unit" readonly="readonly"
                             id="volume_unit_${cargo_last_row_id}" maxlength="3"
                             value="${volume_unit}" title="${volume_unit}"
                             placeholder="Maximum allowed characters 3"  class='form-control volume_unit'/>
                      </td>
                      <td>
                          <input type="text" name="package_code" readonly="readonly"
                             id="package_code_${cargo_last_row_id}" maxlength="3"
                             value="${package_code}" title="${package_code}" placeholder="Maximum allowed characters 3" class='form-control package_code'/>
                      </td>
                      <td>
                          <input type="text" name="equipment_reference" readonly="readonly"
                             id="equipment_reference_${cargo_last_row_id}" maxlength="15" readonly="readonly"
                             value="${equipment_reference}" title="${equipment_reference}"
                             placeholder="Maximum allowed characters 15"  class='form-control equipment_reference'/>
                      </td>
                      <td>
                          <input type="hidden" name="cargo_array_created_by"
                             id="cargo_array_created_by_${cargo_last_row_id}"
                             value="${cargo_created_by}" title="${cargo_created_by}"
                             class='form-control cargo_created_by'/>
                      </td>
                      <td>
                        <button class="btn btn-primary cargo_view" id="cargo_view"
                            type="button"><small><i class="fa fa-pencil"></i> </small></button>
                      </td>
                      <td>
                        <button class="btn btn-primary remove" id="cargo_remove"
                            type="button"><small><i class='fa fa-trash-o'></i></small></button>
                      </td>

                   </tr>`);
                   }
            }],
        });
        dialog.opened().then(function () {
            var created_by = document.getElementById("new_si_created_by").value;
            document.getElementById("cargo_array_created_by_form").value = created_by;

            var transport_cont_id = document.getElementById("transport_container_id").value;
            document.getElementById("equipment_reference_form").value = transport_cont_id;

            var carrier_booking_reference = document.getElementById("carrier_booking_reference").value;
            document.getElementById("carrier_booking_reference_form").value = carrier_booking_reference;


            var cl = document.getElementById("cargo_line_item_id_form").value;
            var form = document.getElementById('theForm');
            for(var i=0; i < form.elements.length; i++){
                if(form.elements[i].hasAttribute('required')){
                     form.elements[i].style.background='#ADD8E6';
                }
            }
            /*if (cl === ""){
                alert("cl");
                document.getElementById("cargo_line_item_id_form").focus();
                 document.getElementById("cargo_line_item_id_div").innerHTML = "Please fill this field";
                 document.getElementById("cargo_line_item_id_div").style.color="Red";
            }*/

        });
        dialog.open();
    },

    on_click_create_si_save_child_values: function (ev){
        var self = this;
                var parent_vals =  new Array();
                var new_si_created_by = document.getElementById("new_si_created_by").value;
                if (new_si_created_by == "") {
                    document.getElementById("new_si_created_by_div").innerHTML="Please fill this field";
                    document.getElementById("new_si_created_by_div").style.color="Red";
                    document.getElementById("new_si_created_by").focus();
                    return false;
                }
                else
                {
                    document.getElementById("new_si_created_by_div").innerHTML="";
                }

                var transport_document_type_code = document.getElementById("transport_document_type_code").value;
                if (transport_document_type_code == "") {
                    document.getElementById("transport_document_type_code_div").innerHTML="Please fill this field";
                    document.getElementById("transport_document_type_code_div").style.color="Red";
                    document.getElementById("transport_document_type_code").focus();
                    return false;
                }
                else
                {
                    document.getElementById("transport_document_type_code_div").innerHTML="";
                }

                if (transport_document_type_code === "BOL" || transport_document_type_code === "bol" || transport_document_type_code === "swb" || transport_document_type_code === "SWB"){
                    document.getElementById("transport_document_type_code_div").innerHTML= "";
                }
                else {
                    document.getElementById("transport_document_type_code_div").innerHTML= "Please enter BOL or SWB";
                    document.getElementById("transport_document_type_code_div").style.color="Red";
                    document.getElementById("transport_document_type_code").focus();
                    return false;
                }
                var is_shipper_owned = document.getElementById("is_shipped_onboard_type");
                var shipper_owned_tq;
                if(is_shipper_owned.checked == true){
                    shipper_owned_tq = true;
                } else {
                    shipper_owned_tq = false;
                }
                var is_electronic = document.getElementById("is_electronic");
                var is_electronic_val;
                if(is_electronic.checked == true){
                    is_electronic_val = true;
                } else {
                    is_electronic_val = false;
                }
                var is_charges_displayed = document.getElementById("is_charges_displayed");
                var is_charges_displayed_val;
                if(is_charges_displayed.checked == true){
                    is_charges_displayed_val = true;
                } else {
                    is_charges_displayed_val = false;
                }
                var number_of_copies = document.getElementById("number_of_copies").value;
                if (number_of_copies.toString().length > 9){
                    document.getElementById("number_of_copies_div").innerHTML="Max allowed 9 numbers ony";
                    document.getElementById("number_of_copies_div").style.color="Red";
                    document.getElementById("number_of_copies").focus();
                    return false;
                } else {
                    document.getElementById("number_of_copies_div").innerHTML = "";
                }
                var number_of_originals = document.getElementById("number_of_originals").value;
                if (number_of_originals.toString().length > 9){
                    document.getElementById("number_of_originals_div").innerHTML="Max allowed 9 numbers ony";
                    document.getElementById("number_of_originals_div").style.color="Red";
                    document.getElementById("number_of_originals").focus();
                    return false;
                } else {
                    document.getElementById("number_of_originals_div").innerHTML = "";
                }
                var carrier_booking_reference = document.getElementById("carrier_booking_reference").value;
                if (carrier_booking_reference == "") {
                    document.getElementById("carrier_booking_reference_div").innerHTML="Please fill this field";
                    document.getElementById("carrier_booking_reference_div").style.color="Red";
                    document.getElementById("carrier_booking_reference").focus();
                    return false;
                }
                else
                {
                    document.getElementById("carrier_booking_reference_div").innerHTML="";
                }
                var pre_carriage_under_shippers_responsibility = document.getElementById("pre_carriage_under_shippers_responsibility").value;
                // Invoice Payable At - vals
                var inv_payable_location_name = document.getElementById("inv_payable_location_name").value;
                if (inv_payable_location_name == "") {
                    document.getElementById("inv_payable_location_name_div").innerHTML="Please fill this field";
                    document.getElementById("inv_payable_location_name_div").style.color="Red";
                    document.getElementById("inv_payable_location_name").focus();
                    return false;
                }
                else
                {
                    document.getElementById("inv_payable_location_name_div").innerHTML="";
                }

                var inv_payable_un_location_code = document.getElementById("inv_payable_un_location_code").value;
                if (inv_payable_un_location_code == "") {
                    document.getElementById("inv_payable_un_location_code_div").innerHTML="Please fill this field";
                    document.getElementById("inv_payable_un_location_code_div").style.color="Red";
                    document.getElementById("inv_payable_un_location_code").focus();
                    return false;
                }
                else
                {
                    document.getElementById("inv_payable_un_location_code_div").innerHTML="";
                }


                var inv_payable_city_name = document.getElementById("inv_payable_city_name").value;
                if (inv_payable_city_name == "") {
                    document.getElementById("inv_payable_city_name_div").innerHTML="Please fill this field";
                    document.getElementById("inv_payable_city_name_div").style.color="Red";
                    document.getElementById("inv_payable_city_name").focus();
                    return false;
                }
                else
                {
                    document.getElementById("inv_payable_city_name_div").innerHTML="";
                }

                var inv_payable_state_region = document.getElementById("inv_payable_state_region").value;
                if (inv_payable_state_region == "") {
                    document.getElementById("inv_payable_state_region_div").innerHTML="Please fill this field";
                    document.getElementById("inv_payable_state_region_div").style.color="Red";
                    document.getElementById("inv_payable_state_region").focus();
                    return false;
                } else {
                    document.getElementById("inv_payable_state_region_div").innerHTML="";
                }

                var inv_payable_country = document.getElementById("inv_payable_country").value;
                if (inv_payable_country == "") {
                    document.getElementById("inv_payable_country_div").innerHTML="Please fill this field";
                    document.getElementById("inv_payable_country_div").style.color="Red";
                    document.getElementById("inv_payable_country").focus();
                    return false;
                } else  {
                    document.getElementById("inv_payable_country_div").innerHTML="";
                }

                var si_created_by_parent_val = document.getElementById("new_si_created_by").value;
                var si_create_inquiry_no = document.getElementById("si_create_inquiry_no").value;
                var si_create_job_id = document.getElementById("new_si_job_id").value;
                var si_create_transport_id = document.getElementById("new_si_transport_id").value;
                var saved_si_id = document.getElementById("saved_si_id").value;
                var save_si_name = document.getElementById("saved_si_name").value;
                var saved_cont_id = document.getElementById("transport_container_id").value;

                var cargo_tbl = document.getElementById("cargo_tbody");
                var tq_tbl = document.getElementById("tq_tbody");
                var dp_tbl = document.getElementById("dp_tbody");
                var sl_tbl = document.getElementById("sl_tbody");
                var rc_tbl = document.getElementById("rc_tbody");

                var rc_table_count = rc_tbl.rows.length;
                var sl_table_count = sl_tbl.rows.length;
                var dp_table_count = dp_tbl.rows.length;
                var tq_table_count = tq_tbl.rows.length;
                var cargo_table_count = cargo_tbl.rows.length;

                var parent_col_vals = {
                    'transport_document_type_code': transport_document_type_code,
                    'is_shipper_owned': shipper_owned_tq,
                    'is_electronic': is_electronic_val,
                    'is_charges_displayed': is_charges_displayed_val,
                    'carrier_booking_reference': carrier_booking_reference,
                    'pre_carriage_under_shippers_responsibility': pre_carriage_under_shippers_responsibility,
                    'number_of_originals': number_of_originals,
                    'number_of_copies': number_of_copies,
                    'inv_payable_location_name': inv_payable_location_name,
                    'inv_payable_un_location_code': inv_payable_un_location_code,
                    'inv_payable_city_name': inv_payable_city_name,
                    'inv_payable_state_region': inv_payable_state_region,
                    'inv_payable_country': inv_payable_country,
                    'state': "open",
                    'is_saved': true,
                    'cargo_table_count': cargo_table_count,
                    'tq_table_count': tq_table_count,
                    'dp_table_count': dp_table_count,
                    'sl_table_count': sl_table_count,
                    'rc_table_count': rc_table_count,
                    'si_created_by_parent_val': si_created_by_parent_val,
                    'si_create_inquiry_no': si_create_inquiry_no,
                    'si_create_job_id': si_create_job_id,
                    'si_create_transport_id': si_create_transport_id,
                    'saved_si_id': saved_si_id,
                    'saved_si_name': save_si_name,
                    'saved_cont_id': saved_cont_id,
                }

                parent_vals.push(parent_col_vals);
                var CargoTableColData = new Array();
                for(var i=0;i<cargo_table_count;i++){
                    var cargo_tds = cargo_tbl.rows.item(i).cells;
                    for (var j = 0; j < cargo_tds.length; j++) {
                        var row_count = (cargo_tbl.rows[i].cells[0].textContent.trim());
                        var column_name = cargo_tbl.rows[i].cells[j].children[0].name;
                     //   alert("column_name:"+column_name);

                        if (column_name === "row_count_id") {
                            var row_count_cargo = cargo_tbl.rows[i].cells[j].children[0].value;
//                            alert("row_count:"+ cargo_row_count_id);
                        }
                        else if (column_name === "cargo_line_item_id") {
                            var cargo_line_item_id = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "shipping_marks") {
                            var shipping_marks = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "carrier_booking_reference") {
                            var carrier_booking_reference = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "description_of_goods") {
                            var description_of_goods = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "hs_code") {
                            var hs_code = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "no_of_packages") {
                            var no_of_packages = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "weight") {
                            var weight = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "volume") {
                            var volume = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "weight_unit") {
                            var weight_unit = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "volume_unit") {
                            var volume_unit = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "package_code") {
                            var package_code = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if(column_name === "equipment_reference") {
                            var equipment_reference = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if(column_name === "cargo_array_created_by") {
                            var cargo_array_created_by = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        CargoTableColData[i] = {
                            "row_count_cargo": row_count_cargo,
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
//                        alert("xc:"+ JSON.stringify(CargoTableColData));
                    }
                }
//                alert("CargoTableColData:"+ JSON.stringify(CargoTableColData));
                // Child column values - Transport Equipment
                var TransportEquipmentTableColData = new Array();
                for(var m=0;m<tq_table_count;m++){
                    var transport_eq_tds = tq_tbl.rows.item(m).cells;
                    for (var k = 0; k < transport_eq_tds.length; k++) {
                        var tq_row_count = (tq_tbl.rows[m].cells[0].textContent.trim());
                        var tq_column_name = tq_tbl.rows[m].cells[k].children[0].name;

                        if (tq_column_name === "row_count_tq") {
                            var row_count_tq = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "equipment_reference") {
                            var equipment_reference = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "weight_unit_tq") {
                            var weight_unit_tq = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "cargo_gross_weight") {
                            var cargo_gross_weight = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "container_tare_weight") {
                            var container_tare_weight = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "iso_equipment_code") {
                            var iso_equipment_code = tq_tbl.rows[m].cells[k].children[0].value;
                        }

                        else if (tq_column_name === "is_shipper_owned") {
                            var is_shipper_owned = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "temperature_min") {
                            var temperature_min = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "temperature_max") {
                            var temperature_max = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "temperature_unit") {
                            var temperature_unit = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "humidity_min") {
                            var humidity_min = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "humidity_min") {
                            var humidity_min = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "humidity_max") {
                            var humidity_max = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "ventilation_min") {
                            var ventilation_min = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "ventilation_min") {
                            var ventilation_min = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "ventilation_max") {
                            var ventilation_max = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "seal_number") {
                            var seal_number = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "seal_source") {
                            var seal_source = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "seal_type") {
                            var seal_type = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "tq_array_created_by") {
                            var tq_array_created_by = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        TransportEquipmentTableColData[m] = {
                            "equipment_reference": equipment_reference,
                            "weight_unit_tq": weight_unit_tq,
                            "cargo_gross_weight": cargo_gross_weight,
                            "container_tare_weight": container_tare_weight,
                            "iso_equipment_code": iso_equipment_code,
                            "is_shipper_owned": is_shipper_owned,
                            "temperature_min": temperature_min,
                            "temperature_max": temperature_max,
                            "temperature_unit": temperature_unit,
                            "humidity_min": humidity_min,
                            "humidity_max": humidity_max,
                            "ventilation_min": ventilation_min,
                            "ventilation_max": ventilation_max,
                            "seal_number": seal_number,
                            "seal_source": seal_source,
                            "seal_type": seal_type,
                            "tq_array_created_by": tq_array_created_by,
                            "row_count_tq": row_count_tq,
                        }
                    }
                }

                // Child column values - Document Parties
                var DocumentPartiesTableColData = new Array();
                for(var z=0; z<dp_table_count; z++){
                    var document_parties_tds = dp_tbl.rows.item(z).cells;
                    for (var l = 0; l < document_parties_tds.length; l++) {
                        var dp_row_count = (dp_tbl.rows[z].cells[0].textContent.trim());
                        var dp_column_name = dp_tbl.rows[z].cells[l].children[0].name;

                        if (dp_column_name === "row_count_dp") {
                            var row_count_dp = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "party_name") {
                            var party_name = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "tax_reference_1_dp") {
                            var tax_reference_1_dp = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "public_key") {
                            var public_key = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "street") {
                            var street = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "street_number") {
                            var street_number = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "floor") {
                            var floor = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "post_code") {
                            var post_code = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "city") {
                            var city = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "state_region") {
                            var state_region = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "country") {
                            var country = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "tax_reference_2") {
                            var tax_reference_2 = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "nmfta_code") {
                            var nmfta_code = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "party_function") {
                            var party_function = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "address_line") {
                            var address_line = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "name") {
                            var name = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "email") {
                            var email = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "phone") {
                            var phone = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "is_to_be_notified") {
                            var is_to_be_notified = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "dp_array_created_by") {
                            var dp_array_created_by = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        DocumentPartiesTableColData[z] = {
                            "party_name": party_name,
                            "tax_reference_1_dp": tax_reference_1_dp,
                            "public_key": public_key,
                            "street": street,
                            "street_number": street_number,
                            "floor": floor,
                            "post_code": post_code,
                            "city": city,
                            "state_region": state_region,
                            "country": country,
                            "tax_reference_2": tax_reference_2,
                            "nmfta_code": nmfta_code,
                            "party_function": party_function,
                            "address_line": address_line,
                            "name": name,
                            "email": email,
                            "phone": phone,
                            "is_to_be_notified": is_to_be_notified,
                            "dp_array_created_by": dp_array_created_by,
                            "row_count_dp": row_count_dp,
                        }
                    }
                }
                // Child column values - Shipment Locations
                var ShipmentLocationsTableColData = new Array();
                for(var d=0; d<sl_table_count; d++){
                    var shipment_location_tds = sl_tbl.rows.item(d).cells;
                    for (var p = 0; p < shipment_location_tds.length; p++) {
                        var sl_row_count = (sl_tbl.rows[d].cells[0].textContent.trim());
                        var sl_column_name = sl_tbl.rows[d].cells[p].children[0].name;

                        if (sl_column_name === "row_count_sl") {
                            var row_count_sl = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "location_type") {
                            var location_type = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "location_name") {
                            var location_name = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "latitude") {
                            var latitude = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "longitude") {
                            var longitude = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "un_location_code") {
                            var un_location_code = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "street_name") {
                            var street_name = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "street_number") {
                            var street_number = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "floor") {
                            var floor = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "post_code") {
                            var post_code = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "city_name") {
                            var city_name = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "state_region") {
                            var state_region = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "country") {
                            var country = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "displayed_name") {
                            var displayed_name = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "displayed_name") {
                            var displayed_name = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "sl_array_created_by") {
                            var sl_array_created_by = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        ShipmentLocationsTableColData[d] = {
                            "location_type": location_type,
                            "location_name": location_name,
                            "latitude": latitude,
                            "longitude": longitude,
                            "un_location_code": un_location_code,
                            "street_name": street_name,
                            "street_number": street_number,
                            "floor": floor,
                            "post_code": post_code,
                            "city_name": city_name,
                            "state_region": state_region,
                            "country": country,
                            "displayed_name": displayed_name,
                            "sl_array_created_by": sl_array_created_by,
                            "row_count_sl": row_count_sl,
                        }
                    }
                }
                // Child column values - References
                var ReferencesTableColData = new Array();
                for(var q=0; q<rc_table_count; q++){
                    var references_tds = rc_tbl.rows.item(q).cells;
                    for (var r = 0; r < references_tds.length; r++) {
                        var rc_row_count = (rc_tbl.rows[q].cells[0].textContent.trim());
                        var rc_column_name = rc_tbl.rows[q].cells[r].children[0].name;

                        if (rc_column_name === "row_count_rc") {
                            var row_count_rc = rc_tbl.rows[q].cells[r].children[0].value;
                        }
                        else if (rc_column_name === "reference_type") {
                            var reference_type = rc_tbl.rows[q].cells[r].children[0].value;
                        }
                        else if (rc_column_name === "reference_value") {
                            var reference_value = rc_tbl.rows[q].cells[r].children[0].value;
                        }
                        else if (rc_column_name === "ref_array_created_by") {
                            var ref_array_created_by = rc_tbl.rows[q].cells[r].children[0].value;
                        }
                        ReferencesTableColData[q] = {
                            "reference_type": reference_type,
                            "reference_value": reference_value,
                            "ref_array_created_by": ref_array_created_by,
                            "row_count_rc": row_count_rc,
                        }
                    }
                }

                rpc.query({
                    route: '/si_vals',
                    params: {
                        parent_vals: parent_vals,
                        cargo_vals: CargoTableColData,
                        tq_vals: TransportEquipmentTableColData,
                        dp_vals: DocumentPartiesTableColData,
                        sl_vals: ShipmentLocationsTableColData,
                        rc_vals: ReferencesTableColData,
                    },
                }).then(function (res) {
                    document.getElementById("saved_si_id").value = res['si_rec_id'];
                    Dialog.alert(this, _t('Shipping Instruction saved successfully'));
                });
    },

    on_click_create_si_save_parent_values: function (ev){
        var self = this;
                var parent_vals =  new Array();
                var new_si_created_by = document.getElementById("new_si_created_by").value;
                if (new_si_created_by == "") {
                    document.getElementById("new_si_created_by_div").innerHTML="Please fill this field";
                    document.getElementById("new_si_created_by_div").style.color="Red";
                    document.getElementById("new_si_created_by").focus();
                    return false;
                }
                else
                {
                    document.getElementById("new_si_created_by_div").innerHTML="";
                }

                var transport_document_type_code = document.getElementById("transport_document_type_code").value;
                if (transport_document_type_code == "") {
                    document.getElementById("transport_document_type_code_div").innerHTML="Please fill this field";
                    document.getElementById("transport_document_type_code_div").style.color="Red";
                    document.getElementById("transport_document_type_code").focus();
                    return false;
                }
                else
                {
                    document.getElementById("transport_document_type_code_div").innerHTML="";
                }

                if (transport_document_type_code === "BOL" || transport_document_type_code === "bol" || transport_document_type_code === "swb" || transport_document_type_code === "SWB"){
                    document.getElementById("transport_document_type_code_div").innerHTML= "";
                }
                else {
                    document.getElementById("transport_document_type_code_div").innerHTML= "Please enter BOL or SWB";
                    document.getElementById("transport_document_type_code_div").style.color="Red";
                    document.getElementById("transport_document_type_code").focus();
                    return false;
                }
                var is_shipper_owned = document.getElementById("is_shipped_onboard_type");
                var shipper_owned_tq;
                if(is_shipper_owned.checked == true){
                    shipper_owned_tq = true;
                } else {
                    shipper_owned_tq = false;
                }
                var is_electronic = document.getElementById("is_electronic");
                var is_electronic_val;
                if(is_electronic.checked == true){
                    is_electronic_val = true;
                } else {
                    is_electronic_val = false;
                }
                var is_charges_displayed = document.getElementById("is_charges_displayed");
                var is_charges_displayed_val;
                if(is_charges_displayed.checked == true){
                    is_charges_displayed_val = true;
                } else {
                    is_charges_displayed_val = false;
                }
                var number_of_copies = document.getElementById("number_of_copies").value;
                if (number_of_copies.toString().length > 9){
                    document.getElementById("number_of_copies_div").innerHTML="Max allowed 9 numbers ony";
                    document.getElementById("number_of_copies_div").style.color="Red";
                    document.getElementById("number_of_copies").focus();
                    return false;
                } else {
                    document.getElementById("number_of_copies_div").innerHTML = "";
                }
                var number_of_originals = document.getElementById("number_of_originals").value;
                if (number_of_originals.toString().length > 9){
                    document.getElementById("number_of_originals_div").innerHTML="Max allowed 9 numbers ony";
                    document.getElementById("number_of_originals_div").style.color="Red";
                    document.getElementById("number_of_originals").focus();
                    return false;
                } else {
                    document.getElementById("number_of_originals_div").innerHTML = "";
                }
                var carrier_booking_reference = document.getElementById("carrier_booking_reference").value;
                if (carrier_booking_reference == "") {
                    document.getElementById("carrier_booking_reference_div").innerHTML="Please fill this field";
                    document.getElementById("carrier_booking_reference_div").style.color="Red";
                    document.getElementById("carrier_booking_reference").focus();
                    return false;
                }
                else
                {
                    document.getElementById("carrier_booking_reference_div").innerHTML="";
                }
                var pre_carriage_under_shippers_responsibility = document.getElementById("pre_carriage_under_shippers_responsibility").value;
                // Invoice Payable At - vals
                var inv_payable_location_name = document.getElementById("inv_payable_location_name").value;
                if (inv_payable_location_name == "") {
                    document.getElementById("inv_payable_location_name_div").innerHTML="Please fill this field";
                    document.getElementById("inv_payable_location_name_div").style.color="Red";
                    document.getElementById("inv_payable_location_name").focus();
                    return false;
                }
                else
                {
                    document.getElementById("inv_payable_location_name_div").innerHTML="";
                }

                var inv_payable_un_location_code = document.getElementById("inv_payable_un_location_code").value;
                if (inv_payable_un_location_code == "") {
                    document.getElementById("inv_payable_un_location_code_div").innerHTML="Please fill this field";
                    document.getElementById("inv_payable_un_location_code_div").style.color="Red";
                    document.getElementById("inv_payable_un_location_code").focus();
                    return false;
                }
                else
                {
                    document.getElementById("inv_payable_un_location_code_div").innerHTML="";
                }


                var inv_payable_city_name = document.getElementById("inv_payable_city_name").value;
                if (inv_payable_city_name == "") {
                    document.getElementById("inv_payable_city_name_div").innerHTML="Please fill this field";
                    document.getElementById("inv_payable_city_name_div").style.color="Red";
                    document.getElementById("inv_payable_city_name").focus();
                    return false;
                }
                else
                {
                    document.getElementById("inv_payable_city_name_div").innerHTML="";
                }

                var inv_payable_state_region = document.getElementById("inv_payable_state_region").value;
                if (inv_payable_state_region == "") {
                    document.getElementById("inv_payable_state_region_div").innerHTML="Please fill this field";
                    document.getElementById("inv_payable_state_region_div").style.color="Red";
                    document.getElementById("inv_payable_state_region").focus();
                    return false;
                } else {
                    document.getElementById("inv_payable_state_region_div").innerHTML="";
                }

                var inv_payable_country = document.getElementById("inv_payable_country").value;
                if (inv_payable_country == "") {
                    document.getElementById("inv_payable_country_div").innerHTML="Please fill this field";
                    document.getElementById("inv_payable_country_div").style.color="Red";
                    document.getElementById("inv_payable_country").focus();
                    return false;
                } else  {
                    document.getElementById("inv_payable_country_div").innerHTML="";
                }

                var si_created_by_parent_val = document.getElementById("new_si_created_by").value;
                var si_create_inquiry_no = document.getElementById("si_create_inquiry_no").value;
                var si_create_job_id = document.getElementById("new_si_job_id").value;
                var si_create_transport_id = document.getElementById("new_si_transport_id").value;
                var saved_si_id = document.getElementById("saved_si_id").value;
                var saved_cont_id = document.getElementById("transport_container_id").value;

                var cargo_tbl = document.getElementById("cargo_tbody");
                var tq_tbl = document.getElementById("tq_tbody");
                var dp_tbl = document.getElementById("dp_tbody");
                var sl_tbl = document.getElementById("sl_tbody");
                var rc_tbl = document.getElementById("rc_tbody");

                var rc_table_count = rc_tbl.rows.length;
                var sl_table_count = sl_tbl.rows.length;
                var dp_table_count = dp_tbl.rows.length;
                var tq_table_count = tq_tbl.rows.length;
                var cargo_table_count = cargo_tbl.rows.length;

                var parent_col_vals = {
                    'transport_document_type_code': transport_document_type_code,
                    'is_shipper_owned': shipper_owned_tq,
                    'is_electronic': is_electronic_val,
                    'is_charges_displayed': is_charges_displayed_val,
                    'carrier_booking_reference': carrier_booking_reference,
                    'pre_carriage_under_shippers_responsibility': pre_carriage_under_shippers_responsibility,
                    'number_of_originals': number_of_originals,
                    'number_of_copies': number_of_copies,
                    'inv_payable_location_name': inv_payable_location_name,
                    'inv_payable_un_location_code': inv_payable_un_location_code,
                    'inv_payable_city_name': inv_payable_city_name,
                    'inv_payable_state_region': inv_payable_state_region,
                    'inv_payable_country': inv_payable_country,
                    'state': "open",
                    'is_saved': true,
                    'cargo_table_count': cargo_table_count,
                    'tq_table_count': tq_table_count,
                    'dp_table_count': dp_table_count,
                    'sl_table_count': sl_table_count,
                    'rc_table_count': rc_table_count,
                    'si_created_by_parent_val': si_created_by_parent_val,
                    'si_create_inquiry_no': si_create_inquiry_no,
                    'si_create_job_id': si_create_job_id,
                    'si_create_transport_id': si_create_transport_id,
                    'saved_si_id': saved_si_id,
                    'saved_cont_id': saved_cont_id,

                }

                parent_vals.push(parent_col_vals);
                var CargoTableColData = new Array();
                for(var i=0;i<cargo_table_count;i++){
                    var cargo_tds = cargo_tbl.rows.item(i).cells;
                    for (var j = 0; j < cargo_tds.length; j++) {
                        var row_count = (cargo_tbl.rows[i].cells[0].textContent.trim());
                        var column_name = cargo_tbl.rows[i].cells[j].children[0].name;
                     //   alert("column_name:"+column_name);

                        if (column_name === "row_count_id") {
                            var row_count_cargo = cargo_tbl.rows[i].cells[j].children[0].value;
//                            alert("row_count:"+ cargo_row_count_id);
                        }
                        else if (column_name === "cargo_line_item_id") {
                            var cargo_line_item_id = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "shipping_marks") {
                            var shipping_marks = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "carrier_booking_reference") {
                            var carrier_booking_reference = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "description_of_goods") {
                            var description_of_goods = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "hs_code") {
                            var hs_code = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "no_of_packages") {
                            var no_of_packages = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "weight") {
                            var weight = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "volume") {
                            var volume = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "weight_unit") {
                            var weight_unit = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "volume_unit") {
                            var volume_unit = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if (column_name === "package_code") {
                            var package_code = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if(column_name === "equipment_reference") {
                            var equipment_reference = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        else if(column_name === "cargo_array_created_by") {
                            var cargo_array_created_by = cargo_tbl.rows[i].cells[j].children[0].value;
                        }
                        CargoTableColData[i] = {
                            "row_count_cargo": row_count_cargo,
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
//                        alert("xc:"+ JSON.stringify(CargoTableColData));
                    }
                }
//                alert("CargoTableColData:"+ JSON.stringify(CargoTableColData));
                // Child column values - Transport Equipment
                var TransportEquipmentTableColData = new Array();
                for(var m=0;m<tq_table_count;m++){
                    var transport_eq_tds = tq_tbl.rows.item(m).cells;
                    for (var k = 0; k < transport_eq_tds.length; k++) {
                        var tq_row_count = (tq_tbl.rows[m].cells[0].textContent.trim());
                        var tq_column_name = tq_tbl.rows[m].cells[k].children[0].name;

                        if (tq_column_name === "row_count_tq") {
                            var row_count_tq = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "equipment_reference") {
                            var equipment_reference = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "weight_unit_tq") {
                            var weight_unit_tq = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "cargo_gross_weight") {
                            var cargo_gross_weight = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "container_tare_weight") {
                            var container_tare_weight = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "iso_equipment_code") {
                            var iso_equipment_code = tq_tbl.rows[m].cells[k].children[0].value;
                        }

                        else if (tq_column_name === "is_shipper_owned") {
                            var is_shipper_owned = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "temperature_min") {
                            var temperature_min = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "temperature_max") {
                            var temperature_max = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "temperature_unit") {
                            var temperature_unit = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "humidity_min") {
                            var humidity_min = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "humidity_min") {
                            var humidity_min = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "humidity_max") {
                            var humidity_max = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "ventilation_min") {
                            var ventilation_min = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "ventilation_min") {
                            var ventilation_min = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "ventilation_max") {
                            var ventilation_max = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "seal_number") {
                            var seal_number = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "seal_source") {
                            var seal_source = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "seal_type") {
                            var seal_type = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        else if (tq_column_name === "tq_array_created_by") {
                            var tq_array_created_by = tq_tbl.rows[m].cells[k].children[0].value;
                        }
                        TransportEquipmentTableColData[m] = {
                            "equipment_reference": equipment_reference,
                            "weight_unit_tq": weight_unit_tq,
                            "cargo_gross_weight": cargo_gross_weight,
                            "container_tare_weight": container_tare_weight,
                            "iso_equipment_code": iso_equipment_code,
                            "is_shipper_owned": is_shipper_owned,
                            "temperature_min": temperature_min,
                            "temperature_max": temperature_max,
                            "temperature_unit": temperature_unit,
                            "humidity_min": humidity_min,
                            "humidity_max": humidity_max,
                            "ventilation_min": ventilation_min,
                            "ventilation_max": ventilation_max,
                            "seal_number": seal_number,
                            "seal_source": seal_source,
                            "seal_type": seal_type,
                            "tq_array_created_by": tq_array_created_by,
                            "row_count_tq": row_count_tq,
                        }
                    }
                }

                // Child column values - Document Parties
                var DocumentPartiesTableColData = new Array();
                for(var z=0; z<dp_table_count; z++){
                    var document_parties_tds = dp_tbl.rows.item(z).cells;
                    for (var l = 0; l < document_parties_tds.length; l++) {
                        var dp_row_count = (dp_tbl.rows[z].cells[0].textContent.trim());
                        var dp_column_name = dp_tbl.rows[z].cells[l].children[0].name;

                        if (dp_column_name === "row_count_dp") {
                            var row_count_dp = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "party_name") {
                            var party_name = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "tax_reference_1_dp") {
                            var tax_reference_1_dp = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "public_key") {
                            var public_key = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "street") {
                            var street = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "street_number") {
                            var street_number = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "floor") {
                            var floor = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "post_code") {
                            var post_code = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "city") {
                            var city = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "state_region") {
                            var state_region = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "country") {
                            var country = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "tax_reference_2") {
                            var tax_reference_2 = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "nmfta_code") {
                            var nmfta_code = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "party_function") {
                            var party_function = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "address_line") {
                            var address_line = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "name") {
                            var name = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "email") {
                            var email = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "phone") {
                            var phone = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "is_to_be_notified") {
                            var is_to_be_notified = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        else if (dp_column_name === "dp_array_created_by") {
                            var dp_array_created_by = dp_tbl.rows[z].cells[l].children[0].value;
                        }
                        DocumentPartiesTableColData[z] = {
                            "party_name": party_name,
                            "tax_reference_1_dp": tax_reference_1_dp,
                            "public_key": public_key,
                            "street": street,
                            "street_number": street_number,
                            "floor": floor,
                            "post_code": post_code,
                            "city": city,
                            "state_region": state_region,
                            "country": country,
                            "tax_reference_2": tax_reference_2,
                            "nmfta_code": nmfta_code,
                            "party_function": party_function,
                            "address_line": address_line,
                            "name": name,
                            "email": email,
                            "phone": phone,
                            "is_to_be_notified": is_to_be_notified,
                            "dp_array_created_by": dp_array_created_by,
                            "row_count_dp": row_count_dp,
                        }
                    }
                }
                // Child column values - Shipment Locations
                var ShipmentLocationsTableColData = new Array();
                for(var d=0; d<sl_table_count; d++){
                    var shipment_location_tds = sl_tbl.rows.item(d).cells;
                    for (var p = 0; p < shipment_location_tds.length; p++) {
                        var sl_row_count = (sl_tbl.rows[d].cells[0].textContent.trim());
                        var sl_column_name = sl_tbl.rows[d].cells[p].children[0].name;

                        if (sl_column_name === "row_count_sl") {
                            var row_count_sl = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "location_type") {
                            var location_type = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "location_name") {
                            var location_name = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "latitude") {
                            var latitude = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "longitude") {
                            var longitude = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "un_location_code") {
                            var un_location_code = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "street_name") {
                            var street_name = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "street_number") {
                            var street_number = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "floor") {
                            var floor = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "post_code") {
                            var post_code = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "city_name") {
                            var city_name = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "state_region") {
                            var state_region = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "country") {
                            var country = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "displayed_name") {
                            var displayed_name = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "displayed_name") {
                            var displayed_name = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        else if (sl_column_name === "sl_array_created_by") {
                            var sl_array_created_by = sl_tbl.rows[d].cells[p].children[0].value;
                        }
                        ShipmentLocationsTableColData[d] = {
                            "location_type": location_type,
                            "location_name": location_name,
                            "latitude": latitude,
                            "longitude": longitude,
                            "un_location_code": un_location_code,
                            "street_name": street_name,
                            "street_number": street_number,
                            "floor": floor,
                            "post_code": post_code,
                            "city_name": city_name,
                            "state_region": state_region,
                            "country": country,
                            "displayed_name": displayed_name,
                            "sl_array_created_by": sl_array_created_by,
                            "row_count_sl": row_count_sl,
                        }
                    }
                }
                // Child column values - References
                var ReferencesTableColData = new Array();
                for(var q=0; q<rc_table_count; q++){
                    var references_tds = rc_tbl.rows.item(q).cells;
                    for (var r = 0; r < references_tds.length; r++) {
                        var rc_row_count = (rc_tbl.rows[q].cells[0].textContent.trim());
                        var rc_column_name = rc_tbl.rows[q].cells[r].children[0].name;

                        if (rc_column_name === "row_count_rc") {
                            var row_count_rc = rc_tbl.rows[q].cells[r].children[0].value;
                        }
                        else if (rc_column_name === "reference_type") {
                            var reference_type = rc_tbl.rows[q].cells[r].children[0].value;
                        }
                        else if (rc_column_name === "reference_value") {
                            var reference_value = rc_tbl.rows[q].cells[r].children[0].value;
                        }
                        else if (rc_column_name === "ref_array_created_by") {
                            var ref_array_created_by = rc_tbl.rows[q].cells[r].children[0].value;
                        }
                        ReferencesTableColData[q] = {
                            "reference_type": reference_type,
                            "reference_value": reference_value,
                            "ref_array_created_by": ref_array_created_by,
                            "row_count_rc": row_count_rc,
                        }
                    }
                }


                var dialog = new Dialog(this, {
                    title: _t("Shpping Instruction"),
                    $content: $(qweb.render('freightbox.create_si_save_popup')),
                    buttons: [{
                        text: _t('Save'),
                        classes: "btn-primary",
                        close: false,
                        click: function () {
                            var save_si_name = document.getElementById("create_si_save_form_name").value;
                            if (save_si_name == ""){
                                document.getElementById("create_si_save_form_div").innerHTML="Please fill this field";
                                document.getElementById("create_si_save_form_div").style.color="Red";
                                document.getElementById("create_si_save_form_name").focus();
                                return;
                            } else {
                                document.getElementById("create_si_save_form_div").innerHTML= "";
                                document.getElementById("saved_si_name").value = save_si_name;
                            }
                            parent_col_vals['saved_si_name'] = save_si_name;
                            // RPC call to create shipping instructions with its childs
                            rpc.query({
                                route: '/si_vals',
                                params: {
                                    parent_vals: parent_vals,
                                    cargo_vals: CargoTableColData,
                                    tq_vals: TransportEquipmentTableColData,
                                    dp_vals: DocumentPartiesTableColData,
                                    sl_vals: ShipmentLocationsTableColData,
                                    rc_vals: ReferencesTableColData,
                                },
                            }).then(function (res) {
//                                alert("res"+ JSON.stringify(res['si_rec_id']));
                                document.getElementById("saved_si_id").value = res['si_rec_id'];
                                Dialog.alert(this, _t('Shipping Instruction saved successfully'));
                            });
                            dialog.close();
                        }
                    }],
                });

                dialog.opened().then(function () {
                });
                dialog.open();

    }

});

publicWidget.registry.WebsiteShippingInstructionsInstance = publicWidget.Widget.extend({
    selector: '#shipping_instructions_form',

    /**
     * @override
     */
    start: function () {
        var def = this._super.apply(this, arguments);
        this.instance = new WebsiteShippingInstructions(this);
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

return WebsiteShippingInstructions;
});

