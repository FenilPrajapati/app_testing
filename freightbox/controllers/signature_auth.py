from odoo import http
from odoo.http import request

GROUP_SYSTEM = 'base.group_system'


class SignAuthController(http.Controller):

    @http.route(['/signature_auth/<int:rec_id>/<string:type>'], type='http', auth="public", website=True)
    def signature_auth(self, rec_id, type, **kw):
        r = request.render('freightbox.form_signature_auth', {
            'rec_id': int(rec_id),
            'type': type
        })
        user = request.env.user
        if user.allow_print_without_signature:
            if type == 'sq':
                sq_rec = request.env['shipment.quote'].sudo().browse(rec_id)
                action = request.env.ref('freightbox.action_shipment_quote')
                r = request.render('freightbox.accept_or_reject_sq_form', {
                    'sq_rec': sq_rec,
                    'action': action,

                })
            if type == 'si':
                job_rec = request.env['job'].sudo().browse(rec_id)
                r = request.render('freightbox.view_or_update_si_form', {
                    'job_rec': job_rec,
                })
            if type == 'bol':

                hbol_rec = request.env['bill.of.lading'].sudo().search(
                    [('job_id', '=', rec_id), ('is_house_bill_of_lading', '=', True)], limit=1)
                bol_rec = request.env['bill.of.lading'].sudo().search(
                    [('job_id', '=', rec_id), ('is_master_bill_of_lading', '=', True)], limit=1)
                try:
                    payment_due = bol_rec.job_id.so_id.partner_id.is_due_exceeded
                except:
                    payment_due = False
                if hbol_rec:
                    print("---------------- in If ----------")
                    if hbol_rec.is_alow_shipper_to_create:
                        r = request.render('freightbox.create_bol_form', {
                            'bol_rec': hbol_rec,
                            'payment_due': payment_due
                        })
                    else:
                        r = request.render('freightbox.view_or_update_bol_form', {
                            'bol_rec': hbol_rec,
                            'payment_due': payment_due
                        })
                else:
                    print("---------------- in else ----------")
                    if bol_rec.is_alow_shipper_to_create:
                        r = request.render('freightbox.create_bol_form', {
                            'bol_rec': bol_rec,
                            'payment_due': payment_due
                        })
                    else:
                        r = request.render('freightbox.view_or_update_bol_form', {
                            'bol_rec': bol_rec,
                            'payment_due': payment_due
                        })

        return r

    @http.route(['/check_signature_auth'], type='json', method=['POST'], auth="public", website=True)
    def check_signature_auth(self, signature, **kw):
        user = request.env.user
        return user.check_signature(signature)

    @http.route("/test_post_url", type="http", auth="public", website=True, methods=["POST"])
    def test_post_url(self, **post):
        # Access the POST parameters using request.params
        param1 = request.params.get("param1")
        param2 = request.params.get("param2")

        # Do something with the parameters

        # Return a response
        r = request.render('freightbox.view_or_update_si_form', {
            'job_rec': param1,
        })
        return r