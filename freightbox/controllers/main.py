from odoo import http, _

from odoo.addons.auth_signup.controllers.main import AuthSignupHome
from odoo.addons.web.controllers.main import ensure_db, Home

from odoo.http import request

import re

# Shared parameters for all login/signup flows
SIGN_UP_REQUEST_PARAMS = {'db', 'login', 'debug', 'token', 'message', 'error', 'scope', 'mode',
                          'redirect', 'redirect_hostname', 'email', 'name', 'partner_id',
                          'password', 'confirm_password', 'city', 'country_id', 'lang'}


class EmailValid(Home):

    @http.route()
    def web_login(self, *args, **kw):
        ensure_db()
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if request.params:
            if not (re.fullmatch(regex, request.params['login'])):
                values = {k: v for k, v in request.params.items() if k in SIGN_UP_REQUEST_PARAMS}
                values['error'] = _("Wrong Email Formate")
                response = request.render('web.login', values)
                response.headers['X-Frame-Options'] = 'DENY'
                return response
        response = super(EmailValid, self).web_login(*args, **kw)
        return response


class SignUpEmail(AuthSignupHome):
    @http.route()
    def web_auth_signup(self, *args, **kw):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if request.params:
            if not (re.fullmatch(regex, request.params['login'])):
                values = {k: v for k, v in request.params.items() if k in SIGN_UP_REQUEST_PARAMS}
                values['error'] = _("Wrong Email Formate")
                response = request.render('auth_signup.signup', values)
                response.headers['X-Frame-Options'] = 'DENY'
                return response
        return super().web_auth_signup(*args, **kw)
