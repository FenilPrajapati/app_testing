# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountMove(models.TransientModel):
    _name = 'apirate.wizard'
    _description = "Api Rate Wizard"

    api_company_currency_rate = fields.Float(
        'Api Company Currency Rate', digits=(9, 6)
    )
    currency_id = fields.Many2one(
        'res.currency', string='Company Currency', readonly=True,
        help="The Invoice Currency"
    )
    api_billing_currency_rate = fields.Float(
        'Api Billing Currency Rate', digits=(9, 6)
    )
    billing_currency_id = fields.Many2one(
        'res.currency', string='Billing Currency', readonly=True,
        help="The Invoice Billing  currency"
    )
    billing_currency_tot = fields.Monetary(currency_field='billing_currency_id', readonly=True,
                                           string="Billing Currency Total")
    api_difference_rate = fields.Float('Api Difference Rate', digits=(9, 6))
    edit_exchange_rate = fields.Boolean(string="Update Exchange rate")

    def update_exchange_rate(self):
        AccountMove = self.env['account.move']
        current_invoice_rec = AccountMove.browse([(self._context['default_current_id'])])
        print("sssss", self.env.company)
        ResCurrencyRate = self.env['res.currency.rate']
        record = ResCurrencyRate.search(
            [
                ("company_id", "=", self.env.company.id),
                ("currency_id", "=", current_invoice_rec.billing_currency_id.id),
                ("name", "=", fields.Datetime.now()),
            ],
            limit=1,
        )
        print("record:::::::::::", record)
        if record:
            original_exchange_rate = record.rate
            print("record:::", original_exchange_rate)
            manual_exchange_rate = self.api_billing_currency_rate
            print("manual_exchange_rate::", manual_exchange_rate)
            if manual_exchange_rate != original_exchange_rate:
                record.write({'rate': manual_exchange_rate})
            amt_total = current_invoice_rec.amount_total
            if amt_total != 0.0:
                amount_in_rate_currency = current_invoice_rec.currency_id._convert(
                    amt_total, current_invoice_rec.billing_currency_id, self.env.company, fields.Date.today(),
                    round=False)
                current_invoice_rec.billing_currency_tot = amount_in_rate_currency
            # record.write({'rate': original_exchange_rate})
        else:
            raise UserError(_('Rate is not defined in the system for %s today. '
                              'Please check your Currency table') % current_invoice_rec.billing_currency_id.name)
