from odoo import models, fields, _, api
from odoo.exceptions import ValidationError,UserError
from lxml import etree


class BillOfLading(models.Model):
    _name = 'bill.of.lading'
    _inherit = ['shipping.instruction', 'mail.thread', 'mail.activity.mixin']
    _description = "Bill of lading"
    _rec_name = 'transport_document_reference'

    def button_approve(self):
        if self.is_master_bill_of_lading:
            self.job_id.sudo().write({'state': 'bol_received'})
        if not self.bol_cargo_line:
            raise ValidationError('Please Add Cargo Items')
        elif not self.bol_tq_line:
            raise ValidationError('Please Add Transport equipment Items')
        elif not self.bol_dp_line:
            raise ValidationError('Please Add Document Parties Items')
        elif not self.bol_sl_line:
            raise ValidationError('Please Add Shipment Location Items')
        elif not self.bol_ref_line:
            raise ValidationError('Please Add References Items')
        else:
            self.write({'state': 'approve'})

    def button_settodraft(self):
        self.write({'state': 'draft'})

    def button_update(self):
        if self.is_master_bill_of_lading == True:
            self.job_id.write({'state': 'update_bol'})
        if not self.bol_cargo_line:
            raise ValidationError('Please Add Cargo Items')
        elif not self.bol_tq_line:
            raise ValidationError('Please Add Transport equipment Items')
        elif not self.bol_dp_line:
            raise ValidationError('Please Add Document Parties Items')
        elif not self.bol_sl_line:
            raise ValidationError('Please Add Shipment Location Items')
        elif not self.bol_ref_line:
            raise ValidationError('Please Add References Items')
        else:
            self.write({'state': 'update'})

    def button_surrender(self):
        self.write({'state': 'done'})
        if self.is_master_bill_of_lading == True:
            self.job_id.write({'state': 'cargo_released'})

    def button_invoice(self):
        so_order_line = self.job_id.so_id.order_line
        product_id = False
        for o in so_order_line:
            product_id = o.product_id
        account_move = self.env['account.move']
        if self.charges_line:
            if self.total_charge <= 0:
                raise ValidationError('Total Charges should be a greater than 0')
            bol_invoice = account_move.search([('bol_id', '=', self.id)])
            if not bol_invoice:
                consumer = self.job_id.so_id.partner_id
                if self.job_id.po_id.total_collect_charges > 0:
                    party_name = self.job_id.po_id.party_name_id
                    consumer = self.env['res.partner'].create({
                        'name': party_name.name,
                        'street': self.job_id.po_id.street,
                        'street2': self.job_id.po_id.street_number,
                        'city': self.job_id.po_id.city,
                        'zip': self.job_id.po_id.post_code,
                    })
                if self.is_master_bill_of_lading == True:
                    inv = account_move.create({
                        'ref': self.carrier_booking_reference,
                        'move_type': 'out_invoice',
                        'invoice_origin': self.carrier_booking_reference,
                        'partner_id': consumer.id,
                        # 'partner_shipping_id': self.job_id.so_id.partner_shipping_id.id,
                        'currency_id': self.job_id.so_id.pricelist_id.currency_id.id,
                        'payment_reference': self.carrier_booking_reference,
                        'invoice_payment_term_id': self.job_id.so_id.payment_term_id.id,
                        'bol_id': self.id,
                        'booking_id': self.job_id.so_id.booking_id,
                        'place_of_origin': self.job_id.so_id.place_of_origin,
                        'place_of_destination': self.job_id.so_id.final_port_of_destination,
                        'vessel_name': self.job_id.vessel_name,
                        'voyage': self.job_id.voyage,
                        'rotation': self.job_id.rotation,
                        'imo_no': self.job_id.imo_no,
                        'is_bol_invoice': True,
                        'is_master_bill_of_lading': True,

                    })
                elif self.is_house_bill_of_lading == True:
                    inv = account_move.create({
                        'ref': self.carrier_booking_reference,
                        'move_type': 'out_invoice',
                        'invoice_origin': self.carrier_booking_reference,
                        'partner_id': consumer.id,
                        # 'partner_shipping_id': self.job_id.so_id.partner_shipping_id.id,
                        'currency_id': self.job_id.so_id.pricelist_id.currency_id.id,
                        'payment_reference': self.carrier_booking_reference,
                        'invoice_payment_term_id': self.job_id.so_id.payment_term_id.id,
                        'bol_id': self.id,
                        'booking_id': self.job_id.so_id.booking_id,
                        'place_of_origin': self.job_id.so_id.place_of_origin,
                        'place_of_destination': self.job_id.so_id.final_port_of_destination,
                        'vessel_name': self.job_id.vessel_name,
                        'voyage': self.job_id.voyage,
                        'rotation': self.job_id.rotation,
                        'imo_no': self.job_id.imo_no,
                        'is_bol_invoice': True,
                        'is_house_bill_of_lading': True,
                    })
                if inv:
                    for line in self.charges_line:
                        rec = inv.bol_charge_line.create({
                            'charge_type': line.charge_type,
                            # 'currency_amount': line.currency_amount,
                            'currency_code': line.currency_code,
                            'payment_term': line.payment_term,
                            'unit_price': line.unit_price,
                            'quantity': line.quantity,
                            'calculation_basis': 'per_day',
                            'currency_amount': line.quantity * line.unit_price,
                            # 'final_amount': line.final_amount,
                            'bol_account_charge_line_id': inv.id,
                        })
                    account = inv.journal_id.default_account_id
                    if product_id:
                        inv_lines = {
                            'name': product_id.name,
                            'move_id': inv.id,
                            'product_id': product_id.id,
                            'product_uom_id': product_id.uom_id.id,
                            'quantity': inv.bol_id.job_id.confirmed_no_of_container, #len(inv.job_charge_line),
                            'price_unit': inv.bol_total_charge / inv.bol_id.job_id.confirmed_no_of_container, #len(inv.job_charge_line),
                            'account_id': account.id,
                            # 'exclude_from_invoice_tab': False,
                        }
                    inv.invoice_line_ids.with_context(check_move_validity=False).create(inv_lines)
                    if self.is_master_bill_of_lading:
                        inv.write({'is_master_bill_of_lading': True})
                    if self.is_house_bill_of_lading:
                        inv.write({'is_house_bill_of_lading': True})
                    inv.write({'bol_id': self.id})
                    bol_inv_ids = self.env['account.move'].sudo().search(
                        [('bol_id', '=', self.id), ('is_bol_invoice', '=', True)])
                    self.invoice_ids = [(6, 0, bol_inv_ids.ids)]
                    self.invoice_status = "partial"
        else:
            raise ValidationError('No Chagres Lines to Create Invoice')

    def button_cancel(self):
        self.write({'state': 'cancelled'})

    def action_bol_send(self):
        """ Open a window to compose an email, with the edi invoice template
            message loaded by default
        """
        outmail_rec = self.env['ir.mail_server'].search([])
        if not outmail_rec:
            raise UserError("Outgoing mail server not set !!!")

        if not self.bol_cargo_line:
            raise ValidationError('Please Add Cargo Items')
        elif not self.bol_tq_line:
            raise ValidationError('Please Add Transport equipment Items')
        elif not self.bol_dp_line:
            raise ValidationError('Please Add Document Parties Items')
        elif not self.bol_sl_line:
            raise ValidationError('Please Add Shipment Location Items')
        elif not self.bol_ref_line:
            raise ValidationError('Please Add References Items')
        self.ensure_one()
        template = self.env.ref('freightbox.mail_template_bol', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='bill.of.lading',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template.id,
            default_composition_mode='comment',
            force_email=True,
        )
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

    @api.depends('charges_line.calculation_basis')
    def _compute_total_charge(self):
        for order in self:
            amount_total = 0
            for line in order.charges_line:
                amount_total += line.currency_amount
            order.write({
                'total_charge': amount_total,
            })

    # def button_create_bol_items(self):
    #     self.ensure_one()
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'bol.templates.wiz',
    #         'view_mode': 'form',
    #         'views': [(self.env.ref('freightbox.bol_template_form_view_wiz').id, "form")],
    #         'context': {'current_id': self.id},
    #         'target': 'new',
    #     }

    # def write(self, vals):
    #     res = super(BillOfLading, self).write(vals)
    #     message = ""
    #     print("---------------------- write ----------------------",vals)
    #     if vals.get('bol_cargo_line'):
    #         data_text = ""
    #         for i in vals.get('bol_cargo_line'):
    #             if i[2]:
    #                 data_text += str(i[2]) + ","
    #         message = _("Changes in Cargo Item Line %s ",data_text if data_text else "Delete")
    #         self.message_post(body=message)
    #
    #     if vals.get('bol_tq_line'):
    #         data_text = ""
    #         for i in vals.get('bol_tq_line'):
    #             if i[2]:
    #                 data_text += str(i[2]) + ","
    #
    #         message = _("Changes in Transport Equipment Line %s ",data_text if data_text else "Delete")
    #         self.message_post(body=message)
    #
    #     if vals.get('bol_dp_line'):
    #         data_text = ""
    #         for i in vals.get('bol_dp_line'):
    #             if i[2]:
    #                 data_text += str(i[2]) + ","
    #
    #         message = _("Changes in Document Parties Line %s ",data_text if data_text else "Delete")
    #         self.message_post(body=message)
    #
    #     if vals.get('bol_sl_line'):
    #         data_text = ""
    #         for i in vals.get('bol_sl_line'):
    #             if i[2]:
    #                 data_text += str(i[2]) + ","
    #
    #         message = _("Changes in Shipment Location Line %s ",data_text if data_text else "Delete")
    #         self.message_post(body=message)
    #
    #     if vals.get('bol_ref_line'):
    #         data_text = ""
    #         for i in vals.get('bol_ref_line'):
    #             if i[2]:
    #                 data_text += str(i[2]) + ","
    #
    #         message = _("Changes in References Line %s ",data_text if data_text else "Delete")
    #         self.message_post(body=message)
    #
    #     if vals.get('carrier_clauses_line'):
    #         data_text = ""
    #         for i in vals.get('carrier_clauses_line'):
    #             if i[2]:
    #                 data_text += str(i[2]) + ","
    #
    #         message = _("Changes in Carrier Clauses Line %s ",data_text if data_text else "Delete")
    #         self.message_post(body=message)
    #
    #     if vals.get('transport_leg_line'):
    #         data_text = ""
    #         for i in vals.get('transport_leg_line'):
    #             if i[2]:
    #                 data_text += str(i[2]) + ","
    #
    #         message = _("Changes in Transport Leg Line %s ",data_text if data_text else "Delete")
    #         self.message_post(body=message)
    #
    #     if vals.get('charges_line'):
    #         data_text = ""
    #         for i in vals.get('charges_line'):
    #             if i[2]:
    #                 data_text += str(i[2]) + ","
    #
    #         message = _("Changes in Charges Line %s ",data_text if data_text else "Delete")
    #         self.message_post(body=message)
    #
    #     return res


    shipping_instruction_ID = fields.Text("Shipping Instruction ID", required=True,
                                          help="The associated Shipping Instruction ID for the reference",
                                          tracking=True)
    transport_document_reference = fields.Text("Transport Document Reference", tracking=True, required=True,
                                               help="A unique reference allocated by the shipping line "
                                                    "to the transport document, and the main number used for the "
                                                    "tracking of the status of the shipment.")
    shipped_onboard_date = fields.Date("Shipped OnBoard Date", tracking=True,
                                       help="Date when the last container that is linked to the transport "
                                            "document will be physically loaded onboard the vessel indicated on the "
                                            "transport document.")
    terms_and_conditions = fields.Text("Terms and Conditions", tracking=True, required=True,
                                       help="Additional carrier terms and conditions aside from the general "
                                            "terms and conditions")
    reciept_or_deliverytype_at_origin = fields.Text("Reciept or Delivery type at Origin", tracking=True, required=True,
                                                    help="Indicates the type of service offered at the place"
                                                         " of receipt.")
    reciept_or_deliverytype_at_dest = fields.Text("Reciept or Delivery type at Destination", tracking=True,
                                                  required=True,
                                                  help="Indicates the type of service offered at the or "
                                                       "place of delivery.")
    cargo_movement_type_at_origin = fields.Text("Cargo movement type at Origin", required=True, tracking=True,
                                                help="Indicates who is responsible for stuffing and stripping the "
                                                     "container at place of receipt.")
    cargo_movement_type_at_dest = fields.Text("Cargo movement type at Destination", required=True, tracking=True,
                                              help="Indicates who is responsible for stuffing and stripping the "
                                                   "container at place of delivery.")
    issue_date = fields.Date("Issue Date", required=True, tracking=True,
                             help=". Date when the Original Bill of Lading will be issued.")

    bol_dp_line = fields.One2many('document.parties', 'bol_dp_line_id', copy=True)
    bol_cargo_line = fields.One2many('cargo.line.items', 'bol_cargo_line_id', copy=True)
    bol_tq_line = fields.One2many('transport.equipment', 'bol_tq_line_id', copy=True)
    bol_sl_line = fields.One2many('shipment.location', 'bol_sl_line_id', copy=True)
    bol_ref_line = fields.One2many('shipping.references', 'bol_ref_line_id', copy=True)
    transport_leg_line = fields.One2many('transportleg.line.items', 'transportleg_line_id', string="Transport Leg",
                                         copy=True)

    # PLACE OF ISSUE object
    poi_location_name = fields.Text(string="Location Name", tracking=True, help="Name of the location.")
    poi_un_location_code = fields.Text(string="UN Location Code", tracking=True,
                                       help="The UN Location code specifying where the place is located.")
    poi_street_name = fields.Text(string="Street Name", tracking=True,
                                  help="The name of the street of the party’s address.")
    poi_street_number = fields.Text(string="Street Number", tracking=True,
                                    help="The number of the street of the party’s address.")
    poi_floor = fields.Text(string="Floor", tracking=True, help="The floor of the party’s street number.")
    poi_post_code = fields.Text(string="Post Code", tracking=True, help="The post code of the party’s address.")
    poi_city_name = fields.Text(string="City Name", tracking=True, help="The city name of the party’s address.")
    poi_state_region = fields.Text(string="State Region", tracking=True,
                                   help="The state/region of the party’s address.")
    poi_country = fields.Text(string="Country", tracking=True, help="The country of the party’s address.")

    received_for_shipment_date = fields.Date("Recieved for shipment Date", tracking=True,
                                             help="Date when the carrier has taken possession of the last container "
                                                  "linked to the B/L")
    service_contract_reference = fields.Text("Service Contract Reference", tracking=True,
                                             help="Reference number for agreement between shipper and carrier "
                                                  "through which the shipper commits to provide a certain minimum "
                                                  "quantity of cargo.")

    declared_value = fields.Integer('Declared Value', tracking=True,
                                    help="The value of the cargo that the shipper declares in order to avoid the "
                                         "carrier's limitation of liability and Ad Valorem freight.")
    declared_value_currency = fields.Text('Declared Value Currency', tracking=True,
                                          help="The currency used for the declared value, using the 3-character code "
                                               "defined by ISO 4217.")
    issuer_code = fields.Text('Issuer Code', required=True, tracking=True,
                              help="The SCAC code of the issuing carrier of the Transport Document.")
    issuer_code_list_provider = fields.Text('Issuer Code list provider', tracking=True, required=True,
                                            help="The code list provider for the issuer code. Can be either "
                                                 "NMFTA or SMDG.")

    carrier_clauses_line = fields.One2many('carrier.clauses.line.items', 'carrier_clauses_line_id', copy=True,
                                           string="Carrier Clauses",
                                           help="Additional clauses for a specific shipment added by the carrier to the"
                                                " bill of lading, subject to local rules / guidelines or certain "
                                                "mandatory information required to be shared with the customer.")

    no_of_rider_pages = fields.Integer('Number of rider pages', tracking=True,
                                       help="The number of additional pages required to contain the goods"
                                            " description on a transport document. ")
    binary_copy = fields.Binary('Binary copy', tracking=True,
                                help="Allowed formats: jpg, pdf, png. Maximum allowed size: 4MB.")
    document_hash = fields.Text('Document hash', tracking=True,
                                help="Cryptographic hash of the binary copy using the SHA-256 algorithm, "
                                     "only applicable for electronic documents.")
    planned_arrival_date = fields.Date("Planned Arrival Date", tracking=True, required=True,
                                       help="The date of arrival at place of destination")
    planned_departure_date = fields.Date("Planned Departure Date", tracking=True, required=True,
                                         help=" The date of departure from place of receipt")
    pre_carried_by = fields.Text('Pre-carried by', tracking=True,
                                 help=" Mode of transportation for precarriage (e.g., truck, barge,vessel, rail)")
    si_ids = fields.Many2many('shipping.instruction', tracking=True, string='Shipping Instruction')
    job_id = fields.Many2one('job', tracking=True, string='Job ID', ondelete='cascade')
    inquiry_id = fields.Many2one('crm.lead', string="Inquiry ID", readonly=True, tracking=True)
    company_id = fields.Many2one('res.company',string="Company Name",default=lambda self:self.env.user.company_id.id)


    # PLACE OF RECIEPT object
    por_location_name = fields.Text(string="Location Name", tracking=True)
    por_un_location_code = fields.Text(string="UN Location Code", tracking=True)
    por_street_name = fields.Text(string="Street Name", tracking=True)
    por_street_number = fields.Text(string="Street Number", tracking=True)
    por_floor = fields.Text(string="Floor", tracking=True)
    por_post_code = fields.Text(string="Post Code", tracking=True)
    por_city_name = fields.Text(string="City Name", tracking=True)
    por_state_region = fields.Text(string="State Region", tracking=True)
    por_country = fields.Text(string="Country", tracking=True)

    # PORT OF LOADING object
    pol_location_name = fields.Text(string="Location Name", required=True, tracking=True)
    pol_un_location_code = fields.Text(string="UN Location Code", required=True, tracking=True)
    pol_city_name = fields.Text(string="City Name", required=True, tracking=True)
    pol_state_region = fields.Text(string="State Region", required=True, tracking=True)
    pol_country = fields.Text(string="Country", required=True, tracking=True)

    # PORT OF DISCHARGE object
    pod_location_name = fields.Text(string="Location Name", required=True, tracking=True)
    pod_un_location_code = fields.Text(string="UN Location Code", required=True, tracking=True)
    pod_city_name = fields.Text(string="City Name", required=True, tracking=True)
    pod_state_region = fields.Text(string="State Region", required=True, tracking=True)
    pod_country = fields.Text(string="Country", required=True, tracking=True)

    # PLACE OF DELIVERY object
    plod_location_name = fields.Text(string="Location Name", tracking=True)
    plod_un_location_code = fields.Text(string="UN Location Code", tracking=True)
    plod_street_name = fields.Text(string="Street Name", tracking=True)
    plod_street_number = fields.Text(string="Street Number", tracking=True)
    plod_floor = fields.Text(string="Floor", tracking=True)
    plod_post_code = fields.Text(string="Post Code", tracking=True)
    plod_city_name = fields.Text(string="City Name", tracking=True)
    plod_state_region = fields.Text(string="State Region", tracking=True)
    plod_country = fields.Text(string="Country", tracking=True)

    # ONWARD INLAND ROUTING object
    oir_location_name = fields.Text(string="Location Name", tracking=True)
    oir_un_location_code = fields.Text(string="UN Location Code", tracking=True)
    oir_street_name = fields.Text(string="Street Name", tracking=True)
    oir_street_number = fields.Text(string="Street Number", tracking=True)
    oir_floor = fields.Text(string="Floor", tracking=True)
    oir_post_code = fields.Text(string="Post Code", tracking=True)
    oir_city_name = fields.Text(string="City Name", tracking=True)
    oir_state_region = fields.Text(string="State Region", tracking=True)
    oir_country = fields.Text(string="Country", tracking=True)

    # PRE-CARRIAGE UNDER SHIPPER'S RESPONSIBILITY object
    pre_location_name = fields.Text(string="Location Name", tracking=True)
    pre_latitude = fields.Text(string="Latitude", tracking=True)
    pre_longitude = fields.Text(string="Longitude", tracking=True)
    pre_un_location_code = fields.Text(string="UN Location Code", tracking=True)
    pre_street_name = fields.Text(string="Street Name", tracking=True)
    pre_street_number = fields.Text(string="Street Number", tracking=True)
    pre_floor = fields.Text(string="Floor", tracking=True)
    pre_post_code = fields.Text(string="Post Code", tracking=True)
    pre_city_name = fields.Text(string="City Name", tracking=True)
    pre_state_region = fields.Text(string="State Region", tracking=True)
    pre_country = fields.Text(string="Country", tracking=True)

    charges_line = fields.One2many('charges.line.items', 'charges_line_id', string="Charges", copy=True)

    # is_prepare_bill_of_lading = fields.Boolean(string="Is Prepare Bill of Lading")
    is_issue_bill_of_lading = fields.Boolean(string="Is Issue Bill of Lading")
    is_master_bill_of_lading = fields.Boolean(string="Is Master Bill of Lading")
    is_house_bill_of_lading = fields.Boolean(string="Is House Bill of Lading")
    is_switch_bill_of_lading = fields.Boolean(string="Is Switch Bill of Lading")
    is_hold_bill_of_lading = fields.Boolean(string="Is Hold Bill of Lading")
    # is_house_bol_needed = fields.Boolean(string="Is House BOL needed")
    is_created_from_master_bol = fields.Boolean(string="Is Created from Master BOL")
    url = fields.Char('URL')
    db_name = fields.Char('Database Name')
    db_username = fields.Char('Username')
    api_bol_id = fields.Integer(string="Bol Api ID")
    invoice_ids = fields.Many2many("account.move", string='Invoices')
    invoice_status = fields.Selection([
        ('paid', 'Fully Invoiced (paid)'),
        ('partial', 'Partially Invoiced'),
        ('to invoice', 'To Invoice'),
        ('no', 'Nothing to Invoice')
    ], string='Invoice Status', default='no')
    # compute='_get_invoice_status')
    # job_count = fields.Integer(string='Job Count', compute='_get_job_count', readonly=True)
    # invoice_count = fields.Integer(string='Invoice Count', compute='_get_invoice_count', readonly=True)
    # si_count = fields.Integer(string='SI Count', compute='_get_si_count', readonly=True)
    total_charge = fields.Float(compute='_compute_total_charge', string="Total Charge")
    # state = fields.Selection([
    #     ('draft', 'Draft'),
    #     ('update', 'Update In Progress'),
    #     ('approve', 'Issue B/L'),
    #     ('amend', 'Amend In Progress'),
    #     ('hold', 'On hold'),
    #     ('release_hold', 'Release hold'),
    #     ('switch', 'Switch'),
    #     ('done', 'Done'),
    #     ('cancelled', 'Cancelled')
    # ], string='Status', readonly=True, default='draft', tracking=True)
    # bol_templates = fields.Many2one('bol.templates', string="BOL Template")
    is_onward_inland_routing = fields.Boolean(string="Is Onward Inland Routing?")
    is_precarriage = fields.Boolean(string="Is Precarriage under shipper's Responsibility?")
    active = fields.Boolean(string='Active', default=True)
    booking_user_id = fields.Many2one('res.users', string="Shipper/FF")
    # hold_reason = fields.Text('Hold Reason', tracking=True)
    # hold_bool = fields.Boolean(string='Hold Bool')
    is_alow_shipper_to_create = fields.Boolean(string='Allow Shipper to Create BOL ?')
    cargo_plus_ids = fields.Many2many("cargo.plus", "cargo_plus_bol_rel", "cargo_plus_id",
                                      "bol_id", string="Cargo Plus")

    @api.constrains('planned_departure_date', 'planned_arrival_date')
    def _check_planned_arrival_date(self):
        for rec in self:
            today = fields.Date.today()
            if rec.planned_departure_date > rec.planned_arrival_date:
                raise ValidationError(_("Planned Arrival Date cannot be before Planned Departure Date"))
            if rec.planned_arrival_date<today:
                raise ValidationError(_("Planned Arrival Date, cannot be a Past Date"))

    @api.model
    def action_open_draft_bol_form_view(self):
        view_id = self.env.ref('freightbox.bill_of_lading_tree_view').id
        view_form_id = self.env.ref('freightbox.bill_of_lading_form_view').id
        action = {
            'name': _('Draft BOL'),
            'type': 'ir.actions.act_window',
            'res_model': 'bill.of.lading',
            'view_type': 'list',
            'views': [(view_id, 'list'), (view_form_id, 'form')],
            # 'context': {'search_default_group_booking_id': 1},
            'view_mode': 'list,form',
        }
        return action

    @api.constrains('shipping_instruction_ID')
    def _check_shipping_instruction_id(self):
        if len(self.shipping_instruction_ID) > 100:
            raise ValidationError('Shipping Instruction ID (No. of characters must not exceed 100)')

    @api.constrains('transport_document_reference')
    def _check_transport_document_reference(self):
        if len(self.transport_document_reference) > 20:
            raise ValidationError('Transport Document Reference (No. of characters must not exceed 20)')

    @api.constrains('reciept_or_deliverytype_at_origin')
    def _check_reciept_or_deliverytype_at_origin(self):
        if len(self.reciept_or_deliverytype_at_origin) > 3:
            raise ValidationError('Reciept or Deliverytype at Origin (No. of characters must not exceed 3)')

    @api.constrains('reciept_or_deliverytype_at_dest')
    def _check_reciept_or_deliverytype_at_dest(self):
        if len(self.reciept_or_deliverytype_at_dest) > 3:
            raise ValidationError('Reciept or Deliverytype at Destination (No. of characters must not exceed 3)')

    @api.constrains('cargo_movement_type_at_origin')
    def _check_cargo_movement_type_at_origin(self):
        if len(self.cargo_movement_type_at_origin) > 3:
            raise ValidationError('Cargo movement type at Origin (No. of characters must not exceed 3)')

    @api.constrains('cargo_movement_type_at_dest')
    def _check_cargo_movement_type_at_dest(self):
        if len(self.cargo_movement_type_at_dest) > 3:
            raise ValidationError('Cargo movement type at Destination (No. of characters must not exceed 3)')

    @api.constrains('poi_location_name')
    def _check_poi_location_name(self):
        if self.poi_location_name and len(self.poi_location_name) > 100:
            raise ValidationError('Place of Issue, Location name (No. of characters must not exceed 100)')

    @api.constrains('poi_un_location_code')
    def _check_poi_un_location_code(self):
        if self.poi_un_location_code and len(self.poi_un_location_code) > 5:
            raise ValidationError('Place of Issue, UN Location Code(No. of characters must not exceed 5)')

    @api.constrains('poi_street_name')
    def _check_poi_street_name(self):
        if self.poi_street_name and len(self.poi_street_name) > 100:
            raise ValidationError('Place of Issue, Street Name (No. of characters must not exceed 100)')

    @api.constrains('poi_street_number')
    def _check_poi_street_number(self):
        if self.poi_street_number and len(self.poi_street_number) > 50:
            raise ValidationError('Place of Issue, Street Number(No. of characters must not exceed 50)')

    @api.constrains('poi_floor')
    def _check_poi_floor(self):
        if self.poi_floor and len(self.poi_floor) > 50:
            raise ValidationError('Place of Issue, Floor (No. of characters must not exceed 50)')

    @api.constrains('poi_post_code')
    def _check_poi_post_code(self):
        if self.poi_post_code and len(self.poi_post_code) > 10:
            raise ValidationError('Place of Issue, PostCode (No. of characters must not exceed 10)')

    @api.constrains('poi_city_name')
    def _check_poi_city_name(self):
        if self.poi_city_name and len(self.poi_city_name) > 65:
            raise ValidationError('Place of Issue, City Name (No. of characters must not exceed 65)')

    @api.constrains('poi_state_region')
    def _check_poi_state_region(self):
        if self.poi_state_region and len(self.poi_state_region) > 65:
            raise ValidationError('Place of Issue, State Region (No. of characters must not exceed 65)')

    @api.constrains('poi_country')
    def _check_poi_country(self):
        if self.poi_country and len(self.poi_country) > 75:
            raise ValidationError('Place of Issue, Country (No. of characters must not exceed 75)')

    @api.constrains('service_contract_reference')
    def _check_service_contract_reference(self):
        if self.service_contract_reference and len(self.service_contract_reference) > 30:
            raise ValidationError('Service Contract Reference (No. of characters must not exceed 30)')

    @api.constrains('declared_value_currency')
    def _check_declared_value_currency(self):
        if self.declared_value_currency and len(self.declared_value_currency) > 3:
            raise ValidationError('Declared Value Currency (No. of characters must not exceed 3)')

    @api.constrains('issuer_code')
    def _check_issuer_code(self):
        if len(self.issuer_code) > 4:
            raise ValidationError('Issuer Code (No. of characters must not exceed 4)')

    @api.constrains('issuer_code_list_provider')
    def _check_issuer_code_list_provider(self):
        if len(self.issuer_code_list_provider) > 5:
            raise ValidationError('Issuer Code List Provider (No. of characters must not exceed 5)')

    @api.constrains('por_location_name')
    def _check_por_location_name(self):
        if self.por_location_name and len(self.por_location_name) > 100:
            raise ValidationError('Place of Receipt, Location name (No. of characters must not exceed 100)')

    @api.constrains('por_un_location_code')
    def _check_por_un_location_code(self):
        if self.por_un_location_code and len(self.por_un_location_code) > 5:
            raise ValidationError('Place of Receipt, UN Location Code(No. of characters must not exceed 5)')

    @api.constrains('por_street_name')
    def _check_por_street_name(self):
        if self.por_street_name and len(self.por_street_name) > 100:
            raise ValidationError('Place of Receipt, Street Name (No. of characters must not exceed 100)')

    @api.constrains('por_street_number')
    def _check_por_street_number(self):
        if self.por_street_number and len(self.por_street_number) > 50:
            raise ValidationError('Place of Receipt, Street Number(No. of characters must not exceed 50)')

    @api.constrains('por_floor')
    def _check_por_floor(self):
        if self.por_floor and len(self.por_floor) > 50:
            raise ValidationError('Place of Receipt, Floor (No. of characters must not exceed 50)')

    @api.constrains('por_post_code')
    def _check_por_post_code(self):
        if self.por_post_code and len(self.por_post_code) > 10:
            raise ValidationError('Place of Receipt, PostCode (No. of characters must not exceed 10)')

    @api.constrains('por_city_name')
    def _check_por_city_name(self):
        if self.por_city_name and len(self.por_city_name) > 65:
            raise ValidationError('Place of Receipt, City Name (No. of characters must not exceed 65)')

    @api.constrains('por_state_region')
    def _check_por_state_region(self):
        if self.por_state_region and len(self.por_state_region) > 65:
            raise ValidationError('Place of Receipt, State Region (No. of characters must not exceed 65)')

    @api.constrains('por_country')
    def _check_por_country(self):
        if self.por_country and len(self.por_country) > 75:
            raise ValidationError('Place of Receipt, Country (No. of characters must not exceed 75)')

    @api.constrains('pol_location_name')
    def _check_pol_location_name(self):
        if len(self.pol_location_name) > 100:
            raise ValidationError('Port of Loading, Location name (No. of characters must not exceed 100)')

    @api.constrains('pol_un_location_code')
    def _check_pol_un_location_code(self):
        if len(self.pol_un_location_code) > 5:
            raise ValidationError('Port of Loading, UN Location Code(No. of characters must not exceed 5)')

    @api.constrains('pol_city_name')
    def _check_pol_city_name(self):
        if len(self.pol_city_name) > 65:
            raise ValidationError('Port of Loading, City Name (No. of characters must not exceed 65)')

    @api.constrains('pol_state_region')
    def _check_pol_state_region(self):
        if len(self.pol_state_region) > 65:
            raise ValidationError('Port of Loading, State Region (No. of characters must not exceed 65)')

    @api.constrains('pol_country')
    def _check_pol_country(self):
        if len(self.pol_country) > 75:
            raise ValidationError('Port of Loading, Country (No. of characters must not exceed 75)')

    @api.constrains('pod_location_name')
    def _check_pod_location_name(self):
        if len(self.pod_location_name) > 100:
            raise ValidationError('Port of Discharge, Location name (No. of characters must not exceed 100)')

    @api.constrains('pod_un_location_code')
    def _check_pod_un_location_code(self):
        if len(self.pod_un_location_code) > 5:
            raise ValidationError('Port of Discharge, UN Location Code(No. of characters must not exceed 5)')

    @api.constrains('pod_city_name')
    def _check_pod_city_name(self):
        if len(self.pod_city_name) > 65:
            raise ValidationError('Port of Discharge, City Name (No. of characters must not exceed 65)')

    @api.constrains('pod_state_region')
    def _check_pod_state_region(self):
        if len(self.pod_state_region) > 65:
            raise ValidationError('Port of Discharge, State Region (No. of characters must not exceed 65)')

    @api.constrains('pod_country')
    def _check_pod_country(self):
        if len(self.pod_country) > 75:
            raise ValidationError('Port of Discharge, Country (No. of characters must not exceed 75)')

    @api.constrains('plod_location_name')
    def _check_plod_location_name(self):
        if self.plod_location_name and len(self.plod_location_name) > 100:
            raise ValidationError('Place of Delivery, Location name (No. of characters must not exceed 100)')

    @api.constrains('plod_un_location_code')
    def _check_plod_un_location_code(self):
        if self.plod_un_location_code and len(self.plod_un_location_code) > 5:
            raise ValidationError('Place of Delivery, UN Location Code(No. of characters must not exceed 5)')

    @api.constrains('plod_street_name')
    def _check_plod_street_name(self):
        if self.plod_street_name and len(self.plod_street_name) > 100:
            raise ValidationError('Place of Delivery, Street Name (No. of characters must not exceed 100)')

    @api.constrains('plod_street_number')
    def _check_plod_street_number(self):
        if self.plod_street_number and len(self.plod_street_number) > 50:
            raise ValidationError('Place of Delivery, Street Number(No. of characters must not exceed 50)')

    @api.constrains('plod_floor')
    def _check_plod_floor(self):
        if self.plod_floor and len(self.plod_floor) > 50:
            raise ValidationError('Place of Delivery, Floor (No. of characters must not exceed 50)')

    @api.constrains('plod_post_code')
    def _check_plod_post_code(self):
        if self.plod_post_code and len(self.plod_post_code) > 10:
            raise ValidationError('Place of Delivery, PostCode (No. of characters must not exceed 10)')

    @api.constrains('plod_city_name')
    def _check_plod_city_name(self):
        if self.plod_city_name and len(self.plod_city_name) > 65:
            raise ValidationError('Place of Delivery, City Name (No. of characters must not exceed 65)')

    @api.constrains('plod_state_region')
    def _check_plod_state_region(self):
        if self.plod_state_region and len(self.plod_state_region) > 65:
            raise ValidationError('Place of Delivery, State Region (No. of characters must not exceed 65)')

    @api.constrains('plod_country')
    def _check_plod_country(self):
        if self.plod_country and len(self.plod_country) > 75:
            raise ValidationError('Place of Delivery, Country (No. of characters must not exceed 75)')

    @api.constrains('oir_location_name')
    def _check_oir_location_name(self):
        if self.oir_location_name and len(self.oir_location_name) > 100:
            raise ValidationError('Onward Inland Routing, Location name (No. of characters must not exceed 100)')

    @api.constrains('oir_un_location_code')
    def _check_oir_un_location_code(self):
        if self.oir_un_location_code and len(self.oir_un_location_code) > 5:
            raise ValidationError('Onward Inland Routing, UN Location Code(No. of characters must not exceed 5)')

    @api.constrains('oir_street_name')
    def _check_oir_street_name(self):
        if self.oir_street_name and len(self.oir_street_name) > 100:
            raise ValidationError('Onward Inland Routing, Street Name (No. of characters must not exceed 100)')

    @api.constrains('oir_street_number')
    def _check_oir_street_number(self):
        if self.oir_street_number and len(self.oir_street_number) > 50:
            raise ValidationError('Onward Inland Routing, Street Number(No. of characters must not exceed 50)')

    @api.constrains('oir_floor')
    def _check_oir_floor(self):
        if self.oir_floor and len(self.oir_floor) > 50:
            raise ValidationError('Onward Inland Routing, Floor (No. of characters must not exceed 50)')

    @api.constrains('oir_post_code')
    def _check_oir_post_code(self):
        if self.oir_post_code and len(self.oir_post_code) > 10:
            raise ValidationError('Onward Inland Routing, PostCode (No. of characters must not exceed 10)')

    @api.constrains('oir_city_name')
    def _check_oir_city_name(self):
        if self.oir_city_name and len(self.oir_city_name) > 65:
            raise ValidationError('Onward Inland Routing, City Name (No. of characters must not exceed 65)')

    @api.constrains('oir_state_region')
    def _check_oir_state_region(self):
        if self.oir_state_region and len(self.oir_state_region) > 65:
            raise ValidationError('Onward Inland Routing, State Region (No. of characters must not exceed 65)')

    @api.constrains('oir_country')
    def _check_oir_country(self):
        if self.oir_country and len(self.oir_country) > 75:
            raise ValidationError('Onward Inland Routing, Country (No. of characters must not exceed 75)')

    @api.constrains('pre_location_name')
    def _check_pre_location_name(self):
        if self.pre_location_name and len(self.pre_location_name) > 100:
            raise ValidationError(
                'Pre-Carraige under Shippers Responsibility, Location name (No. of characters must not exceed 100)')

    @api.constrains('pre_latitude')
    def _check_pre_latitude(self):
        if self.pre_latitude and len(self.pre_latitude) > 10:
            raise ValidationError(
                'Pre-Carraige under Shippers Responsibility, Latitude (No. of characters must not exceed 10)')

    @api.constrains('pre_longitude')
    def _check_pre_longitude(self):
        if self.pre_longitude and len(self.pre_longitude) > 11:
            raise ValidationError(
                'Pre-Carraige under Shippers Responsibility, Longitude (No. of characters must not exceed 11)')

    @api.constrains('pre_un_location_code')
    def _check_pre_un_location_code(self):
        if self.pre_un_location_code and len(self.pre_un_location_code) > 5:
            raise ValidationError(
                'Pre-Carraige under Shippers Responsibility, UN Location Code(No. of characters must not exceed 5)')

    @api.constrains('pre_street_name')
    def _check_pre_street_name(self):
        if self.pre_street_name and len(self.pre_street_name) > 100:
            raise ValidationError(
                'Pre-Carraige under Shippers Responsibility, Street Name (No. of characters must not exceed 100)')

    @api.constrains('pre_street_number')
    def _check_pre_street_number(self):
        if self.pre_street_number and len(self.pre_street_number) > 50:
            raise ValidationError(
                'Pre-Carraige under Shippers Responsibility, Street Number(No. of characters must not exceed 50)')

    @api.constrains('pre_floor')
    def _check_pre_floor(self):
        if self.pre_floor and len(self.pre_floor) > 50:
            raise ValidationError(
                'Pre-Carraige under Shippers Responsibility, Floor (No. of characters must not exceed 50)')

    @api.constrains('pre_post_code')
    def _check_pre_post_code(self):
        if self.pre_post_code and len(self.pre_post_code) > 10:
            raise ValidationError(
                'Pre-Carraige under Shippers Responsibility, PostCode (No. of characters must not exceed 10)')

    @api.constrains('pre_city_name')
    def _check_pre_city_name(self):
        if self.pre_city_name and len(self.pre_city_name) > 65:
            raise ValidationError(
                'Pre-Carraige under Shippers Responsibility, City Name (No. of characters must not exceed 65)')

    @api.constrains('pre_state_region')
    def _check_pre_state_region(self):
        if self.pre_state_region and len(self.pre_state_region) > 65:
            raise ValidationError(
                'Pre-Carraige under Shippers Responsibility, State Region (No. of characters must not exceed 65)')

    @api.constrains('pre_country')
    def _check_pre_country(self):
        if self.pre_country and len(self.pre_country) > 75:
            raise ValidationError(
                'Pre-Carraige under Shippers Responsibility, Country (No. of characters must not exceed 75)')


class TransportLeg(models.Model):
    _name = 'transportleg.line.items'
    _description = "Transportleg Line Items"

    @api.constrains('vessel_name')
    def _check_vessel_name(self):
        for line in self:
            if len(line.vessel_name) > 35:
                raise ValidationError('Vessel Name in Transport Leg(No. of characters must not exceed 35)')

    @api.constrains('carrier_voyage_number')
    def _check_carrier_voyage_number(self):
        for line in self:
            if len(line.carrier_voyage_number) > 50:
                raise ValidationError('Carrier Voyage Number in Transport Leg (No. of characters must not exceed 50)')

    @api.constrains('load_location')
    def _check_load_location(self):
        for line in self:
            if len(line.load_location) > 50:
                raise ValidationError('Load Location in Transport Leg (No. of characters must not exceed 50)')

    @api.constrains('discharge_location')
    def _check_discharge_location(self):
        for line in self:
            if len(line.discharge_location) > 50:
                raise ValidationError('Discharge Location in Transport Leg (No. of characters must not exceed 50)')

    @api.constrains('mode_of_transport')
    def _check_mode_of_transport(self):
        for line in self:
            if len(line.mode_of_transport) > 50:
                raise ValidationError('Mode of Transport in Transport Leg (No. of characters must not exceed 50)')

    transportleg_line_id = fields.Many2one('bill.of.lading', string='Transport Leg Line Item')
    transportleg_line_row_id = fields.Text('Transport leg row ID')
    vessel_name = fields.Text("Vessel Name", required=True)
    carrier_voyage_number = fields.Text("Carrier Voyage Number", required=True)
    load_location = fields.Text("Load Location", required=True)
    discharge_location = fields.Text("Discharge Location", required=True)
    mode_of_transport = fields.Text("Mode of transport", required=True)


class CarrierClauses(models.Model):
    _name = 'carrier.clauses.line.items'
    _description = "CarrierClauses Line Items"

    carrier_clauses_line_id = fields.Many2one('bill.of.lading', string='Carrier Clauses Line Item')
    carrier_clauses_row_id = fields.Text('Carrier clauses row ID')
    clause_content = fields.Text("Clause content")


class Charges(models.Model):
    _name = 'charges.line.items'
    _description = "Charges Line Items"

    @api.constrains('charge_type')
    def _check_charge_type(self):
        for line in self:
            if len(line.charge_type) > 20:
                raise ValidationError('Charge Type in Charges (No. of characters must not exceed 20)')

    @api.constrains('currency_code')
    def _check_currency_code(self):
        for line in self:
            if line.currency_code and len(line.currency_code) > 3:
                raise ValidationError('Currency Code in Charges (No. of characters must not exceed 3)')

    @api.constrains('payment_term')
    def _check_payment_term(self):
        for line in self:
            if line.payment_term and len(line.payment_term) > 3:
                raise ValidationError('Payment Term in Charges (No. of characters must not exceed 3)')

    # @api.constrains('calculation_basis')
    # def _check_calculation_basis(self):
    #     for line in self:
    #         if str(line.calculation_basis) > 50:
    #             raise ValidationError('Calculation Basis in Charges (No. of characters must not exceed 50)')

    @api.depends('unit_price', 'quantity')
    def _get_final_amount(self):
        for line in self:
            line.currency_amount = line.unit_price * line.quantity

    charges_line_id = fields.Many2one('bill.of.lading', string='Charges Line Item')
    charge_job_line_id = fields.Many2one('job', string='Charges Line Item')
    job_account_charge_line_id = fields.Many2one('account.move', string='Charges Line Item')
    bol_account_charge_line_id = fields.Many2one('account.move', string='Charges Line Item')
    charges_line_row_id = fields.Text('Charges row ID')
    charge_type = fields.Text('Charge type', required=True)
    currency_amount = fields.Float(compute='_get_final_amount', string='Currency Amount', required=True)
    currency_code = fields.Text('Currency Code', required=True)
    # payment_term = fields.Text('Payment Term', required=True)
    payment_term = fields.Selection([
        ('pre', 'Prepaid'),
        ('col', 'Collect'),
    ], string="Payment Term", tracking=True)
    # calculation_value = fields.Integer('Value')
    # calculation_basis = fields.Float(compute='_get_final_amount', string='Calculation Basis', required=True)
    calculation_basis = fields.Selection([
        ('per_day', 'Per Day'),
        ('per_ton', 'Per Ton'),
        ('per_sq_mt', 'Per Sq. Meter'), ], string="Calculation Basis", tracking=True)
    unit_price = fields.Float('Unit Price', required=True)
    quantity = fields.Integer('Quantity', required=True)
    final_amount = fields.Float(string="Sub Total")
