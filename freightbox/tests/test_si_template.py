# # -*- coding: utf-8 -*-
# # Part of Odoo. See LICENSE file for full copyright and licensing details.

# from odoo.tests import common
# from odoo import fields
# from odoo.tests import tagged, Form
# import logging

# _logger = logging.getLogger(__name__)

# class TestSiTemplate(common.TransactionCase):

#     @classmethod
#     def setUpClass(cls):
#         super(TestSiTemplate, cls).setUpClass()

#     def test_compare_inquiry_no(self):
#         lead = self.env['shipping.instruction'].browse(11)
#         # print("??????????????????????????????????????????LEAD",lead.cargo_items_line.cargo_line_items_id)
#         print("LLLLLLLLLLLLLLLLLLLLLLL", lead)

#         print("CCCCCCCCCCCCCCCCC", lead.cargo_items_line)
#         for si_cl, si_template_cl in zip(lead.cargo_items_line, lead.si_templates.si_template_cargo_items_line):
#             self.assertEqual(si_cl.cargo_line_items_id,si_template_cl.cargo_line_items_id)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare cargo line item id's is successful")
#             self.assertEqual(si_cl.shipping_marks,si_template_cl.shipping_marks)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::shipping_marks is successful")
#             self.assertEqual(si_cl.carrier_booking_reference,si_template_cl.carrier_booking_reference)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare carrier_booking_reference is successful")
#             self.assertEqual(si_cl.description_of_goods,si_template_cl.description_of_goods)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare description_of_goods is successful")
#             self.assertEqual(si_cl.hs_code,si_template_cl.hs_code)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare hs_code is successful")
#             self.assertEqual(si_cl.number_of_packages,si_template_cl.number_of_packages)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare number_of_packages is successful")
#             self.assertEqual(si_cl.weight,si_template_cl.weight)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare weight is successful")
#             self.assertEqual(si_cl.volume,si_template_cl.volume)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare volume is successful")
#             self.assertEqual(si_cl.weight_unit,si_template_cl.weight_unit)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare weight_unit is successful")
#             self.assertEqual(si_cl.volume_unit,si_template_cl.volume_unit)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare volume_unit is successful")
#             self.assertEqual(si_cl.package_code,si_template_cl.package_code)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare package_code is successful")
#             # self.assertEqual(si_cl.equipment_reference,si_template_cl.equipment_reference)
#             # print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare equipment_reference is successful")

#         for si_tr, si_template_tr in zip(lead.transport_equipment_line, lead.si_templates.si_template_transport_equipment_line):
#             # self.assertEqual(si_tr.equipment_reference_id,si_template_tr.equipment_reference_id)
#             # print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare equipment_reference_id is successful")
#             self.assertEqual(si_tr.weight_unit,si_template_tr.weight_unit)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare weight_unit is successful")
#             self.assertEqual(si_tr.cargo_gross_weight,si_template_tr.cargo_gross_weight)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare cargo_gross_weight is successful")
#             self.assertEqual(si_tr.container_tare_weight,si_template_tr.container_tare_weight)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare container_tare_weight is successful")
#             self.assertEqual(si_tr.iso_equipment_code,si_template_tr.iso_equipment_code)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare iso_equipment_code is successful")
#             self.assertEqual(si_tr.is_shipper_owned,si_template_tr.is_shipper_owned)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare is_shipper_owned is successful")
#             self.assertEqual(si_tr.temperature_min,si_template_tr.temperature_min)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare temperature_min is successful")
#             self.assertEqual(si_tr.temperature_max,si_template_tr.temperature_max)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare temperature_max is successful")
#             self.assertEqual(si_tr.temperature_unit,si_template_tr.temperature_unit)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare temperature_unit is successful")
#             self.assertEqual(si_tr.humidity_min,si_template_tr.humidity_min)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare humidity_min is successful")
#             self.assertEqual(si_tr.humidity_max,si_template_tr.humidity_max)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare humidity_max is successful")
#             self.assertEqual(si_tr.ventilation_min,si_template_tr.ventilation_min)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare ventilation_min is successful")
#             self.assertEqual(si_tr.ventilation_max,si_template_tr.ventilation_max)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare ventilation_max is successful")
#             self.assertEqual(si_tr.seal_number,si_template_tr.seal_number)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare seal_number is successful")
#             self.assertEqual(si_tr.seal_source,si_template_tr.seal_source)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare seal_source is successful")
#             self.assertEqual(si_tr.seal_type,si_template_tr.seal_type)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare seal_type is successful")
            
#         for si_dp, si_template_dp in zip(lead.document_parties_line, lead.si_templates.si_template_document_parties_line):
#             self.assertEqual(si_dp.party_name_id,si_template_dp.party_name_id)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare party_name_id is successful")
#             self.assertEqual(si_dp.tax_reference_1,si_template_dp.tax_reference_1)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare tax_reference_1 is successful")
#             self.assertEqual(si_dp.public_key,si_template_dp.public_key)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare public_key is successful")
#             self.assertEqual(si_dp.street,si_template_dp.street)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare street is successful")
#             self.assertEqual(si_dp.street_number,si_template_dp.street_number)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare street_number is successful")
#             self.assertEqual(si_dp.floor,si_template_dp.floor)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare floor is successful")
#             self.assertEqual(si_dp.post_code,si_template_dp.post_code)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare post_code is successful")
#             self.assertEqual(si_dp.city,si_template_dp.city)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare city is successful")
#             self.assertEqual(si_dp.state_region,si_template_dp.state_region)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare state_region is successful")
#             self.assertEqual(si_dp.country,si_template_dp.country)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare country is successful")
#             self.assertEqual(si_dp.tax_reference_2,si_template_dp.tax_reference_2)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare tax_reference_2 is successful")
#             self.assertEqual(si_dp.nmfta_code,si_template_dp.nmfta_code)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare nmfta_code is successful")
#             self.assertEqual(si_dp.party_function,si_template_dp.party_function)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare party_function is successful")
#             self.assertEqual(si_dp.address_line,si_template_dp.address_line)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare address_line is successful")
#             self.assertEqual(si_dp.name,si_template_dp.name)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare name is successful")
#             self.assertEqual(si_dp.email,si_template_dp.email)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare email is successful")
#             self.assertEqual(si_dp.phone,si_template_dp.phone)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare phone is successful")
#             self.assertEqual(si_dp.is_to_be_notified,si_template_dp.is_to_be_notified)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare is_to_be_notified is successful")

#         for si_sl, si_template_sl in zip(lead.shipment_location_line, lead.si_templates.si_template_shipment_location_line):
#             self.assertEqual(si_sl.location_type,si_template_sl.location_type)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare location_type is successful")
#             self.assertEqual(si_sl.location_name,si_template_sl.location_name)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare location_name is successful")
#             self.assertEqual(si_sl.latitude,si_template_sl.latitude)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare latitude is successful")
#             self.assertEqual(si_sl.longitude,si_template_sl.longitude)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare longitude is successful")
#             self.assertEqual(si_sl.un_location_code,si_template_sl.un_location_code)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare un_location_code is successful")
#             self.assertEqual(si_sl.street_name,si_template_sl.street_name)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare street_name is successful")
#             self.assertEqual(si_sl.street_number,si_template_sl.street_number)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare street_number is successful")
#             self.assertEqual(si_sl.floor,si_template_sl.floor)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare floor is successful")
#             self.assertEqual(si_sl.post_code,si_template_sl.post_code)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare post_code is successful")
#             self.assertEqual(si_sl.city_name,si_template_sl.city_name)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare city_name is successful")
#             self.assertEqual(si_sl.state_region,si_template_sl.state_region)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare state_region is successful")
#             self.assertEqual(si_sl.country,si_template_sl.country)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare country is successful")
#             self.assertEqual(si_sl.displayed_name,si_template_sl.displayed_name)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare displayed_name is successful")

#         for si_rf, si_template_rf in zip(lead.references_line, lead.si_templates.si_template_references_line):
#             self.assertEqual(si_rf.reference_type,si_template_rf.reference_type)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare reference_type is successful")
#             self.assertEqual(si_rf.reference_value,si_template_rf.reference_value)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare reference_value is successful")
            