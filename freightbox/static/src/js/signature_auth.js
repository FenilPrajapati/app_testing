odoo.define('freightbox.signature_auth', function (require) {
    'use strict';
    console.log(">>> SIGNATURE JS CALL")
    var rpc = require('web.rpc');
    $(document).on('click', '#check_sign', function(){
        console.log(">>> SIGNATURE CLICK METHOD CALL")
        var rec_id = document.getElementById('rec_id').value;
        var type = document.getElementById('rec_type').value;
        var signature = document.getElementById('signature').value;
        console.log(">>> rec_id : ",rec_id)
        console.log(">>> type : ",type)
        console.log(">>> sq_signature : ",signature)
        rpc.query({
            route: '/check_signature_auth',
            params: {
                signature: signature,
            }
       }).then(function (res) {
            console.log('method_called')
            console.log('>>> res : ', res)
            if (res == true) {
                if (type == 'sq') {
                    window.location.href = '/accept_or_reject_sq/'+rec_id;
                }
                else if (type == 'si') {
                    window.location.href = '/view_or_update_si/'+rec_id;
                }
                else if (type == 'bol') {
                    window.location.href =  '/view_or_update_bol/'+rec_id;
                }
                else {
                    window.location.href = "/signature_auth/"+rec_id+"/"+type;
                }

            }
            else {
                window.location.href = "/signature_auth/"+rec_id+"/"+type;
            }
       });
    });
 });