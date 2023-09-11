odoo.define('freightbox.user_dashboard', function (require) {
    'use strict';
    console.log(">>> USER DASHBOARD JS CALL")
    var rpc = require('web.rpc');
    $(document).on('click', '#arrow_switch', function(){
        console.log(">>> USER DASHBOARD CLICK METHOD 1 CALL")
        console.log(">>> Name : ", this.name)

        var arrow_icons_up = document.getElementsByClassName("fa fa-chevron-up");
        var arrow_icons_down = document.getElementsByClassName("fa fa-chevron-down");
        var access_right_tr = document.getElementsByClassName("dashboard_access_right");


        for (var i=0; i<arrow_icons_up.length; i++) {
            if (arrow_icons_up[i].id == this.name) {
                if (arrow_icons_up[i].style.display == 'none') {
                    arrow_icons_up[i].style.display = 'block';
                }
                else {
                    arrow_icons_up[i].style.display = 'none';
                }
            }
        }

        for (var i=0; i<arrow_icons_down.length; i++) {
            if (arrow_icons_down[i].id == this.name) {
                if (arrow_icons_down[i].style.display == 'none') {
                    arrow_icons_down[i].style.display = 'block';
                }
                else {
                    arrow_icons_down[i].style.display = 'none';
                }
            }
        }

        for (var i=0; i<access_right_tr.length; i++) {
            if (access_right_tr[i].id == this.name) {
                if (access_right_tr[i].style.display == 'none') {
                    access_right_tr[i].style.display = 'block';
                    access_right_tr[i].style.width = '100%';
                }
                else {
                    access_right_tr[i].style.display = 'none';
                }
            }
        }

    });

 });
