# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.fields import Datetime
from odoo import tools

class TestCommon():

    @classmethod
    def setUpClass(cls):
        super(TestCommon, cls).setUpClass()
        cls.booking_no = cls.env['crm.lead'].search([
            ('booking_id', '=', 'erpbox00331')])
        cls.enquiry_no = cls.env['request.for.quote'].search([
            ('booking_id', '=', 'erpbox00331')])