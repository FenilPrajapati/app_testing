# # -*- coding: utf-8 -*-
# # Part of Odoo. See LICENSE file for full copyright and licensing details.

# from odoo.tests import common
# from odoo import fields
# from odoo.tests import tagged, Form
# import logging

# _logger = logging.getLogger(__name__)

# class TestBolTemplate(common.TransactionCase):

#     @classmethod
#     def setUpClass(cls):
#         super(TestBolTemplate, cls).setUpClass()

#     def test_compare_bol_template(self):
#         bol = self.env['bill.of.lading'].browse(3)
        
#         try:
#             self.assertEqual(bol.carrier_booking_reference,bol.bol_templates.carrier_booking_reference)
#             _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare carrier_booking_reference is successful")
#         except:
#             _logger.warning(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare carrier_booking_reference is not successful")

#         self.assertEqual(bol.transport_document_type_code,bol.bol_templates.transport_document_type_code)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare transport_document_type_code is successful")

#         self.assertEqual(bol.number_of_originals,bol.bol_templates.number_of_originals)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare number_of_originals is successful")

#         self.assertEqual(bol.number_of_copies,bol.bol_templates.number_of_copies)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare number_of_copies is successful")

#         self.assertEqual(bol.is_electronic,bol.bol_templates.is_electronic)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare is_electronic is successful")

#         self.assertEqual(bol.is_charges_displayed,bol.bol_templates.is_charges_displayed)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare is_charges_displayed is successful")

#         self.assertEqual(bol.location_name,bol.bol_templates.location_name)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare location_name is successful")

#         self.assertEqual(bol.un_location_code,bol.bol_templates.un_location_code)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare un_location_code is successful")

#         self.assertEqual(bol.city_name,bol.bol_templates.city_name)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare city_name is successful")

#         self.assertEqual(bol.state_region,bol.bol_templates.state_region)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare state_region is successful")

#         self.assertEqual(bol.country,bol.bol_templates.country)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare country is successful")

#         self.assertEqual(bol.shipping_instruction_ID,bol.bol_templates.shipping_instruction_ID)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare shipping_instruction_ID is successful")

#         self.assertEqual(bol.transport_document_reference,bol.bol_templates.transport_document_reference)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare transport_document_reference is successful")

#         self.assertEqual(bol.shipped_onboard_date,bol.bol_templates.shipped_onboard_date)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare shipped_onboard_date is successful")

#         self.assertEqual(bol.terms_and_conditions,bol.bol_templates.terms_and_conditions)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare terms_and_conditions is successful")

#         self.assertEqual(bol.reciept_or_deliverytype_at_origin,bol.bol_templates.reciept_or_deliverytype_at_origin)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare reciept_or_deliverytype_at_origin is successful")

#         self.assertEqual(bol.reciept_or_deliverytype_at_dest,bol.bol_templates.reciept_or_deliverytype_at_dest)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare reciept_or_deliverytype_at_dest is successful")

#         self.assertEqual(bol.cargo_movement_type_at_origin,bol.bol_templates.cargo_movement_type_at_origin)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare cargo_movement_type_at_origin is successful")

#         self.assertEqual(bol.cargo_movement_type_at_dest,bol.bol_templates.cargo_movement_type_at_dest)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare cargo_movement_type_at_dest is successful")

#         self.assertEqual(bol.issue_date,bol.bol_templates.issue_date)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare issue_date is successful")

#         self.assertEqual(bol.poi_location_name,bol.bol_templates.poi_location_name)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare poi_location_name is successful")

#         self.assertEqual(bol.poi_un_location_code,bol.bol_templates.poi_un_location_code)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare poi_un_location_code is successful")

#         self.assertEqual(bol.poi_street_name,bol.bol_templates.poi_street_name)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare poi_street_name is successful")

#         self.assertEqual(bol.poi_street_number,bol.bol_templates.poi_street_number)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare poi_street_number is successful")

#         self.assertEqual(bol.poi_floor,bol.bol_templates.poi_floor)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare poi_floor is successful")

#         self.assertEqual(bol.poi_post_code,bol.bol_templates.poi_post_code)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare poi_post_code is successful")

#         self.assertEqual(bol.poi_state_region,bol.bol_templates.poi_state_region)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare poi_state_region is successful")

#         self.assertEqual(bol.poi_country,bol.bol_templates.poi_country)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare poi_country is successful")

#         self.assertEqual(bol.received_for_shipment_date,bol.bol_templates.received_for_shipment_date)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare received_for_shipment_date is successful")

#         self.assertEqual(bol.service_contract_reference,bol.bol_templates.service_contract_reference)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare service_contract_reference is successful")

#         self.assertEqual(bol.declared_value,bol.bol_templates.declared_value)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare declared_value is successful")

#         self.assertEqual(bol.declared_value_currency,bol.bol_templates.declared_value_currency)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare declared_value_currency is successful")

#         self.assertEqual(bol.issuer_code,bol.bol_templates.issuer_code)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare issuer_code is successful")

#         self.assertEqual(bol.issuer_code_list_provider,bol.bol_templates.issuer_code_list_provider)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare issuer_code_list_provider is successful")

#         self.assertEqual(bol.no_of_rider_pages,bol.bol_templates.no_of_rider_pages)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare no_of_rider_pages is successful")

#         self.assertEqual(bol.binary_copy,bol.bol_templates.binary_copy)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare binary_copy is successful")

#         self.assertEqual(bol.document_hash,bol.bol_templates.document_hash)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare document_hash is successful")

#         self.assertEqual(bol.planned_arrival_date,bol.bol_templates.planned_arrival_date)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare planned_arrival_date is successful")

#         self.assertEqual(bol.planned_departure_date,bol.bol_templates.planned_departure_date)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare planned_departure_date is successful")

#         self.assertEqual(bol.pre_carried_by,bol.bol_templates.pre_carried_by)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare pre_carried_by is successful")

#         self.assertEqual(bol.por_location_name,bol.bol_templates.por_location_name)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare por_location_name is successful")

#         self.assertEqual(bol.por_un_location_code,bol.bol_templates.por_un_location_code)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare por_un_location_code is successful")

#         self.assertEqual(bol.por_street_name,bol.bol_templates.por_street_name)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare por_street_name is successful")

#         self.assertEqual(bol.por_street_number,bol.bol_templates.por_street_number)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare por_street_number is successful")

#         self.assertEqual(bol.por_floor,bol.bol_templates.por_floor)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare por_floor is successful")

#         self.assertEqual(bol.por_post_code,bol.bol_templates.por_post_code)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare por_post_code is successful")

#         self.assertEqual(bol.por_city_name,bol.bol_templates.por_city_name)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare por_city_name is successful")

#         self.assertEqual(bol.por_state_region,bol.bol_templates.por_state_region)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare por_state_region is successful")

#         self.assertEqual(bol.por_country,bol.bol_templates.por_country)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare por_country is successful")

#         self.assertEqual(bol.pol_location_name,bol.bol_templates.pol_location_name)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare pol_location_name is successful")

#         self.assertEqual(bol.pol_un_location_code,bol.bol_templates.pol_un_location_code)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare pol_un_location_code is successful")

#         self.assertEqual(bol.pol_city_name,bol.bol_templates.pol_city_name)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare pol_city_name is successful")

#         self.assertEqual(bol.pol_state_region,bol.bol_templates.pol_state_region)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare pol_state_region is successful")

#         self.assertEqual(bol.pol_country,bol.bol_templates.pol_country)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare pol_country is successful")

#         self.assertEqual(bol.pod_location_name,bol.bol_templates.pod_location_name)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare pod_location_name is successful")

#         self.assertEqual(bol.pod_un_location_code,bol.bol_templates.pod_un_location_code)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare pod_un_location_code is successful")

#         self.assertEqual(bol.pod_city_name,bol.bol_templates.pod_city_name)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare pod_city_name is successful")

#         self.assertEqual(bol.pod_state_region,bol.bol_templates.pod_state_region)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare pod_state_region is successful")

#         self.assertEqual(bol.pod_country,bol.bol_templates.pod_country)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare pod_country is successful")

#         self.assertEqual(bol.plod_location_name,bol.bol_templates.plod_location_name)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare plod_location_name is successful")

#         self.assertEqual(bol.plod_un_location_code,bol.bol_templates.plod_un_location_code)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare plod_un_location_code is successful")

#         self.assertEqual(bol.plod_street_name,bol.bol_templates.plod_street_name)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare plod_street_name is successful")

#         self.assertEqual(bol.plod_street_number,bol.bol_templates.plod_street_number)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare plod_street_number is successful")

#         self.assertEqual(bol.plod_floor,bol.bol_templates.plod_floor)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare plod_floor is successful")

#         self.assertEqual(bol.plod_post_code,bol.bol_templates.plod_post_code)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare plod_post_code is successful")

#         self.assertEqual(bol.plod_city_name,bol.bol_templates.plod_city_name)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare plod_city_name is successful")

#         self.assertEqual(bol.plod_state_region,bol.bol_templates.plod_state_region)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare plod_state_region is successful")

#         self.assertEqual(bol.plod_country,bol.bol_templates.plod_country)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare plod_country is successful")

#         self.assertEqual(bol.oir_location_name,bol.bol_templates.oir_location_name)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare oir_location_name is successful")

#         self.assertEqual(bol.oir_un_location_code,bol.bol_templates.oir_un_location_code)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare oir_un_location_code is successful")

#         self.assertEqual(bol.oir_street_name,bol.bol_templates.oir_street_name)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare oir_street_name is successful")

#         self.assertEqual(bol.oir_street_number,bol.bol_templates.oir_street_number)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare oir_street_number is successful")

#         self.assertEqual(bol.oir_floor,bol.bol_templates.oir_floor)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare oir_floor is successful")

#         self.assertEqual(bol.oir_post_code,bol.bol_templates.oir_post_code)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare oir_post_code is successful")

#         self.assertEqual(bol.oir_city_name,bol.bol_templates.oir_city_name)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare oir_city_name is successful")

#         self.assertEqual(bol.oir_state_region,bol.bol_templates.oir_state_region)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare oir_state_region is successful")

#         self.assertEqual(bol.oir_country,bol.bol_templates.oir_country)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare oir_country is successful")

#         self.assertEqual(bol.pre_location_name,bol.bol_templates.pre_location_name)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare pre_location_name is successful")

#         self.assertEqual(bol.pre_latitude,bol.bol_templates.pre_latitude)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare pre_latitude is successful")

#         self.assertEqual(bol.pre_longitude,bol.bol_templates.pre_longitude)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare pre_longitude is successful")

#         self.assertEqual(bol.pre_un_location_code,bol.bol_templates.pre_un_location_code)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare pre_un_location_code is successful")

#         self.assertEqual(bol.pre_street_name,bol.bol_templates.pre_street_name)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare pre_street_name is successful")

#         self.assertEqual(bol.pre_street_number,bol.bol_templates.pre_street_number)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare pre_street_number is successful")

#         self.assertEqual(bol.pre_floor,bol.bol_templates.pre_floor)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare pre_floor is successful")

#         self.assertEqual(bol.pre_post_code,bol.bol_templates.pre_post_code)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare pre_post_code is successful")

#         self.assertEqual(bol.pre_city_name,bol.bol_templates.pre_city_name)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare pre_city_name is successful")

#         self.assertEqual(bol.pre_state_region,bol.bol_templates.pre_state_region)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare pre_state_region is successful")

#         self.assertEqual(bol.pre_country,bol.bol_templates.pre_country)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare pre_country is successful")