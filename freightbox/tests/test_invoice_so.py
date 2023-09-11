# # -*- coding: utf-8 -*-
# # Part of Odoo. See LICENSE file for full copyright and licensing details.

# from odoo.tests import common
# from odoo import fields
# from odoo.tests import tagged, Form
# from odoo.addons.crm.tests.common import TestCrmCommon
# import logging

# _logger = logging.getLogger(__name__)

# class TestInv(TestCrmCommon):

#     @classmethod
#     def setUpClass(cls):
#         super(TestInv, cls).setUpClass()
#         cls.so_id = cls.env['sale.order'].search([
#             ('so_inquiry_id', '=', 'erpbox00331')])
#         cls.inv_id = cls.env['account.move'].search([
#             ('booking_id', '=', 'erpbox00331'), ('partner_id', '=', 'Indra Ltd')])

#     def test_booking_id(self):
#         test_so=self.so_id
#         test_invoice=self.inv_id
#         # self.assertEqual(test_so.so_inquiry_id,test_invoice.booking_id)
#         print(":::::::::::::::::::::::::::::::::::::::::::::::::::::test_so.so_inquiry_id",test_so.so_inquiry_id.booking_id)
#         print(":::::::::::::::::::::::::::::::::::::::::::::::::::::test_invoice.booking_id",test_invoice.booking_id)
#         self.assertEqual(test_so.so_inquiry_id.booking_id,test_invoice.booking_id)
#         print(":::::::::::::::::::::::::::::::::::::::::::::::::::::booking id is compared")

#     def test_compare_so_invoice(self):
#         test_so=self.so_id
#         test_invoice=self.inv_id
#         self.assertEqual(test_so.place_of_origin,test_invoice.place_of_origin)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare place of origin is successful")
#         self.assertEqual(test_so.final_port_of_destination,test_invoice.place_of_destination)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare quantity is successful")
    
#     def test_not_readonly(self):
#         inv = Form(self.inv_id)
#         try:
#             inv.booking_id="1"
#             _logger.info("booking_id id is not readonly field")
#         except:
#             _logger.warning("booking_id id is readonly field")

#         try:
#             inv.partner_id.name="BC"
#             _logger.info("partner id is not readonly field")
#         except:
#             _logger.warning("partner id is readonly field")

#         try:
#             inv.invoice_date="1/2/12"
#             _logger.info("invoice_date id is not readonly field")
#         except:
#             _logger.warning("invoice_date id is readonly field")


#     def test_compare_container_type(self):
#         test_inv = self.inv_id
        
#         for inv_il, inv_rt in zip(test_inv.invoice_line_ids, test_inv.charges_line):
#             self.assertEqual(inv_il.product_id.name,inv_rt.container_type.code)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare container type is successful")

#     def test_total(self):
#         test_inv = self.inv_id
#         total=0
#         for inv_il in test_inv.invoice_line_ids:
#             total=inv_il.quantity*inv_il.price_unit
#             print("::::::::::::::::::::::::::total",total)
#             self.assertEqual(inv_il.price_subtotal,total)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare  total is successful")

#     def test_total_charge(self):
#         test_total=self.inv_id
#         amount_total = 0
#         for inv_total in test_total.charges_line:
#             # amount_total = 0
#             amount_total =amount_total+inv_total.final_amount
#         print("??????????????????????????????????????????????amount_total",amount_total)
#         print("??????????????????????????????????????????????test_total.total_charge",test_total.total_charge)
#         self.assertEqual(test_total.total_charge,amount_total)
#         print(":::::::::::::::::::::::::::::::::::::::::::::::::::::total charge is correct")

#     def test_calc_with_taxes_inv(self):
#         tax_calc=self.inv_id
#         inv_total=0
#         inv_total_amount=0
#         for inv_tax in tax_calc.charges_line:
#             if inv_tax.taxes_id:
#                 tax=inv_tax.taxes_id.amount/100
#                 print("gsdfgsdfgfdg",tax)
#                 inv_total=inv_tax.units*inv_tax.unit_price*tax
#                 self.assertEqual(inv_tax.tax_amt,inv_total)
#                 # print("gsdfgsdfgfdg",inv_tax.tax_amt)
#                 # print("gsdfgsdfgfdg",inv_total)
#                 _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::with tax calculation is successful")
#                 # print(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,",inv_tax.taxes_id.amount)
#                 inv_total_amount=inv_tax.units*inv_tax.unit_price+inv_total
#                 self.assertEqual(inv_tax.final_amount,inv_total_amount)
#             else:
#                 inv_total=inv_tax.units*inv_tax.unit_price
#                 print("dddddddddddddd",inv_total)
#                 print("dddddddddddddd",inv_tax.inal_amount)
#                 self.assertEqual(inv_tax.final_amount,inv_total)
#                 _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::calculation is successful")

    
#     def test_total_origin_inv(self):
#         freight_total=self.inv_id
#         inv_total=0
#         for inv_tax in freight_total.charges_line:
#             if inv_tax.charges_type=="origin":
#                 # tax=inv_tax.taxes_id.amount/100
#                 # print("gsdfgsdfgfdg",tax)
#                 inv_total=inv_total+inv_tax.final_amount
#         print(":::::::::::::::::::::::::inv_total",inv_total)
#         self.assertEqual(freight_total.total_origin_charge,inv_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::origin calculation is successful")

    
#     def test_total_freight_inv(self):
#         freight_total=self.inv_id
#         inv_total=0
#         for inv_tax in freight_total.charges_line:
#             if inv_tax.charges_type=="freight":
#                 # tax=inv_tax.taxes_id.amount/100
#                 # print("gsdfgsdfgfdg",tax)
#                 inv_total=inv_total+inv_tax.final_amount
#         print(":::::::::::::::::::::::::inv_total",inv_total)
#         self.assertEqual(freight_total.total_freight_charge,inv_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::freight calculation is successful")

#     def test_total_destination_inv(self):
#         freight_total=self.inv_id
#         inv_total=0
#         for inv_tax in freight_total.charges_line:
#             if inv_tax.charges_type=="destination":
#                 # tax=inv_tax.taxes_id.amount/100
#                 # print("gsdfgsdfgfdg",tax)
#                 inv_total=inv_total+inv_tax.final_amount
#         print(":::::::::::::::::::::::::inv_total",inv_total)
#         self.assertEqual(freight_total.total_destination_charge,inv_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::destination calculation is successful")

#     def test_total_charge_inv(self):
#         freight_total=self.inv_id
#         inv_total=freight_total.total_destination_charge+freight_total.total_origin_charge+freight_total.total_freight_charge
#         print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",inv_total)
#         self.assertEqual(freight_total.total_charge,inv_total)
#         print(":::::::::::::::::",freight_total.total_charge)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::total charge calculation is successful")

#     def test_total_charge_for_loop_inv(self):
#         freight_total=self.inv_id
#         inv_total=inv_total_destination=inv_total_origin=inv_total_freight=0
#         for inv_tax in freight_total.charges_line:
#             if inv_tax.charges_type=="destination":
#                 inv_total_destination=inv_total_destination+inv_tax.final_amount
#             if inv_tax.charges_type=="origin":
#                 inv_total_origin=inv_total_origin+inv_tax.final_amount
#             if inv_tax.charges_type=="freight":
#                 inv_total_freight=inv_total_freight+inv_tax.final_amount
#         inv_total=inv_total_destination+inv_total_origin+inv_total_freight
#         self.assertEqual(freight_total.total_charge,inv_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::total charge calculation inside for loop is successful")

#     def test_total_prepaid_inv(self):
#         freight_total=self.inv_id
#         inv_total=0
#         for inv_tax in freight_total.charges_line:
#             if inv_tax.prepaid==True:
#                 tax=inv_tax.taxes_id.amount/100*inv_tax.unit_price
#                 inv_total=inv_tax.unit_price+tax
#                 print("gsdfgsdfgfdg",tax)
#                 print("gsdfgsdfgfdg",inv_total)
#                 inv_total=inv_total+inv_tax.final_amount_per_unit
#         print("gsdfgsdfgfdg",inv_total)
#         self.assertEqual(freight_total.total_prepaid_charges,inv_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::prepaid calculation is successful")

#     def test_total_collect_inv(self):
#         freight_total=self.inv_id
#         inv_total=0
#         for inv_tax in freight_total.charges_line:
#             if inv_tax.collect==True:
#                 tax=inv_tax.taxes_id.amount/100*inv_tax.unit_price
#                 inv_total=inv_tax.unit_price+tax
#                 print("gsdfgsdfgfdg",tax)
#                 print("gsdfgsdfgfdg",inv_total)
#                 # inv_total=inv_total+inv_tax.final_amount_per_unit
#                 print("gsdfgsdfgfdg",inv_total)
#                 self.assertEqual(freight_total.total_collect_charges,inv_total)
#                 _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::prepaid calculation is successful")
            


