from odoo import models, fields, _, api
from odoo.exceptions import ValidationError, UserError
from lxml import etree
from datetime import date
import requests
import json


class Job(models.Model):
    _name = 'job'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Job"
    _rec_name = 'job_no'
    _order = 'id desc'

    @api.depends('charge_line.calculation_basis')
    def _compute_total_charge(self):
        for order in self:
            amount_total = 0
            for line in order.charge_line:
                amount_total += line.currency_amount
            order.write({
                'total_charge': amount_total,
            })

    booking_id = fields.Many2one('sale.order', string="Enquiry No", tracking=True)
    job_no = fields.Char("Job No.", required=True, copy=False, tracking=True, readonly=True, index=True,
                         default=lambda self: _('New'))
    job_date = fields.Date("Job Date", required=True, readonly="1", tracking=True, default=fields.Date.today())
    job_state_for_hold = fields.Selection([
        ('draft', 'Draft'),
        ('si_created', 'SI Created'),
        ('si_accepted', 'All SI accepted'),
        ('draft_bol', 'Draft M BoL created'),
        ('update_bol', 'Update on M BoL'),
        ('bol_received', 'M BoL Issued'),
        ('hold', 'On hold'),
        ('cargo_released', 'Cargo Released'),
        ('container', 'Container Returned'),
        ('inactive', 'Inactive'),
        # ('invoiced', 'Invoiced'),
        ('done', 'Done')
    ], string='Job Status', default='draft')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('si_created', 'SI Created'),
        ('si_accepted', 'All SI accepted'),
        ('draft_bol', 'Draft M BoL created'),
        ('update_bol', 'Update on M BoL'),
        ('bol_received', 'M BoL Issued'),
        ('hold', 'On hold'),
        ('cargo_released', 'Cargo Released'),
        ('container', 'Container Returned'),
        ('inactive', 'Inactive'),
        # ('invoiced', 'Invoiced'),
        ('done', 'Done')
    ], string='Status', index=True, readonly=True, copy=False, default='draft', tracking=True)
    carrier_booking = fields.Char("Carrier Booking", tracking=True)
    carrrier_date = fields.Date("Carrier Date", tracking=True)
    carrrier_id = fields.Char("Carrier Id", tracking=True)
    # svc_cont = fields.Char("Service Contract", tracking=True)
    # service_type_origin = fields.Many2one('service.type', string="Service Type Origin", tracking=True)
    # service_type_dest = fields.Many2one('service.type', string="Service Type Destination", tracking=True)
    shipment_terms_origin = fields.Selection([
        ('lcl', 'LCL'),
        ('fcl', 'FCL'),
        ('both', 'LCL and FCL'),
        ('bb', 'BB')], "Shipment Terms Origin", tracking=True)
    shipment_terms_dest = fields.Selection([
        ('lcl', 'LCL'),
        ('fcl', 'FCL'),
        ('both', 'LCL and FCL'),
        ('bb', 'BB')], "Shipment Terms Destination", tracking=True)
    # commodity_hs_code = fields.Char("Commodity HS Code")
    commodity_description = fields.Char("Commodity Description", tracking=True)
    cargo_gross_weight = fields.Float("Cargo Gross Weight", tracking=True)
    cargo_uom_id = fields.Many2one('uom.uom', "Gross Unit", tracking=True)
    shipment_id = fields.Char("Shipment Id", tracking=True)
    requested_equipment_type = fields.Many2one("container.iso.code", "Requested Container Type", tracking=True)
    requested_equip_unit_id = fields.Many2one('uom.uom', "Requested Equipment Unit", tracking=True)
    confirmed_equipment_type = fields.Many2one("container.iso.code", "Confirmed Container Type", tracking=True)
    confirmed_equip_unit_id = fields.Many2one('uom.uom', "Confirmed Equipment Unit")
    requested_date_time = fields.Datetime("Requested Date Time", tracking=True)
    actual_date_time = fields.Datetime("Actual Date Time", tracking=True)
    reference_id = fields.Char("Reference Id", tracking=True)
    reference_type = fields.Char("Reference Type", tracking=True)
    place_of_origin = fields.Char("Point of Origin", tracking=True)
    final_port_of_destination = fields.Char("Point of Destination", tracking=True)
    shipping_description = fields.Text("Shipping Description", tracking=True)
    so_id = fields.Many2one("sale.order", string="Sale order", tracking=True, ondelete='cascade')
    po_id = fields.Many2one("purchase.order", string="Purchase order", tracking=True)
    shipper_id = fields.Many2one("res.partner", string="Shipper", tracking=True)
    shipping_instruction_ids = fields.Many2many('shipping.instruction', string="Shipping Instruction", tracking=True)
    transport_ids = fields.Many2many('transport', string="Transport", tracking=True)
    confirmed_transport_ids = fields.Many2many('transport', 'job_rel', 'job_id', 'transport_id',
                                               string="Confirmed Transport", tracking=True)
    # transport_count = fields.Integer(compute='_compute_transport', string="Transport Count")
    # stop_transport_creation = fields.Boolean(compute='_compute_transport',
    #                                          string="Stop Transport Creation", tracking=True)
    exp_no_of_container = fields.Float('Expected No of Container', tracking=True)
    confirmed_no_of_container = fields.Float('Confirmed No of Container', tracking=True)
    inquiry_id = fields.Many2one('crm.lead', string="Inquiry ID", readonly=True, tracking=True)
    vessel_name = fields.Char("Vessel Name", tracking=True)
    voyage = fields.Char("Voyage", tracking=True)
    rotation = fields.Char("Rotation", tracking=True)
    imo_no = fields.Char("IMO No.", tracking=True)
    user_id = fields.Many2one("res.users", string="User", tracking=True)
    invoice_ids = fields.Many2many("account.move", string='Invoices', tracking=True)
    # si_count = fields.Integer(string='SI Count', compute='_get_si_count', readonly=True)
    # trans_count = fields.Integer(string='Total Transport Count', compute='_get_trans_count', readonly=True)
    # mbol_count = fields.Integer(string='Master BOL Count', compute='_get_mbol_count', readonly=True)
    # hbol_count = fields.Integer(string='House BOL Count', compute='_get_hbol_count', readonly=True)
    # invoice_count = fields.Integer(string='Job Invoice Count', compute='_get_job_invoice_count', readonly=True)
    # mb_invoice_count = fields.Integer(string='Master B/L Invoice Count', compute='_get_mbl_invoice_count', readonly=True)
    # hb_invoice_count = fields.Integer(string='House B/L Invoice Count', compute='_get_hbl_invoice_count', readonly=True)
    # charge_line = fields.One2many('charges.line.items', 'charge_job_line_id', string="Charges", tracking=True)
    # total_charge = fields.Float(compute='_compute_total_charge', string="Total Charge", tracking=True)
    # tnt_count = fields.Integer(string='TNT Count', compute='_get_tnt_count', readonly=True, tracking=True)
    is_cont_released = fields.Boolean("Is Container Released", tracking=True)
    # is_multi_modal = fields.Boolean("Is Transhipment?", tracking=True)
    # vessel_name1 = fields.Char("Vessel Name", tracking=True)
    # voyage1 = fields.Char("Voyage", tracking=True)
    # rotation1 = fields.Char("Rotation", tracking=True)
    # imo_no1 = fields.Char("IMO No.", tracking=True)
    # intermediate_pol_id = fields.Many2one("port", string="Intermediate port of loading", tracking=True)
    # second_vessel_mode = fields.Many2one('mode', string='Mode of transport from Port', tracking=True)
    # is_another_ship_needed = fields.Boolean("Is another ship needed?", tracking=True)
    # vessel_name2 = fields.Char("Vessel Name", tracking=True)
    # voyage2 = fields.Char("Voyage", tracking=True)
    # rotation2 = fields.Char("Rotation", tracking=True)
    # imo_no2 = fields.Char("IMO No.", tracking=True)
    # second_intermediate_pol_id = fields.Many2one("port", string="Second Intermediate port of loading", tracking=True)
    # third_vessel_mode = fields.Many2one('mode', string='Mode of transport from Port', tracking=True)
    is_house_bol_needed = fields.Boolean(string="Is House BOL needed")
    active = fields.Boolean(string='Active', default=True)
    booking_user_id = fields.Many2one('res.users', string="Shipper/FF")
    hold_reason = fields.Text('Hold Reason', tracking=True)
    hold_bool = fields.Boolean(string='Hold Bool')
    # load_free_days = fields.Integer(string='Loading Free days', tracking=True)
    # discharge_free_days = fields.Integer(string='Discharge Free days', tracking=True)
    # detention = fields.Integer(string='Detention during load & discharge', tracking=True)
    # lay_time = fields.Integer(string='Lay Time', tracking=True)
    port_of_origin_id = fields.Many2one('port', string='Port of Origin', tracking=True, required=True, domain=[('one', '=', True)])
    final_port_of_destination_id = fields.Many2one('port', string='Final Point of Destination', help="Final Port of Destination", tracking=True, required=True, domain=[('one', '=', True)])
    # vessel_location_track_count = fields.Integer(string='Vessel Location Track Count', compute='_get_vessel_location_track_count', readonly=True, tracking=True)
    # status = fields.Selection([('on_time', 'On Time'),
    #                            ('late', 'Late')],
    #                           'Status', default='on_time', required=1,
    #                           compute='_get_job_status')
    # allow_import_way_points = fields.Boolean("Allow Import Waypoints", default=True)
    # allow_import_vessel_location = fields.Boolean("Allow Import Waypoints", default=False)
    # route_waypoints = fields.Text('Waypoints')
    # vessel_location_api_datetime = fields.Datetime('Last API Called At')
    # vessel_location_api_parameters = fields.Text('API Parameters')
    # vessel_location_api_response = fields.Text('API Response')
    company_id = fields.Many2one('res.company', 'Company', required=True,
                                 default=lambda self: self.env.company.id)
    cargo_plus_ids = fields.Many2many("cargo.plus", string="Cargo Plus")
    # is_send_mail = fields.Boolean(string="Send Mail")
    # is_cargo_send_mail = fields.Boolean(string="Send Mail")
    # agents_line = fields.One2many('res.partner', 'agent_type_id', string='Agents Lines')

    # def _get_job_status(self):
    #     for record in self:
    #         record.status = 'on_time'
            # track_records = tnt_counts = self.env['track.trace.event'].search([('carrier_booking', '=', record.carrier_booking)])
            # hold_jobs = track_records.mapped('transport_event_line').filtered(lambda transport_event_line: transport_event_line.delay_reason and len(transport_event_line.delay_reason.strip()) > 0)
            # if hold_jobs:
            #     record.status = 'late'

    invoice_status = fields.Selection([
        ('paid', 'Fully Invoiced (paid)'),
        ('partial', 'Partially Invoiced'),
        ('to invoice', 'To Invoice'),
        ('no', 'Nothing to Invoice')
    ], string='Invoice Status', default='no')

    def button_release(self):
        # self.job_status = self.state
        self.write({'state': self.job_state_for_hold})

    def button_inactive(self):
        self.write({'state': 'inactive'})

    def button_settodraft(self):
        self.write({'state': 'draft'})

    def button_close_job(self):
        so_invoice_paid = all(inv.payment_state == 'paid' for inv in self.so_id.invoice_ids) if self.so_id else False
        po_invoice_paid = all(inv.payment_state == 'paid' for inv in self.po_id.invoice_ids) if self.po_id else False

        if self.po_id and not po_invoice_paid:
            raise ValidationError('PO invoice is not fully paid')
        if self.so_id and not so_invoice_paid:
            raise ValidationError('SO invoice is not fully paid')
        if self.is_house_bol_needed:
            house_bol = self.env['bill.of.lading'].search(
                [('job_id', '=', self.id), ('is_house_bill_of_lading', '=', True)])
            if house_bol:
                if house_bol.state != 'done':
                    raise ValidationError('House BOL is not in Done State')
                if house_bol.invoice_status != 'paid':
                    raise ValidationError('House BOL invoice is not fully paid')

        self.write({'state': 'done'})

    def button_container(self):
        self.write({'state': 'container'})

    @api.onchange('booking_id')
    def _onchange_booking_id(self):
        inquiry_id = False
        if not self.booking_id:
            self.inquiry_id = False
            self.so_id = False
            self.po_id = False
            self.shipper_id = False
            self.exp_no_of_container = 0.00
            self.confirmed_no_of_container = 0.00
            self.requested_equipment_type = False
            self.confirmed_equipment_type = False
            self.commodity_description = ''
            self.cargo_gross_weight = 0.00
            self.cargo_uom_id = False
            self.place_of_origin = ''
            self.final_port_of_destination = ''
        if self.booking_id:
            inquiry_id = self.booking_id.po_id.rfq_id.booking_id.id
            self.inquiry_id = inquiry_id
            self.so_id = self.booking_id.id
            self.po_id = self.booking_id.po_id.id
            self.shipper_id = self.booking_id.partner_id.id
            self.exp_no_of_container = self.booking_id.po_id.rfq_id.booking_id.no_of_expected_container
            self.confirmed_no_of_container = self.booking_id.no_of_expected_container
            self.requested_equipment_type = self.so_id.container_type.id
            self.confirmed_equipment_type = self.so_id.container_type.id
            self.commodity_description = self.booking_id.cargo_name
            self.cargo_gross_weight = self.booking_id.weight
            self.cargo_uom_id = self.booking_id.weight_uom.id
            self.place_of_origin = self.booking_id.place_of_origin
            self.final_port_of_destination = self.booking_id.final_port_of_destination

    @api.model
    def create(self, vals):
        if vals.get('job_no', _('New')) == _('New'):
            sequence = self.env['ir.sequence'].next_by_code('job.seq') or _('New')
            vals['job_no'] = sequence
        result = super(Job, self).create(vals)
        if result.inquiry_id:
            self.inquiry_id.job_id = result.id
        if result.so_id:
            result.so_id.job_id = result.id
            result.so_id.shipment_quote_id.job_id = result.id
            result.po_id.job_id = result.id
            result.po_id.rfq_id.job_id = result.id
            result.po_id.rfq_id.booking_id.job_id = result.id
        return result