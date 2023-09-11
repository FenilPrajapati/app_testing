# # -*- coding: utf-8 -*-
# # Part of Odoo. See LICENSE file for full copyright and licensing details.

# from odoo.tests import common
# from odoo import fields
# from odoo.tests import tagged, Form
# from odoo.addons.crm.tests.common import TestCrmCommon
# import logging

# _logger = logging.getLogger(__name__)

# # from odoo.powerpbox_modules.freightbox.models import request_for_quote
# # from odoo.powerpbox_modules.freightbox.models.request_for_quote import RequestForQuote

# class TestRc(TestCrmCommon):

#     @classmethod
#     def setUpClass(cls):
#         super(TestRc, cls).setUpClass()
#         # cls.charges_id = cls.env.ref('charges')
#         cls.booking_no = cls.env['crm.lead'].search([
#             ('booking_id', '=', 'erpbox00331')])
#         cls.enquiry_no = cls.env['request.for.quote'].search([
#             ('booking_id', '=', 'erpbox00331')])
#         cls.country_ref = cls.env.ref('base.be')
#         cls.test_email = 'abcd@jdfjshdg.com'
#         cls.test_phone = '0485112233'
#         cls.booking_id  = "291"

#     def test_compare_inquiry_no(self):
#         lead = self.booking_no
#         test_name=self.enquiry_no
#         #     'shipping_name_id':'53',
#         #     # 'booking_id': 'erpbox00009',
#         #     'valid_from':'2022-05-12',
#         #     'valid_to':'2022-06-10',
#         #     'company_id':'1',
#         #     'container_type':'1',
#         #     'booking_id':self.booking_id
#         # })

#         self.assertEqual(lead.booking_id,test_name.booking_id.booking_id)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare test is successful")
    
#     # def test_save_button(self):
#     #     # lead = self.env['crm.lead'].browse(274)
#     #     test_name=self.env['request.for.quote'].create({
#     #         'shipping_name_id':'53',
#     #         # 'booking_id': 'erpbox00009',
#     #         'valid_from':'2022-05-12',
#     #         'valid_to':'2022-06-10',
#     #         'company_id':'1',
#     #         'container_type':'1',
#     #         'booking_id':self.booking_no.booking_id,
#     #         # 'charges_line':cls.charges_id,
#     #         # 'charges_type':'Freight',
#     #         # 'container_type':
#     #         # 'units':'3',
#     #         # 'unit_price':'1000',
#     #         # 'currency_id':'INR',
#     #         # 'to_currency_id':'INR'

#     #     })

#     #     # self.assertEqual(lead.booking_id,test_name.booking_id)
#     #     test_name.save()
#     #     _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::button test is successful")

#     # def test_check_array_values(self):
#     #     rc = self.env['request.for.quote'].create({
#     #         'shipping_name_id':'53',
#     #         # 'booking_id': 'erpbox00009',
#     #         'valid_from':'2022-05-12',
#     #         'valid_to':'2022-06-10',
#     #         'company_id':'1',
#     #         'container_type':'1',
#     #         # 'booking_id':'450',
#     #         # 'charges_line':cls.charges_id,
#     #         # 'charges_type':'Freight',
#     #         # # 'container_type':
#     #         # 'units':'3',
#     #         # 'unit_price':'1000',
#     #         # 'currency_id':'INR',
#     #         # 'to_currency_id':'INR'

#     #     })
#     #     _logger.info("::::::::::::::::::::::::::::::::::::::::::::rc",rc)
#     #     charges1 = {
#     #         'charges_type':'freight',
#     #         'container_type':rc.container_type,
#     #         'units':rc.no_of_expected_container,
#     #         'unit_price':1000,
#     #         'currency_id':1,
#     #         'to_currency_id':1,
#     #         'rfq_id': rc.id

#     #     }
#     #     charges2 = {
#     #         'charges_type':'freight',
#     #         'container_type':rc.container_type,
#     #         'units':rc.no_of_expected_container,
#     #         'unit_price':2000,
#     #         'currency_id':2,
#     #         'to_currency_id':2,
#     #         'rfq_id': rc.id

#     #     }
#     #     lead1 = rc.charges_line.create(charges1)
#     #     lead2 = rc.charges_line.create(charges2)
#     #     _logger.info("::::::::::::::::::::::::::::::::::::::::::::lead",lead1)
#     #     self.assertEqual(lead1.units,lead2.units)
#     #     _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::units is equal")
#     #     self.assertEqual(lead1.unit_price,lead2.unit_price)
#     #     _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::unit price is equal")

#     #     _logger.info("::::::::::::::::::::::::::::::::::::::::::::UNITSSS",rc.charges_line.units)

#         # rc.charges_line.charges_id = "Freight"
#         # _logger.info("?????????????????????????????????",rc.charges_line.charges_id)
#         # with rc.charges_line.new() as rc_line:
#         #     rc_line.charges_type = self.charges_type
#         #     rc_line.container_type = self.container_type

#         #     rc_line.units = '1'
#         #     rc_line.unit_price = '100'
#         #     rc_line.currency_id = 'INR'
#         #     rc_line.to_currency_id = 'INR'
#         # with rc.charges_line.new() as rc_line:
#         #     rc_line.charges_type = Freight
#         #     rc_line.units = '1'
#         #     rc_line.unit_price = '100'
#         #     rc_line.currency_id = 'INR'
#         #     rc_line.to_currency_id = 'INR'
        
#         # rc = rc.save()

#     def test_date(self):
#         today = fields.Date.today()
#         # _logger.info("today's date is")
#         lead=self.enquiry_no
#         self.assertEqual(lead.valid_from,today)
#         _logger.info("test date issuccessful")
        

#     def test_no_of_containers(self):
#         test_cont=self.enquiry_no
#         rc=test_cont.charges_line.browse(1)
#         rc1=test_cont.charges_line.browse(2)
#         self.assertEqual(test_cont.no_of_expected_container,rc.units)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare no of containers is successful")
#         self.assertEqual(rc.units,rc1.units)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare no of containers in each row is successful")

#     # def test_calc_without_taxes(self):
#     #     test_calc=self.enquiry_no
#     #     rc_total=0
#     #     for rc_cargo in test_calc.charges_line:
#     #         rc_total=rc_cargo.units*rc_cargo.new_unit_price
#     #     print("dddddddddddddd",rc_total)
#     #     print("dddddddddddddd",rc_cargo.final_amount)
#     #     self.assertEqual(rc_cargo.final_amount,rc_total)
#     #     _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::calculation is successful")

#     # def test_subscribed_or_not(self):
#     #     # tax_calc=self.enquiry_no
#     #     try:
#     #         tax_calc=self.enquiry_no
#     #         rc_total=0
#     #         for rc_tax in tax_calc.charges_line:
#     #             tax=rc_tax.taxes_id.amount
#     #             rc_total=rc_tax.units*rc_tax.unit_price*tax
#     #         self.assertEqual(rc_tax.final_amount,rc_total)
#     #         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::calculation is successful")
#     #     except:
#     #         tax_calc=self.enquiry_no
#     #         rc_total=0
#     #         for rc_cargo in tax_calc.charges_line:
#     #             rc_total=rc_cargo.units*rc_cargo.unit_price
#     #         print("dddddddddddddd",rc_total)
#     #         print("dddddddddddddd",rc_cargo.final_amount)
#     #         self.assertEqual(rc_cargo.final_amount,rc_total)
#     #         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::calculation is successful")

#     def test_calc_with_taxes_rc(self):
#         tax_calc=self.enquiry_no
#         rc_total=0
#         rc_total_amount=0
#         for rc_tax in tax_calc.charges_line:
#             if rc_tax.taxes_id:
#                 tax=rc_tax.taxes_id.amount/100
#                 print("gsdfgsdfgfdg",tax)
#                 rc_total=rc_tax.units*rc_tax.unit_price*tax
#                 self.assertEqual(rc_tax.tax_amt,rc_total)
#                 # print("gsdfgsdfgfdg",rc_tax.tax_amt)
#                 # print("gsdfgsdfgfdg",rc_total)
#                 _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::with tax calculation is successful")
#                 print(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,sq_tax.taxes_id",rc_tax.taxes_id.amount)
#                 rc_total_amount=rc_tax.units*rc_tax.unit_price+rc_total
#                 self.assertEqual(rc_tax.final_amount,rc_total_amount)
#             else:
#                 rc_total=rc_tax.units*rc_tax.unit_price
#                 print("dddddddddddddd",rc_total)
#                 print("dddddddddddddd",rc_tax.final_amount)
#                 self.assertEqual(rc_tax.final_amount,rc_total)
#                 _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::calculation is successful")

#     def test_total_origin_rc(self):
#         freight_total=self.enquiry_no
#         rc_total=0
#         rc_total_amount=0
#         for rc_tax in freight_total.charges_line:
#             if rc_tax.charges_type=="origin":
#                 # tax=rc_tax.taxes_id.amount/100
#                 # print("gsdfgsdfgfdg",tax)
#                 rc_total=rc_total+rc_tax.final_amount
#         self.assertEqual(freight_total.total_origin_charge,rc_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::origin calculation is successful")

#     def test_total_freight_rc(self):
#         freight_total=self.enquiry_no
#         rc_total=0
#         for rc_tax in freight_total.charges_line:
#             if rc_tax.charges_type=="freight":
#                 # tax=rc_tax.taxes_id.amount/100
#                 # print("gsdfgsdfgfdg",tax)
#                 rc_total=rc_total+rc_tax.final_amount
#         self.assertEqual(freight_total.total_freight_charge,rc_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::freight calculation is successful")
            
#     def test_total_destination_rc(self):
#         freight_total=self.enquiry_no
#         rc_total=0
#         for rc_tax in freight_total.charges_line:
#             if rc_tax.charges_type=="destination":
#                 # tax=rc_tax.taxes_id.amount/100
#                 # print("gsdfgsdfgfdg",tax)
#                 rc_total=rc_total+rc_tax.final_amount
#         self.assertEqual(freight_total.total_destination_charge,rc_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::destination calculation is successful")

#     def test_total_charge_rc(self):
#         freight_total=self.enquiry_no
#         rc_total=freight_total.total_destination_charge+freight_total.total_origin_charge+freight_total.total_freight_charge
#         self.assertEqual(freight_total.total_charge,rc_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::total charge calculation is successful")
            
            

#         # rc=test_calc.charges_line.unit_price
#         # rc1=test_calc.charges_line.units
#         # rc_total=test_calc.charges_line.final_amount
#         # _logger.info("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP rc",rc)
#         # total=rc*rc1
#         # # _logger.info("???????????????????????????????????????????????", rc.final_amount)
#         # self.assertEqual(rc_total,total)
#         # _logger.info("???????????????????????????????????????????????", rc_total)
#         # _logger.info("???????????????????????????????????????????????", total)
#         # _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::taxxx is successful")

#     # def test_units(self):
#     #     test_calc=self.enquiry_no
#     #     rc=test_calc.charges_line(1).unit_price
#     #     rc1=test_calc.charges_line(2).unit_price
#     #     # rc_total=test_calc.charges_line.final_amount
#     #     _logger.info("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP rc",rc)
#     #     # total=rc*rc1
#     #     # _logger.info("???????????????????????????????????????????????", rc.final_amount)
#     #     self.assertEqual(rc,rc1)
#     #     _logger.info("???????????????????????????????????????????????", rc1)
#     #     _logger.info("???????????????????????????????????????????????", total)
#     #     _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::charge is successful")

#     def test_valid_to(self):
#         today = fields.Date.today()
#         lead=self.enquiry_no
#         self.assertGreater(lead.valid_to,today)
#         _logger.info("valid to is greater ???????????????????????????????????????????????")
#         self.assertGreater(lead.valid_to,lead.valid_from)
#         _logger.info("valid to is greater than valid from ???????????????????????????????????????????????")
        

#     def test_compare_cargo_crm_rfq(self):
        
#         test_name=self.env['request.for.quote'].browse(29)
#         lead = self.env['purchase.order'].browse(31)
#         self.assertEqual(lead.no_of_expected_container,test_name.no_of_expected_container)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare no of containers is successful")
#         self.assertEqual(lead.quantity,test_name.quantity)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare quantity is successful")
#         self.assertEqual(lead.weight,test_name.weight)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare weight is successful")
#         self.assertEqual(lead.volume,test_name.volume)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare volume is successful")
#         self.assertEqual(lead.move_type,test_name.move_type)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare move_type is successful")
#         self.assertEqual(lead.incoterm_id,test_name.incoterm_id)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare incoterm_id is successful")
#         self.assertEqual(lead.place_of_origin,test_name.place_of_origin)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare Point of Origin is successful")
#         self.assertEqual(lead.final_port_of_destination,test_name.final_port_of_destination)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare Point of Destination is successful")
#         # self.assertEqual(lead.point_of_stuffing,test_name.point_of_stuffing)
#         # _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare Point of Stuffing is successful")
#         # self.assertEqual(lead.point_of_destuffing,test_name.point_of_destuffing)
#         # _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare Point of Destuffing is successful")
#         self.assertEqual(lead.container_type,test_name.container_type)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare container type is successful")
#         self.assertEqual(lead.expected_date_of_shipment,test_name.expected_date_of_shipment)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compareexpected_date_of_shipment is successful")
#         self.assertEqual(lead.shipment_terms,test_name.shipment_terms)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare shipment terms is successful")
#         # self.assertEqual(lead.remarks,test_name.remarks)
#         # _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare remarks is successful")
    
#     def test_readonly(self):
#         rc = Form(self.env['request.for.quote'])
#         try:
#             rc.currency_id="INR"
#             _logger.info("not readonly field")
#         # rc.unit_price=2
#         # amt=rc.units* rc.unit_price
#         except:
#             _logger.warning("readonlyd")

#     def test_not_readonly(self):
#         rc = Form(self.env['request.for.quote'])
#         try:
#             rc.valid_to="06/22/2022"
#             _logger.info("not readonly field")
#         # rc.unit_price=2
#         # amt=rc.units* rc.unit_price
#         except:
#             _logger.warning("readonly")

#     def test_load_charges(self):
#         charges=self.env['request.for.quote'].sudo().search([('booking_id','=', 'erpbox01234')], limit=1)
#         print("::::::::::::::::::charges",charges)
#         print("::::::::::::::::::charges_template_ids",charges.charges_template_ids.ids)
#         print("::::::::::::::::::charges_template_ids",charges.currency_id)
#         if charges.charges_template_ids:
#             print("::::::::::::::::::charges_template_ids",charges.charges_template_ids.ids)
#             load=charges.action_load_charges()
#             print("load:::::::::::::::::::",charges.charges_line)
#             for value in charges.charges_line:
#                 # self.assertIsNone(value.charges_id,"False")
#                 print(":::::::::::::::::::::::::::::::::", value.rfq_id)
#                 try:
#                     self.assertEqual(value.units,charges.no_of_expected_container)
#                     print("value.units:::::::::::::::::::::::::::::",value.units)
#                     print("equal")
#                 except:
#                     print("not equal")

#     def test_delete_charges(self):
#         charges=self.env['request.for.quote'].sudo().search([('booking_id','=', 'erpbox01234')], limit=1)
#         print("::::::::::::::::::charges",charges)
#         print("::::::::::::::::::charges_template_ids",charges.charges_template_ids.ids)
#         print("::::::::::::::::::charges_template_ids",charges.currency_id)
#         if charges.charges_template_ids:
#             print("::::::::::::::::::charges_template_ids",charges.charges_template_ids.ids)
#             charges.action_load_charges()
#             print("load:::::::::::::::::::",charges.charges_line)
#             delete=charges.delete_charges()
#             print("delete:::::::::::::::::::",charges.charges_line)
#             for value in charges.charges_line:
#                 # self.assertIsNone(value.charges_id,"False")
#                 print(":::::::::::::::::::::::::::::::::", value.rfq_id)
#                 try:
#                     self.assertEqual(value.units,charges.no_of_expected_container)
#                     print("value.units:::::::::::::::::::::::::::::",value.units)
#                     print("equal")
#                 except:
#                     print("not equal")

#     def test_update_charges(self):
#         charges=self.env['request.for.quote'].sudo().search([('booking_id','=', 'erpbox01234')], limit=1)
#         print("::::::::::::::::::charges",charges)
#         print("::::::::::::::::::charges_template_ids",charges.charges_template_ids.ids)
#         print("::::::::::::::::::charges_template_ids",charges.currency_id)
#         if charges.charges_template_ids:
#             print("::::::::::::::::::charges_template_ids",charges.charges_template_ids.ids)
#             charges.action_load_charges()
#             print("load:::::::::::::::::::",charges.charges_line)
#             load=charges.action_update_charges_prepaid_collect()
#             print("delete:::::::::::::::::::",charges.charges_line)
#             for value in charges.charges_line:
#                 # self.assertIsNone(value.charges_id,"False")
#                 print(":::::::::::::::::::::::::::::::::", value.rfq_id)
#                 try:
#                     self.assertEqual(value.units,charges.no_of_expected_container)
#                     print("value.units:::::::::::::::::::::::::::::",value.units)
#                     print("equal")
#                 except:
#                     print("not equal")


