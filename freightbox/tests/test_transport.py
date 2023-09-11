# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.tests import common
from odoo import fields
from odoo.tests import tagged, Form
from odoo.addons.crm.tests.common import TestCrmCommon
import logging

_logger = logging.getLogger(__name__)

class TestTransport(TestCrmCommon):

    @classmethod
    def setUpClass(cls):
        super(TestTransport, cls).setUpClass()
        cls.job_id = cls.env['job'].search([
            ('inquiry_id', '=', 'erpbox00331')])
        cls.transport_id = cls.env['transport'].search([
            ('inquiry_id', '=', 'erpbox00331')])

    def test_booking_id(self):
        test_job=self.job_id
        test_transport=self.transport_id
        # self.assertEqual(test_job.job_inquiry_id,test_invoice.booking_id)
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::test_job.job_inquiry_id",test_job.inquiry_id.booking_id)
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::test_transport.booking_id",test_transport.inquiry_id.booking_id)
        self.assertEqual(test_job.inquiry_id.booking_id,test_transport.inquiry_id.booking_id)
        print(":::::::::::::::::::::::::::::::::::::::::::::::::::::booking id is compared")

    def test_compare(self):
        test_job=self.job_id
        test_transport=self.transport_id
        self.assertEqual(test_job.carrier_booking,test_transport.carrier_booking)
        _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare carrier_booking is successful")
        # self.assertEqual(test_job.final_port_of_destination,test_so.final_port_of_destination)
        # _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare final port of destination is successful")
    
    def test_not_readonly(self):
        test_job = Form(self.transport_id)
        try:
            test_job.inquiry_id="1"
            _logger.info("inquiry_id id is not readonly field")
        except:
            _logger.warning("inquiry_id  id is readonly field")

        try:
            test_job.vessel_name="abc"
            _logger.info("vessel_name  is not readonly field")
        except:
            _logger.warning("vessel_name id is readonly field")

        try:
            test_job.voyage="FCL"
            _logger.info("voyage id is not readonly field")
        except:
            _logger.warning("voyage id is readonly field")