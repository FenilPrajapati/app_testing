from odoo import http
from odoo.http import request


class BolApi(http.Controller):
    _name = 'bol.api'

    @http.route(['/api/send_bol_datas'], type='json', auth='none', csrf=False)
    def api_all_bol_datas(self, **kwargs):
        data = request.jsonrequest
        bol_dict = {}
        BillOfLading = request.env['bill.of.lading']
        carrier_booking_reference = data.get('carrier_booking_reference')
        request._cr.execute("SELECT id FROM bill_of_lading WHERE "
                            "carrier_booking_reference='%s'" % carrier_booking_reference)
        bol_recs = request._cr.fetchall()
        if not bol_recs:
            return {'status': "No data found in the client system"}
        if bol_recs:
            parent_vals = []
            for rec in bol_recs:
                bill_of_lading = BillOfLading.sudo().browse(rec[0])
                parent_col_vals = {
                    'parent_id': False,
                    'bol_id': bill_of_lading.id,
                    'transport_document_type_code': bill_of_lading.transport_document_type_code,
                    'number_of_originals': bill_of_lading.number_of_originals,
                    'number_of_copies': bill_of_lading.number_of_copies,
                    'pre_carriage_under_shippers_responsibility':
                        bill_of_lading.pre_carriage_under_shippers_responsibility,
                    'carrier_booking_reference': bill_of_lading.carrier_booking_reference,
                    'is_electronic': bill_of_lading.is_electronic,
                    'is_charges_displayed': bill_of_lading.is_charges_displayed,
                    'location_name': bill_of_lading.location_name,
                    'un_location_code': bill_of_lading.un_location_code,
                    'city_name': bill_of_lading.city_name,
                    'state_region': bill_of_lading.state_region,
                    'country': bill_of_lading.country,
                    'shipping_instruction_ID': bill_of_lading.shipping_instruction_ID,
                    'transport_document_reference': bill_of_lading.transport_document_reference,
                    'shipped_onboard_date': bill_of_lading.shipped_onboard_date,
                    'terms_and_conditions': bill_of_lading.terms_and_conditions,
                    'reciept_or_deliverytype_at_origin': bill_of_lading.reciept_or_deliverytype_at_origin,
                    'reciept_or_deliverytype_at_dest': bill_of_lading.reciept_or_deliverytype_at_dest,
                    'cargo_movement_type_at_origin': bill_of_lading.cargo_movement_type_at_origin,
                    'cargo_movement_type_at_dest': bill_of_lading.cargo_movement_type_at_dest,
                    'issue_date': bill_of_lading.issue_date,
                    'poi_location_name': bill_of_lading.poi_location_name,
                    'poi_un_location_code': bill_of_lading.poi_un_location_code,
                    'poi_street_name': bill_of_lading.poi_street_name,
                    'poi_street_number': bill_of_lading.poi_street_number,
                    'poi_floor': bill_of_lading.poi_floor,
                    'poi_post_code': bill_of_lading.poi_post_code,
                    'poi_city_name': bill_of_lading.poi_city_name,
                    'poi_state_region': bill_of_lading.poi_state_region,
                    'poi_country': bill_of_lading.poi_country,
                    'received_for_shipment_date': bill_of_lading.received_for_shipment_date,
                    'service_contract_reference': bill_of_lading.service_contract_reference,
                    'declared_value': bill_of_lading.declared_value,
                    'declared_value_currency': bill_of_lading.declared_value_currency,
                    'issuer_code': bill_of_lading.issuer_code,
                    'issuer_code_list_provider': bill_of_lading.issuer_code_list_provider,
                    'no_of_rider_pages': bill_of_lading.no_of_rider_pages,
                    'document_hash': bill_of_lading.document_hash,
                    'planned_arrival_date': bill_of_lading.planned_arrival_date,
                    'planned_departure_date': bill_of_lading.planned_departure_date,
                    'pre_carried_by': bill_of_lading.pre_carried_by,
                    'por_location_name': bill_of_lading.por_location_name,
                    'por_un_location_code': bill_of_lading.por_un_location_code,
                    'por_street_name': bill_of_lading.por_street_name,
                    'por_street_number': bill_of_lading.por_street_number,
                    'por_floor': bill_of_lading.por_floor,
                    'por_post_code': bill_of_lading.por_post_code,
                    'por_city_name': bill_of_lading.por_city_name,
                    'por_state_region': bill_of_lading.por_state_region,
                    'por_country': bill_of_lading.por_country,
                    'pol_location_name': bill_of_lading.pol_location_name,
                    'pol_un_location_code': bill_of_lading.pol_un_location_code,
                    'pol_city_name': bill_of_lading.pol_city_name,
                    'pol_state_region': bill_of_lading.pol_state_region,
                    'pol_country': bill_of_lading.pol_country,
                    'pod_location_name': bill_of_lading.pod_location_name,
                    'pod_un_location_code': bill_of_lading.pod_un_location_code,
                    'pod_city_name': bill_of_lading.pod_city_name,
                    'pod_state_region': bill_of_lading.pod_state_region,
                    'pod_country': bill_of_lading.pod_country,
                    'plod_location_name': bill_of_lading.plod_location_name,
                    'plod_un_location_code': bill_of_lading.plod_un_location_code,
                    'plod_street_name': bill_of_lading.plod_street_name,
                    'plod_street_number': bill_of_lading.plod_street_number,
                    'plod_floor': bill_of_lading.plod_floor,
                    'plod_post_code': bill_of_lading.plod_post_code,
                    'plod_city_name': bill_of_lading.plod_city_name,
                    'plod_state_region': bill_of_lading.plod_state_region,
                    'plod_country': bill_of_lading.plod_country,
                    'oir_location_name': bill_of_lading.oir_location_name,
                    'oir_un_location_code': bill_of_lading.oir_un_location_code,
                    'oir_street_name': bill_of_lading.oir_street_name,
                    'oir_street_number': bill_of_lading.oir_street_number,
                    'oir_floor': bill_of_lading.oir_floor,
                    'oir_post_code': bill_of_lading.oir_post_code,
                    'oir_city_name': bill_of_lading.oir_city_name,
                    'oir_state_region': bill_of_lading.oir_state_region,
                    'oir_country': bill_of_lading.oir_country,
                    'pre_location_name': bill_of_lading.pre_location_name,
                    'pre_latitude': bill_of_lading.pre_latitude,
                    'pre_longitude': bill_of_lading.pre_longitude,
                    'pre_un_location_code': bill_of_lading.pre_un_location_code,
                    'pre_street_name': bill_of_lading.pre_street_name,
                    'pre_street_number': bill_of_lading.pre_street_number,
                    'pre_floor': bill_of_lading.pre_floor,
                    'pre_post_code': bill_of_lading.pre_post_code,
                    'pre_city_name': bill_of_lading.pre_city_name,
                    'pre_state_region': bill_of_lading.pre_state_region,
                    'pre_country': bill_of_lading.pre_country,
                    'is_master_bill_of_lading': True,
                }
                parent_vals.append(parent_col_vals)
                CargoTableColData = []
                cl_list = []
                for c in bill_of_lading.bol_cargo_line:
                    CargoTableColData = {
                        'parent_id': bill_of_lading.id,
                        'bol_cargo_line_id': bill_of_lading.id,
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
                    }
                    cl_list.append(CargoTableColData)
                TransportEquipmentTableColData = []
                tq_list = []
                for tq in bill_of_lading.bol_tq_line:
                    TransportEquipmentTableColData = {
                        'parent_id': bill_of_lading.id,
                        'bol_tq_line_id': bill_of_lading.id,
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
                    }
                    tq_list.append(TransportEquipmentTableColData)
                dp_list = []
                for dp in bill_of_lading.bol_dp_line:
                    DocumentPartiesTableColData = {
                        'parent_id': bill_of_lading.id,
                        'bol_dp_line_id': bill_of_lading.id,
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
                    }
                    dp_list.append(DocumentPartiesTableColData)
                sl_list = []
                for sl in bill_of_lading.bol_sl_line:
                    ShipmentLocationsTableColData = {
                        'parent_id': bill_of_lading.id,
                        'bol_sl_line_id': bill_of_lading.id,
                        'location_type': sl.location_type.name,
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
                    }
                    sl_list.append(ShipmentLocationsTableColData)
                rc_list = []
                for rc in bill_of_lading.bol_ref_line:
                    ReferencesTableColData = {
                        'parent_id': bill_of_lading.id,
                        'bol_ref_line_id': bill_of_lading.id,
                        'reference_type': rc.reference_type,
                        'reference_value': rc.reference_value,
                    }
                    rc_list.append(ReferencesTableColData)
                tl_list = []
                for tl in bill_of_lading.transport_leg_line:
                    TransportLegColData = {
                        'parent_id': bill_of_lading.id,
                        'transportleg_line_id': bill_of_lading.id,
                        'vessel_name': tl.vessel_name,
                        'carrier_voyage_number': tl.carrier_voyage_number,
                        'load_location': tl.load_location,
                        'discharge_location': tl.discharge_location,
                        'mode_of_transport': tl.mode_of_transport,
                    }
                    tl_list.append(TransportLegColData)
                cc_list = []
                for cc in bill_of_lading.carrier_clauses_line:
                    CarrierClausesColData = {
                        'parent_id': bill_of_lading.id,
                        'carrier_clauses_line_id': bill_of_lading.id,
                        'clause_content': cc.clause_content,
                    }
                    cc_list.append(CarrierClausesColData)
                ch_list = []
                for ch in bill_of_lading.charges_line:
                    ChargesColData = {
                        'parent_id': bill_of_lading.id,
                        'charges_line_id': bill_of_lading.id,
                        'charge_type': ch.charge_type,
                        'currency_amount': ch.currency_amount,
                        'currency_code': ch.currency_code,
                        'payment_term': ch.payment_term,
                        'calculation_basis': ch.calculation_basis,
                        'unit_price': ch.unit_price,
                        'quantity': ch.quantity,
                    }
                    ch_list.append(ChargesColData)
            bol_parent_child_dict = {
                'parent_vals': parent_vals,
                'cargo_vals': cl_list,
                'tq_vals': tq_list,
                'dp_vals': dp_list,
                'sl_vals': sl_list,
                'rc_vals': rc_list,
                'tl_vals': tl_list,
                'cc_vals': cc_list,
                'ch_vals': ch_list,
            }
            bol_dict = {
                'parent_bol': bol_parent_child_dict,
            }
        return bol_dict
