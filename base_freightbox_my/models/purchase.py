# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError
from odoo.tools.misc import formatLang, get_lang


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    # @api.depends('name', 'partner_ref', 'rfq_id')
    # def name_get(self):
    #     result = []
    #     for po in self:
    #         name = po.name
    #         if po.partner_ref:
    #             name += ' (' + po.partner_ref + ')'
    #         if po.rfq_id and po.booking_id:
    #             name += '/' + po.booking_id
    #         if self.env.context.get('show_total_amount') and po.amount_total:
    #             name += ': ' + formatLang(self.env, po.amount_total, currency_obj=po.currency_id)
    #         result.append((po.id, name))
    #     return result

    @api.depends('charges_line')
    def _get_total(self):
        for rec in self:
            total_freight_charge = 0.0
            total_destination_charge = 0.0
            total_origin_charge = 0.0
            for line in rec.charges_line:
                if line.charges_type == 'freight':
                    total_freight_charge += line.company_currency_total
                if line.charges_type == 'destination':
                    total_destination_charge += line.company_currency_total
                if line.charges_type == 'origin':
                    total_origin_charge += line.company_currency_total
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
                    rate.final_amount, self.currency_id, self.env.company, fields.Date.today(), round=False)
                total_prepaid_charges += total_prepaid_charges_amt
            if rate.collect:
                total_collect_charges_amt = rate.to_currency_id._convert(
                    rate.final_amount, self.currency_id, self.env.company, fields.Date.today(), round=False)
                total_collect_charges += total_collect_charges_amt
        self.total_prepaid_charges = total_prepaid_charges
        self.total_collect_charges = total_collect_charges

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
    rfq_id = fields.Many2one('request.for.quote', string='Rate Comparision', ondelete='cascade')
    po_inquiry_status = fields.Selection([
        ('shipment_quote_created', "Shipment Quote Created"),
        ('shipment_quote_accepted', "Shipment Quote Accepted"),
        ('under_correction', 'Under Correction'),
        ('correction_done', 'Correction Done')], "PO Status")
    party_name_id = fields.Many2one('res.partner', string="Party Name")
    tax_reference_1 = fields.Text(string="Tax Reference 1")
    street = fields.Text(string="Street")
    street_number = fields.Text(string="Street Number")
    floor = fields.Text(string="Floor")
    post_code = fields.Text(string="Post Code")
    city = fields.Text(string="City")
    state_region = fields.Text(string="State Region")
    country = fields.Text(string="Country")

    booking_id = fields.Char(string='Enquiry NO.')
    expected_date_of_shipment = fields.Date("Expected Date of Shipment")
    remarks = fields.Char("Remarks")
    job_id = fields.Many2one('job', "Job")
    charges_line = fields.One2many('charges.line', 'purchase_order_id', string='Charges')
    is_rate_camparison = fields.Boolean("Is Rate Camparison")
    valid_from = fields.Date("Valid From")
    valid_to = fields.Date("Valid To")
    total_freight_charge = fields.Float(compute='_get_total', string="Total Freight Charge", digits='Freight')
    total_destination_charge = fields.Float(compute='_get_total', string="Total Destination Charge", digits='Freight')
    total_origin_charge = fields.Float(compute='_get_total', string="Total Origin Charge", digits='Freight')
    total_charge = fields.Float(compute='_get_total', string="Total Charge", digits='Freight')
    invoice_id = fields.Many2one('account.move', string='Customer Invoice')
    vendor_bill_id = fields.Many2one('account.move', string='Vendor Bill')
    # correct_reason = fields.Text('Reason For Correction', tracking=True)
    # correct_reason_bool = fields.Boolean(string='Correct Bool')
    total_prepaid_charges = fields.Float(compute='_get_final_amount_per_unit',
                                         string="Prepaid Amt", digits='Freight')
    total_collect_charges = fields.Float(compute='_get_final_amount_per_unit',
                                         string="Collect Amt", digits='Freight')
    container_type = fields.Many2one('container.iso.code', "Container Type")
    volume_uom = fields.Many2one('uom.uom', "Volume Unit")
    weight_uom = fields.Many2one('uom.uom', "Weight Unit")
    # sq_count = fields.Integer(string='SQ Count', compute='_get_sq_count', readonly=True)
    is_freight_box_po = fields.Boolean('Is FB?')
    po_inquiry_id = fields.Many2one('crm.lead', string='Inquiry ID')
    active = fields.Boolean(string='Active', default=True)
    booking_user_id = fields.Many2one('res.users', string="Shipper/FF")
    # delivery_type_id = fields.Many2one('service.type', string="Delivery Type", tracking=True)
    cargo_plus_ids = fields.Many2many("cargo.plus", "container_line_purchase_rel", "container_line_id",
                                      "purchase_id", string="Cargo Plus")

    @api.onchange('rfq_id')
    def _onchange_rfq_id(self):
        if not self.rfq_id:
            return
        if self.rfq_id:
            self.partner_id = self.rfq_id.shipping_name_id.id or False
            self.cargo_name = self.rfq_id.cargo_name or ''
            self.quantity = self.rfq_id.quantity
            self.shipment_terms = self.rfq_id.shipment_terms
            self.weight = self.rfq_id.weight
            self.weight_uom = self.rfq_id.weight_uom
            self.volume = self.rfq_id.volume
            self.volume_uom = self.rfq_id.volume_uom
            self.incoterm_id = self.rfq_id.incoterm_id.id
            self.place_of_origin = self.rfq_id.place_of_origin
            self.final_port_of_destination = self.rfq_id.final_port_of_destination
            self.point_of_stuffing = self.rfq_id.point_of_stuffing.id if self.point_of_stuffing else False
            self.point_of_destuffing = self.rfq_id.point_of_destuffing.id if self.point_of_destuffing else False
            self.no_of_expected_container = self.rfq_id.no_of_expected_container
            self.container_type = self.rfq_id.container_type.id
            self.expected_date_of_shipment = self.rfq_id.expected_date_of_shipment
            self.valid_from = self.rfq_id.valid_from
            self.valid_to = self.rfq_id.valid_to
            self.remarks = self.rfq_id.remarks
            self.move_type = self.rfq_id.move_type.id
            self.charges_line = self.rfq_id.charges_line.ids

    def button_cancel(self):
        for order in self:
            for inv in order.invoice_ids:
                if inv and inv.state not in ('cancel', 'draft'):
                    raise UserError(
                        _("Unable to cancel this purchase order. You must first cancel the related vendor bills."))
        if self.rfq_id:
            self.rfq_id.write({'state': 'cancelled', 'is_po_created': False})
        self.write({'state': 'cancel'})


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    is_charges = fields.Boolean(string='Charges', default=False)
    today_exchange_rate = fields.Float("Exchange Rate", digits=(12, 3))
    exchange_from_to_currency = fields.Char("From/To Currency")

    def _product_id_change(self):
        if not self.product_id:
            return

        self.product_uom = self.product_id.uom_po_id or self.product_id.uom_id
        product_lang = self.product_id.with_context(
            lang=get_lang(self.env, self.partner_id.lang).code,
            partner_id=self.partner_id.id,
            company_id=self.company_id.id,
        )
        self.name = self._get_product_purchase_description(product_lang)

        # added below condition - not to calculate tax if is_freight_container = true for product
        if not self.product_id.is_freight_container == True:
            self._compute_tax_id()
