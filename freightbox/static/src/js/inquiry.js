/*
odoo.define('freightbox.inquiry', function (require) {
'use strict';

var publicWidget = require('web.public.widget');
const Dialog = require('web.Dialog');
const { qweb, _t } = require('web.core');
var rpc = require('web.rpc');

publicWidget.registry.websiteInquiry = publicWidget.Widget.extend({
selector: '#start_booking_inquiry_form',

    */
/**
     * @override
     *//*

    start: function () {
        var self = this;
        var res = this._super.apply(this.arguments).then(function () {
            $('#start_booking_inquiry_form').on('click', '.submit_inquiry_form', function (ev) {
                 var inquiry_company_name = document.getElementById("inquiry_company_name").value;
                 var inquiry_company_email = document.getElementById("inquiry_company_email").value;
//                 alert("inquiry_company_email"+ inquiry_company_email);
                 return rpc.query({
                    route: '/inquiry_values',
                    params: {
                        inquiry_company_name: inquiry_company_name,
                        inquiry_company_email: inquiry_company_email,
                    }
               }).then(function (res) {
//                alert("resssss"+ res);
                if (res == true){
                    Dialog.alert(this, _t('This email is already registered. Please try diffrent email'));
                    return false;
                } else {
                    window.location.href = "/create/partner_for_inquiry/"+inquiry_company_name+"/"+inquiry_company_email+"/";
                }
               });
            });
        });
    },
});
});
*/
