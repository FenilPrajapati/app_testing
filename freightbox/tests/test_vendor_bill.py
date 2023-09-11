# # -*- coding: utf-8 -*-
# # Part of Odoo. See LICENSE file for full copyright and licensing details.

# from odoo.tests import common
# from odoo import fields
# from odoo.tests import tagged, Form
# from odoo.addons.crm.tests.common import TestCrmCommon
# import logging

# _logger = logging.getLogger(__name__)

# class TestVendorBill(TestCrmCommon):

#     @classmethod
#     def setUpClass(cls):
#         super(TestVendorBill, cls).setUpClass()
#         cls.po_id = cls.env['purchase.order'].search([
#             ('rfq_id', '=', 'erpbox00331')])
#         cls.vendor_bill_id = cls.env['account.move'].search([
#             ('booking_id', '=', 'erpbox00331') , ('partner_id', '=', 'Abc company')])

#     def test_booking_id(self):
#         test_po=self.po_id
#         test_vendor_bill=self.vendor_bill_id
#         # self.assertEqual(test_po.rfq_id,test_vendor_bill.booking_id)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::test_po.rfq_id",test_po.rfq_id.booking_id.booking_id)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::test_vendor_bill.booking_id",test_vendor_bill.booking_id)
#         self.assertEqual(test_po.rfq_id.booking_id.booking_id,test_vendor_bill.booking_id)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::booking id is compared")

#     def test_compare_vendor(self):
#         test_po=self.po_id
#         test_bill=self.vendor_bill_id
#         self.assertEqual(test_po.partner_id.name,test_bill.partner_id.name)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare vendor is successful")

#     def test_compare_po_bill(self):
#         test_po=self.po_id
#         test_vendor_bill=self.vendor_bill_id
#         self.assertEqual(test_po.place_of_origin,test_vendor_bill.place_of_origin)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare place of origin is successful")
#         self.assertEqual(test_po.final_port_of_destination,test_vendor_bill.place_of_destination)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare quantity is successful")
    
#     def test_not_readonly(self):
#         bill = Form(self.vendor_bill_id)
#         try:
#             bill.booking_id="1"
#             _logger.info("booking_id id is not readonly field")
#         except:
#             _logger.warning("booking_id id is readonly field")

#         try:
#             bill.partner_id.name="BC"
#             _logger.info("partner id is not readonly field")
#         except:
#             _logger.warning("partner id is readonly field")

#         try:
#             bill.date="1/2/12"
#             _logger.info("date id is not readonly field")
#         except:
#             _logger.warning("date id is readonly field")


#     def test_compare_container_type(self):
#         test_bill = self.vendor_bill_id
        
#         for bill_il, bill_rt in zip(test_bill.invoice_line_ids, test_bill.charges_line):
#             self.assertEqual(bill_il.product_id.name,bill_rt.container_type.code)
#             _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare container type is successful")

#     def test_total(self):
#         test_bill = self.vendor_bill_id
#         total=0
#         for bill_il in test_bill.invoice_line_ids:
#             total=bill_il.quantity*bill_il.price_unit
#             _logger.debug("::::::::::::::::::::::::::total",total)
#             self.assertEqual(bill_il.price_subtotal,total)
#             _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare  total is successful")

#     def test_total_charge(self):
#         test_total=self.vendor_bill_id
#         amount_total = 0
#         for bill_total in test_total.charges_line:
#             # amount_total = 0
#             amount_total =amount_total+bill_total.final_amount
#         _logger.info("??????????????????????????????????????????????amount_total",amount_total)
#         _logger.info("??????????????????????????????????????????????test_total.total_charge",test_total.total_charge)
#         self.assertEqual(test_total.total_charge,amount_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::total charge is correct")

#     def test_calc_with_taxes_bill(self):
#         tax_calc=self.vendor_bill_id
#         bill_total=0
#         bill_total_amount=0
#         for bill_tax in tax_calc.charges_line:
#             if bill_tax.taxes_id:
#                 tax=bill_tax.taxes_id.amount/100
#                 _logger.info("gsdfgsdfgfdg",tax)
#                 bill_total=bill_tax.units*bill_tax.unit_price*tax
#                 self.assertEqual(bill_tax.tax_amt,bill_total)
#                 # _logger.info("gsdfgsdfgfdg",bill_tax.tax_amt)
#                 # _logger.info("gsdfgsdfgfdg",bill_total)
#                 _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::with tax calculation is successful")
#                 # _logger.info(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,",bill_tax.taxes_id.amount)
#                 bill_total_amount=bill_tax.units*bill_tax.unit_price+bill_total
#                 self.assertEqual(bill_tax.final_amount,bill_total_amount)
#             else:
#                 bill_total=bill_tax.units*bill_tax.unit_price
#                 _logger.info("dddddddddddddd",bill_total)
#                 _logger.info("dddddddddddddd",bill_tax.inal_amount)
#                 self.assertEqual(bill_tax.final_amount,bill_total)
#                 _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::calculation is successful")

    
#     def test_total_origin_bill(self):
#         freight_total=self.vendor_bill_id
#         bill_total=0
#         for bill_tax in freight_total.charges_line:
#             if bill_tax.charges_type=="origin":
#                 # tax=bill_tax.taxes_id.amount/100
#                 # _logger.info("gsdfgsdfgfdg",tax)
#                 bill_total=bill_total+bill_tax.final_amount
#         _logger.info(":::::::::::::::::::::::::bill_total",bill_total)
#         self.assertEqual(freight_total.total_origin_charge,bill_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::origin calculation is successful")

    
#     def test_total_freight_bill(self):
#         freight_total=self.vendor_bill_id
#         bill_total=0
#         for bill_tax in freight_total.charges_line:
#             if bill_tax.charges_type=="freight":
#                 # tax=bill_tax.taxes_id.amount/100
#                 # _logger.info("gsdfgsdfgfdg",tax)
#                 bill_total=bill_total+bill_tax.final_amount
#         print(":::::::::::::::::::::::::bill_total",bill_total)
#         self.assertEqual(freight_total.total_freight_charge,bill_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::freight calculation is successful")

#     def test_total_destination_bill(self):
#         freight_total=self.vendor_bill_id
#         bill_total=0
#         for bill_tax in freight_total.charges_line:
#             if bill_tax.charges_type=="destination":
#                 # tax=bill_tax.taxes_id.amount/100
#                 # _logger.info("gsdfgsdfgfdg",tax)
#                 bill_total=bill_total+bill_tax.final_amount
#         print(":::::::::::::::::::::::::bill_total",bill_total)
#         self.assertEqual(freight_total.total_destination_charge,bill_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::destination calculation is successful")

#     def test_total_charge_bill(self):
#         freight_total=self.vendor_bill_id
#         bill_total=freight_total.total_destination_charge+freight_total.total_origin_charge+freight_total.total_freight_charge
#         print(bill_total)
#         self.assertEqual(freight_total.total_charge,bill_total)
#         print(":::::::::::::::::",freight_total.total_charge)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::total charge calculation is successful")

#     def test_total_charge_for_loop_vendor_bill(self):
#         freight_total=self.vendor_bill_id
#         bill_total=bill_total_destination=bill_total_origin=bill_total_freight=0
#         for bill_tax in freight_total.charges_line:
#             if bill_tax.charges_type=="destination":
#                 bill_total_destination=bill_total_destination+bill_tax.final_amount
#             if bill_tax.charges_type=="origin":
#                 bill_total_origin=bill_total_origin+bill_tax.final_amount
#             if bill_tax.charges_type=="freight":
#                 bill_total_freight=bill_total_freight+bill_tax.final_amount
#         bill_total=bill_total_destination+bill_total_origin+bill_total_freight
#         self.assertEqual(freight_total.total_charge,bill_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::total charge calculation inside for loop is successful")

#     def test_total_prepaid_bill(self):
#         freight_total=self.vendor_bill_id
#         bill_total=0
#         for bill_tax in freight_total.charges_line:
#             if bill_tax.prepaid==True:
#                 tax=bill_tax.taxes_id.amount/100*bill_tax.unit_price
#                 bill_total=bill_tax.unit_price+tax
#                 print("gsdfgsdfgfdg",tax)
#                 print("gsdfgsdfgfdg",bill_total)
#                 bill_total=bill_total+bill_tax.final_amount_per_unit
#         print("gsdfgsdfgfdg",bill_total)
#         self.assertEqual(freight_total.total_prepaid_charges,bill_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::prepaid calculation is successful")

#     def test_total_collect_bill(self):
#         freight_total=self.vendor_bill_id
#         bill_total=0
#         for bill_tax in freight_total.charges_line:
#             if bill_tax.collect==True:
#                 tax=bill_tax.taxes_id.amount/100*bill_tax.unit_price
#                 bill_total=bill_tax.unit_price+tax
#                 print("gsdfgsdfgfdg",tax)
#                 print("gsdfgsdfgfdg",bill_total)
#                 # bill_total=bill_total+bill_tax.final_amount_per_unit
#                 print("gsdfgsdfgfdg",bill_total)
#                 self.assertEqual(freight_total.total_collect_charges,bill_total)
#                 _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::prepaid calculation is successful")
            

