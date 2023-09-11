# # -*- coding: utf-8 -*-
# # Part of Odoo. See LICENSE file for full copyright and licensing details.

# from odoo.tests import common
# from odoo.addons.crm.models.crm_lead import PARTNER_FIELDS_TO_SYNC, PARTNER_ADDRESS_FIELDS_TO_SYNC
# from odoo.addons.crm.tests.common import TestCrmCommon, INCOMING_EMAIL
# from odoo.addons.phone_validation.tools.phone_validation import phone_format
# from odoo.tests.common import Form, users
# from odoo.addons.account.tests.common import AccountTestInvoicingCommon
# from odoo.addons.base.tests.common import SavepointCase
# # from odoo.freightbox.tests.common import TestCommon
# import logging

# _logger = logging.getLogger(__name__)



# class TestCRMLead(SavepointCase):

#     @classmethod
#     def setUpClass(cls):
#         super(TestCRMLead, cls).setUpClass()
#         cls.country_ref = cls.env.ref('base.be')
#         cls.booking_no = cls.env['crm.lead'].search([
#             ('booking_id', '=', 'erpbox00331')])
#         cls.enquiry_no = cls.env['request.for.quote'].search([
#             ('booking_id', '=', 'erpbox00331')])
#         cls.test_email = 'abcd@jdfjsdg.com'
#         cls.test_phone = '0485112233'
#         cls.cargo_name  = "TESTCARGONAME"

#     def test_button(self):
#         lead = self.booking_no
#         lead.action_create_rate_comparision()
#         rc = self.env['request.for.quote'].create({
#             'shipping_name_id':'53',
#             # 'booking_id': 'erpbox00009',
#             'valid_from':'2022-05-12',
#             'valid_to':'2022-06-10',
#             'company_id':'1',
#             'container_type':'1',
#             # 'booking_id':'450',
#             # 'charges_line':cls.charges_id,
#             # 'charges_type':'Freight',
#             # # 'container_type':
#             # 'units':'3',
#             # 'unit_price':'1000',
#             # 'currency_id':'INR',
#             # 'to_currency_id':'INR'

#         })
        
#         print("rc_rount::::::::::::::::::::::::::::::::::::::::::",lead.rc_count)


#     def test_email_data(self):
#         lead_data = {
#             'name': 'TestMixed',
#             'partner_id': '53',
#             # address
#             # 'country_id': 'india',
#             # other contact fields
#             'partner_name': 'Parmesan Rappeur',
#             'contact_name': 'Parmesan',
#             # specific contact fields
#             # 'email_from': 'bhargavi@gmail.com',
#             # 'phone': '4598349',
#             'email_from': self.test_email,
#             'phone': self.test_phone,
#             'cargo_name':self.cargo_name
#             }
#         lead = self.env['crm.lead'].create(lead_data)
#         # self.assertEqual(lead.name, "TestMixed")
#         # _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::name test is successful")
#         self.assertEqual(lead.email_from, self.test_email)
#         _logger.info("====================================================================lead.email_from",lead.email_from)
#         _logger.info("====================================================================self.test_email",self.test_email)
#         _logger.info("====================================================================self.booking_no",self.booking_no)
#         # self.assertFalse(lead.user_subscribed,msg=None)
#         # _logger.info("::::::::::::::::::::::::::::::::::::::::::user is not subscribed")
#         # lead.action_create_rate_comparision()
#         # _logger.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>",lead.rc_count)

#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::email test is successful")
#         # self.assertEqual(lead.contact_name, self.contact_1.name)
#         # self.assertEqual(lead.email_from, 'bhargavi@gamil.com')
#         # self.assertEqual(lead.phone, '4598349')

#     def test_rc_count(self):
#         lead = self.booking_no
#         lead.action_create_rate_comparision()
#         lead_data=self.env['request.for.quote'].create({
#             'shipping_name_id':'59',
#             'booking_id': '00009',
#             'valid_from':'2022-05-12',
#             'valid_to':'2022-06-10',
#             'company_id':'1',
#             'container_type':'1',
#             'cargo_name':self.cargo_name
#         })
#         lead_form = Form(lead_data)
#         lead_form.save()
#         _logger.info(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>", lead.rc_count)


#     # def test_subscribed(self):
#     #     lead = self.booking_no
#     #     self.assertTrue(lead.user_subscribed,msg=None)
#     #     _logger.info("::::::::::::::::::::::::::::::::::::::::::user is subscribed")

#     def test_subscribed_or_not(self):
#         lead = self.booking_no
#         try:
#             self.assertTrue(lead.user_subscribed,msg=None)
#             _logger.info("::::::::::::::::::::::::::::::::::::::::::user is subscribed")
#         except:
#             self.assertFalse(lead.user_subscribed,msg=None)
#             _logger.info("::::::::::::::::::::::::::::::::::::::::::user is not subscribed")


#     # def test_not_subscribed(self):
#     #     lead = self.booking_no
#     #     self.assertFalse(lead.user_subscribed,msg=None)
#     #     _logger.info("::::::::::::::::::::::::::::::::::::::::::user is not subscribed")

#     def test_partner_name(self):
#         # lead_data={
#         #      'partner_name': 'Parmesan Rappeur',
#         # }
#         lead = self.env['crm.lead'].new({
#             'partner_name': 'ParmesanRappeur',
#         })
#         self.assertEqual(lead.partner_name, "ParmesanRappeur")
#         _logger.info("::::::::::::::::::::::::::::::::::::::::::::::::::::: partner name test is successful")

#     def test_name(self):
#         lead = self.env['crm.lead'].new({
#             'name': 'TestMixed',
#         })
#         self.assertEqual(lead.name, "TestMixed")
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::name test is successful")
        
#         # test_cargo_name=self.env['crm.lead'].create({
#         #     'cargo_name':self.cargo_name
#         # })
#     def test_compare_cargo(self):
#         lead = self.env['crm.lead'].new({
#             'cargo_name':self.cargo_name
#         })
#         test_name=self.env['request.for.quote'].create({
#             'shipping_name_id':'59',
#             'booking_id': '00009',
#             'valid_from':'2022-05-12',
#             'valid_to':'2022-06-10',
#             # 'company_id':'89',
#             # 'container_type':'20GP',
#             'cargo_name':self.cargo_name
#         })

#         self.assertEqual(lead.cargo_name,test_name.cargo_name)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare test is successful")

#     def test_compare_cargo_crm_rfq(self):
#         lead = self.booking_no
#         test_name=self.enquiry_no
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
        
#     def test_phone_mobile_search(self):
#         lead_1 = self.env['crm.lead'].create({
#             'name': 'Lead 1',
#             'country_id': self.env.ref('base.be').id,
#             'phone': '+32485001122',
#         })
#         lead_2 = self.env['crm.lead'].create({
#             'name': 'Lead 2',
#             'country_id': self.env.ref('base.be').id,
#             'phone': '+32485112233',
#         })
#         self.assertEqual(lead_2, self.env['crm.lead'].search([
#             ('phone_mobile_search', 'like', '+32485112233')
#         ]))

#     # def test_readonly_crm(self):
#     #     test_crm = self.booking_no

#     #     if test_crm.user_subscribed:
#     #         test_crm.user_subscribed=False
#     #         _logger.info("its not a readonly field")
#     #         # rc.unit_price=2
#     #     # amt=rc.units* rc.unit_price
#     #     # else:
#     #     #     _logger.info("its a readonly field")
#     #         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::rtest_crm.user_subscribed",test_crm.user_subscribed)
#     #     else:
#     #         _logger.info("readonly")

#     # def test_not_readonly_crm(self):
#     #     test_crm = self.booking_no
#     #     if test_crm.cargo_name:
#     #         test_crm.cargo_name="changed"
#     #         _logger.info("its not a readonly field")

#     def test_readonly_crm(self):
#         lead = Form(self.env['crm.lead'])
#         try:
#             lead.booking_id="1"
#             _logger.info("booking_id is not readonly field")
#         except:
#             _logger.info("booking_id is readonly")
        
#         try:
#             lead.user_subscribed=False
#             _logger.info("user_subscribed is not readonly field")
#         except:
#             _logger.info("user_subscribed is readonly")


#     def test_not_readonly_crm(self):
#         lead = Form(self.env['crm.lead'])
#         try:
#             lead.cargo_name="ABC"
#             _logger.info("cargo_name is not readonly field")
#         # rc.unit_price=2
#         # amt=rc.units* rc.unit_price
#         except:
#             _logger.info("cargo_name readonlyd")
#         try:
#             lead.email_from="abc@hghgh.com"
#             _logger.info("email_from is not readonly field")
#         except:
#             _logger.info("email_from is readonly")

