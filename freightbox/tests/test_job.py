# # -*- coding: utf-8 -*-
# # Part of Odoo. See LICENSE file for full copyright and licensing details.

# from odoo.tests import common
# from odoo import fields
# from odoo.tests import tagged, Form
# from odoo.addons.crm.tests.common import TestCrmCommon
# import logging

# _logger = logging.getLogger(__name__)

# class TestJob(TestCrmCommon):

#     @classmethod
#     def setUpClass(cls):
#         super(TestJob, cls).setUpClass()
#         cls.job_id = cls.env['job'].search([
#             ('inquiry_id', '=', 'erpbox00331')])
#         cls.so_id = cls.env['sale.order'].search([
#             ('so_inquiry_id', '=', 'erpbox00331')])

#     def test_booking_id(self):
#         test_job=self.job_id
#         test_so=self.so_id
#         # self.assertEqual(test_job.job_inquiry_id,test_invoice.booking_id)
#         print(":::::::::::::::::::::::::::::::::::::::::::::::::::::test_job.job_inquiry_id",test_job.inquiry_id.booking_id)
#         print(":::::::::::::::::::::::::::::::::::::::::::::::::::::test_invoice.booking_id",test_so.so_inquiry_id.booking_id)
#         self.assertEqual(test_job.inquiry_id.booking_id,test_so.so_inquiry_id.booking_id)
#         print(":::::::::::::::::::::::::::::::::::::::::::::::::::::booking id is compared")

#     def test_compare_job_invoice(self):
#         test_job=self.job_id
#         test_so=self.so_id
#         self.assertEqual(test_job.place_of_origin,test_so.place_of_origin)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare place of origin is successful")
#         self.assertEqual(test_job.final_port_of_destination,test_so.final_port_of_destination)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare final port of destination is successful")
    
#     def test_not_readonly(self):
#         test_job = Form(self.job_id)
#         try:
#             test_job.inquiry_id="1"
#             _logger.info("inquiry_id id is not readonly field")
#         except:
#             _logger.warning("inquiry_id  id is readonly field")

#         try:
#             test_job.exp_no_of_container="4"
#             _logger.info("exp_no_of_container  is not readonly field")
#         except:
#             _logger.warning("exp_no_of_container id is readonly field")

#         try:
#             test_job.shipment_terms_origin="FCL"
#             _logger.info("shipment_terms_origin id is not readonly field")
#         except:
#             _logger.warning("shipment_terms_origin id is readonly field")

#     def test_date(self):
#         # today_time = datetime.datetime.now()
#         # print("???????????????????????????????????????????????", today_time)
#         test_date = self.job_id
#         print(":::::::::::::::::::::",test_date.create_date)
#         self.assertAlmostEqual(test_date.job_date,test_date.create_date)