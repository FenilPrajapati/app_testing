# -*- coding: utf-8 -*-

from odoo import fields, models, _
import requests
from odoo.exceptions import ValidationError


class CurrencyRate(models.Model):
    _name = 'currency.rate.provider'
    _description = "Currency Rates Provider"

    def _schedule_auto_currency_rate(self):
        api_model = self.env['api.integration'].search([('model_id.model', '=', "request.for.quote")])[-1]
        if api_model:
            headers = {'x-rapidapi-key': api_model.key, 'x-rapidapi-host': api_model.host}
            base_currency = self.env.company.currency_id
            ResCurrency = self.env['res.currency']
            ResCurrencyRate = self.env['res.currency.rate']
            active_currency_ids = ResCurrency.search([('active', '=', True)])
            past_record = ResCurrencyRate.search([("name", ">", fields.Date.today())])
            if past_record:
                past_record.sudo().unlink()
            for currency in active_currency_ids:
                record = ResCurrencyRate.search(
                    [
                        ("company_id", "=", self.env.company.id),
                        ("currency_id", "=", currency.id),
                        ("name", "=", fields.Date.today()),
                    ],
                    limit=1,
                )
                if currency.name != base_currency.name:
                    querystring = {"to": currency.name, "from": base_currency.name, "q": "1.0"}
                    response = requests.request("GET", api_model.url, headers=headers, params=querystring)
                    body_msg = "Dear ${api_model.user_id.partner_id.id},  <br/> Response message from API is ${response.text} "
                    print("response.status_code::", response.status_code)
                    print("response.text::", response.text)
                    if response.status_code == 200:
                        rate = response.text
                        if rate != "0":
                            if record:
                                record.write({"rate": response.text})
                            else:
                                ResCurrencyRate.create({
                                    'name': fields.Date.today(),
                                    'rate': rate,
                                    'company_id': self.env.company.id,
                                    'currency_id': currency.id,
                                })
                    # else:
                    #     self.env['mail.mail'].sudo().create({
                    #         'subject': response.text,
                    #         'email_from': api_model.user_id.partner_id.email,
                    #         'author_id': api_model.user_id.partner_id.id,
                    #         'email_to': api_model.user_id.partner_id.email,
                    #         'body_html': body_msg,
                    #     }).send()
                    #     api_model.write({'description': response.text})
                        # raise ValidationError(_('Dear User, Please check your API connection!'))
                else:
                    if record:
                        record.write({"rate": 1})
                    else:
                        ResCurrencyRate.create({
                            'name': fields.Date.today(),
                            'rate': 1,
                            'company_id': self.env.company.id,
                            'currency_id': currency.id,
                        })
                api_model.write({'last_executed_date': fields.Datetime.now()})
