from odoo.addons.portal.controllers.web import Home
from odoo import http
from odoo.http import request
import hashlib


class FreightCustomerPortal(http.Controller):

    # @http.route()
    # def index(self, **kw):
    #     super(WebsiteSort, self).index()
    #     vals = {}
    #     res = request.render('freightbox.freightbox_homepage', vals)
    #     return res

    @http.route('/customer_portal', type='http', auth='public', website=True)
    def customer_portal(self, **post):
        vals = {}
        res = request.render('freightbox.freight_customer_portal', vals)
        return res

    @http.route('/add/my/sign', type='http', auth='public', website=True)
    def start_booking(self, **post):

        if request.env.user._is_public():
            result = http.redirect_with_hash('/web/login')

        else:
            user = request.env.user
            result = request.render('freightbox.portal_my_add_sign', {
                'user': user})
        return result

    @http.route('/add_sign', type='http', auth='public', website=True)
    def add_sign(self, **post):
        user = request.env.user
        if post['new_sign'] != post['confirm_sign']:
            error_message = 'Sign do not match'
            return request.render('freightbox.portal_my_add_sign', {'error_message': error_message})

        hash_object = hashlib.sha256()
        hash_object.update(post['new_sign'].encode())
        encrypted_sign = hash_object.hexdigest()
        user.sudo().write({
            'print_signature': encrypted_sign,
        })
        return request.redirect('/my/home')
