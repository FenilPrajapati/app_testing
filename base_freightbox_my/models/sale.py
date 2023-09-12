# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.tools.misc import get_lang
from datetime import date


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def name_get(self):
        for order in self:
            res = []
            name = order.name
            if order.shipment_quote_id and order.booking_id:
                name += '/' + order.booking_id
            if order._context.get('sale_show_partner_name'):
                if order.partner_id.name:
                    name = '%s - %s' % (name, order.partner_id.name)
            res.append((order.id, name))
            return res
        return super(SaleOrder, self).name_get()

    @api.depends('charges_line')
    def _get_total(self):
        for rec in self:
            total_freight_charge = 0.0
            total_destination_charge = 0.0
            total_origin_charge = 0.0
            for line in rec.charges_line:
                company_currency = rec.currency_id
                line_currency = line.to_currency_id
                if line.charges_id.type_of_charges == 'freight':
                    if line_currency:
                        if line_currency.id != company_currency.id:
                            line_currency_to_company_crr = line_currency._convert(
                                line.sale_final_amount, company_currency, self.env.company, fields.Date.today(),
                                round=False)
                            total_freight_charge = total_freight_charge + line_currency_to_company_crr
                        else:
                            total_freight_charge = total_freight_charge + line.sale_final_amount
                    else:
                        total_freight_charge = total_freight_charge + line.sale_final_amount

                if line.charges_id.type_of_charges == 'destination':
                    if line_currency:
                        if line_currency.id != company_currency.id:
                            line_currency_to_company_crr = line_currency._convert(
                                line.sale_final_amount, company_currency, self.env.company, fields.Date.today(),
                                round=False)
                            total_destination_charge = total_destination_charge + line_currency_to_company_crr
                        else:
                            total_destination_charge = total_destination_charge + line.sale_final_amount
                    else:
                        total_destination_charge = total_destination_charge + line.sale_final_amount

                if line.charges_id.type_of_charges == 'origin':
                    if line_currency:
                        if line_currency.id != company_currency.id:
                            line_currency_to_company_crr = line_currency._convert(
                                line.sale_final_amount, company_currency, self.env.company, fields.Date.today(),
                                round=False)
                            total_origin_charge = total_origin_charge + line_currency_to_company_crr
                        else:
                            total_origin_charge = total_origin_charge + line.sale_final_amount
                    else:
                        total_origin_charge = total_origin_charge + line.sale_final_amount

            rec.total_freight_charge = total_freight_charge
            rec.total_destination_charge = total_destination_charge
            rec.total_origin_charge = total_origin_charge
            rec.total_charge = rec.total_freight_charge + rec.total_destination_charge + rec.total_origin_charge

    @api.depends('charges_line')
    def _get_final_amount_per_unit(self):
        total_collect_charges = total_prepaid_charges = 0.0
        for rate in self.charges_line:
            if rate.prepaid:
                total_prepaid_charges_amt = rate.to_currency_id._convert(
                    rate.sale_final_amount, self.currency_id, self.env.company, fields.Date.today(),
                    round=False)
                total_prepaid_charges += total_prepaid_charges_amt
            if rate.collect:
                total_collect_charges_amt = rate.to_currency_id._convert(
                    rate.sale_final_amount, self.currency_id, self.env.company, fields.Date.today(),
                    round=False)
                total_collect_charges += total_collect_charges_amt
        self.total_prepaid_charges = total_prepaid_charges
        self.total_collect_charges = total_collect_charges

    @api.depends('po_id.order_line.invoice_lines.move_id')
    def _compute_bills(self):
        for order in self:
            bills = order.po_id.mapped('order_line.invoice_lines.move_id')
            order.bill_ids = bills
            order.bill_count = len(bills)

    cargo_name = fields.Char("Cargo Description")
    quantity = fields.Float("Quantity")
    shipment_terms = fields.Selection([
        ('lcl', 'LCL'),
        ('fcl', 'FCL'),
        ('both', 'LCL and FCL'),
        ('bb', 'BB')], "Shipment Terms")
    weight = fields.Float("Weight")
    volume = fields.Float("Volume")
    move_type = fields.Many2one('move.type', "Move Type")
    incoterm_id = fields.Many2one('account.incoterms', "Incoterms")
    place_of_origin = fields.Char("Point of Origin")
    final_port_of_destination = fields.Char("Point of Destination")
    point_of_stuffing = fields.Many2one('port', string='Point of Stuffing', tracking=True)
    point_of_destuffing = fields.Many2one('port', string='Point of Destuffing', tracking=True)
    no_of_expected_container = fields.Float("No. of Expected Container")
    po_id = fields.Many2one('purchase.order', string='Purchase Order')
    booking_id = fields.Char(string='Inquiry NO.')
    is_purchase_confirmed = fields.Boolean(string='Is Purchase Confirmed')
    expected_date_of_shipment = fields.Date("Expected Date of Shipment")
    valid_from = fields.Date("Valid From")
    valid_to = fields.Date("Valid To")
    remarks = fields.Char("Remarks")
    shipment_quote_id = fields.Many2one('shipment.quote', string='Shipment Quote', ondelete='cascade')
    job_id = fields.Many2one('job', "Job")
    charges_line = fields.One2many('charges.line', 'sale_order_id', string='Charges')
    total_freight_charge = fields.Float(compute='_get_total', string="Total Freight Charge", digits='Freight')
    total_destination_charge = fields.Float(compute='_get_total', string="Total Destination Charge", digits='Freight')
    total_origin_charge = fields.Float(compute='_get_total', string="Total Origin Charge", digits='Freight')
    total_charge = fields.Float(compute='_get_total', string="Total Charge", digits='Freight')
    invoice_id = fields.Many2one('account.move', string='Customer Invoice')
    vendor_bill_id = fields.Many2one('account.move', string='Vendor Bill')
    total_final_amount_per_unit = fields.Float(compute='_get_final_amount_per_unit',
                                               string="Sum of final Amount", digits='Freight')
    total_prepaid_charges = fields.Float(compute='_get_final_amount_per_unit',
                                         string="Sum of Prepaid charges", digits='Freight')
    total_collect_charges = fields.Float(compute='_get_final_amount_per_unit',
                                         string="Sum of Collect charges", digits='Freight')
    container_type = fields.Many2one('container.iso.code', "Container Type")
    so_inquiry_status = fields.Selection([
        ('po_confirm', 'PO confirmed'), ('under_correction', 'Under Correction'),
        ('correction_done', 'Correction Done')], "Inquiry Status")
    volume_uom = fields.Many2one('uom.uom', "Volume Unit")
    weight_uom = fields.Many2one('uom.uom', "Weight Unit")
    bill_count = fields.Integer(compute="_compute_bills", string='Bill Count')
    job_count = fields.Integer(compute="_get_job_count", string='Job Count')
    bill_ids = fields.Many2many('account.move', compute="_compute_bills", string='Bills')
    so_inquiry_id = fields.Many2one('crm.lead', string='Inquiry ID')
    is_freight_box_so = fields.Boolean('Is FB?')
    so_inquiry_status = fields.Selection([
        ('po_confirm', 'PO confirmed'), ('under_correction', 'Under Correction'),
        ('correction_done', 'Correction Done')], "Inquiry Status")
    volume_uom = fields.Many2one('uom.uom', "Volume Unit")
    weight_uom = fields.Many2one('uom.uom', "Weight Unit")

    prepaid_total_without_tax = fields.Float(compute='_get_final_amount_per_unit',
                                         string="Prepaid Sale", digits='Freight')
    prepaid_total_tax = fields.Float(compute='_get_final_amount_per_unit',
                                         string="Prepaid Tax - tax amt", digits='Freight')
    collect_total_without_tax = fields.Float(compute='_get_final_amount_per_unit',
                                             string="Collect Sale", digits='Freight')
    collect_total_tax = fields.Float(compute='_get_final_amount_per_unit',
                                     string="Collect Tax", digits='Freight')
    active = fields.Boolean(string='Active', default=True)
    booking_user_id = fields.Many2one('res.users', string="Shipper/FF")
    cargo_plus_ids = fields.Many2many("cargo.plus", "cargo_plus_sale_rel", "cargo_plus_id",
                                      "sale_id", string="Cargo Plus")

    @api.onchange('so_inquiry_id')
    def _onchange_so_inquiry_id(self):
        charge_list = []
        if not self.so_inquiry_id:
            return
        if self.so_inquiry_id:
            self.partner_id = self.so_inquiry_id.partner_id.id or False
            self.cargo_name = self.so_inquiry_id.cargo_name or ''
            self.quantity = self.so_inquiry_id.quantity
            self.shipment_terms = self.so_inquiry_id.shipment_terms
            self.weight = self.so_inquiry_id.weight
            self.weight_uom = self.so_inquiry_id.weight_uom
            self.volume = self.so_inquiry_id.volume
            self.volume_uom = self.so_inquiry_id.volume_uom
            self.incoterm_id = self.so_inquiry_id.incoterm_id.id
            self.place_of_origin = self.so_inquiry_id.place_of_origin
            self.point_of_destination = self.so_inquiry_id.final_port_of_destination


            self.no_of_expected_container = self.so_inquiry_id.no_of_expected_container
            self.container_type = self.so_inquiry_id.container_type.id
            self.expected_date_of_shipment = self.so_inquiry_id.expected_date_of_shipment
            self.remarks = self.so_inquiry_id.remarks
            # self.valid_from = self.so_inquiry_id.valid_from
            # self.po_id = self.so_inquiry_id.sq_id.
            self.booking_id = self.so_inquiry_id.booking_id
            # self.inquiry_id = self.so_inquiry_id.booking_id
            self.move_type = self.so_inquiry_id.move_type.id

            # for record in self.po_id.rfq_id.charges_line:
            #     charge_list.append((0, 0, {'charges_id': record.charges_id.id,
            #                                'units': record.units,
            #                                'unit_price': record.unit_price,
            #                                }))
            # self.charges_line = charge_list

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            if order.po_id:
                order.po_id.po_inquiry_status = 'shipment_quote_accepted'
            # order.partner_id.last_transaction_date = order.date_order
            # order.partner_id.is_manual_active = False
            # order.partner_id.is_cust_active = True
        return res

    def action_confirm_po(self):
        if self.po_id:
            self.po_id.state = 'purchase'
            self.po_id.po_inquiry_id = self.so_inquiry_id.id,
            self.is_purchase_confirmed = True
        self.write({'so_inquiry_status': 'po_confirm'})

    @api.onchange('shipment_quote_id')
    def _onchange_shipment_quote_id(self):
        if not self.shipment_quote_id:
            return
        if self.shipment_quote_id:
            self.partner_id = self.shipment_quote_id.partner_id.id or False
            self.cargo_name = self.shipment_quote_id.cargo_name or ''
            self.quantity = self.shipment_quote_id.quantity
            self.shipment_terms = self.shipment_quote_id.shipment_terms
            self.weight = self.shipment_quote_id.weight
            self.weight_uom = self.shipment_quote_id.weight_uom
            self.volume = self.shipment_quote_id.volume
            self.volume_uom = self.shipment_quote_id.volume_uom
            self.incoterm_id = self.shipment_quote_id.incoterm_id.id
            self.place_of_origin = self.shipment_quote_id.place_of_origin
            self.point_of_destination = self.shipment_quote_id.point_of_destination
            self.point_of_stuffing = self.shipment_quote_id.point_of_stuffing.id if self.shipment_quote_id and self.shipment_quote_id.point_of_stuffing else False
            self.point_of_destuffing = self.shipment_quote_id.point_of_destuffing.id if self.shipment_quote_id and self.shipment_quote_id.point_of_destuffing else False
            self.no_of_expected_container = self.shipment_quote_id.no_of_expected_container
            self.container_type = self.shipment_quote_id.container_type.id
            self.expected_date_of_shipment = self.shipment_quote_id.expected_date_of_shipment
            self.valid_from = self.shipment_quote_id.valid_from
            self.valid_to = self.shipment_quote_id.valid_to
            self.remarks = self.shipment_quote_id.remarks
            self.move_type = self.move_type.id
            self.charges_line = self.shipment_quote_id.charges_line.ids

    def action_cancel(self):
        cancel_warning = self._show_cancel_wizard()
        if cancel_warning:
            return {
                'name': _('Cancel Sales Order'),
                'view_mode': 'form',
                'res_model': 'sale.order.cancel',
                'view_id': self.env.ref('sale.sale_order_cancel_view_form').id,
                'type': 'ir.actions.act_window',
                'context': {'default_order_id': self.id},
                'target': 'new'
            }
        inv = self.invoice_ids.filtered(lambda inv: inv.state == 'draft')
        inv.button_cancel()
        shipment_quote_id = self.shipment_quote_id
        if shipment_quote_id:
            shipment_quote_id.write({'state': 'rejected'})
            shipment_quote_id.po_id.write({'state': 'cancel'})
            shipment_quote_id.po_id.rfq_id.write({'state': 'cancelled'})
        return self.write({'state': 'cancel'})


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_charges = fields.Boolean(string='Charges', default=False)
    today_exchange_rate = fields.Float("Exchange Rate", digits=(12, 3))
    exchange_from_to_currency = fields.Char("From/To Currency")

    @api.onchange('product_id')
    def product_id_change(self):
        if not self.product_id:
            return
        valid_values = self.product_id.product_tmpl_id.valid_product_template_attribute_line_ids.product_template_value_ids
        # remove the is_custom values that don't belong to this template
        for pacv in self.product_custom_attribute_value_ids:
            if pacv.custom_product_template_attribute_value_id not in valid_values:
                self.product_custom_attribute_value_ids -= pacv

        # remove the no_variant attributes that don't belong to this template
        for ptav in self.product_no_variant_attribute_value_ids:
            if ptav._origin not in valid_values:
                self.product_no_variant_attribute_value_ids -= ptav

        vals = {}
        if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
            vals['product_uom'] = self.product_id.uom_id
            vals['product_uom_qty'] = self.product_uom_qty or 1.0

        product = self.product_id.with_context(
            lang=get_lang(self.env, self.order_id.partner_id.lang).code,
            partner=self.order_id.partner_id,
            quantity=vals.get('product_uom_qty') or self.product_uom_qty,
            date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id
        )

        vals.update(name=self.get_sale_order_line_multiline_description_sale(product))

        if not self.product_id.is_freight_container == True:
            self._compute_tax_id()

        if self.order_id.pricelist_id and self.order_id.partner_id:
            vals['price_unit'] = self.env['account.tax']._fix_tax_included_price_company(
                self._get_display_price(product), product.taxes_id, self.tax_id, self.company_id)
        self.update(vals)

        title = False
        message = False
        result = {}
        warning = {}
        if product.sale_line_warn != 'no-message':
            title = _("Warning for %s", product.name)
            message = product.sale_line_warn_msg
            warning['title'] = title
            warning['message'] = message
            result = {'warning': warning}
            if product.sale_line_warn == 'block':
                self.product_id = False
        return result
