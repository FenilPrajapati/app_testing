# -*- coding: utf-8 -*-
from odoo import fields, api, models, _
from odoo.exceptions import ValidationError
import requests
import json
import socket
import logging
_logger = logging.getLogger(__name__)
Hostname = socket.gethostname()


class ApiIntegration(models.Model):
    _name = 'api.integration'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "API Integration"
    _rec_name = 'model_id'

    @api.model
    def _default_user(self):
        return self.env.context.get('user_id', self.env.user.id)

    url = fields.Char('URL', tracking=True)
    key = fields.Text('Key', tracking=True)
    host = fields.Text('Host', tracking=True)
    last_executed_date = fields.Datetime('Last Executed Date', tracking=True)
    description = fields.Char('Description', tracking=True)
    user_id = fields.Many2one('res.users', string='Responsible User', default=_default_user, tracking=True)
    model_id = fields.Many2one('ir.model', string='Model', help='The model object for the field to evaluate',
                               tracking=True)
    ip_address = fields.Char('IP Address', tracking=True)
    name = fields.Char('Name')
    password = fields.Char('Password', tracking=True)
    token = fields.Text('Token', tracking=True)
    token_expiry_date = fields.Date('Date of expiry of token', tracking=True)
    username = fields.Char('Username', tracking=True)

    def get_allowed_track_count(self):
        res_config_settings_obj = self.env['ir.config_parameter']
        allowed_api_calls = 0
        hostname = socket.gethostname()
        dbuuid = res_config_settings_obj.sudo().get_param('database.uuid')
        username = hostname + '_' + dbuuid
        api_rec = self.env['api.integration'].search([('name', '=', 'get_allowed_gh_api_calls')])[-1]
        if not api_rec:
            raise ValidationError("API Record does not exist for 'get_allowed_gh_api_calls'.")
        url = '%s/%s/1/0' % (api_rec.url, username)
        response = requests.get(url)
        if response.status_code == 200:
            response_data = json.loads(response.content)
            if response_data.get('data', {}).get('allowed_transport_requests', 0):
                allowed_api_calls = response_data.get('data', {}).get('allowed_transport_requests', 0)
                res_config_settings_obj.sudo().set_param('odoo_v14_frieght.allowed_track_count', allowed_api_calls)

    def _schedule_send_inquiry(self):
        inquiry_events = []
        inquiry_recs = self.env['crm.lead'].sudo().search([('booking_id', '!=', False), ('cargo_name', '!=', False)])
        dbuuid = self.env['ir.config_parameter'].sudo().get_param('database.uuid')
        username = Hostname + '_' + dbuuid
        for rec in inquiry_recs:
            parent_vals = {
                'email_from': rec.email_from,
                'partner_id': rec.partner_id.name,
                'partner_name': rec.partner_name,
                'phone': rec.phone,
                'cargo_name': rec.cargo_name,
                'quantity': rec.quantity,
                'shipment_terms': rec.shipment_terms,
                'weight': rec.weight,
                'volume': rec.volume,
                'move_type': rec.move_type.name,
                'incoterm_id': rec.incoterm_id.name,
                'place_of_origin': rec.place_of_origin,
                'final_port_of_destination': rec.final_port_of_destination,
                'booking_id': rec.booking_id,
                'expected_date_of_shipment': str(rec.expected_date_of_shipment),
                'remarks': rec.remarks,
                'place_of_origin': rec.place_of_origin,
                'final_port_of_destination': rec.final_port_of_destination,
                'point_of_stuffing': rec.point_of_stuffing if rec.point_of_stuffing else '',
                'point_of_destuffing': rec.point_of_destuffing if rec.point_of_destuffing else '',
                'container_type': rec.container_type.name,
                'volume_uom': rec.volume_uom.id,
                'weight_uom': rec.weight_uom.id,
                'booking_date': str(rec.booking_date),
                'shipping_line_id': rec.shipping_line_id.name,
                'inquiry_user_name': username,
            }
            inquiry_events.append(parent_vals)
        api_rec = self.env['api.integration'].search([('name', '=', 'post_inquiry_from_freightbox')])[-1]
        if not api_rec:
            raise ValidationError("API Record does not exist for 'post_inquiry_from_freightbox'.")
        res = requests.post(api_rec.url, data=json.dumps(inquiry_events))
        return res

    def _schedule_send_job(self):
        job_events = []
        job_recs = self.env['job'].sudo().search([])
        dbuuid = self.env['ir.config_parameter'].sudo().get_param('database.uuid')
        username = Hostname + '_' + dbuuid
        for rec in job_recs:
            parent_vals = {
                'job_user_name': username,
                'carrier_booking': rec.carrier_booking,
                'carrrier_date': str(rec.carrrier_date),
                'carrrier_id': rec.carrrier_id,
                'job_no': rec.job_no,
                'job_date': str(rec.job_date),
                'vessel_name': rec.vessel_name,
                'voyage': rec.voyage,
                'rotation': rec.rotation,
                'imo_no': rec.imo_no,
                'cargo_gross_weight': rec.cargo_gross_weight,
                'commodity_description': rec.commodity_description,
                'place_of_origin': rec.place_of_origin,
                'final_port_of_destination': rec.final_port_of_destination,
                'requested_date_time': str(rec.requested_date_time),
                'actual_date_time': str(rec.actual_date_time),
                # 'requested_equipment_type': rec.requested_equipment_type,
                # 'confirmed_equipment_type': rec.confirmed_equipment_type,
                'exp_no_of_container': rec.exp_no_of_container,
                'confirmed_no_of_container': rec.confirmed_no_of_container,
            }
            print("parent_vals", parent_vals)
            job_events.append(parent_vals)
            api_rec = self.env['api.integration'].search([('name', '=', 'post_job_from_freightbox')])[-1]
            res = requests.post(api_rec.url, data=json.dumps(job_events))
            print("res job=-----", res)
            if not api_rec:
                raise ValidationError("API Record does not exist for 'post_job_from_freightbox'.")
        print("job_events--", job_events)

        return res

    def _create_si_parent_vals(self, si_rec_id):
        dbuuid = self.env['ir.config_parameter'].sudo().get_param('database.uuid')
        username = Hostname + '_' + dbuuid
        parent_vals = {
            'parent_id': si_rec_id.id,
            'si_user_name': username,
            'transport_document_type_code': si_rec_id.transport_document_type_code,
            'number_of_originals': si_rec_id.number_of_originals,
            'number_of_copies': si_rec_id.number_of_copies,
            'pre_carriage_under_shippers_responsibility':
                si_rec_id.pre_carriage_under_shippers_responsibility,
            'carrier_booking_reference': si_rec_id.carrier_booking_reference,
            'shipping_instruction_id': si_rec_id.shipping_instruction_id,
            'is_electronic': si_rec_id.is_electronic,
            'is_charges_displayed': si_rec_id.is_charges_displayed,
            'location_name': si_rec_id.location_name,
            'un_location_code': si_rec_id.un_location_code,
            'city_name': si_rec_id.city_name,
            'state_region': si_rec_id.state_region,
            'country': si_rec_id.country,
            'si_sequence_id': si_rec_id.si_sequence_id,
            'state': si_rec_id.state,
            'shipper_id': si_rec_id.shipper_id.name,
            'si_inquiry_no': si_rec_id.si_inquiry_no.booking_id,
        }
        return parent_vals

    def _create_cargo_item_vals(self, cargo_item_id):
        cargo_vals = {
            'cargo_line_items_row_id': cargo_item_id.cargo_line_items_row_id,
            'cargo_line_items_id': cargo_item_id.cargo_line_items_id,
            'shipping_marks': cargo_item_id.shipping_marks,
            'carrier_booking_reference': cargo_item_id.carrier_booking_reference,
            'description_of_goods': cargo_item_id.description_of_goods,
            'hs_code': cargo_item_id.hs_code,
            'number_of_packages': cargo_item_id.number_of_packages,
            'weight': cargo_item_id.weight,
            'volume': cargo_item_id.volume,
            'weight_unit': cargo_item_id.weight_unit,
            'volume_unit': cargo_item_id.volume_unit,
            'equipment_reference': cargo_item_id.equipment_reference,
            'package_code': cargo_item_id.package_code,
        }
        return cargo_vals

    def _create_tq_item_vals(self, tq_item_id):
        tq_vals = {
            'equipment_reference_id': tq_item_id.equipment_reference_id,
            'transport_equipment_row_id': tq_item_id.transport_equipment_row_id,
            'weight_unit': tq_item_id.weight_unit,
            'cargo_gross_weight': tq_item_id.cargo_gross_weight,
            'container_tare_weight': tq_item_id.container_tare_weight,
            'iso_equipment_code': tq_item_id.iso_equipment_code,
            'is_shipper_owned': tq_item_id.is_shipper_owned,
            'temperature_min': tq_item_id.temperature_min,
            'temperature_max': tq_item_id.temperature_max,
            'temperature_unit': tq_item_id.temperature_unit,
            'humidity_min': tq_item_id.humidity_min,
            'humidity_max': tq_item_id.humidity_max,
            'ventilation_min': tq_item_id.ventilation_min,
            'ventilation_max': tq_item_id.ventilation_max,
            'seal_number': tq_item_id.seal_number,
            'seal_source': tq_item_id.seal_source,
            'seal_type': tq_item_id.seal_type,
        }
        return tq_vals

    def _create_dp_item_vals(self, dp_item_id):
        dp_vals = {
            'document_parties_row_id': dp_item_id.document_parties_row_id,
            'party_name_id': dp_item_id.party_name_id,
            'tax_reference_1': dp_item_id.tax_reference_1,
            'public_key': dp_item_id.public_key,
            'street': dp_item_id.street,
            'street_number': dp_item_id.street_number,
            'floor': dp_item_id.floor,
            'post_code': dp_item_id.post_code,
            'city': dp_item_id.city,
            'state_region': dp_item_id.state_region,
            'country': dp_item_id.country,
            'tax_reference_2': dp_item_id.tax_reference_2,
            'nmfta_code': dp_item_id.nmfta_code,
            'party_function': dp_item_id.party_function,
            'address_line': dp_item_id.address_line,
            'name': dp_item_id.name,
            'email': dp_item_id.email,
            'phone': dp_item_id.phone,
            'is_to_be_notified': dp_item_id.is_to_be_notified,
        }
        return dp_vals

    def _create_sl_item_vals(self, sl_item_id):
        sl_vals = {
            'shipment_location_row_id': sl_item_id.shipment_location_row_id,
            'location_type': sl_item_id.location_type.name,
            'location_name': sl_item_id.location_name,
            'latitude': sl_item_id.latitude,
            'longitude': sl_item_id.longitude,
            'un_location_code': sl_item_id.un_location_code,
            'street_name': sl_item_id.street_name,
            'street_number': sl_item_id.street_number,
            'floor': sl_item_id.floor,
            'post_code': sl_item_id.post_code,
            'city_name': sl_item_id.city_name,
            'state_region': sl_item_id.state_region,
            'country': sl_item_id.country,
            'displayed_name': sl_item_id.displayed_name,
        }
        return sl_vals

    def _create_rc_item_vals(self, rc_item_id):
        rc_vals = {
            'shipping_references_row_id': rc_item_id.shipping_references_row_id,
            'reference_type': rc_item_id.reference_type,
            'reference_value': rc_item_id.reference_value,
        }
        return rc_vals

    def _schedule_send_si(self):
        shipping_instruction_recs = self.env['shipping.instruction'].sudo().search([])
        for si_rec_id in shipping_instruction_recs:
            si_events = []
            si_event_list = {}
            # action to get parent vals as dict in common method
            parent_vals = self._create_si_parent_vals(si_rec_id)
            si_event_list['parent'] = parent_vals
            # action to get cargo vals as dict in common method
            cargo_child_lst = []
            for c in si_rec_id.cargo_items_line:
                cargo_vals = self._create_cargo_item_vals(c)
                cargo_child_lst.append(cargo_vals)
            si_event_list['cargo'] = cargo_child_lst
            # action to get tq vals as dict in common method
            tq_child_lst = []
            for tq in si_rec_id.transport_equipment_line:
                tq_vals = self._create_tq_item_vals(tq)
                tq_child_lst.append(tq_vals)
            si_event_list['TransportEquipment'] = tq_child_lst
            # action to get dp vals as dict in common method
            dp_child_lst = []
            for dp in si_rec_id.document_parties_line:
                dp_vals = self._create_dp_item_vals(dp)
                dp_child_lst.append(dp_vals)
            si_event_list['DocumentParties'] = dp_child_lst
            # action to get sl vals as dict in common method
            sl_child_lst = []
            for sl in si_rec_id.shipment_location_line:
                sl_vals = self._create_sl_item_vals(sl)
                sl_child_lst.append(sl_vals)
            si_event_list['ShipmentLocations'] = sl_child_lst
            # action to get rc vals as dict in common method
            rc_child_lst = []
            for rc in si_rec_id.references_line:
                rc_vals = self._create_rc_item_vals(rc)
                rc_child_lst.append(rc_vals)
            si_event_list['References'] = rc_child_lst
            # append parent and child values in one array
            si_events.append(si_event_list)
            # post data
            api_rec = self.env['api.integration'].search([('name', '=', 'post_si_from_freightbox')])[-1]
            if not api_rec:
                raise ValidationError("API Record does not exist for 'post_si_from_freightbox'.")
            res = requests.post(api_rec.url, data=json.dumps(si_events))
            if res.status_code == 208:
                api_rec = self.env['api.integration'].search([('name', '=', 'update_si_from_freightbox')])[-1]
                if not api_rec:
                    raise ValidationError("API Record does not exist for 'update_si_from_freightbox'.")
                url = "%s/%s" % (api_rec.url, si_rec_id.si_sequence_id)
                res = requests.post(url, json.dumps(si_events))
        return True

    def _create_bol_parent_vals(self, bol_rec_id):
        dbuuid = self.env['ir.config_parameter'].sudo().get_param('database.uuid')
        username = Hostname + '_' + dbuuid
        bol_parent_vals = {
            'parent_id': bol_rec_id.id,
            'bol_user_name': username,
            'transport_document_type_code': bol_rec_id.transport_document_type_code,
            'number_of_originals': bol_rec_id.number_of_originals,
            'number_of_copies': bol_rec_id.number_of_copies,
            'pre_carriage_under_shippers_responsibility':
                bol_rec_id.pre_carriage_under_shippers_responsibility,
            'carrier_booking_reference': bol_rec_id.carrier_booking_reference,
            'is_electronic': bol_rec_id.is_electronic,
            'is_charges_displayed': bol_rec_id.is_charges_displayed,
            'location_name': bol_rec_id.location_name,
            'un_location_code': bol_rec_id.un_location_code,
            'city_name': bol_rec_id.city_name,
            'state_region': bol_rec_id.state_region,
            'country': bol_rec_id.country,

            'shipping_instruction_ID': bol_rec_id.shipping_instruction_ID,
            'transport_document_reference': bol_rec_id.transport_document_reference,
            'shipped_onboard_date': bol_rec_id.shipped_onboard_date,
            'terms_and_conditions': bol_rec_id.terms_and_conditions,
            'reciept_or_deliverytype_at_origin': bol_rec_id.reciept_or_deliverytype_at_origin,
            'reciept_or_deliverytype_at_dest': bol_rec_id.reciept_or_deliverytype_at_dest,
            'cargo_movement_type_at_origin': bol_rec_id.cargo_movement_type_at_origin,
            'cargo_movement_type_at_dest': bol_rec_id.cargo_movement_type_at_dest,
            'issue_date': str(bol_rec_id.issue_date),
            'poi_location_name': bol_rec_id.poi_location_name,
            'poi_un_location_code': bol_rec_id.poi_un_location_code,
            'poi_street_name': bol_rec_id.poi_street_name,
            'poi_street_number': bol_rec_id.poi_street_number,
            'poi_floor': bol_rec_id.poi_floor,
            'poi_post_code': bol_rec_id.poi_post_code,
            'poi_city_name': bol_rec_id.poi_city_name,
            'poi_state_region': bol_rec_id.poi_state_region,
            'poi_country': bol_rec_id.poi_country,
            'received_for_shipment_date': str(bol_rec_id.received_for_shipment_date),
            'service_contract_reference': bol_rec_id.service_contract_reference,
            'declared_value': bol_rec_id.declared_value,
            'declared_value_currency': bol_rec_id.declared_value_currency,
            'issuer_code': bol_rec_id.issuer_code,
            'issuer_code_list_provider': bol_rec_id.issuer_code_list_provider,
            'no_of_rider_pages': bol_rec_id.no_of_rider_pages,
            'document_hash': bol_rec_id.document_hash,
            'planned_arrival_date': str(bol_rec_id.planned_arrival_date),
            'planned_departure_date': str(bol_rec_id.planned_departure_date),
            'pre_carried_by': bol_rec_id.pre_carried_by,
            'por_location_name': bol_rec_id.por_location_name,
            'por_un_location_code': bol_rec_id.por_un_location_code,
            'por_street_name': bol_rec_id.por_street_name,
            'por_street_number': bol_rec_id.por_street_number,
            'por_floor': bol_rec_id.por_floor,
            'por_post_code': bol_rec_id.por_post_code,
            'por_city_name': bol_rec_id.por_city_name,
            'por_state_region': bol_rec_id.por_state_region,
            'por_country': bol_rec_id.por_country,
            'pol_location_name': bol_rec_id.pol_location_name,
            'pol_un_location_code': bol_rec_id.pol_un_location_code,
            'pol_city_name': bol_rec_id.pol_city_name,
            'pol_state_region': bol_rec_id.pol_state_region,
            'pol_country': bol_rec_id.pol_country,
            'pod_location_name': bol_rec_id.pod_location_name,
            'pod_un_location_code': bol_rec_id.pod_un_location_code,
            'pod_city_name': bol_rec_id.pod_city_name,
            'pod_state_region': bol_rec_id.pod_state_region,
            'pod_country': bol_rec_id.pod_country,
            'plod_location_name': bol_rec_id.plod_location_name,
            'plod_un_location_code': bol_rec_id.plod_un_location_code,
            'plod_street_name': bol_rec_id.plod_street_name,
            'plod_street_number': bol_rec_id.plod_street_number,
            'plod_floor': bol_rec_id.plod_floor,
            'plod_post_code': bol_rec_id.plod_post_code,
            'plod_city_name': bol_rec_id.plod_city_name,
            'plod_state_region': bol_rec_id.plod_state_region,
            'plod_country': bol_rec_id.plod_country,
            'oir_location_name': bol_rec_id.oir_location_name,
            'oir_un_location_code': bol_rec_id.oir_un_location_code,
            'oir_street_name': bol_rec_id.oir_street_name,
            'oir_street_number': bol_rec_id.oir_street_number,
            'oir_floor': bol_rec_id.oir_floor,
            'oir_post_code': bol_rec_id.oir_post_code,
            'oir_city_name': bol_rec_id.oir_city_name,
            'oir_state_region': bol_rec_id.oir_state_region,
            'oir_country': bol_rec_id.oir_country,
            'pre_location_name': bol_rec_id.pre_location_name,
            'pre_latitude': bol_rec_id.pre_latitude,
            'pre_longitude': bol_rec_id.pre_longitude,
            'pre_un_location_code': bol_rec_id.pre_un_location_code,
            'pre_street_name': bol_rec_id.pre_street_name,
            'pre_street_number': bol_rec_id.pre_street_number,
            'pre_floor': bol_rec_id.pre_floor,
            'pre_post_code': bol_rec_id.pre_post_code,
            'pre_city_name': bol_rec_id.pre_city_name,
            'pre_state_region': bol_rec_id.pre_state_region,
            'pre_country': bol_rec_id.pre_country
        }
        return bol_parent_vals

    def _create_tl_item_vals(self, tl_item_id):
        tl_vals = {
            'vessel_name': tl_item_id.vessel_name,
            'carrier_voyage_number': tl_item_id.carrier_voyage_number,
            'load_location': tl_item_id.load_location,
            'discharge_location': tl_item_id.discharge_location,
            'mode_of_transport': tl_item_id.mode_of_transport,
        }
        return tl_vals

    def _create_ch_item_vals(self, ch_item_id):
        ch_vals = {
            'charge_type': ch_item_id.charge_type,
            'currency_amount': ch_item_id.currency_amount,
            'currency_code': ch_item_id.currency_code,
            'payment_term': ch_item_id.payment_term,
            'calculation_basis': ch_item_id.calculation_basis,
            'unit_price': ch_item_id.unit_price,
            'quantity': ch_item_id.quantity,
        }
        return ch_vals

    def _schedule_send_bol(self):
        bol_events = []
        # res = []
        bol_event_list = {}
        bol_obj = self.env['bill.of.lading']
        bol_recs = bol_obj.sudo().search([])
        for bol_rec_id in bol_recs:
            # action to get bol parent vals as dict
            bol_parent_vals = self._create_bol_parent_vals(bol_rec_id)
            bol_event_list['parent'] = bol_parent_vals

            # action to get cargo vals as dict
            cargo_child_lst = []
            for c in bol_rec_id.bol_cargo_line:
                cargo_vals = self._create_cargo_item_vals(c)
                cargo_child_lst.append(cargo_vals)
            bol_event_list['cargo'] = cargo_child_lst

            # action to get tq vals as dict
            tq_child_lst = []
            for tq in bol_rec_id.bol_tq_line:
                tq_vals = self._create_tq_item_vals(tq)
                tq_child_lst.append(tq_vals)
            bol_event_list['TransportEquipment'] = tq_child_lst

            # action to get dp vals as dict
            dp_child_lst = []
            for dp in bol_rec_id.bol_dp_line:
                dp_vals = self._create_dp_item_vals(dp)
                dp_child_lst.append(dp_vals)
            bol_event_list['DocumentParties'] = dp_child_lst

            # action to get sl vals as dict
            sl_child_lst = []
            for sl in bol_rec_id.bol_sl_line:
                sl_vals = self._create_sl_item_vals(sl)
                sl_child_lst.append(sl_vals)
            bol_event_list['ShipmentLocations'] = sl_child_lst

            # action to get rc vals as dict
            rc_child_lst = []
            for rc in bol_rec_id.bol_ref_line:
                rc_vals = self._create_rc_item_vals(rc)
                rc_child_lst.append(rc_vals)
            bol_event_list['References'] = rc_child_lst

            # action to get tl vals as dict
            tl_child_lst = []
            for tl in bol_rec_id.transport_leg_line:
                tl_vals = self._create_tl_item_vals(tl)
                tl_child_lst.append(tl_vals)
            bol_event_list['TransportLeg'] = tl_child_lst

            # action to get cc vals as dict
            cc_child_lst = []
            for cc in bol_rec_id.carrier_clauses_line:
                cc_vals = {
                    'clause_content': cc.clause_content,
                }
                cc_child_lst.append(cc_vals)
            bol_event_list['CarrierClauses'] = cc_child_lst

            # action to get ch vals as dict
            ch_child_lst = []
            for ch in bol_rec_id.charges_line:
                ch_vals = self._create_ch_item_vals(ch)
                ch_child_lst.append(ch_vals)
            bol_event_list['Charges'] = ch_child_lst
            # append parent and child vals together to post
            bol_events.append(bol_event_list)
            api_rec = self.env['api.integration'].search([('name', '=', 'post_bol_from_freightbox')])[-1]
            if not api_rec:
                raise ValidationError("API Record does not exist for 'post_bol_from_freightbox'.")
            res = requests.post(api_rec.url, data=json.dumps(bol_events))
        return True

    def import_tnt_cron(self, transports=False):
        _logger.info("\n\n=========================================== CRON START ===========================================\n\n")
        if not transports:
            transports = self.env["transport"].sudo().search([('state', '=', 'confirm'), ('job_id.state', 'not in', ['draft', 'inactive', 'done'])])

        for rec in transports:

            carrier_booking_ref = rec.carrier_booking
            cont_id = rec.cont_id

            api_rec = self.env['api.integration'].sudo().search([('name','=','track_trace_ref')])[-1]
            url = ""
            headers ={}
            eq_response = False
            if api_rec:
                url = str(api_rec.url) + str(carrier_booking_ref)
                headers = {'Tnt-Access-Token': api_rec.token,
                           'username': api_rec.username,
                           'passwd': api_rec.password}

            # url = "https://mother.powerpbox.org/mother_odoo14/get_track_trace_events_gh/%s" % carrier_booking_ref
            # headers = {'Tnt-Access-Token': "447b2d295a113f7c784bf1e7528a76123ab1a6d0",
            #            'username': "indra",
            #            'passwd': "indra"}
                eq_response = requests.get(url, headers=headers)
                print("eq_response-----------------------------------------", eq_response.status_code)
            if eq_response and eq_response.status_code == 200:
                equip = json.loads(eq_response.content)
                tnt_obj = self.env['track.trace.event']
                track_equipment_event = self.env['track.equipment.event']
                track_transport_event = self.env['track.transport.event']

                if 'Datas' in equip:
                    track_trace_event_id = tnt_obj.sudo().search([('carrier_booking', '=', carrier_booking_ref),('transport_id', '=', rec.id)], order="id desc", limit=1)
                    if not track_trace_event_id:
                        track_trace_event_id = tnt_obj.sudo().create({'carrier_booking': carrier_booking_ref, 'transport_id': rec.id})
                    _logger.info("\n\n Track Trace Event : %s " % track_trace_event_id)

                    for eq in equip['Datas'][0]['eq']:
                        _logger.info("EQ : %s" % eq)
                        import datetime
                        print("eq['event_created_datetime']", eq['event_created_datetime'])
                        if len(eq['event_created_datetime']) > 20:
                            event_created_datetime = datetime.datetime.strptime(eq['event_created_datetime'],
                                                                                "%Y-%m-%d %H:%M:%S.%f")
                        else:
                            event_created_datetime = eq['event_created_datetime']
                        if len(eq['event_datetime']) > 20:
                            final_event_datetime = datetime.datetime.strptime(eq['event_datetime'],
                                                                              "%Y-%m-%d %H:%M:%S.%f")
                        else:
                            final_event_datetime = eq['event_datetime']
                        equipment_event_occured = False
                        if eq['event_classifier_code'] == 'ACT':
                            equipment_event_occured = True
                        equip_events_vals = {
                            'track_trace_event_id': track_trace_event_id.id,
                            'equip_event_type_code': eq['equip_event_type_code'],
                            'equip_event_id': eq['equip_event_id'],
                            'event_created_datetime': event_created_datetime,
                            'event_classifier_code': eq['event_classifier_code'] or 'ACT',
                            'event_datetime': final_event_datetime,
                            'transport_call': eq['transport_call'],
                            'equip_reference': eq['equip_reference'],
                            'iso_equip_code': eq['iso_equip_code'],
                            'empty_indicator_code': eq['empty_indicator_code'],
                            'event_type': eq['event_type'],
                            'event_description': eq['event_description'],
                            'locode': eq['locode'],
                            'location_name': eq['location_name'],
                            'country': eq['country'],
                            'timezone': eq['timezone'],
                            'latitude': eq['latitude'],
                            'longitude': eq['longitude'],
                            'event_location': eq['location_name'],
                            'equipment_event_occured': equipment_event_occured
                        }
                        track_eq_event = track_equipment_event.sudo().search([('equip_reference', '=', eq['equip_reference']),
                                                                              ('locode', '=', eq['locode']),
                                                                              ('equip_event_type_code', '=', eq['equip_event_type_code'])],
                                                                             order="id asc", limit=1)
                        if not track_eq_event:
                            track_eq_event = track_equipment_event.sudo().search(
                                [('equip_reference', '=', eq['equip_reference']),
                                 ('event_location', '=', eq['event_location']),
                                 ('equip_event_type_code', '=', eq['equip_event_type_code'])],
                                order="id asc", limit=1)
                        if track_eq_event:
                            track_eq_event.sudo().write(equip_events_vals)
                        else:
                            if eq['equip_reference'] == rec.cont_id:
                                track_equipment_event.sudo().create(equip_events_vals)

                    for transport in equip['Datas'][0]['transport']:
                        _logger.info("\n\nTransport : %s" % transport)
                        import datetime
                        if len(transport['event_created_datetime']) > 20:
                            event_created_datetime = datetime.datetime.strptime(transport['event_created_datetime'],
                                                                                "%Y-%m-%d %H:%M:%S.%f")
                        else:
                            event_created_datetime = transport['event_created_datetime']
                        if len(transport['event_datetime']) > 20:
                            final_event_datetime = datetime.datetime.strptime(transport['event_datetime'],
                                                                              "%Y-%m-%d %H:%M:%S.%f")
                        else:
                            final_event_datetime = transport['event_datetime']
                        transport_event_occured = False
                        if transport['event_classifier_code'] == 'ACT':
                            transport_event_occured = True
                        transport_events_vals = {
                            'track_trace_event_id': track_trace_event_id.id,
                            'transport_event_type_code': transport['transport_event_type_code'],
                            'transport_event_id': transport['transport_event_id'],
                            'event_created_datetime': event_created_datetime,
                            'event_classifier_code': transport['event_classifier_code'] or 'ACT',
                            'event_datetime': final_event_datetime,
                            'delay_reason': transport['delay_reason'],
                            'change_remark': transport['change_remark'],
                            'transport_call_id': transport['transport_call_id'],
                            'carrier_service_code': transport['carrier_service_code'],
                            'carrier_voyage_number': transport['carrier_voyage_number'],
                            'un_location_code': transport['un_location_code'],
                            'mode_of_transport_code': transport['mode_of_transport_code'],
                            'vessel_imo_number': transport['vessel_imo_number'],
                            'vessel_name': transport['vessel_name'],
                            'vessel_operator_carrier_code': transport['vessel_operator_carrier_code'],
                            'vessel_operator_carrier_code_list_provider': transport['vessel_operator_carrier_code_list_provider'],
                            'container_id': transport['container_id'],
                            'event_type': transport['event_type'],
                            'event_description': transport['event_description'],
                            'locode': transport['locode'],
                            'location_name': transport['location_name'],
                            'country': transport['country'],
                            'timezone': transport['timezone'],
                            'latitude': transport['latitude'],
                            'longitude': transport['longitude'],
                            'location': transport['location'],
                            'transport_event_occured': transport_event_occured
                        }
                        track_transport_event_rec = track_transport_event.sudo().search(
                            [('container_id', '=', transport['container_id']),
                             ('locode', '=', transport['locode']),
                             ('transport_event_type_code', '=', transport['transport_event_type_code']),],
                            order="id", limit=1)
                        if not track_transport_event_rec:
                            track_transport_event_rec = track_transport_event.sudo().search(
                                [('container_id', '=', transport['container_id']),
                                 ('location', '=', transport['location']),
                                 ('transport_event_type_code', '=', transport['transport_event_type_code'])],
                                order="id", limit=1)
                        if track_transport_event_rec:
                            track_transport_event_rec.sudo().write(transport_events_vals)
                        else:
                            if rec.cont_id == transport['container_id']:
                                track_transport_event.sudo().create(transport_events_vals)
                    track_trace_event_id.onchange_transport_event_code()
                else:
                    # print("ELSE:", equip)
                    # raise UserError(_(equip['message']))
                    _logger.info(
                        "\n\n=========================================== CRON FINISH 1 ===========================================\n\n")
                    # return/
                    continue
            else:
                # resp = eq_response.text
                # raise UserError(resp)
                _logger.info(
                    "\n\n=========================================== CRON FINISH 2 ===========================================\n\n")
                # return
                continue
        _logger.info(
            "\n\n=========================================== CRON FINISH 3===========================================\n\n")

    # def Freight_video_corn(self):
    #     # job_recs = self.env['job'].sudo().search([])
    #     # dbuuid = self.env['ir.config_parameter'].sudo().get_param('database.uuid')
    #     # username = Hostname + '_' + dbuuid
    #     parent_vals = {
    #                     "jsonrpc":"2.0",
                          
    #                 }
    #     headers = {
    #         'Content-Type': 'application/json',
    #         'Accept': 'application/json',
    #     }

    #     # job_events.append(parent_vals)
    #     url = 'http://192.168.1.5:1114/api/get_video_link'
    #     response = requests.request("POST",url,headers=headers,params=json.dumps(parent_vals))
    #     print("--------------------- res",response)


    #     response = requests.post("http://127.0.0.1:1114/api/get_video_link",
    #                         params=parent_vals)
    #     print("--------------------- res",response)

    #     return response