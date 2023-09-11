from odoo import models, fields, _, api
from odoo.exceptions import ValidationError,UserError
from lxml import etree


class BillOfLading(models.Model):
    _inherit = 'bill.of.lading'
    # _inherit = ['shipping.instruction', 'mail.thread', 'mail.activity.mixin']
    # _description = "Bill of lading"
    # _rec_name = 'transport_document_reference'

    # def button_approve(self):
    #     if self.is_master_bill_of_lading:
    #         self.job_id.sudo().write({'state': 'bol_received'})
    #     if not self.bol_cargo_line:
    #         raise ValidationError('Please Add Cargo Items')
    #     elif not self.bol_tq_line:
    #         raise ValidationError('Please Add Transport equipment Items')
    #     elif not self.bol_dp_line:
    #         raise ValidationError('Please Add Document Parties Items')
    #     elif not self.bol_sl_line:
    #         raise ValidationError('Please Add Shipment Location Items')
    #     elif not self.bol_ref_line:
    #         raise ValidationError('Please Add References Items')
    #     else:
    #         self.write({'state': 'approve'})

    def button_amend(self):
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
            self.write({'state': 'amend'})

    def button_switch(self):
        if self.is_master_bill_of_lading == True:
            self.job_id.write({'state': 'update_bol'})
        self.write({'state': 'switch'})

    def button_releasehold(self):
        self.write({'state': 'release_hold'})

    # def button_surrender(self):
    #     self.write({'state': 'done'})
    #     if self.is_master_bill_of_lading == True:
    #         self.job_id.write({'state': 'cargo_released'})

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

    # def button_cancel(self):
    #     self.write({'state': 'cancelled'})

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

    def action_get_job(self):
        item_ids = self.env['job'].search([('id', '=', self.job_id.id)])
        item_ids = item_ids.ids
        return {
            'name': "Job",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'job',
            'view_id': False,
            'domain': [('id', 'in', item_ids)],
            'target': 'current',
        }

    def action_get_si(self):
        item_ids = self.env['shipping.instruction'].search([('bill_of_lading_id', '=', self.id)])
        item_ids = item_ids.ids
        return {
            'name': "Shipping Instruction",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'shipping.instruction',
            'view_id': False,
            'domain': [('id', 'in', item_ids)],
            'target': 'current',
        }

    def action_get_invoice(self):
        item_ids = self.env['account.move'].search([('bol_id', '=', self.id)])
        item_ids = item_ids.ids
        return {
            'name': "Invoice",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'view_id': False,
            'domain': [('id', 'in', item_ids)],
            'target': 'current',
        }

    def _get_si_count(self):
        si_counts = self.env['shipping.instruction'].search_count([('bill_of_lading_id', '=', self.id)])
        self.si_count = si_counts

    def _get_job_count(self):
        job_counts = self.env['job'].search_count([('id', '=', self.job_id.id)])
        self.job_count = job_counts

    def _get_invoice_count(self):
        invoice_counts = self.env['account.move'].search_count([('bol_id', '=', self.id)])
        self.invoice_count = invoice_counts

    def button_get_si_items(self):
        ctx = {}
        bol_cl_lines = []
        bol_tq_lines = []
        bol_dp_lines = []
        bol_sl_lines = []
        bol_rc_lines = []
        bol_tl_lines = []
        bol_ch_lines = []

        self.bol_cargo_line = False
        self.bol_tq_line = False
        self.bol_dp_line = False
        self.bol_sl_line = False
        self.bol_ref_line = False
        self.transport_leg_line = False
        self.charges_line = False
        for si in self.si_ids:
            ctx = {
                'location_name': self.location_name,
                'un_location_code': self.un_location_code,
                'city_name': self.city_name,
                'state_region': self.state_region,
                'country': self.country,
            }
            si.is_bol_created = True
            if si.state == "accepted":
                for c in si.cargo_items_line:
                    vals = {
                        'bol_cargo_line_id': self.id,
                        'cargo_line_items_id': c.cargo_line_items_id,
                        'shipping_marks': c.shipping_marks,
                        'carrier_booking_reference': c.carrier_booking_reference,
                        'description_of_goods': c.description_of_goods,
                        'hs_code': c.hs_code,
                        'number_of_packages': c.number_of_packages,
                        'weight': c.weight,
                        'volume': c.volume,
                        'weight_unit': c.weight_unit,
                        'volume_unit': c.volume_unit,
                        'equipment_reference': c.equipment_reference,
                        'package_code': c.package_code,
                        'si_name': si.si_sequence_id,
                    }
                    bol_cl_lines.append(vals)
                for tq in si.transport_equipment_line:
                    tq_vals = {
                        'bol_tq_line_id': self.id,
                        'equipment_reference_id': tq.equipment_reference_id,
                        'weight_unit': tq.weight_unit,
                        'cargo_gross_weight': tq.cargo_gross_weight,
                        'container_tare_weight': tq.container_tare_weight,
                        'iso_equipment_code': tq.iso_equipment_code,
                        'is_shipper_owned': tq.is_shipper_owned,
                        'temperature_min': tq.temperature_min,
                        'temperature_max': tq.temperature_max,
                        'temperature_unit': tq.temperature_unit,
                        'humidity_min': tq.humidity_min,
                        'humidity_max': tq.humidity_max,
                        'ventilation_min': tq.ventilation_min,
                        'ventilation_max': tq.ventilation_max,
                        'seal_number': tq.seal_number,
                        'seal_source': tq.seal_source,
                        'seal_type': tq.seal_type,
                        'si_name': si.si_sequence_id,
                    }
                    bol_tq_lines.append(tq_vals)
                for dp in si.document_parties_line:
                    dp_vals = {
                        'bol_dp_line_id': self.id,
                        'party_name_id': dp.party_name_id,
                        'tax_reference_1': dp.tax_reference_1,
                        'public_key': dp.public_key,
                        'street': dp.street,
                        'street_number': dp.street_number,
                        'floor': dp.floor,
                        'post_code': dp.post_code,
                        'city': dp.city,
                        'state_region': dp.state_region,
                        'country': dp.country,
                        'tax_reference_2': dp.tax_reference_2,
                        'nmfta_code': dp.nmfta_code,
                        'party_function': dp.party_function,
                        'address_line': dp.address_line,
                        'name': dp.name,
                        'email': dp.email,
                        'phone': dp.phone,
                        'is_to_be_notified': dp.is_to_be_notified,
                        'si_name': si.si_sequence_id,
                    }
                    bol_dp_lines.append(dp_vals)
                for sl in si.shipment_location_line:
                    sl_vals = {
                        'bol_sl_line_id': self.id,
                        'location_type': sl.location_type.id,
                        'location_name': sl.location_name,
                        'latitude': sl.latitude,
                        'longitude': sl.longitude,
                        'un_location_code': sl.un_location_code,
                        'street_name': sl.street_name,
                        'street_number': sl.street_number,
                        'floor': sl.floor,
                        'post_code': sl.post_code,
                        'city_name': sl.city_name,
                        'state_region': sl.state_region,
                        'country': sl.country,
                        'displayed_name': sl.displayed_name,
                        'si_name': si.si_sequence_id,
                    }
                    bol_sl_lines.append(sl_vals)
                for rc in si.references_line:
                    rc_vals = {
                        'bol_ref_line_id': self.id,
                        'reference_type': rc.reference_type,
                        'reference_value': rc.reference_value,
                        'si_name': si.si_sequence_id,
                    }
                    bol_rc_lines.append(rc_vals)
        if self.job_id:
            transport_leg_vals = {
                'transportleg_line_id': self.id,
                'vessel_name': self.job_id.vessel_name,
                'carrier_voyage_number': self.job_id.voyage,
                'load_location': self.job_id.place_of_origin,
                'discharge_location': self.job_id.final_port_of_destination,
                'mode_of_transport': 'Vessel',
            }
            bol_tl_lines.append(transport_leg_vals)
            if self.job_id.is_multi_modal:
                transport_leg_vals1 = {
                    'transportleg_line_id': self.id,
                    'vessel_name': self.job_id.vessel_name1,
                    'carrier_voyage_number': self.job_id.voyage1,
                    'load_location': self.job_id.intermediate_pol_id.name,
                    'discharge_location': self.job_id.final_port_of_destination,
                    'mode_of_transport': 'Vessel',
                }
                bol_tl_lines.append(transport_leg_vals1)
            po = self.job_id.po_id
            so = self.job_id.so_id
            if po and self.is_master_bill_of_lading:
                if po.charges_line:
                    for po_ch in po.charges_line:
                        if po_ch.charges_id.prepaid:
                            payment_term = 'pre'
                        if po_ch.charges_id.collect:
                            payment_term = 'col'
                        if po_ch.collect:
                            ch_vals = {
                                'charges_line_id': self.id,
                                'charge_type': po_ch.charges_id.code,
                                'currency_code': po_ch.currency_id.name,
                                'unit_price': po_ch.unit_price,
                                'quantity': po_ch.units,
                                # 'currency_amount': 0,
                                'payment_term': payment_term,
                                'calculation_basis': po_ch.charges_id.calculation_basis,
                                'currency_amount': po_ch.unit_price * po_ch.units,
                            }
                            bol_ch_lines.append(ch_vals)
            if so and self.is_house_bill_of_lading:
                if so.charges_line:
                    for so_ch in so.charges_line:
                        if so_ch.collect:
                            print("so_ch", so_ch.new_unit_price)
                            print("units", so_ch.units)
                            print("so_ch.new_unit_price * so_ch.units", so_ch.new_unit_price * so_ch.units)
                            ch_vals = {
                                'charges_line_id': self.id,
                                'charge_type': so_ch.charges_id.code,
                                'currency_code': so_ch.currency_id.name,
                                'unit_price': so_ch.new_unit_price,
                                'quantity': so_ch.units,
                                # 'currency_amount': 0,
                                'payment_term': 'pre',
                                'calculation_basis': so_ch.charges_id.calculation_basis,
                                'currency_amount': so_ch.new_unit_price * so_ch.units,
                            }
                            bol_ch_lines.append(ch_vals)
        self.bol_cargo_line.create(bol_cl_lines)
        self.bol_tq_line.create(bol_tq_lines)
        self.bol_dp_line.create(bol_dp_lines)
        self.bol_sl_line.create(bol_sl_lines)
        self.bol_ref_line.create(bol_rc_lines)
        self.transport_leg_line.create(bol_tl_lines)
        self.charges_line.create(bol_ch_lines)
        return ctx

    def button_create_bol_items(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'bol.templates.wiz',
            'view_mode': 'form',
            'views': [(self.env.ref('freightbox.bol_template_form_view_wiz').id, "form")],
            'context': {'current_id': self.id},
            'target': 'new',
        }

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


    # shipping_instruction_ID = fields.Text("Shipping Instruction ID", required=True,
    #                                       help="The associated Shipping Instruction ID for the reference",
    #                                       tracking=True)
    # transport_document_reference = fields.Text("Transport Document Reference", tracking=True, required=True,
    #                                            help="A unique reference allocated by the shipping line "
    #                                                 "to the transport document, and the main number used for the "
    #                                                 "tracking of the status of the shipment.")
    # shipped_onboard_date = fields.Date("Shipped OnBoard Date", tracking=True,
    #                                    help="Date when the last container that is linked to the transport "
    #                                         "document will be physically loaded onboard the vessel indicated on the "
    #                                         "transport document.")
    # terms_and_conditions = fields.Text("Terms and Conditions", tracking=True, required=True,
    #                                    help="Additional carrier terms and conditions aside from the general "
    #                                         "terms and conditions")
    # reciept_or_deliverytype_at_origin = fields.Text("Reciept or Delivery type at Origin", tracking=True, required=True,
    #                                                 help="Indicates the type of service offered at the place"
    #                                                      " of receipt.")
    # reciept_or_deliverytype_at_dest = fields.Text("Reciept or Delivery type at Destination", tracking=True,
    #                                               required=True,
    #                                               help="Indicates the type of service offered at the or "
    #                                                    "place of delivery.")
    # cargo_movement_type_at_origin = fields.Text("Cargo movement type at Origin", required=True, tracking=True,
    #                                             help="Indicates who is responsible for stuffing and stripping the "
    #                                                  "container at place of receipt.")
    # cargo_movement_type_at_dest = fields.Text("Cargo movement type at Destination", required=True, tracking=True,
    #                                           help="Indicates who is responsible for stuffing and stripping the "
    #                                                "container at place of delivery.")
    # issue_date = fields.Date("Issue Date", required=True, tracking=True,
    #                          help=". Date when the Original Bill of Lading will be issued.")
    #
    # bol_dp_line = fields.One2many('document.parties', 'bol_dp_line_id', copy=True)
    # bol_cargo_line = fields.One2many('cargo.line.items', 'bol_cargo_line_id', copy=True)
    # bol_tq_line = fields.One2many('transport.equipment', 'bol_tq_line_id', copy=True)
    # bol_sl_line = fields.One2many('shipment.location', 'bol_sl_line_id', copy=True)
    # bol_ref_line = fields.One2many('shipping.references', 'bol_ref_line_id', copy=True)
    # transport_leg_line = fields.One2many('transportleg.line.items', 'transportleg_line_id', string="Transport Leg",
    #                                      copy=True)

    # PLACE OF ISSUE object
    # poi_location_name = fields.Text(string="Location Name", tracking=True, help="Name of the location.")
    # poi_un_location_code = fields.Text(string="UN Location Code", tracking=True,
    #                                    help="The UN Location code specifying where the place is located.")
    # poi_street_name = fields.Text(string="Street Name", tracking=True,
    #                               help="The name of the street of the party’s address.")
    # poi_street_number = fields.Text(string="Street Number", tracking=True,
    #                                 help="The number of the street of the party’s address.")
    # poi_floor = fields.Text(string="Floor", tracking=True, help="The floor of the party’s street number.")
    # poi_post_code = fields.Text(string="Post Code", tracking=True, help="The post code of the party’s address.")
    # poi_city_name = fields.Text(string="City Name", tracking=True, help="The city name of the party’s address.")
    # poi_state_region = fields.Text(string="State Region", tracking=True,
    #                                help="The state/region of the party’s address.")
    # poi_country = fields.Text(string="Country", tracking=True, help="The country of the party’s address.")
    #
    # received_for_shipment_date = fields.Date("Recieved for shipment Date", tracking=True,
    #                                          help="Date when the carrier has taken possession of the last container "
    #                                               "linked to the B/L")
    # service_contract_reference = fields.Text("Service Contract Reference", tracking=True,
    #                                          help="Reference number for agreement between shipper and carrier "
    #                                               "through which the shipper commits to provide a certain minimum "
    #                                               "quantity of cargo.")
    #
    # declared_value = fields.Integer('Declared Value', tracking=True,
    #                                 help="The value of the cargo that the shipper declares in order to avoid the "
    #                                      "carrier's limitation of liability and Ad Valorem freight.")
    # declared_value_currency = fields.Text('Declared Value Currency', tracking=True,
    #                                       help="The currency used for the declared value, using the 3-character code "
    #                                            "defined by ISO 4217.")
    # issuer_code = fields.Text('Issuer Code', required=True, tracking=True,
    #                           help="The SCAC code of the issuing carrier of the Transport Document.")
    # issuer_code_list_provider = fields.Text('Issuer Code list provider', tracking=True, required=True,
    #                                         help="The code list provider for the issuer code. Can be either "
    #                                              "NMFTA or SMDG.")
    #
    # carrier_clauses_line = fields.One2many('carrier.clauses.line.items', 'carrier_clauses_line_id', copy=True,
    #                                        string="Carrier Clauses",
    #                                        help="Additional clauses for a specific shipment added by the carrier to the"
    #                                             " bill of lading, subject to local rules / guidelines or certain "
    #                                             "mandatory information required to be shared with the customer.")
    #
    # no_of_rider_pages = fields.Integer('Number of rider pages', tracking=True,
    #                                    help="The number of additional pages required to contain the goods"
    #                                         " description on a transport document. ")
    # binary_copy = fields.Binary('Binary copy', tracking=True,
    #                             help="Allowed formats: jpg, pdf, png. Maximum allowed size: 4MB.")
    # document_hash = fields.Text('Document hash', tracking=True,
    #                             help="Cryptographic hash of the binary copy using the SHA-256 algorithm, "
    #                                  "only applicable for electronic documents.")
    # planned_arrival_date = fields.Date("Planned Arrival Date", tracking=True, required=True,
    #                                    help="The date of arrival at place of destination")
    # planned_departure_date = fields.Date("Planned Departure Date", tracking=True, required=True,
    #                                      help=" The date of departure from place of receipt")
    # pre_carried_by = fields.Text('Pre-carried by', tracking=True,
    #                              help=" Mode of transportation for precarriage (e.g., truck, barge,vessel, rail)")
    # si_ids = fields.Many2many('shipping.instruction', tracking=True, string='Shipping Instruction')
    # job_id = fields.Many2one('job', tracking=True, string='Job ID', ondelete='cascade')
    # inquiry_id = fields.Many2one('crm.lead', string="Inquiry ID", readonly=True, tracking=True)
    # company_id = fields.Many2one('res.company',string="Company Name",default=lambda self:self.env.user.company_id.id)


    # PLACE OF RECIEPT object
    # por_location_name = fields.Text(string="Location Name", tracking=True)
    # por_un_location_code = fields.Text(string="UN Location Code", tracking=True)
    # por_street_name = fields.Text(string="Street Name", tracking=True)
    # por_street_number = fields.Text(string="Street Number", tracking=True)
    # por_floor = fields.Text(string="Floor", tracking=True)
    # por_post_code = fields.Text(string="Post Code", tracking=True)
    # por_city_name = fields.Text(string="City Name", tracking=True)
    # por_state_region = fields.Text(string="State Region", tracking=True)
    # por_country = fields.Text(string="Country", tracking=True)
    #
    # # PORT OF LOADING object
    # pol_location_name = fields.Text(string="Location Name", required=True, tracking=True)
    # pol_un_location_code = fields.Text(string="UN Location Code", required=True, tracking=True)
    # pol_city_name = fields.Text(string="City Name", required=True, tracking=True)
    # pol_state_region = fields.Text(string="State Region", required=True, tracking=True)
    # pol_country = fields.Text(string="Country", required=True, tracking=True)

    # PORT OF DISCHARGE object
    # pod_location_name = fields.Text(string="Location Name", required=True, tracking=True)
    # pod_un_location_code = fields.Text(string="UN Location Code", required=True, tracking=True)
    # pod_city_name = fields.Text(string="City Name", required=True, tracking=True)
    # pod_state_region = fields.Text(string="State Region", required=True, tracking=True)
    # pod_country = fields.Text(string="Country", required=True, tracking=True)
    #
    # # PLACE OF DELIVERY object
    # plod_location_name = fields.Text(string="Location Name", tracking=True)
    # plod_un_location_code = fields.Text(string="UN Location Code", tracking=True)
    # plod_street_name = fields.Text(string="Street Name", tracking=True)
    # plod_street_number = fields.Text(string="Street Number", tracking=True)
    # plod_floor = fields.Text(string="Floor", tracking=True)
    # plod_post_code = fields.Text(string="Post Code", tracking=True)
    # plod_city_name = fields.Text(string="City Name", tracking=True)
    # plod_state_region = fields.Text(string="State Region", tracking=True)
    # plod_country = fields.Text(string="Country", tracking=True)

    # ONWARD INLAND ROUTING object
    # oir_location_name = fields.Text(string="Location Name", tracking=True)
    # oir_un_location_code = fields.Text(string="UN Location Code", tracking=True)
    # oir_street_name = fields.Text(string="Street Name", tracking=True)
    # oir_street_number = fields.Text(string="Street Number", tracking=True)
    # oir_floor = fields.Text(string="Floor", tracking=True)
    # oir_post_code = fields.Text(string="Post Code", tracking=True)
    # oir_city_name = fields.Text(string="City Name", tracking=True)
    # oir_state_region = fields.Text(string="State Region", tracking=True)
    # oir_country = fields.Text(string="Country", tracking=True)
    #
    # # PRE-CARRIAGE UNDER SHIPPER'S RESPONSIBILITY object
    # pre_location_name = fields.Text(string="Location Name", tracking=True)
    # pre_latitude = fields.Text(string="Latitude", tracking=True)
    # pre_longitude = fields.Text(string="Longitude", tracking=True)
    # pre_un_location_code = fields.Text(string="UN Location Code", tracking=True)
    # pre_street_name = fields.Text(string="Street Name", tracking=True)
    # pre_street_number = fields.Text(string="Street Number", tracking=True)
    # pre_floor = fields.Text(string="Floor", tracking=True)
    # pre_post_code = fields.Text(string="Post Code", tracking=True)
    # pre_city_name = fields.Text(string="City Name", tracking=True)
    # pre_state_region = fields.Text(string="State Region", tracking=True)
    # pre_country = fields.Text(string="Country", tracking=True)

    # charges_line = fields.One2many('charges.line.items', 'charges_line_id', string="Charges", copy=True)

    # is_prepare_bill_of_lading = fields.Boolean(string="Is Prepare Bill of Lading")
    # is_issue_bill_of_lading = fields.Boolean(string="Is Issue Bill of Lading")
    # is_master_bill_of_lading = fields.Boolean(string="Is Master Bill of Lading")
    # is_house_bill_of_lading = fields.Boolean(string="Is House Bill of Lading")
    # is_switch_bill_of_lading = fields.Boolean(string="Is Switch Bill of Lading")
    # is_hold_bill_of_lading = fields.Boolean(string="Is Hold Bill of Lading")
    # is_house_bol_needed = fields.Boolean(string="Is House BOL needed")
    # is_created_from_master_bol = fields.Boolean(string="Is Created from Master BOL")
    # url = fields.Char('URL')
    # db_name = fields.Char('Database Name')
    # db_username = fields.Char('Username')
    # api_bol_id = fields.Integer(string="Bol Api ID")
    # invoice_ids = fields.Many2many("account.move", string='Invoices')
    # invoice_status = fields.Selection([
    #     ('paid', 'Fully Invoiced (paid)'),
    #     ('partial', 'Partially Invoiced'),
    #     ('to invoice', 'To Invoice'),
    #     ('no', 'Nothing to Invoice')
    # ], string='Invoice Status', default='no')
    # compute='_get_invoice_status')
    job_count = fields.Integer(string='Job Count', compute='_get_job_count', readonly=True)
    invoice_count = fields.Integer(string='Invoice Count', compute='_get_invoice_count', readonly=True)
    si_count = fields.Integer(string='SI Count', compute='_get_si_count', readonly=True)
    # total_charge = fields.Float(compute='_compute_total_charge', string="Total Charge")
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
    bol_templates = fields.Many2one('bol.templates', string="BOL Template")
    # is_onward_inland_routing = fields.Boolean(string="Is Onward Inland Routing?")
    # is_precarriage = fields.Boolean(string="Is Precarriage under shipper's Responsibility?")
    # active = fields.Boolean(string='Active', default=True)
    # booking_user_id = fields.Many2one('res.users', string="Shipper/FF")
    hold_reason = fields.Text('Hold Reason', tracking=True)
    hold_bool = fields.Boolean(string='Hold Bool')
    # is_alow_shipper_to_create = fields.Boolean(string='Allow Shipper to Create BOL ?')
    # cargo_plus_ids = fields.Many2many("cargo.plus", "cargo_plus_bol_rel", "cargo_plus_id",
    #                                   "bol_id", string="Cargo Plus")

    def check_validity_on_hold_bol(self):
        hold_rec = self.search([('state','=','hold')])
        
        if hold_rec:
            for i in hold_rec:
                body = """
                        Dear Sir/Madam,
                        <br/>
                        <b><p> Your BOL Is On Hold For %s Reason. </p></b>
                        <p><b>  </b> </p> 
                        
                        """%str(i.hold_reason)
               
                to_email = ""
                if i.shipper_id.email:
                    to_email = i.shipper_id.email


                self.env['mail.mail'].sudo().create({
                    'email_from': "fenil.prajapati@powerpbox.org",
                    'author_id': self.env.user.partner_id.id,
                    'body_html': body,
                    'subject': 'Your BOL %s '%str(i.job_no),
                    'email_to': to_email,
                }).send()

    @api.onchange('bol_templates')
    def onchange_bol_template(self):
        bol_template = self.bol_templates
        if bol_template:
            self.transport_document_type_code = bol_template.transport_document_type_code
            self.is_shipped_onboard_type = bol_template.is_shipped_onboard_type
            self.number_of_originals = bol_template.number_of_originals
            self.number_of_copies = bol_template.number_of_copies
            self.pre_carriage_under_shippers_responsibility = bol_template.pre_carriage_under_shippers_responsibility
            self.is_charges_displayed = bol_template.is_charges_displayed
            self.location_name = bol_template.location_name
            self.un_location_code = bol_template.un_location_code
            self.city_name = bol_template.city_name
            self.state_region = bol_template.state_region
            self.country = bol_template.country
            self.shipping_instruction_ID = bol_template.shipping_instruction_ID
            self.transport_document_reference = bol_template.transport_document_reference
            self.shipped_onboard_date = bol_template.shipped_onboard_date
            self.terms_and_conditions = bol_template.terms_and_conditions
            self.reciept_or_deliverytype_at_origin = bol_template.reciept_or_deliverytype_at_origin
            self.reciept_or_deliverytype_at_dest = bol_template.reciept_or_deliverytype_at_dest
            self.cargo_movement_type_at_origin = bol_template.cargo_movement_type_at_origin
            self.cargo_movement_type_at_dest = bol_template.cargo_movement_type_at_dest
            self.issue_date = bol_template.issue_date

            self.poi_location_name = bol_template.poi_location_name
            self.poi_un_location_code = bol_template.poi_un_location_code
            self.poi_street_name = bol_template.poi_street_name
            self.poi_street_number = bol_template.poi_street_number
            self.poi_floor = bol_template.poi_floor
            self.poi_post_code = bol_template.poi_post_code
            self.poi_city_name = bol_template.poi_city_name
            self.poi_state_region = bol_template.poi_state_region
            self.poi_country = bol_template.poi_country

            self.received_for_shipment_date = bol_template.received_for_shipment_date
            self.service_contract_reference = bol_template.service_contract_reference
            self.declared_value = bol_template.declared_value
            self.declared_value_currency = bol_template.declared_value_currency
            self.issuer_code = bol_template.issuer_code
            self.issuer_code_list_provider = bol_template.issuer_code_list_provider
            self.no_of_rider_pages = bol_template.no_of_rider_pages
            self.binary_copy = bol_template.binary_copy
            self.document_hash = bol_template.document_hash
            self.planned_arrival_date = bol_template.planned_arrival_date
            self.planned_departure_date = bol_template.planned_departure_date
            self.pre_carried_by = bol_template.pre_carried_by

            self.por_location_name = bol_template.por_location_name
            self.por_un_location_code = bol_template.por_un_location_code
            self.por_street_name = bol_template.por_street_name
            self.por_street_number = bol_template.por_street_number
            self.por_floor = bol_template.por_floor
            self.por_post_code = bol_template.por_post_code
            self.por_city_name = bol_template.por_city_name
            self.por_state_region = bol_template.por_state_region
            self.por_country = bol_template.por_country

            self.pol_location_name = bol_template.pol_location_name
            self.pol_un_location_code = bol_template.pol_un_location_code
            self.pol_city_name = bol_template.pol_city_name
            self.pol_state_region = bol_template.pol_state_region
            self.pol_country = bol_template.pol_country

            self.pod_location_name = bol_template.pod_location_name
            self.pod_un_location_code = bol_template.pod_un_location_code
            self.pod_city_name = bol_template.pod_city_name
            self.pod_state_region = bol_template.pod_state_region
            self.pod_country = bol_template.pod_country

            self.plod_location_name = bol_template.plod_location_name
            self.plod_un_location_code = bol_template.plod_un_location_code
            self.plod_street_name = bol_template.plod_street_name
            self.plod_street_number = bol_template.plod_street_number
            self.plod_floor = bol_template.plod_floor
            self.plod_post_code = bol_template.plod_post_code
            self.plod_city_name = bol_template.plod_city_name
            self.plod_state_region = bol_template.plod_state_region
            self.plod_country = bol_template.plod_country

            self.oir_location_name = bol_template.oir_location_name
            self.oir_un_location_code = bol_template.oir_un_location_code
            self.oir_street_name = bol_template.oir_street_name
            self.oir_street_number = bol_template.oir_street_number
            self.oir_floor = bol_template.oir_floor
            self.oir_post_code = bol_template.oir_post_code
            self.oir_city_name = bol_template.oir_city_name
            self.oir_state_region = bol_template.oir_state_region
            self.oir_country = bol_template.oir_country

            self.pre_location_name = bol_template.pre_location_name
            self.pre_latitude = bol_template.pre_latitude
            self.pre_longitude = bol_template.pre_longitude
            self.pre_un_location_code = bol_template.pre_un_location_code
            self.pre_street_name = bol_template.pre_street_name
            self.pre_street_number = bol_template.pre_street_number
            self.pre_floor = bol_template.pre_floor
            self.pre_post_code = bol_template.pre_post_code
            self.pre_city_name = bol_template.pre_city_name
            self.pre_state_region = bol_template.pre_state_region
            self.pre_country = bol_template.pre_country
        else:
            self.transport_document_type_code = ""
            self.is_shipped_onboard_type = ""
            self.number_of_originals = ""
            self.number_of_copies = ""
            self.pre_carriage_under_shippers_responsibility = ""
            self.is_charges_displayed = ""
            self.location_name = ""
            self.un_location_code = ""
            self.city_name = ""
            self.state_region = ""
            self.country = ""
            self.shipping_instruction_ID = ""
            self.transport_document_reference = ""
            self.shipped_onboard_date = ""
            self.terms_and_conditions = ""
            self.reciept_or_deliverytype_at_origin = ""
            self.reciept_or_deliverytype_at_dest = ""
            self.cargo_movement_type_at_origin = ""
            self.cargo_movement_type_at_dest = ""
            self.issue_date = ""

            self.poi_location_name = ""
            self.poi_un_location_code = ""
            self.poi_street_name = ""
            self.poi_street_number = ""
            self.poi_floor = ""
            self.poi_post_code = ""
            self.poi_city_name = ""
            self.poi_state_region = ""
            self.poi_country = ""

            self.received_for_shipment_date = ""
            self.service_contract_reference = ""
            self.declared_value = ""
            self.declared_value_currency = ""
            self.issuer_code = ""
            self.issuer_code_list_provider = ""
            self.no_of_rider_pages = ""
            self.binary_copy = ""
            self.document_hash = ""
            self.planned_arrival_date = ""
            self.planned_departure_date = ""
            self.pre_carried_by = ""

            self.por_location_name = ""
            self.por_un_location_code = ""
            self.por_street_name = ""
            self.por_street_number = ""
            self.por_floor = ""
            self.por_post_code = ""
            self.por_city_name = ""
            self.por_state_region = ""
            self.por_country = ""

            self.pol_location_name = ""
            self.pol_un_location_code = ""
            self.pol_city_name = ""
            self.pol_state_region = ""
            self.pol_country = ""

            self.pod_location_name = ""
            self.pod_un_location_code = ""
            self.pod_city_name = ""
            self.pod_state_region = ""
            self.pod_country = ""

            self.plod_location_name = ""
            self.plod_un_location_code = ""
            self.plod_street_name = ""
            self.plod_street_number = ""
            self.plod_floor = ""
            self.plod_post_code = ""
            self.plod_city_name = ""
            self.plod_state_region = ""
            self.plod_country = ""

            self.oir_location_name = ""
            self.oir_un_location_code = ""
            self.oir_street_name = ""
            self.oir_street_number = ""
            self.oir_floor = ""
            self.oir_post_code = ""
            self.oir_city_name = ""
            self.oir_state_region = ""
            self.oir_country = ""

            self.pre_location_name = ""
            self.pre_latitude = ""
            self.pre_longitude = ""
            self.pre_un_location_code = ""
            self.pre_street_name = ""
            self.pre_street_number = ""
            self.pre_floor = ""
            self.pre_post_code = ""
            self.pre_city_name = ""
            self.pre_state_region = ""
            self.pre_country = ""

    @api.model
    # def action_open_draft_bol_form_view(self):
    #     view_id = self.env.ref('freightbox.bill_of_lading_tree_view').id
    #     view_form_id = self.env.ref('freightbox.bill_of_lading_form_view').id
    #     action = {
    #         'name': _('Draft BOL'),
    #         'type': 'ir.actions.act_window',
    #         'res_model': 'bill.of.lading',
    #         'view_type': 'list',
    #         'views': [(view_id, 'list'), (view_form_id, 'form')],
    #         # 'context': {'search_default_group_booking_id': 1},
    #         'view_mode': 'list,form',
    #     }
    #     return action

    @api.model
    def bol_dashboard(self):
        """ This function returns the values to populate the custom dashboard in
            the Bill Of leading views.
        """

        result = {
            'master_bl': 0,
            'house_bl': 0,
        }

        result['master_bl'] = self.search_count([('is_master_bill_of_lading', '=', True)])
        result['house_bl'] = self.search_count([('is_house_bill_of_lading', '=', True)])

        return result

    def bol_tutorial_video_new_tab(self):
        url = self.env['ir.config_parameter'].sudo().get_param('freightbox.complete_tutorial_video_start_to_end',
                                                               "/freightbox/static/src/img/index_file_images/not_found.png")
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }

    @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    def get_view(self, view_id=None, view_type='form', **options):
        # result = super().fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        result = super().get_view(view_id, view_type, **options)
        if view_id == self.env.ref("freightbox.bill_of_lading_form_view").id:
            url = self.env['ir.config_parameter'].sudo().get_param('freightbox.bol_tutorial_video',
                                                                   "/freightbox/static/src/img/index_file_images/not_found.png")
            doc = etree.XML(result['arch'])
            for node in doc.xpath("//iframe[@id='bol_tutorial_video']"):
                node.set('src', url)
            result['arch'] = etree.tostring(doc)
        return result


# class TransportLeg(models.Model):
#     _name = 'transportleg.line.items'
#     _description = "Transportleg Line Items"
#
#     @api.constrains('vessel_name')
#     def _check_vessel_name(self):
#         for line in self:
#             if len(line.vessel_name) > 35:
#                 raise ValidationError('Vessel Name in Transport Leg(No. of characters must not exceed 35)')
#
#     @api.constrains('carrier_voyage_number')
#     def _check_carrier_voyage_number(self):
#         for line in self:
#             if len(line.carrier_voyage_number) > 50:
#                 raise ValidationError('Carrier Voyage Number in Transport Leg (No. of characters must not exceed 50)')
#
#     @api.constrains('load_location')
#     def _check_load_location(self):
#         for line in self:
#             if len(line.load_location) > 50:
#                 raise ValidationError('Load Location in Transport Leg (No. of characters must not exceed 50)')
#
#     @api.constrains('discharge_location')
#     def _check_discharge_location(self):
#         for line in self:
#             if len(line.discharge_location) > 50:
#                 raise ValidationError('Discharge Location in Transport Leg (No. of characters must not exceed 50)')
#
#     @api.constrains('mode_of_transport')
#     def _check_mode_of_transport(self):
#         for line in self:
#             if len(line.mode_of_transport) > 50:
#                 raise ValidationError('Mode of Transport in Transport Leg (No. of characters must not exceed 50)')
#
#     transportleg_line_id = fields.Many2one('bill.of.lading', string='Transport Leg Line Item')
#     transportleg_line_row_id = fields.Text('Transport leg row ID')
#     vessel_name = fields.Text("Vessel Name", required=True)
#     carrier_voyage_number = fields.Text("Carrier Voyage Number", required=True)
#     load_location = fields.Text("Load Location", required=True)
#     discharge_location = fields.Text("Discharge Location", required=True)
#     mode_of_transport = fields.Text("Mode of transport", required=True)


# class CarrierClauses(models.Model):
#     _name = 'carrier.clauses.line.items'
#     _description = "CarrierClauses Line Items"
#
#     carrier_clauses_line_id = fields.Many2one('bill.of.lading', string='Carrier Clauses Line Item')
#     carrier_clauses_row_id = fields.Text('Carrier clauses row ID')
#     clause_content = fields.Text("Clause content")
#
#
# class Charges(models.Model):
#     _name = 'charges.line.items'
#     _description = "Charges Line Items"
#
#     @api.constrains('charge_type')
#     def _check_charge_type(self):
#         for line in self:
#             if len(line.charge_type) > 20:
#                 raise ValidationError('Charge Type in Charges (No. of characters must not exceed 20)')
#
#     @api.constrains('currency_code')
#     def _check_currency_code(self):
#         for line in self:
#             if line.currency_code and len(line.currency_code) > 3:
#                 raise ValidationError('Currency Code in Charges (No. of characters must not exceed 3)')
#
#     @api.constrains('payment_term')
#     def _check_payment_term(self):
#         for line in self:
#             if line.payment_term and len(line.payment_term) > 3:
#                 raise ValidationError('Payment Term in Charges (No. of characters must not exceed 3)')
#
#     # @api.constrains('calculation_basis')
#     # def _check_calculation_basis(self):
#     #     for line in self:
#     #         if str(line.calculation_basis) > 50:
#     #             raise ValidationError('Calculation Basis in Charges (No. of characters must not exceed 50)')
#
#     @api.depends('unit_price', 'quantity')
#     def _get_final_amount(self):
#         for line in self:
#             line.currency_amount = line.unit_price * line.quantity
#
#     charges_line_id = fields.Many2one('bill.of.lading', string='Charges Line Item')
#     charge_job_line_id = fields.Many2one('job', string='Charges Line Item')
#     job_account_charge_line_id = fields.Many2one('account.move', string='Charges Line Item')
#     bol_account_charge_line_id = fields.Many2one('account.move', string='Charges Line Item')
#     charges_line_row_id = fields.Text('Charges row ID')
#     charge_type = fields.Text('Charge type', required=True)
#     currency_amount = fields.Float(compute='_get_final_amount', string='Currency Amount', required=True)
#     currency_code = fields.Text('Currency Code', required=True)
#     # payment_term = fields.Text('Payment Term', required=True)
#     payment_term = fields.Selection([
#         ('pre', 'Prepaid'),
#         ('col', 'Collect'),
#     ], string="Payment Term", tracking=True)
#     # calculation_value = fields.Integer('Value')
#     # calculation_basis = fields.Float(compute='_get_final_amount', string='Calculation Basis', required=True)
#     calculation_basis = fields.Selection([
#         ('per_day', 'Per Day'),
#         ('per_ton', 'Per Ton'),
#         ('per_sq_mt', 'Per Sq. Meter'), ], string="Calculation Basis", tracking=True)
#     unit_price = fields.Float('Unit Price', required=True)
#     quantity = fields.Integer('Quantity', required=True)
#     final_amount = fields.Float(string="Sub Total")
