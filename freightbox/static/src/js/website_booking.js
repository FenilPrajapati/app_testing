odoo.define('freightbox.website_booking', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
const Dialog = require('web.Dialog');
const { qweb, _t } = require('web.core');
var rpc = require('web.rpc');
var core = require('web.core');

$(document).ready(function () {
    console.log(">> TEMPLATE METHOD CALL")
    $('#add-container-line').click(function () {
        console.log(">> ON CLICK METHOD CALL")
        var cargo_plus_lines = document.getElementsByClassName('container_div');
        console.log(">>> cargo_plus_lines : ",cargo_plus_lines)
        console.log(">>> cargo_plus_lines.length : ",cargo_plus_lines.length)
        var container_index = cargo_plus_lines.length + 1;
        console.log(">>> container_index : ",container_index)

        let selectTemplate = `
            <label id="container_type_label_${container_index}" name="container_type_label_${container_index}" class="container_type_label" for="container_type_${container_index}" style="position: relative; left: 522px; top: -212px; width:47.5%; font-weight: 400; font-size: inherit; line-height: 1.5;">Container Type * </label>
            <select id="container_type_select_${container_index}" name="container_type_${container_index}" required="required" class="container_type_selection" style="position: relative; width: 47.5%; top: -185px; left: 40px; padding: 0.375rem 0.75rem; font-size: 1rem; font-weight: 400; line-height: 1.5; color: #212529; background-clip: padding-box; border: 1px solid #CED4DA; appearance: none; border-radius: 0.25rem; transition: background-color 0.05s ease-in-out, border-color 0.05s ease-in-out, box-shadow 0.05s ease-in-out; background-color: #ADD8E6;">
                <option value="">-- Select Record --</option>
            </select>

            <select id="weight_uom_select_${container_index}" name="weight_id_${container_index}" required="required" class="weight_uom_selection" style="position: relative; width: 13%; top: -66px; left: 371px; padding: 0.375rem 0.75rem; font-size: 1rem; font-weight: 400; line-height: 1.5; color: #212529; background-clip: padding-box; border: 1px solid #CED4DA; appearance: none; border-radius: 0.25rem; transition: background-color 0.05s ease-in-out, border-color 0.05s ease-in-out, box-shadow 0.05s ease-in-out; background-color: #ADD8E6;">
                <option value="">-- Select UOM --</option>
            </select>

            <select id="volume_uom_select_${container_index}" name="volume_id_${container_index}" required="required" class="volume_uom_selection" style="position: relative; width: 13%; top: -66px; left: 762px; padding: 0.375rem 0.75rem; font-size: 1rem; font-weight: 400; line-height: 1.5; color: #212529; background-clip: padding-box; border: 1px solid #CED4DA; appearance: none; border-radius: 0.25rem; transition: background-color 0.05s ease-in-out, border-color 0.05s ease-in-out, box-shadow 0.05s ease-in-out; background-color: #ADD8E6;">
                <option value="">-- Select UOM --</option>
            </select>

            <label id="move_type_label_${container_index}" name="move_type_label_${container_index}" class="move_type_label" for="move_type_id_${container_index}" style="position: relative; left: -274px; top: -19px; width:47.5%; font-weight: 400; font-size: inherit; line-height: 1.5;">Move Type * </label>
            <select id="move_type_id_${container_index}" name="move_type_id_${container_index}" required="required" class="move_type_selection" style="position: relative; width: 48.5%; top: -25px; left: 7px; padding: 0.375rem 0.75rem; font-size: 1rem; font-weight: 400; line-height: 1.5; color: #212529; background-clip: padding-box; border: 1px solid #CED4DA; appearance: none; border-radius: 0.25rem; transition: background-color 0.05s ease-in-out, border-color 0.05s ease-in-out, box-shadow 0.05s ease-in-out; background-color: #ADD8E6;">
                <option value="">-- Select Record --</option>
            </select>

            <label id="incoterm_label_${container_index}" name="incoterm_label_${container_index}" class="incoterm_label" for="incoterm_id_${container_index}" style="position: relative; left: 25px; top: -56px; width:47.5%; font-weight: 400; font-size: inherit; line-height: 1.5;">Incoterm * </label>
            <select id="incoterm_id_${container_index}" name="incoterm_id_${container_index}" required="required" class="incoterm_selection" style="position: relative; width: 47.5%; top: -62px; left: 535px; padding: 0.375rem 0.75rem; font-size: 1rem; font-weight: 400; line-height: 1.5; color: #212529; background-clip: padding-box; border: 1px solid #CED4DA; appearance: none; border-radius: 0.25rem; transition: background-color 0.05s ease-in-out, border-color 0.05s ease-in-out, box-shadow 0.05s ease-in-out; background-color: #ADD8E6;">
                <option value="">-- Select Record --</option>
            </select>
        `;

        function fetchModelRecords(modelName, selectElement) {
            $.ajax({
                url: '/get_model_records',
                type: 'POST',
                data: JSON.stringify({
                    'jsonrpc': '2.0',
                    'method': 'call',
                    'params': {
                        'model_name': modelName,
                    },
                }),
                contentType: 'application/json',
                success: function (result) {
                    selectElement.empty();
                    let records = JSON.parse(result.result);
                    for (let record of records) {
                        selectElement.append(`<option value="${record.id}">${record.name}</option>`);
                    }
                },
            });
        }

        var lineTemplate = '<div class="container_div" id="container_div_'+container_index+'" style="height:220px;">'+
        '<label class="col-form-label font-weight-normal label-optional" for="no_of_expected_container_'+container_index+'" style="position: relative; font-size: inherit; line-height: 1.5;">No. of Expected Container * </label>'+
        '<input type="number" name="no_of_expected_container_'+container_index+'" onkeypress="return event.charCode >= 48" min="0" id="sb_no_of_expected_container" required="required" autofocus="autofocus" t-attf-class="form-control" t-att-title="no_of_expected_container" placeholder="e.g 5" style="position: relative; left: -195px; top: 35px; width: 48.5%; padding: 0.375rem 0.75rem; font-size: 1rem; font-weight: 400; line-height: 1.5; color: #212529;    background-clip: padding-box; border: 1px solid #CED4DA;appearance: none; border-radius: 0.25rem; transition: background-color 0.05s ease-in-out, border-color 0.05s ease-in-out, box-shadow 0.05s ease-in-out;background-color: #ADD8E6;"/>'+
        '<label class="col-form-label font-weight-normal label-optional" for="cargo_description_'+container_index+'" style="position: relative; top:78px; left: -689px; font-size: inherit; line-height: 1.5;">Cargo Description* </label>'+
        '<input type="text" name="cargo_description_'+container_index+'" onkeypress="return event.charCode >= 48" min="0" id="sb_no_of_expected_container" required="required"; autofocus="autofocus" t-attf-class="form-control" t-att-title="no_of_expected_container" placeholder="e.g Cotton Shirt" style="position: relative; top: 75px; width: 48.5%; padding: 0.375rem 0.75rem; font-size: 1rem; font-weight: 400; line-height: 1.5; color: #212529;    background-clip: padding-box; border: 1px solid #CED4DA;appearance: none; border-radius: 0.25rem; transition: background-color 0.05s ease-in-out, border-color 0.05s ease-in-out, box-shadow 0.05s ease-in-out;background-color: #ADD8E6;"/>'+
        '<label class="col-form-label font-weight-normal label-optional" for="cargo_description_'+container_index+'" style="position: relative; top:40px; left: 30px; font-size: inherit; line-height: 1.5;">Quantity* </label>'+
        '<input type="float" name="quantity_'+container_index+'" onkeypress="return event.charCode >= 48" min="0" id="sb_no_of_expected_container" required="required"; autofocus="autofocus" t-attf-class="form-control" t-att-title="no_of_expected_container" placeholder="e.g 1000.00" style="position: relative; top: 37.5px; left:520.5px; width: 48.5%; padding: 0.375rem 0.75rem; font-size: 1rem; font-weight: 400; line-height: 1.5; color: #212529;    background-clip: padding-box; border: 1px solid #CED4DA;appearance: none; border-radius: 0.25rem; transition: background-color 0.05s ease-in-out, border-color 0.05s ease-in-out, box-shadow 0.05s ease-in-out;background-color: #ADD8E6;"/>'+
        '<label class="col-form-label font-weight-normal label-optional" for="weight_'+container_index+'" style="position: relative; top:80px; left: -493px; font-size: inherit; line-height: 1.5;">Weight</label>'+
        '<input type="float" name="weight_'+container_index+'" onkeypress="return event.charCode >= 48" min="0" id="weight_'+container_index+'" required="required"; autofocus="autofocus" t-attf-class="form-control" t-att-title="no_of_expected_container" style="position: relative; top: 115px; left:-549px; width: 35%; padding: 0.375rem 0.75rem; font-size: 1rem; font-weight: 400; line-height: 1.5; color: #212529;    background-clip: padding-box; border: 1px solid #CED4DA;appearance: none; border-radius: 0.25rem; transition: background-color 0.05s ease-in-out, border-color 0.05s ease-in-out, box-shadow 0.05s ease-in-out;background-color: #ADD8E6;"/>'+
        '<label class="col-form-label font-weight-normal label-optional" for="volume_'+container_index+'" style="position: relative; top:80px; left: -379px; font-size: inherit; line-height: 1.5;">Volume* </label>'+
        '<input type="float" name="volume_'+container_index+'" onkeypress="return event.charCode >= 48" min="0" id="sb_no_of_expected_container" required="required"; autofocus="autofocus" t-attf-class="form-control" t-att-title="no_of_expected_container" style="position: relative; top: 78px; left:520.5px; width: 35%; padding: 0.375rem 0.75rem; font-size: 1rem; font-weight: 400; line-height: 1.5; color: #212529;    background-clip: padding-box; border: 1px solid #CED4DA;appearance: none; border-radius: 0.25rem; transition: background-color 0.05s ease-in-out, border-color 0.05s ease-in-out, box-shadow 0.05s ease-in-out;background-color: #ADD8E6;"/>'+
        '<button id="delete-container-line" name="'+container_index+'" class="btn btn-primary " style="width: 82px; position: relative; top:-80px; left: 640px; background-color: transparent; color: grey; border-color: transparent;" title="Delete Line"><i class="fa fa-trash"/></button>'+
        '</div>';
        $('#lines-container').append(lineTemplate);
        let container = $("#lines-container");
        container.append(selectTemplate);
        let containerSelectElement = container.find('select.container_type_selection:last');
        let weightUomSelectElement = container.find('select.weight_uom_selection:last');
        let volumeUomSelectElement = container.find('select.volume_uom_selection:last');
        let moveTypeSelectElement = container.find('select.move_type_selection:last');
        let incotermsSelectElement = container.find('select.incoterm_selection:last');
        fetchModelRecords('shipping.container', containerSelectElement);
        fetchModelRecords('uom.uom', weightUomSelectElement);
        fetchModelRecords('uom.uom', volumeUomSelectElement);
        fetchModelRecords('move.type', moveTypeSelectElement);
        fetchModelRecords('account.incoterms', incotermsSelectElement);

        var line_count_element = document.getElementById('line_count')
        var new_line_count = 1;
        if (line_count_element != null) {
            var line_count = Number(line_count_element.value);
            new_line_count = line_count + 1;
        }
        line_count_element.value = new_line_count;
    });

});

$(document).on('click', '#delete-container-line', function(){
    console.log(">> ON CLICK DELETE DIV METHOD CALL")
    var div_id = "container_div_"+this.name;
    var cont_label = "container_type_label_"+this.name;
    var cont_select = "container_type_select_"+this.name;
    var weight_uom_select = "weight_uom_select_"+this.name;
    var volume_uom_select = "volume_uom_select_"+this.name;
    var move_type_label = "move_type_label_"+this.name;
    var move_type_select = "move_type_id_"+this.name;
    var incoterm_label = "incoterm_label_"+this.name;
    var incoterm_select = "incoterm_id_"+this.name;

    document.getElementById(div_id).remove();
    document.getElementById(cont_label).remove();
    document.getElementById(cont_select).remove();
    document.getElementById(weight_uom_select).remove();
    document.getElementById(volume_uom_select).remove();
    document.getElementById(move_type_label).remove();
    document.getElementById(move_type_select).remove();
    document.getElementById(incoterm_label).remove();
    document.getElementById(incoterm_select).remove();
});


publicWidget.registry.websiteStartBooking = publicWidget.Widget.extend({

    selector: '.booking_country_list',
    events: {
          'change select[name="country_id"]': '_onChangeCountry',
    },
//    xmlDependencies: ['/freightbox/static/src/xml/bookingPopup.xml'],


    /**
     * @override
     */
    start: function () {
        var self = this;
        var $country_name = $('#country_id input[name="country_id"]');
        var comp_name = document.getElementById('sb_company_name').value;
        var comp_email = document.getElementById('sb_email').value;

        /* $('#start_booking_subscription_form').on('click', '.subscribe_user', function (ev) {
            alert("xxxxxxxxxxxxxxxxxxxxxxxxxxx");
            return false;
        });*/
        $('#start_booking_inquiry_form').on('click', '.book_for_another_company', function (ev) {

//            alert("comp_name"+ comp_name);
//            alert("comp_email"+ comp_email);

            var book_for_another_company = document.getElementById("book_for_another_company");
            if(book_for_another_company.checked == true){
                document.getElementById('sb_company_name').removeAttribute('readonly');
                document.getElementById('sb_email').removeAttribute('readonly');
                document.getElementById('sb_company_name').value = "";
                document.getElementById('sb_email').value = "";
            } else {
                 document.getElementById('sb_company_name').value = comp_name;
                 document.getElementById('sb_email').value = comp_email;
                 document.getElementById('sb_company_name').readOnly = true;
                 document.getElementById('sb_email').readOnly = true;

            }

//                alert("book_for_another_company");

         });


        $('#start_booking_inquiry_form').on('click', '.submit_start_booking', function (ev) {
            var reg = /^[+]?\d+(\.\d+)?$/;
            var regex = /^[0-9A-Za-z\s]+$/;
             var sb_weight = document.getElementById("sb_weight").value;
//             alert("sb_weight"+ sb_weight);
             if (sb_weight) {
                 if((sb_weight.match(reg)))
                  {
                  document.getElementById("sb_weight_div").innerHTML = "";
                  }
                else
                  {
                   document.getElementById("sb_weight").focus();
                    document.getElementById("sb_weight_div").innerHTML = "Please enter a valid number";
                    document.getElementById("sb_weight_div").style.color="Red";
                   return false;
                  }
              }
              // Volume
              var sb_volume = document.getElementById("sb_volume").value;
              if (sb_volume) {
                if((sb_volume.match(reg)))
                  {
                 document.getElementById("sb_volume_div").innerHTML = "";
                  }
                else
                  {
                   document.getElementById("sb_volume").focus();
                    document.getElementById("sb_volume_div").innerHTML = "Please enter a valid number";
                    document.getElementById("sb_volume_div").style.color="Red";
                   return false;
                  }
              }

              var sb_place_of_origin = document.getElementById("sb_place_of_origin").value;
              if (sb_place_of_origin) {
                if((sb_place_of_origin.match(regex)))
                  {
                 document.getElementById("sb_place_of_origin_div").innerHTML = "";
                  }
                else
                  {
                   document.getElementById("sb_place_of_origin").focus();
                    document.getElementById("sb_place_of_origin_div").innerHTML = "Please enter a valid location";
                    document.getElementById("sb_place_of_origin_div").style.color="Red";
                   return false;
                  }
              }

              var sb_final_port_of_destination = document.getElementById("sb_final_port_of_destination").value;
              if (sb_final_port_of_destination) {
                if((sb_final_port_of_destination.match(regex)))
                  {
                 document.getElementById("sb_final_port_of_destination_div").innerHTML = "";
                  }
                else
                  {
                   document.getElementById("sb_final_port_of_destination").focus();
                    document.getElementById("sb_final_port_of_destination_div").innerHTML = "Please enter a valid location";
                    document.getElementById("sb_final_port_of_destination_div").style.color="Red";
                   return false;
                  }
              }

              var sb_point_of_stuffing = document.getElementById("sb_point_of_stuffing").value;
              if (sb_point_of_stuffing) {
                if((sb_point_of_stuffing.match(regex)))
                  {
                 document.getElementById("sb_point_of_stuffing_div").innerHTML = "";
                  }
                else
                  {
                   document.getElementById("sb_point_of_stuffing").focus();
                    document.getElementById("sb_point_of_stuffing_div").innerHTML = "Please enter a valid location";
                    document.getElementById("sb_point_of_stuffing_div").style.color="Red";
                   return false;
                  }
              }

              var sb_point_of_destuffing = document.getElementById("sb_point_of_destuffing").value;
              if (sb_point_of_destuffing) {
                if((sb_point_of_destuffing.match(regex)))
                  {
                 document.getElementById("sb_point_of_destuffing_div").innerHTML = "";
                  }
                else
                  {
                   document.getElementById("sb_point_of_destuffing").focus();
                    document.getElementById("sb_point_of_destuffing_div").innerHTML = "Please enter a valid location";
                    document.getElementById("sb_point_of_destuffing_div").style.color="Red";
                   return false;
                  }
              }


              var sb_phone = document.getElementById("sb_phone").value;
              var phone_no_validation = /^[+]*[(]{0,1}[0-9]{1,3}[)]{0,1}[-\s/0-9]*$/g;
                if(sb_phone.match(phone_no_validation)) {
                  if (sb_phone.length > 16){
                      document.getElementById("sb_phone").focus();
                      document.getElementById("sb_phone_div").innerHTML = "Only 15 characters allowed for Phone Number";
                      document.getElementById("sb_phone_div").style.color="Red";
                      return false;
                  }
                  if (sb_phone.length < 8){
                      document.getElementById("sb_phone").focus();
                      document.getElementById("sb_phone_div").innerHTML = "Please enter a valid number";
                      document.getElementById("sb_phone_div").style.color="Red";
                      return false;
                  }
                  document.getElementById("sb_phone_div").innerHTML = "";
              }
            else
              {
               document.getElementById("sb_phone").focus();
                document.getElementById("sb_phone_div").innerHTML = "Please enter a valid number";
                document.getElementById("sb_phone_div").style.color="Red";
               return false;
              }

            var sb_no_of_expected_container = document.getElementById("sb_no_of_expected_container").value;
//            alert("sb_no_of_expected_container:"+ sb_no_of_expected_container);
            if (sb_no_of_expected_container == 0 ){
                document.getElementById("sb_no_of_expected_container").focus();
                document.getElementById("sb_no_of_expected_container_div").innerHTML = "No Of Expected Container must be greater than 0";
                document.getElementById("sb_no_of_expected_container_div").style.color="Red";
                return false;
            }

            var sb_expected_date_of_shipment = document.getElementById("sb_expected_date_of_shipment").value;
//            alert("sb_expected_date_of_shipment:"+ sb_expected_date_of_shipment);
            var dtToday = new Date();
            var month = dtToday.getMonth() + 1;
            var day = dtToday.getDate();
            var year = dtToday.getFullYear();
            if(month < 10)
                month = '0' + month.toString();
            if(day < 10)
                day = '0' + day.toString();
            var todayDate = year + '-' + month + '-' + day;
//            alert(todayDate);
            if (sb_expected_date_of_shipment < todayDate){
//            alert("yes");
                document.getElementById("sb_expected_date_of_shipment").focus();
                document.getElementById("sb_expected_date_of_shipment_div").innerHTML = "Please select a valid date";
                document.getElementById("sb_expected_date_of_shipment_div").style.color="Red";
                return false;
            }

               var sb_quantity = document.getElementById("sb_quantity").value;
               if (sb_quantity <= 0){
                    document.getElementById("sb_quantity").focus();
                    document.getElementById("sb_quantity_div").innerHTML = "Quantity should be greater than 0";
                    document.getElementById("sb_quantity_div").style.color="Red";
                    return false;
               }
               var regex = /^[+-]?\d*\.?\d{0,9}$/;
               if(sb_quantity.match(regex)){
//                if (/^\d*$/.test(sb_quantity)){
                    document.getElementById("sb_quantity_div").innerHTML = "";
                } else {
                    document.getElementById("sb_quantity").focus();
                    document.getElementById("sb_quantity_div").innerHTML = "Please enter a valid number";
                    document.getElementById("sb_quantity_div").style.color="Red";
                    return false;
                }

                var sb_email = document.getElementById("sb_email").value;
                if (/^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/.test(sb_email)){
                    document.getElementById("sb_email").innerHTML = "";
                } else {
                    document.getElementById("sb_email").focus();
                    document.getElementById("sb_email_div").innerHTML = "Please enter a valid email address";
                    document.getElementById("sb_email_div").style.color="Red";
                    return false;
                }

        });
        // start_booking_website_form
        $('#start_booking_inquiry_form').on('click', '.get_user_template_values', function (ev) {

            var user_template = document.getElementById("user_template").value;
            if (user_template == "") {
                Dialog.alert(this, _t('Please select User Template'));
                return;
            } else {
//                alert("sdfdfsdffdsdfsdfdsf:::"+ user_template);
                rpc.query({
                    route: '/user_template_values',
                    params: {
                        user_template: user_template,
                    }
                }).then(function (data) {
//                alert("data:::"+ data["country_id"]);
//                alert("com name;:::"+ data["state_id"]);
//                document.getElementById("sb_company_name").value = data["sb_company_name"];
                document.getElementById("sb_name").value = data["sb_name"];
                var sb_street1;
                var sb_street2;
                if (data["sb_street1"] == false){
                    sb_street1 = ""
                } else {
                    sb_street1 = data["sb_street1"];
                }
                document.getElementById("sb_street1").value = sb_street1;
                if (data["sb_street2"] == false){
                    sb_street2 = ""
                } else {
                    sb_street2 = data["sb_street2"];
                }
                document.getElementById("sb_street2").value = sb_street2;
                document.getElementById("country_id").value = data["country_id"];
                document.getElementById("sb_state_id").value = data["sb_state_id"];
                document.getElementById("sb_zip").value = data["sb_zip"];
//                document.getElementById("sb_email").value = data["sb_email"];
                var sb_phone;
                if (data["sb_phone"] == false){
                    sb_phone = ""
                } else {
                    sb_phone = data["sb_phone"];
                }
                document.getElementById("sb_phone").value = sb_phone;
                document.getElementById("sb_cargo_name").value = data["sb_cargo_name"];
                document.getElementById("sb_quantity").value = data["sb_quantity"];
                var sb_weight;
                if (data["sb_weight"] == false){
                    sb_weight = "0.00"
                } else {
                    sb_weight = data["sb_weight"];
                }
                document.getElementById("sb_weight").value = sb_weight;
                var sb_volume;
                if (data["sb_volume"] == false){
                    sb_volume = "0.00"
                } else {
                    sb_volume = data["sb_volume"];
                }
                document.getElementById("sb_volume").value = sb_volume;
                document.getElementById("weight_id").value = data["sb_weight_id"];
                document.getElementById("volume_id").value = data["sb_volume_id"];
                document.getElementById("move_type_id").value = data["move_type_id"];
                document.getElementById("incoterm_id").value = data["incoterm_id"];
                document.getElementById("sb_place_of_origin").value = data["sb_place_of_origin"];
                document.getElementById("sb_final_port_of_destination").value = data["sb_final_port_of_destination"];
                document.getElementById("sb_point_of_stuffing").value = data["sb_point_of_stuffing"];
                document.getElementById("sb_point_of_destuffing").value = data["sb_point_of_destuffing"];
                document.getElementById("sb_no_of_expected_container").value = data["sb_no_of_expected_container"];
                document.getElementById("container_type").value = data["container_type"];
                document.getElementById("sb_expected_date_of_shipment").value = data["sb_expected_date_of_shipment"];
                var sb_remarks;
                if (data["sb_remarks"] == false){
                    sb_remarks = "";
                } else {
                    sb_remarks = data["sb_remarks"];
                }
                document.getElementById("sb_remarks").value = sb_remarks;
                });
            }
        });

        // SI Template Create action
       /* $('#start_booking_website_form').on('click', '.user_template_create', function (ev) {
//            alert("sdfsdf");
            self.on_click_user_template_create(ev);
        });*/
    },

    _changeCountry: function () {
        if (!$("#country_id").val()) {
            return;
        }
        this._rpc({
            route: "/booking/country_infos/" + $("#country_id").val(),
        }).then(function (data) {
            // populate states
            var selectStates = $("select[name='state_id']");
            var state_list = data.state_ids;
            if (state_list.length > 0) {
                selectStates.html('');
                for (var i = 0; i < state_list.length; i++) {
                    var state_name = state_list[i][1];
                    var state_id = state_list[i][0];
                    var opt = document.createElement('option');
                    opt.value = state_id;
                    opt.innerHTML = state_name;
                    selectStates.append(opt);
                }
                selectStates.parent('div').show();
                } else {
                    selectStates.val('').parent('div').hide();
                }
                selectStates.data('init', 0);
        });
    },
    _onChangeCountry: function (ev) {
        this._changeCountry();
    },


    /*on_click_user_template_create: function (ev) {
        var self = this;
        var sb_company_name = document.getElementById("sb_company_name").value;
        if (sb_company_name == "") {
            document.getElementById("sb_company_name_div").innerHTML="Please fill this field";
            document.getElementById("sb_company_name_div").style.color="Red";
            document.getElementById("sb_company_name").focus();
            return false;
        }
        else
        {
            document.getElementById("sb_company_name_div").innerHTML="";
        }
//                alert("sb_company_name:"+ sb_company_name);
        var sb_name = document.getElementById("sb_name").value;
        if (sb_name == "") {
            document.getElementById("sb_name_div").innerHTML="Please fill this field";
            document.getElementById("sb_name_div").style.color="Red";
            document.getElementById("sb_name").focus();
            return false;
        }
        else
        {
            document.getElementById("sb_name_div").innerHTML="";
        }
//                alert("sb_name:"+ sb_name);
                var sb_street1 = document.getElementById("sb_street1").value;
//                alert("sb_street1:"+ sb_street1);
                var sb_street2 = document.getElementById("sb_street2").value;
//                alert("sb_street2:"+ sb_street2);
        var country_id = document.getElementById("country_id").value;
        if (country_id == "") {
            document.getElementById("country_id_div").innerHTML="Please fill this field";
            document.getElementById("country_id_div").style.color="Red";
            document.getElementById("country_id").focus();
            return false;
        }
        else
        {
            document.getElementById("country_id_div").innerHTML="";
        }
//                alert("country_id:"+ country_id);
        var sb_state_id = document.getElementById("sb_state_id").value;
        if (sb_state_id == "") {
            document.getElementById("sb_state_id_div").innerHTML="Please fill this field";
            document.getElementById("sb_state_id_div").style.color="Red";
            document.getElementById("sb_state_id").focus();
            return false;
        }
        else
        {
            document.getElementById("sb_state_id_div").innerHTML="";
        }
//                alert("sb_state_id:"+ sb_state_id);
        var sb_zip = document.getElementById("sb_zip").value;
        if (sb_zip == "") {
            document.getElementById("sb_zip_div").innerHTML="Please fill this field";
            document.getElementById("sb_zip_div").style.color="Red";
            document.getElementById("sb_zip").focus();
            return false;
        }
        else
        {
            document.getElementById("sb_zip_div").innerHTML="";
        }
//                alert("sb_zip:"+ sb_zip);
                var sb_email = document.getElementById("sb_email").value;
                if (sb_email == "") {
            document.getElementById("sb_email_div").innerHTML="Please fill this field";
            document.getElementById("sb_email_div").style.color="Red";
            document.getElementById("sb_email").focus();
            return false;
        }
        else
        {
            document.getElementById("sb_email_div").innerHTML="";
        }
//                alert("sb_email:"+ sb_email);
                var sb_phone = document.getElementById("sb_phone").value;
                if (sb_phone == "") {
            document.getElementById("sb_phone_div").innerHTML="Please fill this field";
            document.getElementById("sb_phone_div").style.color="Red";
            document.getElementById("sb_phone").focus();
            return false;
        }
        else
        {
            document.getElementById("sb_phone_div").innerHTML="";
        }
//                alert("sb_phone:"+ sb_phone);
                var sb_cargo_name = document.getElementById("sb_cargo_name").value;
                if (sb_cargo_name == "") {
            document.getElementById("sb_cargo_name_div").innerHTML="Please fill this field";
            document.getElementById("sb_cargo_name_div").style.color="Red";
            document.getElementById("sb_cargo_name").focus();
            return false;
        }
        else
        {
            document.getElementById("sb_cargo_name_div").innerHTML="";
        }
//                alert("sb_cargo_name:"+ sb_cargo_name);
                var sb_quantity = document.getElementById("sb_quantity").value;
                if (sb_quantity == "") {
            document.getElementById("sb_quantity_div").innerHTML="Please fill this field";
            document.getElementById("sb_quantity_div").style.color="Red";
            document.getElementById("sb_quantity").focus();
            return false;
        }
        else
        {
            document.getElementById("sb_quantity_div").innerHTML="";
        }
//                alert("sb_quantity:"+ sb_quantity);
                var sb_weight = document.getElementById("sb_weight").value;
//                alert("sb_weight:"+ sb_weight);
                var sb_volume = document.getElementById("sb_volume").value;
//                alert("sb_volume:"+ sb_volume);
                var weight_id = document.getElementById("weight_id").value;
//                alert("weight_id:"+ weight_id);
                var volume_id = document.getElementById("volume_id").value;
//                alert("volume_id:"+ volume_id);
                var move_type_id = document.getElementById("move_type_id").value;
//                alert("move_type_id:"+ move_type_id);
                var incoterm_id = document.getElementById("incoterm_id").value;
//                alert("incoterm_id:"+ incoterm_id);
                var sb_place_of_origin = document.getElementById("sb_place_of_origin").value;
                if (sb_place_of_origin == "") {
            document.getElementById("sb_place_of_origin_div").innerHTML="Please fill this field";
            document.getElementById("sb_place_of_origin_div").style.color="Red";
            document.getElementById("sb_place_of_origin").focus();
            return false;
        }
        else
        {
            document.getElementById("sb_place_of_origin_div").innerHTML="";
        }
//                alert("sb_place_of_origin:"+ sb_place_of_origin);
                var sb_final_port_of_destination = document.getElementById("sb_final_port_of_destination").value;
                if (sb_final_port_of_destination == "") {
            document.getElementById("sb_final_port_of_destination_div").innerHTML="Please fill this field";
            document.getElementById("sb_final_port_of_destination_div").style.color="Red";
            document.getElementById("sb_final_port_of_destination").focus();
            return false;
        }
        else
        {
            document.getElementById("sb_final_port_of_destination_div").innerHTML="";
        }
//                alert("sb_final_port_of_destination:"+ sb_final_port_of_destination);
                var sb_point_of_stuffing = document.getElementById("sb_point_of_stuffing").value;
                if (sb_point_of_stuffing == "") {
            document.getElementById("sb_point_of_stuffing_div").innerHTML="Please fill this field";
            document.getElementById("sb_point_of_stuffing_div").style.color="Red";
            document.getElementById("sb_point_of_stuffing").focus();
            return false;
        }
        else
        {
            document.getElementById("sb_point_of_stuffing_div").innerHTML="";
        }
//                alert("sb_point_of_stuffing:"+ sb_point_of_stuffing);
                var sb_point_of_destuffing = document.getElementById("sb_point_of_destuffing").value;
                if (sb_point_of_destuffing == "") {
            document.getElementById("sb_point_of_destuffing_div").innerHTML="Please fill this field";
            document.getElementById("sb_point_of_destuffing_div").style.color="Red";
            document.getElementById("sb_point_of_destuffing").focus();
            return false;
        }
        else
        {
            document.getElementById("sb_point_of_destuffing_div").innerHTML="";
        }
//                alert("sb_point_of_destuffing:"+ sb_point_of_destuffing);
                var sb_no_of_expected_container = document.getElementById("sb_no_of_expected_container").value;
                if (sb_no_of_expected_container == "") {
            document.getElementById("sb_no_of_expected_container_div").innerHTML="Please fill this field";
            document.getElementById("sb_no_of_expected_container_div").style.color="Red";
            document.getElementById("sb_no_of_expected_container").focus();
            return false;
        }
        else
        {
            document.getElementById("sb_no_of_expected_container_div").innerHTML="";
        }
//                alert("sb_no_of_expected_container:"+ sb_no_of_expected_container);
                var container_type = document.getElementById("container_type").value;
//                alert("container_type:"+ container_type);
                var sb_expected_date_of_shipment = document.getElementById("sb_expected_date_of_shipment").value;
                if (sb_expected_date_of_shipment == "") {
            document.getElementById("sb_expected_date_of_shipment_div").innerHTML="Please fill this field";
            document.getElementById("sb_expected_date_of_shipment_div").style.color="Red";
            document.getElementById("sb_expected_date_of_shipment").focus();
            return false;
        }
        else
        {
            document.getElementById("sb_expected_date_of_shipment_div").innerHTML="";
        }
//                alert("sb_expected_date_of_shipment:"+ sb_expected_date_of_shipment);
                var lcl_fcl_id = document.getElementById("lcl_fcl_id").value;
//                alert("lcl_fcl_id:"+ lcl_fcl_id);
                var sb_remarks = document.getElementById("sb_remarks").value;
//                alert("sb_remarks:"+ sb_remarks);
        var dialog = new Dialog(this, {
            title: _t("Create User Template"),
            $content: $(qweb.render('freightbox.user_template_create_popup')),
            buttons: [{
                text: _t('Create User Template'),
                classes: "btn-primary",
                close: true,
                click: function () {
//                alert("ddddd");
                var user_vals = [];



                user_vals.push({
                    'sb_company_name': sb_company_name,
                    'sb_name': sb_name,
                    'sb_street1': sb_street1,
                    'sb_street2': sb_street2,
                    'country_id': country_id,
                    'sb_state_id': sb_state_id,
                    'sb_zip': sb_zip,
                    'sb_email': sb_email,
                    'sb_phone': sb_phone,
                    'sb_cargo_name': sb_cargo_name,
                    'sb_quantity': sb_quantity,
                    'sb_weight': sb_weight,
                    'sb_volume': sb_volume,
                    'weight_id': weight_id,
                    'volume_id': volume_id,
                    'move_type_id': move_type_id,
                    'incoterm_id': incoterm_id,
                    'sb_place_of_origin': sb_place_of_origin,
                    'sb_final_port_of_destination': sb_final_port_of_destination,
                    'sb_point_of_stuffing': sb_point_of_stuffing,
                    'sb_point_of_destuffing': sb_point_of_destuffing,
                    'sb_no_of_expected_container': sb_no_of_expected_container,
                    'container_type': container_type,
                    'sb_expected_date_of_shipment': sb_expected_date_of_shipment,
                    'lcl_fcl_id': lcl_fcl_id,
                    'sb_remarks': sb_remarks,
                });
                alert("user_vals"+ JSON.stringify(user_vals));

                rpc.query({
                    route: '/user_template_values_for_create',
                    params: {
                        user_vals: user_vals,
                    }
               }).then(function (res) {
                    Dialog.alert(this, _t('Successfully Created User Template'));
               });

                }
            }],
        });
        dialog.opened().then(function () {
           // var ref_created_by = document.getElementById("new_si_created_by").value;
//            document.getElementById("ref_array_created_by_form").value = ref_created_by;
       });
        dialog.open();
    },*/
});
//return WebsiteSubscribe;
});
