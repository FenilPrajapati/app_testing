# # -*- coding: utf-8 -*-
# # Part of Odoo. See LICENSE file for full copyright and licensing details.

# from odoo.tests import common
# from odoo import fields
# from odoo.tests import tagged, Form
# from odoo.addons.crm.tests.common import TestCrmCommon
# import logging

# _logger = logging.getLogger(__name__)
# class TestSq(TestCrmCommon):

#     @classmethod
#     def setUpClass(cls):
#         super(TestSq, cls).setUpClass()
#         cls.booking_no = cls.env['purchase.order'].search([
#             ('rfq_id', '=', 'erpbox00331')])
#         cls.enquiry = cls.env['sale.order'].search([
#             ('so_inquiry_id', '=', 'erpbox00331')])
#         cls.enquiry_no = cls.env['shipment.quote'].search([
#             ('booking_id', '=', 'erpbox00331')])
        

#     def test_compare_inquiry_no(self):
#         lead = self.enquiry_no
#         test_name=self.booking_no
#         #     'shipping_name_id':'53',
#         #     # 'booking_id': 'erpbox00009',
#         #     'valid_from':'2022-05-12',
#         #     'valid_to':'2022-06-10',
#         #     'company_id':'1',
#         #     'container_type':'1',
#         #     'booking_id':self.booking_id
#         # })

#         self.assertEqual(lead.booking_id,test_name.booking_id)
#         print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",lead.booking_id)
#         print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP",test_name.booking_id)
#         print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare test is successful")

#     def test_markup(self):
#         test_markup=0
#         lead = self.enquiry_no
#         self.assertGreater(lead.markup,test_markup)
#         print(":::::::::::::::::::::::::::::::::::::::::::::::::::::markup test is successful")

#     def test_compare_cargo_so_sq(self):
        
#         test_name=self.enquiry_no
#         lead = self.enquiry
#         self.assertEqual(lead.no_of_expected_container,test_name.no_of_expected_container)
#         print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare no of containers is successful")
#         self.assertEqual(lead.quantity,test_name.quantity)
#         print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare quantity is successful")
#         self.assertEqual(lead.weight,test_name.weight)
#         print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare weight is successful")
#         self.assertEqual(lead.volume,test_name.volume)
#         print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare volume is successful")
#         self.assertEqual(lead.move_type,test_name.move_type)
#         print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare move_type is successful")
#         self.assertEqual(lead.incoterm_id,test_name.incoterm_id)
#         print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare incoterm_id is successful")
#         self.assertEqual(lead.place_of_origin,test_name.place_of_origin)
#         print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare Point of Origin is successful")
#         self.assertEqual(lead.final_port_of_destination,test_name.final_port_of_destination)
#         print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare Point of Destination is successful")
#         # self.assertEqual(lead.point_of_stuffing,test_name.point_of_stuffing)
#         # print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare Point of Stuffing is successful")
#         # self.assertEqual(lead.point_of_destuffing,test_name.point_of_destuffing)
#         # print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare Point of Destuffing is successful")
#         self.assertEqual(lead.container_type,test_name.container_type)
#         print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare container type is successful")
#         self.assertEqual(lead.expected_date_of_shipment,test_name.expected_date_of_shipment)
#         print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compareexpected_date_of_shipment is successful")
#         self.assertEqual(lead.shipment_terms,test_name.shipment_terms)
#         print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare shipment terms is successful")
#         # self.assertEqual(lead.remarks,test_name.remarks)
#         # print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare remarks is successful")

#     # def test_reaonly_cargo(self):
#     #     test_cargo=self.env['shipment.quote'].browse(4)
#     #     self.assertReadonly(test_cargo.cargo_name)

#     # def test_readonly(self):
#     #     """Value and multiplier must be readonly"""
#     #     try:
#     #         self.cargo_name.value = 1
#     #         self.fail("Value is not read only")
#     #         print(":::::::::::::::::::::::::::::::::::::::::::::::::::::readonly is false")
#     #     except AttributeError:
#     #         pass
        
#     # def test_readonly_company_name(self):
#     #     sq = Form(self.env['shipment.quote'])
        
#     #     print(":::::::::::::::::::::::::::::::::::::::::::::::::::::readonly is true")

#     # def test_readonly_cargo(self):
#     #     sq = Form(self.env['shipment.quote'])
#     #     try:
#     #         sq.cargo_name="rice"
#     #         print("not readonly field")
#     #     # rc.unit_price=2
#     #     # amt=rc.units* rc.unit_price
#     #     except:
#     #         print("readonlyd")

#     def test__not_readonly(self):
#         sq = Form(self.enquiry_no)
#         try:
#             sq.booking_id="abc"
#             _logger.info("booking_id is not readonly field")
#         except:
#             _logger.warning("booking_id is readonly field")
        
#         try:
#             sq.partner_id="2"
#             _logger.info("partner is not readonly field")
#         except:
#             _logger.warning("partner is readonly field")
        
#         try:
#             sq.currency_id="INR"
#             _logger.info("currency_id is not readonly field")
#         # rc.unit_price=2
#         # amt=rc.units* rc.unit_price
#         except:
#             _logger.warning("currency_id is readonlyd")
        
#         try:
#             sq.po_id="5"
#             _logger.info("po_id is not readonly field")
#         except:
#             _logger.warning("po_id is readonly field")
        
#         try:
#             sq.weightt="89895"
#             _logger.info("weightt is not readonly field")
#         except:
#             _logger.warning("weightt is readonly field")

#     def test_readonly(self):
#         sq = Form(self.enquiry_no)
#         try:
#             sq.cargo_name="abc"
#             _logger.info("Cargo name is not readonly field")
#         except:
#             _logger.warning("cargo name is readonly")


        
#     # def test_sq_calc(self):
#     #     test_calc=self.enquiry_no
#     #     rc=test_calc.charges_line.browse(5)
#     #     # sq_sale=test_calc.markup/100
#     #     # print("???????????????????????????????????????????????", sq_sale)
#     #     print("???????????????????????????????????????????????", rc.unit_price)
#     #     total=rc.unit_price+test_calc.markup
#     #     print("???????????????????????????????????????????????", total)
#     #     self.assertEqual(rc.new_unit_price,total)
#     #     print(":::::::::::::::::::::::::::::::::::::::::::::::::::::taxxx is successful")

#     def test_sq_markup(self):
#         test_calc=self.enquiry_no
#         sq_total=0
#         for sq_tax in test_calc.charges_line:
#             sq_total=sq_tax.unit_price+sq_tax.unit_price*test_calc.markup/100
#             self.assertEqual(sq_tax.new_unit_price,sq_total)
#             print(":::::::::::::::::::::::::::::::::::::::::::::::::::::New Unit price is successful")

#     def test_tax_amount(self):
#         tax_calc=self.enquiry_no
#         sq_total=0
#         for sq_tax in tax_calc.charges_line:
#             tax=sq_tax.taxes_id.amount/100
#             sq_total=sq_tax.units*sq_tax.new_unit_price*tax
#             print(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,sq_tax.taxes_id",sq_tax.taxes_id.amount)
#             # self.assertEqual(so_cargo.sale_final_amount,sq_total)
#             # print(":::::::::::::::::::::::::::::::::::::::::::::::::::::calculation is successful")
#             self.assertEqual(sq_tax.sale_tax_amt,sq_total)
#             _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::Sale tax amount calculation is successful")

#     def test_calc_with_taxes_sq(self):
#         tax_calc=self.enquiry_no
#         sq_total=0
#         sq_total_amount=0
#         for sq_tax in tax_calc.charges_line:
#             if sq_tax.taxes_id:
#                 tax=sq_tax.taxes_id.amount/100
#                 print("gsdfgsdfgfdg",tax)
#                 sq_total=sq_tax.units*sq_tax.unit_price*tax
#                 self.assertEqual(sq_tax.tax_amt,sq_total)
#                 # print("gsdfgsdfgfdg",sq_tax.tax_amt)
#                 # print("gsdfgsdfgfdg",sq_total)
#                 _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::with tax calculation is successful")
#                 print(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,sq_tax.taxes_id",sq_tax.taxes_id.amount)
#                 sq_total_amount=sq_tax.units*sq_tax.unit_price+sq_total
#                 self.assertEqual(sq_tax.final_amount,sq_total_amount)
#             else:
#                 sq_total=sq_tax.units*sq_tax.unit_price
#                 print("dddddddddddddd",sq_total)
#                 print("dddddddddddddd",sq_tax.final_amount)
#                 self.assertEqual(sq_tax.final_amount,sq_total)
#                 _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::calculation is successful")

#     def test_total_origin_sq(self):
#         freight_total=self.enquiry_no
#         sq_total=0
#         for sq_tax in freight_total.charges_line:
#             if sq_tax.charges_type=="origin":
#                 # tax=sq_tax.taxes_id.amount/100
#                 # print("gsdfgsdfgfdg",tax)
#                 sq_total=sq_total+sq_tax.sale_final_amount
#         self.assertEqual(freight_total.total_origin_charge,sq_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::origin calculation is successful")

#     def test_total_freight_sq(self):
#         freight_total=self.enquiry_no
#         sq_total=0
#         for sq_tax in freight_total.charges_line:
#             if sq_tax.charges_type=="freight":
#                 # tax=sq_tax.taxes_id.amount/100
#                 # print("gsdfgsdfgfdg",tax)
#                 sq_total=sq_total+sq_tax.sale_final_amount
#         self.assertEqual(freight_total.total_freight_charge,sq_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::freight calculation is successful")
            
#     def test_total_destination_sq(self):
#         freight_total=self.enquiry_no
#         sq_total=0
#         for sq_tax in freight_total.charges_line:
#             if sq_tax.charges_type=="destination":
#                 # tax=sq_tax.taxes_id.amount/100
#                 # print("gsdfgsdfgfdg",tax)
#                 sq_total=sq_total+sq_tax.sale_final_amount
#         self.assertEqual(freight_total.total_destination_charge,sq_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::destination calculation is successful")

#     def test_total_charge_sq(self):
#         freight_total=self.enquiry_no
#         sq_total=freight_total.total_destination_charge+freight_total.total_origin_charge+freight_total.total_freight_charge
#         self.assertEqual(freight_total.total_charge,sq_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::total charge calculation is successful")

#     def test_total_charge_for_loop_sq(self):
#         freight_total=self.enquiry_no
#         sq_total=sq_total_destination=sq_total_origin=sq_total_freight=0
#         for sq_tax in freight_total.charges_line:
#             if sq_tax.charges_type=="destination":
#                 sq_total_destination=sq_total_destination+sq_tax.sale_final_amount
#             if sq_tax.charges_type=="origin":
#                 sq_total_origin=sq_total_origin+sq_tax.sale_final_amount
#             if sq_tax.charges_type=="freight":
#                 sq_total_freight=sq_total_freight+sq_tax.sale_final_amount
#         sq_total=sq_total_destination+sq_total_origin+sq_total_freight
#         self.assertEqual(freight_total.total_charge,sq_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::total charge calculation inside for loop is successful")

#     def test_sq_markup(self):
#         test_calc=self.env['shipment.quote'].browse(9)
#         sq_total=0
#         if test_calc.markup==0:
#             for sq_markup in test_calc.charges_line:
#                 self.assertEqual(sq_markup.new_unit_price,sq_total)
#                 print(":::::::::::::::::::::::::::::::::::::::::::::::::::::test markup is successful")

#     # def test_sum_of_final_amt_per_unit_sq(self):
#     #     freight_total=self.booking_no
#     #     sq_total=0
#     #     for sq_tax in freight_total.charges_line:
#     #         sq_total=sq_total+sq_tax.final_amount_per_unit
#     #     self.assertEqual(freight_total.total_final_amount_per_unit,sq_total)
#     #     print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPsq_total",sq_total)
#     #     _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::: sum of final amount per unit calculation is successful")
            

#     # def test_sum_of_final_amt_per_unit_2_sq(self):
#     #     freight_total=self.booking_no
#     #     sq_total=sq_prepaid_total=sq_collect_total=0
#     #     for sq_tax in freight_total.charges_line:
#     #         if sq_tax.prepaid==True:
#     #             tax=sq_tax.taxes_id.amount/100*sq_tax.unit_price
#     #             sq_prepaid_total=sq_tax.unit_price+tax
#     #             sq_prepaid_total=sq_prepaid_total+sq_tax.final_amount_per_unit
#     #             print("gsdfgsdfgfdg",sq_prepaid_total)
#     #         if sq_tax.collect==True:
#     #             tax=sq_tax.taxes_id.amount/100*sq_tax.unit_price
#     #             sq_collect_total=sq_tax.unit_price+tax
#     #             print("gsdfgsdfgfdg",tax)
#     #             print("gsdfgsdfgfdg",sq_collect_total)
#     #             # sq_total=sq_total+sq_tax.final_amount_per_unit
#     #             # print("gsdfgsdfgfdg",sq_total)
#     #     sq_total=sq_prepaid_total+sq_collect_total        
#     #     # self.assertEqual(freight_total.total_collect_charges,sq_total)
#     #     self.assertEqual(freight_total.total_final_amount_per_unit,sq_total)
#     #     print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPsq_total",sq_total)
#     #     _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::: sum of final amount per unit calculation with if condition is successful")

#     # def test_sum_of_final_amt_per_unit_3_sq(self):
#     #     freight_total=self.booking_no
#     #     sq_total=freight_total.total_prepaid_charges+freight_total.total_collect_charges
#     #     self.assertEqual(freight_total.total_final_amount_per_unit,sq_total)
#     #     _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::total charge calculation using prepaid and collect charges is successful")    

#     # def test_total_prepaid_sq(self):
#     #     freight_total=self.booking_no
#     #     sq_total=0
#     #     for sq_tax in freight_total.charges_line:
#     #         if sq_tax.prepaid==True:
#     #             tax=sq_tax.taxes_id.amount/100*sq_tax.unit_price
#     #             sq_total=sq_tax.unit_price+tax
#     #             print("gsdfgsdfgfdg",tax)
#     #             print("gsdfgsdfgfdg",sq_total)
#     #             sq_total=sq_total+sq_tax.final_amount_per_unit
#     #     print("gsdfgsdfgfdg",sq_total)
#     #     self.assertEqual(freight_total.total_prepaid_charges,sq_total)
#     #     _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::prepaid calculation is successful")
            

#     # def test_total_collect_sq(self):
#     #     freight_total=self.booking_no
#     #     sq_total=0
#     #     for sq_tax in freight_total.charges_line:
#     #         if sq_tax.collect==True:
#     #             tax=sq_tax.taxes_id.amount/100*sq_tax.unit_price
#     #             sq_total=sq_tax.unit_price+tax
#     #             print("gsdfgsdfgfdg",tax)
#     #             print("gsdfgsdfgfdg",sq_total)
#     #             # sq_total=sq_total+sq_tax.final_amount_per_unit
#     #             print("gsdfgsdfgfdg",sq_total)
#     #             self.assertEqual(freight_total.total_collect_charges,sq_total)
#     #             _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::prepaid calculation is successful")

#     def test_update_sale_price(self):
#         charges=self.env['shipment.quote'].sudo().search([('booking_id','=', 'erpbox01234')], limit=1)
#         print("::::::::::::::::::charges",charges)
#         print("::::::::::::::::::markup",charges.markup)
#         print("::::::::::::::::::currency_id",charges.currency_id)
#         sale_price=0
#         if charges.markup>0:
#             print("::::::::::::::::::markup",charges.markup)
#             update=charges.update_sale_price()
#             print("update:::::::::::::::::::",charges.charges_line)
#             for value in charges.charges_line:
#                 # self.assertIsNone(value.charges_id,"False")
#                 sale_price=0
#                 sale_price=charges.markup/100*value.unit_price+value.unit_price
#                 print(":::::::::::::::::::::::::::::::::", value.rfq_id)
#                 print(":::::::::::::::::::::::::::::::::sale_price",sale_price)
#                 try:
#                     self.assertEqual(value.new_unit_price,sale_price)
#                     # print("value.units:::::::::::::::::::::::::::::",value.units)
#                     print("equal")
#                 except:
#                     print("not equal")




        
    