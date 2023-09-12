from odoo import models, fields, _, api
from odoo.exceptions import UserError, ValidationError


class RequestForQuote(models.Model):
    _name = 'request.for.quote'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Request For Quote"
    _rec_name = 'booking_id'
    _order = 'total_charge asc'

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

    name = fields.Char("Rate Comparison")
    shipping_name_id = fields.Many2one('res.partner', string='Shipping Line', domain="[('supplier_rank', '>', 0)]")
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
    expected_date_of_shipment = fields.Date("Expected Date of Shipment")
    remarks = fields.Char("Remarks")
    # invoice_id = fields.Many2one('account.move', string='Customer Invoice')
    # vendor_bill_id = fields.Many2one('account.move', string='Vendor Bill')
    container_type = fields.Many2one('container.iso.code', "Container Type")
    booking_container_type = fields.Many2one('shipping.container', "Container Type", related='booking_id.container_type')
    volume_uom = fields.Many2one('uom.uom', "Volume Unit")
    weight_uom = fields.Many2one('uom.uom', "Weight Unit")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
        ('expired', 'Expired'),
        ('under_correction', 'Under Correction'),
        ('correction_done', 'Correction Done'),
    ], string='Status', index=True, readonly=True, copy=False, default='draft', tracking=True)

    booking_id = fields.Many2one('crm.lead', string='Inquiry NO.', tracking=True)
    total_freight_charge = fields.Float(compute='_get_total', string="Total Freight Charge", digits='Freight',
                                        tracking=True)
    total_destination_charge = fields.Float(compute='_get_total', string="Total Destination Charge", digits='Freight',
                                            tracking=True)
    total_origin_charge = fields.Float(compute='_get_total', string="Total Origin Charge", digits='Freight',
                                       tracking=True)
    total_charge = fields.Float(compute='_get_total', string="Total Charge", digits='Freight', tracking=True,store=True)
    # charges_template_ids = fields.Many2many('charges.templates', 'rfq_rel', 'charges_templates_id', 'rfq_id',
    #                                         string='Charges Template', tracking=True)
    charges_line = fields.One2many('charges.line', 'rfq_id', string='Charges', tracking=True)
    job_id = fields.Many2one('job', "Job", tracking=True)
    valid_from = fields.Date("Valid From", tracking=True, default=fields.Date.today())
    valid_to = fields.Date("Valid To", tracking=True)
    # charge_load_bool = fields.Boolean("Charge Load Bool")
    # is_loaded_for_rfq = fields.Boolean("Is Loaded for RFQ")
    is_shipment_quote_created = fields.Boolean("Is Shipment Quote Created")
    currency_id = fields.Many2one('res.currency',
                                  string='Currency', default=lambda self: self.env.company.currency_id, readonly=True)
    create_date = fields.Datetime(string='Creation Date', readonly=True,
                                  help="Date on which Rate comparison is created.")
    company_id = fields.Many2one('res.company', 'Company', required=True, default=lambda self: self.env.company)
    reject_reason = fields.Text('Reject Reason', tracking=True)
    comment = fields.Text("Comment")
    reject_bool = fields.Boolean(string='Reject Bool')
    # correct_reason = fields.Text('Reason For Correction', tracking=True)
    # correct_reason_bool = fields.Boolean(string='Correction Bool')
    is_po_created = fields.Boolean(string='PO created')
    # amend_reason = fields.Text("Reason For Amendment", tracking=True)
    # amend_bool = fields.Boolean(string='Amend Bool')
    total_prepaid_charges = fields.Float(compute='_get_final_amount_per_unit',
                                         string="Prepaid Amt", digits='Freight')
    total_collect_charges = fields.Float(compute='_get_final_amount_per_unit',
                                         string="Collect Amt", digits='Freight')
    active = fields.Boolean(string='Active', default=True)
    booking_user_id = fields.Many2one('res.users', string="Shipper/FF")
    delivery_type_id = fields.Many2one('service.type', string="Delivery Type", tracking=True)
    cargo_plus_ids = fields.Many2many("cargo.plus", "cargo_plus_rc_rel", "cargo_plus_id", "rc_id",
                                      string="Cargo Plus")

    @api.depends('charges_line')
    def _get_final_amount_per_unit(self):
        total_collect_charges = total_prepaid_charges = 0.0
        for rate in self.charges_line:
            if rate.prepaid:
                total_prepaid_charges += rate.company_currency_total
            if rate.collect:
                total_collect_charges += rate.company_currency_total
        self.total_prepaid_charges = total_prepaid_charges
        self.total_collect_charges = total_collect_charges

    # def action_get_po(self):
    #     view_id = self.env.ref('shipmybox.purchase_order_tree_view_freightbox').id
    #     view_form_id = self.env.ref('shipmybox.purchase_order_form').id
    #     itemIds = self.env['purchase.order'].search([('rfq_id', '=', self.id)])
    #     itemIds = itemIds.ids
    #     return {
    #         'name': "Purchase Order",
    #         'type': 'ir.actions.act_window',
    #         'view_type': 'form',
    #         'view_mode': 'tree,form',
    #         'res_model': 'purchase.order',
    #         'views': [(view_id, 'list'), (view_form_id, 'form')],
    #         'domain': [('id', 'in', itemIds)],
    #         'target': 'current',
    #     }

    def button_approve(self):
        if not self.charges_line:
            raise UserError(_('Please select Charges'))
        if self.charges_line:
            for ch in self.charges_line:
                if ch.unit_price <= 0:
                    raise UserError(
                    _('Unit Price cannot be less than or equal to Zero for %s') % ch.charges_id.name)
        self.state = 'approved'
        stage_id = self.env['crm.stage'].search([('name', 'ilike', 'Qualified')], limit=1)
        if stage_id:
            self.booking_id.write({'stage_id': stage_id.id})
        return True

    def button_cancel(self):
        self.write({'state': 'cancelled'})

    def button_set_to_draft(self):
        self.write({'state': 'draft'})

    def validity_of_rate(self):
        today = fields.Date.today()
        rfq_id = self.search([('valid_to', '<', today)])
        for rec in rfq_id:
            rec.write({'state': 'expired'})

    @api.onchange('booking_id')
    def _onchange_booking_id(self):
        if not self.booking_id:
            return
        if self.booking_id:
            self.cargo_name = self.booking_id.cargo_name or ''
            self.quantity = self.booking_id.quantity
            self.shipment_terms = self.booking_id.shipment_terms
            self.weight = self.booking_id.weight
            self.weight_uom = self.booking_id.weight_uom
            self.volume = self.booking_id.volume
            self.volume_uom = self.booking_id.volume_uom
            self.incoterm_id = self.booking_id.incoterm_id.id
            self.place_of_origin = self.booking_id.place_of_origin
            self.final_port_of_destination = self.booking_id.final_port_of_destination
            self.point_of_stuffing= self.point_of_stuffing.id if self.point_of_stuffing else False
            self.point_of_destuffing= self.point_of_destuffing.id if self.point_of_destuffing else False
            self.no_of_expected_container = self.booking_id.no_of_expected_container
            self.container_type = self.booking_id.container_type.id
            self.expected_date_of_shipment = self.booking_id.expected_date_of_shipment
            self.remarks = self.booking_id.remarks
            self.move_type = self.booking_id.move_type.id

    @api.constrains('valid_from', 'valid_to')
    def _check_valid_from_to(self):
        for rec in self:
            today = fields.Date.today()
            if rec.valid_from > rec.valid_to:
                raise ValidationError(_("Valid From cannot be greater than Valid To"))
            if rec.valid_to<today:
                raise ValidationError(_("Valid To, cannot be a Past Date"))
            if rec.valid_from<today:
                raise ValidationError(_("Valid From, cannot be a Past Date"))
