# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = "account.move"

    @api.depends('charges_line')
    def _get_total(self):
        total_freight_charge = 0.0
        total_destination_charge = 0.0
        total_origin_charge = 0.0
        total_charge = 0.0
        for rec in self:
            total_freight_charge = 0.0
            total_destination_charge = 0.0
            total_origin_charge = 0.0
            line_amount = 0.0
            for line in rec.charges_line:
                if self.move_type == 'in_invoice':
                    line_amount = line.final_amount
                if self.move_type == 'out_invoice':
                    line_amount = line.sale_final_amount
                company_currency = rec.currency_id
                line_currency = line.to_currency_id
                if line.charges_id.type_of_charges == 'freight':
                    if line_currency:
                        if line_currency.id != company_currency.id:
                            line_currency_to_company_crr = line_currency._convert(
                                line_amount, company_currency, self.env.company, fields.Date.today(), round=False)
                            total_freight_charge = total_freight_charge + line_currency_to_company_crr
                        else:
                            total_freight_charge = total_freight_charge + line_amount
                    else:
                        total_freight_charge = total_freight_charge + line_amount

                if line.charges_id.type_of_charges == 'destination':
                    if line_currency:
                        if line_currency.id != company_currency.id:
                            line_currency_to_company_crr = line_currency._convert(
                                line_amount, company_currency, self.env.company, fields.Date.today(), round=False)
                            total_destination_charge = total_destination_charge + line_currency_to_company_crr
                        else:
                            total_destination_charge = total_destination_charge + line_amount
                    else:
                        total_destination_charge = total_destination_charge + line_amount

                if line.charges_id.type_of_charges == 'origin':
                    if line_currency:
                        if line_currency.id != company_currency.id:
                            line_currency_to_company_crr = line_currency._convert(
                                line_amount, company_currency, self.env.company, fields.Date.today(), round=False)
                            total_origin_charge = total_origin_charge + line_currency_to_company_crr
                        else:
                            total_origin_charge = total_origin_charge + line_amount
                    else:
                        total_origin_charge = total_origin_charge + line_amount
            rec.total_freight_charge = total_freight_charge
            rec.total_destination_charge = total_destination_charge
            rec.total_origin_charge = total_origin_charge
            rec.total_charge = rec.total_freight_charge + rec.total_destination_charge + rec.total_origin_charge

    @api.depends('charges_line')
    def _get_final_amount_per_unit(self):
        self.total_prepaid_charges = 0.0
        self.total_collect_charges = 0.0
        po_total_prepaid_charges = po_total_collect_charges = 0.0
        so_total_prepaid_charges = so_total_collect_charges = 0.0
        for rate in self.charges_line:

            if self.sale_order_id:
                if rate.prepaid:
                    total_prepaid_charges_amt = rate.to_currency_id._convert(
                        rate.sale_final_amount, self.currency_id, self.env.company, fields.Date.today(), round=False)
                    so_total_prepaid_charges += total_prepaid_charges_amt
                if rate.collect:
                    total_collect_charges_amt = rate.to_currency_id._convert(
                        rate.sale_final_amount, self.currency_id, self.env.company, fields.Date.today(), round=False)
                    so_total_collect_charges += total_collect_charges_amt

            if self.purchase_order_id:
                if rate.prepaid:
                    total_prepaid_charges_amt = rate.to_currency_id._convert(
                        rate.final_amount, self.currency_id, self.env.company, fields.Date.today(), round=False)
                    po_total_prepaid_charges += total_prepaid_charges_amt
                if rate.collect:
                    total_collect_charges_amt = rate.to_currency_id._convert(
                        rate.final_amount, self.currency_id, self.env.company, fields.Date.today(), round=False)
                    po_total_collect_charges += total_collect_charges_amt

        if self.sale_order_id:
            self.total_prepaid_charges = so_total_prepaid_charges
            self.total_collect_charges = so_total_collect_charges
        if self.purchase_order_id:
            self.total_prepaid_charges = po_total_prepaid_charges
            self.total_collect_charges = po_total_collect_charges
        # if self.bol_id:
        #     self.total_prepaid_charges = 0.0
        #     self.total_collect_charges = 0.0
        # if self.job_id:
        #     self.total_prepaid_charges = 0.0
        #     self.total_collect_charges = 0.0
        # if self.invoice_line_ids:
        #     for line in self.invoice_line_ids:
        #         if self.total_prepaid_charges != 0.0:
        #             line.price_unit = self.total_prepaid_charges
        #             line.product_qty = self.no_of_expected_container
        #     self._amount_all()

    @api.depends('amount_total', 'billing_currency_id')
    def _get_tot_amt_in_billing_currency(self):
        for line in self:
            amt_total = line.amount_total
            if amt_total != 0.0:
                amount_in_rate_currency = line.currency_id._convert(
                    amt_total, line.billing_currency_id, line.env.company, fields.Date.today(),
                    round=False)
                line.billing_currency_tot = amount_in_rate_currency

    @api.depends('job_charge_line.currency_amount')
    def _compute_total_charge(self):
        for order in self:
            order.job_total_charge = 0.0
            order.bol_total_charge = 0.0
            amount_total = 0
            if order.bol_charge_line:
                for line in order.bol_charge_line:
                    curr = self.env['res.currency'].search([('name', '=', line.currency_code)])
                    if curr:
                        if curr != self.currency_id:
                            price = curr._convert(
                                line.currency_amount, self.currency_id, self.env.company, fields.Date.today(), round=False)
                            amount_total += price
                        else:
                            amount_total += line.currency_amount
                    else:
                        amount_total += line.currency_amount
                order.write({
                    'bol_total_charge': amount_total,
                })
            if order.job_charge_line:
                for line in order.job_charge_line:
                    curr = self.env['res.currency'].search([('name', '=', line.currency_code)])
                    if curr:
                        if curr != self.currency_id:
                            price = curr._convert(
                                line.currency_amount, self.currency_id, self.env.company, fields.Date.today(), round=False)
                            amount_total += price
                        else:
                            amount_total += line.currency_amount
                    else:
                        amount_total += line.currency_amount
                order.write({
                    'job_total_charge': amount_total,
                })

    sale_order_id = fields.Many2one('sale.order', string="Freight Sale Order")
    purchase_order_id = fields.Many2one('purchase.order', string="Freight Purchase Order")
    charges_line = fields.One2many('charges.line', 'invoice_order_id', string='Charges')
    total_freight_charge = fields.Float(compute='_get_total', string="Total Freight Charge")
    total_destination_charge = fields.Float(compute='_get_total', string="Total Destination Charge")
    total_origin_charge = fields.Float(compute='_get_total', string="Total Origin Charge")
    total_charge = fields.Float(compute='_get_total', string="Total Charge")
    billing_currency_tot = fields.Monetary(currency_field='billing_currency_id', store=True, readonly=True,
                                           compute='_get_tot_amt_in_billing_currency', string="Billing Currency Total"
                                           )
    billing_currency_id = fields.Many2one('res.currency', string='Billing Currency',
                                          default=lambda self: self.env.company.currency_id,
                                          help="The Invoice currency.")
    api_company_currency_rate = fields.Float('Api Company Currency Rate', digits='Freight')
    api_billing_currency_rate = fields.Float('Api Billing Currency Rate', digits='Freight')
    api_difference_rate = fields.Float('Api Difference Rate', digits='Freight')
    bol_id = fields.Many2one('bill.of.lading', string="BOL")
    job_id = fields.Many2one('job', string="Job")
    is_job_invoice = fields.Boolean(string="Is Job Invoice Bill of Lading")
    is_bol_invoice = fields.Boolean(string="Is BOL Invoice")
    is_master_bill_of_lading = fields.Boolean(string="Is Master Bill of Lading")
    is_house_bill_of_lading = fields.Boolean(string="Is House Bill of Lading")
    total_prepaid_charges = fields.Float(compute='_get_final_amount_per_unit',
                                         string="Sum of Prepaid", digits='Freight')
    total_collect_charges = fields.Float(compute='_get_final_amount_per_unit',
                                         string="Sum of Collect", digits='Freight')
    job_charge_line = fields.One2many('charges.line.items', 'job_account_charge_line_id', string="Job Charges")
    bol_charge_line = fields.One2many('charges.line.items', 'bol_account_charge_line_id', string="Job Charges")
    job_total_charge = fields.Float(compute='_compute_total_charge', string="JOB Total")
    bol_total_charge = fields.Float(compute='_compute_total_charge', string="BOL Total")
    place_of_origin = fields.Text("Point of Origin")
    place_of_destination = fields.Text("Point of Destination")
    booking_id = fields.Text("Booking ID")
    vessel_name = fields.Text("Vessel Name")
    voyage = fields.Text("Voyage")
    rotation = fields.Text("Rotation")
    imo_no = fields.Text("IMO No.")
    is_send_mail = fields.Boolean(string="Is Send Mail")


    def action_post(self):
        res = super(AccountMove,self).action_post()
        self.is_send_mail = False

    def send_auto_mail_cron(self):
        print("..........................")
        send_mail_rec = self.env['ir.config_parameter'].sudo().get_param('freightbox.send_mail') or False
        print("...................send_mail_rec",send_mail_rec)
        if send_mail_rec:
            print("...................send_mail_rec",send_mail_rec)
            acc_rec = self.env['account.move'].search([('move_type','=','out_invoice')])
            for i in acc_rec:
                if not i.is_send_mail:
                    template_id = self.env.ref('account.email_template_edi_invoice')
                    template_id.send_mail(i.id, force_send=True)
                    i.is_send_mail = True
                    

    @api.onchange('sale_order_id', 'purchase_order_id')
    def _onchange_sale_purchase_id(self):
        if self.sale_order_id:
            self.partner_id = self.sale_order_id.partner_id.id
            self.charges_line = self.sale_order_id.charges_line.ids
        if self.purchase_order_id:
            self.partner_id = self.purchase_order_id.partner_id.id
            self.charges_line = self.purchase_order_id.charges_line.ids

    def action_api_rate_wiz(self):
        self.ensure_one()
        ctx = dict(
            default_currency_id=self.currency_id.id,
            default_current_id=self.id,
            default_billing_currency_id=self.billing_currency_id.id,
            default_api_company_currency_rate=self.currency_id.rate,
            default_api_billing_currency_rate=self.billing_currency_id.rate,
        )
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'apirate.wizard',
            'view_mode': 'form',
            'views': [(self.env.ref('freightbox.view_api_rate_wiz_form').id, "form")],
            'context': ctx,
            'target': 'new',
        }

    def write(self, vals):
        result = super(AccountMove, self).write(vals)

        all_bol_inv_ids = self.search(
            [('payment_state', '=', 'paid'), ('bol_id', '=', self.bol_id.id), ('is_bol_invoice', '=', True)])
        confirmed_bol_inv_id = self.bol_id.invoice_ids.ids
        if len(all_bol_inv_ids.ids) == len(confirmed_bol_inv_id):
            self.bol_id.write({'invoice_status': 'paid'})

        all_job_inv_ids = self.search(
            [('payment_state', '=', 'paid'), ('job_id', '=', self.job_id.id), ('is_job_invoice', '=', True)])
        confirmed_inv_id = self.job_id.invoice_ids.ids
        if len(all_job_inv_ids.ids) == len(confirmed_inv_id):
            self.job_id.write({'invoice_status': 'paid'})
        return result


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    is_charges = fields.Boolean(string='Charges', default=False)
