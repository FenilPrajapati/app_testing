# # -*- coding: utf-8 -*-
# # Part of Odoo. See LICENSE file for full copyright and licensing details.

# from odoo.tests import common
# from odoo import fields
# from odoo.tests import tagged, Form
# from odoo.addons.crm.tests.common import TestCrmCommon
# import logging
# from odoo.addons.sale.tests.common import TestSaleCommon

# _logger = logging.getLogger(__name__)

# class TestSo(TestSaleCommon):

#     @classmethod
#     def setUpClass(cls):
#         super(TestSo, cls).setUpClass()
#         cls.so_id = cls.env['sale.order'].search([
#             ('so_inquiry_id', '=', 'erpbox00331')])
#         cls.sq_id = cls.env['shipment.quote'].search([
#             ('booking_id', '=', 'erpbox00331')])

#     # def test_sq_calc(self):
#     #     test_calc=self.so_id
#     #     for so_cargo in test_calc.charges_line:
#     #         so_total=so_cargo.units*so_cargo.new_unit_price
#     #         self.assertEqual(so_cargo.sale_final_amount,so_total)
#     #         print(":::::::::::::::::::::::::::::::::::::::::::::::::::::calculation is successful")


#     def test_cargo(self):
#         test_cargo=self.so_id
#         for so_cargo in test_cargo.charges_line:
#             # so_total=so_cargo.units*so_cargo.new_unit_price
#             self.assertEqual(test_cargo.no_of_expected_container,so_cargo.units)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::no od expected containers is correct")

#     def test_total_charge(self):
#         test_total=self.so_id
#         amount_total = 0
#         for so_total in test_total.charges_line:
#             # amount_total = 0
#             amount_total =amount_total+so_total.sale_final_amount
#         print("??????????????????????????????????????????????amount_total",amount_total)
#         print("??????????????????????????????????????????????test_total.total_charge",test_total.total_charge)
#         self.assertEqual(test_total.total_charge,amount_total)
#         print(":::::::::::::::::::::::::::::::::::::::::::::::::::::total charge is correct")

#     def test_calc_with_taxes_so(self):
#         tax_calc=self.so_id
#         so_total=0
#         so_total_amount=0
#         for so_tax in tax_calc.charges_line:
#             if so_tax.taxes_id:
#                 tax=so_tax.taxes_id.amount/100
#                 print("gsdfgsdfgfdg",tax)
#                 so_total=so_tax.units*so_tax.new_unit_price*tax
#                 self.assertEqual(so_tax.sale_tax_amt,so_total)
#                 # print("gsdfgsdfgfdg",so_tax.tax_amt)
#                 # print("gsdfgsdfgfdg",so_total)
#                 _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::with tax calculation is successful")
#                 print(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,sq_tax.taxes_id",so_tax.taxes_id.amount)
#                 so_total_amount=so_tax.units*so_tax.new_unit_price+so_total
#                 self.assertEqual(so_tax.sale_final_amount,so_total_amount)
#             else:
#                 so_total=so_tax.units*so_tax.new_unit_price
#                 print("dddddddddddddd",so_total)
#                 print("dddddddddddddd",so_tax.sale_final_amount)
#                 self.assertEqual(so_tax.sale_final_amount,so_total)
#                 _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::calculation is successful")

#     def test_total_origin_so(self):
#         freight_total=self.so_id
#         so_total=0
#         for so_tax in freight_total.charges_line:
#             if so_tax.charges_type=="origin":
#                 # tax=so_tax.taxes_id.amount/100
#                 # print("gsdfgsdfgfdg",tax)
#                 so_total=so_total+so_tax.sale_final_amount
#         self.assertEqual(freight_total.total_origin_charge,so_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::origin calculation is successful")
#         print("dddddddddddddd",so_total)
#         print("dddddddddddddd",freight_total.total_origin_charge)

#     def test_total_freight_so(self):
#         freight_total=self.so_id
#         so_total=0
#         for so_tax in freight_total.charges_line:
#             if so_tax.charges_type=="freight":
#                 # tax=so_tax.taxes_id.amount/100
#                 # print("gsdfgsdfgfdg",tax)
#                 so_total=so_total+so_tax.sale_final_amount
#         self.assertEqual(freight_total.total_freight_charge,so_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::freight calculation is successful")
            
#     def test_total_destination_so(self):
#         freight_total=self.so_id
#         so_total=0
#         for so_tax in freight_total.charges_line:
#             if so_tax.charges_type=="destination":
#                 # tax=so_tax.taxes_id.amount/100
#                 # print("gsdfgsdfgfdg",tax)
#                 so_total=so_total+so_tax.sale_final_amount
#         self.assertEqual(freight_total.total_destination_charge,so_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::destination calculation is successful")

#     def test_total_charge_so(self):
#         freight_total=self.so_id
#         so_total=freight_total.total_destination_charge+freight_total.total_origin_charge+freight_total.total_freight_charge
#         self.assertEqual(freight_total.total_charge,so_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::total charge calculation is successful")

#     def test_total_charge_for_loop_so(self):
#         freight_total=self.so_id
#         so_total=so_total_destination=so_total_origin=so_total_freight=0
#         for so_tax in freight_total.charges_line:
#             if so_tax.charges_type=="destination":
#                 so_total_destination=so_total_destination+so_tax.sale_final_amount
#             if so_tax.charges_type=="origin":
#                 so_total_origin=so_total_origin+so_tax.sale_final_amount
#             if so_tax.charges_type=="freight":
#                 so_total_freight=so_total_freight+so_tax.sale_final_amount
#         so_total=so_total_destination+so_total_origin+so_total_freight
#         self.assertEqual(freight_total.total_charge,so_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::total charge calculation inside for loop is successful")

#     def test_sum_of_final_amt_per_unit_so(self):
#         freight_total=self.so_id
#         so_total=0
#         for so_tax in freight_total.charges_line:
#             so_total=so_total+so_tax.sale_final_amount_per_unit
#         self.assertEqual(freight_total.total_final_amount_per_unit,so_total)
#         print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPso_total",so_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::: sum of final amount per unit calculation is successful")
            

#     def test_sum_of_final_amt_per_unit_2_so(self):
#         freight_total=self.so_id
#         so_total=so_prepaid_total=so_collect_total=0
#         for so_tax in freight_total.charges_line:
#             if so_tax.prepaid==True:
#                 tax=so_tax.taxes_id.amount/100*so_tax.new_unit_price
#                 so_prepaid_total=so_tax.new_unit_price+tax
#                 so_prepaid_total=so_prepaid_total+so_tax.sale_final_amount_per_unit
#                 print("gsdfgsdfgfdg",so_prepaid_total)
#             if so_tax.collect==True:
#                 tax=so_tax.taxes_id.amount/100*so_tax.new_unit_price
#                 so_collect_total=so_tax.new_unit_price+tax
#                 print("gsdfgsdfgfdg",tax)
#                 print("gsdfgsdfgfdg",so_collect_total)
#                 # so_total=so_total+so_tax.final_amount_per_unit
#                 # print("gsdfgsdfgfdg",so_total)
#         so_total=so_prepaid_total+so_collect_total        
#         # self.assertEqual(freight_total.total_collect_charges,so_total)
#         self.assertEqual(freight_total.total_final_amount_per_unit,so_total)
#         print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPso_total",so_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::: sum of final amount per unit calculation with if condition is successful")

#     def test_sum_of_final_amt_per_unit_3_so(self):
#         freight_total=self.so_id
#         so_total=freight_total.total_prepaid_charges+freight_total.total_collect_charges
#         self.assertEqual(freight_total.total_final_amount_per_unit,so_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::total charge calculation using prepaid and collect charges is successful")    

#     def test_total_prepaid_so(self):
#         freight_total=self.so_id
#         so_total=0
#         for so_tax in freight_total.charges_line:
#             if so_tax.prepaid==True:
#                 tax=so_tax.taxes_id.amount/100*so_tax.new_unit_price
#                 so_total=so_tax.new_unit_price+tax
#                 print("gsdfgsdfgfdg",tax)
#                 print("gsdfgsdfgfdg",so_total)
#                 so_total=so_total+so_tax.sale_final_amount_per_unit
#         print("gsdfgsdfgfdg",so_total)
#         self.assertEqual(freight_total.total_prepaid_charges,so_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::prepaid calculation is successful")
            

#     def test_total_collect_so(self):
#         freight_total=self.so_id
#         so_total=0
#         for so_tax in freight_total.charges_line:
#             if so_tax.collect==True:
#                 tax=so_tax.taxes_id.amount/100*so_tax.new_unit_price
#                 so_total=so_tax.new_unit_price+tax
#                 print("gsdfgsdfgfdg",tax)
#                 print("gsdfgsdfgfdg",so_total)
#                 # so_total=so_total+so_tax.final_amount_per_unit
#                 print("gsdfgsdfgfdg",so_total)
#                 self.assertEqual(freight_total.total_collect_charges,so_total)
#                 _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::prepaid calculation is successful")

#     def test__not_readonly(self):
#         so = Form(self.so_id)
#         try:
#             so.so_inquiry_id="1"
#             _logger.info("so_inquiry id is not readonly field")
#         except:
#             _logger.warning("so_inquiry id is readonly field")

#         try:
#             so.partner_id.name="BC"
#             _logger.info("partner id is not readonly field")
#         except:
#             _logger.warning("partner id is readonly field")

#         try:
#             so.validity_date="1/2/12"
#             _logger.info("validity_date id is not readonly field")
#         except:
#             _logger.warning("validity_date id is readonly field")


#     def test_readonly(self):
#         so = Form(self.so_id)
#         try:
#             so.cargo_name="abc"
#             _logger.info("Cargo name is not readonly field")
#         except:
#             _logger.warning("cargo name is readonly")


#     #confirm quotation
#     def test_confirm(self):
        
#         so = self.env['sale.order'].sudo().search([('booking_id','=', 'erpbox01234')], limit=1)
#         print(":::::::::::::::::::::::::::::::::::::so.state",so.state)
#         so.action_confirm()
#         print(":::::::::::::::::::::::::::::::::::::so.state",so.state)
#         self.assertTrue(so.state == 'sale', msg=None)
#         self.assertTrue(so.invoice_status == 'to invoice')
#         print(":::::::::::success")



#     def test_confirm_po(self):
#         so = self.env['sale.order'].sudo().search([('booking_id','=', 'erpbox01234')], limit=1)
#         print(":::::::::::::::::::::::::::::::::::::so.state",so.state)
#         so.action_confirm_po()
#         print(":::::::::::::::::::::::::::::::::::::so.state",so.state)
#         self.assertTrue(so.state == 'po_confirm', msg=None)
#     #     # self.assertFalse(so.is_purchase_confirmed,)
#         self.assertTrue(so.is_purchase_confirmed, msg=None)
#     #     # self.is_purchase_confirmed = True
#     #     # self.write({'state': 'po_confirm'})
#         print(":::::::::::success")

    

    
