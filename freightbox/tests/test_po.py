# # -*- coding: utf-8 -*-
# # Part of Odoo. See LICENSE file for full copyright and licensing details.
# from odoo.addons.account.tests.common import AccountTestInvoicingCommon
# from odoo.tests import Form
# from odoo import fields
# from odoo.tests import common
# from odoo.addons.crm.tests.common import TestCrmCommon
# from datetime import timedelta, datetime
# from freezegun import freeze_time
# import logging

# _logger = logging.getLogger(__name__)

# class TestPurchase(AccountTestInvoicingCommon):

#     @classmethod
#     def setUpClass(cls):
#         super(TestPurchase, cls).setUpClass()
        

#     def test_date_planned(self):
#         """Set a date planned on 2 PO lines. Check that the PO date_planned is the earliest PO line date
#         planned. Change one of the dates so it is even earlier and check that the date_planned is set to
#         this earlier date.
#         """
#         po = Form(self.env['purchase.order'])
#         po.partner_id = self.partner_a
#         with po.order_line.new() as po_line:
#             po_line.product_id = self.product_a
#             po_line.product_qty = 1
#             po_line.price_unit = 100
#         with po.order_line.new() as po_line:
#             po_line.product_id = self.product_b
#             po_line.product_qty = 10
#             po_line.price_unit = 200
#         po = po.save()

#         # Check that the same date is planned on both PO lines.
#         self.assertNotEqual(po.order_line[0].date_planned, False)
#         self.assertAlmostEqual(po.order_line[0].date_planned, po.order_line[1].date_planned, delta=timedelta(seconds=10))
#         self.assertAlmostEqual(po.order_line[0].date_planned, po.date_planned, delta=timedelta(seconds=10))

#         orig_date_planned = po.order_line[0].date_planned

#         # Set an earlier date planned on a PO line and check that the PO expected date matches it.
#         new_date_planned = orig_date_planned - timedelta(hours=1)
#         po.order_line[0].date_planned = new_date_planned
#         self.assertAlmostEqual(po.order_line[0].date_planned, po.date_planned, delta=timedelta(seconds=10))

#         # Set an even earlier date planned on the other PO line and check that the PO expected date matches it.
#         new_date_planned = orig_date_planned - timedelta(hours=72)
#         po.order_line[1].date_planned = new_date_planned
#         self.assertAlmostEqual(po.order_line[1].date_planned, po.date_planned, delta=timedelta(seconds=10))

#     @freeze_time("2021-12-02 21:00")
#     def test_date_planned_02(self):
#         """Check the planned date definition when server is UTC and user is UTC+11"""
#         # UTC:  2021-12-02 21:00
#         # User: 2021-12-03 08:00 (UTC+11)
#         self.env.user.tz = "Australia/Sydney"
#         po_form = Form(self.env['purchase.order'])
#         po_form.partner_id = self.partner_a
#         with po_form.order_line.new() as po_line:
#             po_line.product_id = self.product_a
#         self.assertEqual(po_form.date_planned, datetime.fromisoformat("2021-12-03 01:00:00"),
#                          "Should be 2021-12-03 01:00:00, i.e. 2021-12-03 12:00:00 UTC+11")

#     # def test_compare_vendor(self):
#     #     lead = self.env['purchase.order'].browse(243)
#     #     test_name=self.env['request.for.quote'].browse(148)
        

#     #     self.assertEqual(lead.partner_id,test_name.shipping_name_id)
#     #     print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare vendor is successful")

#     # def test_date(self):
#     #     today_time = datetime.datetime.now()
#     #     print("???????????????????????????????????????????????", today_time)
#     #     lead = self.env['purchase.order'].browse(33)
#     #     self.assertEqual(lead.date_order,today_time)

#     # def test_currency(self):
#     #     today = self.env['res.company'].browse(1)
#     #     print("???????????????????????????????????????????????", today)
#     #     lead=self.env['purchase.order'].browse(32)
#     #     self.assertEqual(lead.currency_id,today.currency_id)

#     # def test_valid_to(self):
#     #     today = fields.Date.today()
#     #     lead=self.env['request.for.quote'].browse(148)
#     #     self.assertGreater(lead.valid_to,today)
#     #     print("valid to is greater ???????????????????????????????????????????????")
#     #     self.assertGreater(lead.valid_to,lead.valid_from)
#     #     print("valid to is greater than valid from")

#     # def test_compare_cargo_rfq_po(self):
        
#     #     test_name=self.env['request.for.quote'].browse(148)
#     #     lead = self.env['purchase.order'].browse(243)
#     #     self.assertEqual(lead.no_of_expected_container,test_name.no_of_expected_container)
#     #     print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare no of containers is successful")
#     #     self.assertEqual(lead.quantity,test_name.quantity)
#     #     print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare quantity is successful")
#     #     self.assertEqual(lead.weight,test_name.weight)
#     #     print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare weight is successful")
#     #     self.assertEqual(lead.volume,test_name.volume)
#     #     print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare volume is successful")
#     #     self.assertEqual(lead.move_type,test_name.move_type)
#     #     print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare move_type is successful")
#     #     self.assertEqual(lead.incoterm_id,test_name.incoterm_id)
#     #     print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare incoterm_id is successful")
#     #     self.assertEqual(lead.place_of_origin,test_name.place_of_origin)
#     #     print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare Point of Origin is successful")
#     #     self.assertEqual(lead.final_port_of_destination,test_name.final_port_of_destination)
#     #     print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare Point of Destination is successful")
#     #     # self.assertEqual(lead.point_of_stuffing,test_name.point_of_stuffing)
#     #     # print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare Point of Stuffing is successful")
#     #     # self.assertEqual(lead.point_of_destuffing,test_name.point_of_destuffing)
#     #     # print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare Point of Destuffing is successful")
#     #     self.assertEqual(lead.container_type,test_name.container_type)
#     #     print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare container type is successful")
#     #     self.assertEqual(lead.expected_date_of_shipment,test_name.expected_date_of_shipment)
#     #     print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compareexpected_date_of_shipment is successful")
#     #     self.assertEqual(lead.shipment_terms,test_name.shipment_terms)
#     #     print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare shipment terms is successful")
#     #     # self.assertEqual(lead.remarks,test_name.remarks)
#     #     # print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare remarks is successful")

#     def test_purchase_order_sequence(self):
#         PurchaseOrder = self.env['purchase.order'].with_context(tracking_disable=True)
#         company = self.env.user.company_id
#         self.env['ir.sequence'].search([
#             ('code', '=', 'purchase.order'),
#         ]).write({
#             'use_date_range': True, 'prefix': 'PO/%(range_year)s/',
#         })
#         vals = {
#             'partner_id': self.partner_a.id,
#             'company_id': company.id,
#             'currency_id': company.currency_id.id,
#             'date_order': '2019-01-01',
#         }
#         purchase_order = PurchaseOrder.create(vals.copy())
#         self.assertTrue(purchase_order.name.startswith('PO/2019/'))
#         vals['date_order'] = '2020-01-01'
#         purchase_order = PurchaseOrder.create(vals.copy())
#         self.assertTrue(purchase_order.name.startswith('PO/2020/'))
#         # In EU/BXL tz, this is actually already 01/01/2020
#         vals['date_order'] = '2019-12-31 23:30:00'
#         purchase_order = PurchaseOrder.with_context(tz='Europe/Brussels').create(vals.copy())
#         self.assertTrue(purchase_order.name.startswith('PO/2020/'))

#     def test_reminder_1(self):
#         """Set to send reminder today, check if a reminder can be send to the
#         partner.
#         """
#         po = Form(self.env['purchase.order'])
#         po.partner_id = self.partner_a
#         with po.order_line.new() as po_line:
#             po_line.product_id = self.product_a
#             po_line.product_qty = 1
#             po_line.price_unit = 100
#         with po.order_line.new() as po_line:
#             po_line.product_id = self.product_b
#             po_line.product_qty = 10
#             po_line.price_unit = 200
#         # set to send reminder today
#         po.date_planned = fields.Datetime.now() + timedelta(days=1)
#         po.receipt_reminder_email = True
#         po.reminder_date_before_receipt = 1
#         po = po.save()
#         po.button_confirm()

#         # check vendor is a message recipient
#         self.assertTrue(po.partner_id in po.message_partner_ids)

#         old_messages = po.message_ids
#         po._send_reminder_mail()
#         messages_send = po.message_ids - old_messages
#         # check reminder send
#         self.assertTrue(messages_send)
#         self.assertTrue(po.partner_id in messages_send.mapped('partner_ids'))

#         # check confirm button
#         po.confirm_reminder_mail()
#         self.assertTrue(po.mail_reminder_confirmed)

#     def test_reminder_2(self):
#         """Set to send reminder tomorrow, check if no reminder can be send.
#         """
#         po = Form(self.env['purchase.order'])
#         po.partner_id = self.partner_a
#         with po.order_line.new() as po_line:
#             po_line.product_id = self.product_a
#             po_line.product_qty = 1
#             po_line.price_unit = 100
#         with po.order_line.new() as po_line:
#             po_line.product_id = self.product_b
#             po_line.product_qty = 10
#             po_line.price_unit = 200
#         # set to send reminder tomorrow
#         po.date_planned = fields.Datetime.now() + timedelta(days=2)
#         po.receipt_reminder_email = True
#         po.reminder_date_before_receipt = 1
#         po = po.save()
#         po.button_confirm()

#         # check vendor is a message recipient
#         self.assertTrue(po.partner_id in po.message_partner_ids)

#         old_messages = po.message_ids
#         po._send_reminder_mail()
#         messages_send = po.message_ids - old_messages
#         # check no reminder send
#         self.assertFalse(messages_send)

#     def test_update_date_planned(self):
#         po = Form(self.env['purchase.order'])
#         po.partner_id = self.partner_a
#         with po.order_line.new() as po_line:
#             po_line.product_id = self.product_a
#             po_line.product_qty = 1
#             po_line.price_unit = 100
#             po_line.date_planned = '2020-06-06 00:00:00'
#         with po.order_line.new() as po_line:
#             po_line.product_id = self.product_b
#             po_line.product_qty = 10
#             po_line.price_unit = 200
#             po_line.date_planned = '2020-06-06 00:00:00'
#         po = po.save()
#         po.button_confirm()

#         # update first line
#         po._update_date_planned_for_lines([(po.order_line[0], fields.Datetime.today())])
#         self.assertEqual(po.order_line[0].date_planned, fields.Datetime.today())
#         activity = self.env['mail.activity'].search([
#             ('summary', '=', 'Date Updated'),
#             ('res_model_id', '=', 'purchase.order'),
#             ('res_id', '=', po.id),
#         ])
#         self.assertTrue(activity)
#         self.assertIn(
#             '<p> partner_a modified receipt dates for the following products:</p><p> \xa0 - product_a from 2020-06-06 to %s </p>' % fields.Date.today(),
#             activity.note,
#         )

#         # update second line
#         po._update_date_planned_for_lines([(po.order_line[1], fields.Datetime.today())])
#         self.assertEqual(po.order_line[1].date_planned, fields.Datetime.today())
#         self.assertIn(
#             '<p> partner_a modified receipt dates for the following products:</p><p> \xa0 - product_a from 2020-06-06 to %s </p><p> \xa0 - product_b from 2020-06-06 to %s </p>' % (fields.Date.today(), fields.Date.today()),
#             activity.note,
#         )

#     def test_with_different_uom(self):
#         """ This test ensures that the unit price is correctly computed"""
#         uom_units = self.env['ir.model.data'].xmlid_to_object('uom.product_uom_unit')
#         uom_dozens = self.env['ir.model.data'].xmlid_to_object('uom.product_uom_dozen')
#         uom_pairs = self.env['uom.uom'].create({
#             'name': 'Pairs',
#             'category_id': uom_units.category_id.id,
#             'uom_type': 'bigger',
#             'factor_inv': 2,
#             'rounding': 1,
#         })
#         product_data = {
#             'name': 'SuperProduct',
#             'type': 'consu',
#             'uom_id': uom_units.id,
#             'uom_po_id': uom_pairs.id,
#             'standard_price': 100
#         }
#         product_01 = self.env['product.product'].create(product_data)
#         product_02 = self.env['product.product'].create(product_data)

#         po_form = Form(self.env['purchase.order'])
#         po_form.partner_id = self.partner_a
#         with po_form.order_line.new() as po_line:
#             po_line.product_id = product_01
#         with po_form.order_line.new() as po_line:
#             po_line.product_id = product_02
#             po_line.product_uom = uom_dozens
#         po = po_form.save()

#         self.assertEqual(po.order_line[0].price_unit, 200)
#         self.assertEqual(po.order_line[1].price_unit, 1200)

# class TestPo(TestCrmCommon):

#     @classmethod
#     def setUpClass(cls):
#         super(TestPo, cls).setUpClass()
#         cls.booking_no = cls.env['purchase.order'].search([
#             ('rfq_id', '=', 'erpbox00331')])
#         cls.enquiry_no = cls.env['request.for.quote'].search([
#             ('booking_id', '=', 'erpbox00331')])
#         cls.enquiry = cls.env['shipment.quote'].search([
#             ('booking_id', '=', 'erpbox00331')])
#         # cls.charges_id = cls.env.ref('charges')
#         # cls.country_ref = cls.env.ref('base.be')
#         # cls.test_email = 'abcd@jdfjshdg.com'
#         # cls.test_phone = '0485112233'
#         # cls.booking_id  = "291"

#     def test_compare_vendor(self):
#         test_vendor = self.booking_no
#         test_name=self.enquiry_no
#         #     'shipping_name_id':'53',
#         #     # 'booking_id': 'erpbox00009',
#         #     'valid_from':'2022-05-12',
#         #     'valid_to':'2022-06-10',
#         #     'company_id':'1',
#         #     'container_type':'1',
#         #     'booking_id':self.booking_id
#         # })

#         self.assertEqual(test_vendor.partner_id,test_name.shipping_name_id)
#         print(":::::::::::::::::::::::::::::::::::::::::::::::::::::compare vendor is successful")

#     def test_date(self):
#         # today_time = datetime.datetime.now()
#         # print("???????????????????????????????????????????????", today_time)
#         test_date = self.booking_no
#         print(":::::::::::::::::::::",test_date.create_date)
#         self.assertEqual(test_date.date_order,test_date.create_date)
    
#     # def test_approve_button(self):
#     #     # lead = self.env['crm.lead'].browse(274)
#     #     test_name=self.env['request.for.quote'].create({
#     #         'shipping_name_id':'53',
#     #         # 'booking_id': 'erpbox00009',
#     #         'valid_from':'2022-05-12',
#     #         'valid_to':'2022-06-10',
#     #         'company_id':'1',
#     #         'container_type':'1',
#     #         'booking_id':'301',
#     #         'charges_line':cls.charges_id,
#     #         'charges_type':'Freight',
#     #         # 'container_type':
#     #         'units':'3',
#     #         'unit_price':'1000',
#     #         'currency_id':'INR',
#     #         'to_currency_id':'INR'

#     #     })

#     #     # self.assertEqual(lead.booking_id,test_name.booking_id)
#     #     test_name.button_approve()
#     #     print(":::::::::::::::::::::::::::::::::::::::::::::::::::::button test is successful")

#     def test_currency(self):
#         currency = self.env['res.company'].browse(1)
#         print("???????????????????????????????????????????????", currency)
#         test_currency=self.booking_no
#         self.assertEqual(test_currency.currency_id,currency.currency_id)

#     # def test_valid_to(self):
#     #     today = fields.Date.today()
#     #     lead=self.env['request.for.quote'].browse(63)
#     #     self.assertGreater(lead.valid_to,today)
#     #     print("valid to is greater ???????????????????????????????????????????????")
#     #     self.assertGreater(lead.valid_to,lead.valid_from)
#     #     print("valid to is greater than valid from ???????????????????????????????????????????????")
        

#     def test_compare_cargo_rfq_po(self):
        
#         test_name=self.enquiry
#         lead = self.booking_no
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

#     def test_calc_with_taxes_po(self):
#         tax_calc=self.booking_no
#         po_total=0
#         po_total_amount=0
#         for po_tax in tax_calc.charges_line:
#             if po_tax.taxes_id:
#                 tax=po_tax.taxes_id.amount/100
#                 print("gsdfgsdfgfdg",tax)
#                 po_total=po_tax.units*po_tax.unit_price*tax
#                 self.assertEqual(po_tax.tax_amt,po_total)
#                 # print("gsdfgsdfgfdg",po_tax.tax_amt)
#                 # print("gsdfgsdfgfdg",po_total)
#                 _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::with tax calculation is successful")
#                 print(",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,sq_tax.taxes_id",po_tax.taxes_id.amount)
#                 po_total_amount=po_tax.units*po_tax.unit_price+po_total
#                 self.assertEqual(po_tax.final_amount,po_total_amount)
#             else:
#                 po_total=po_tax.units*po_tax.unit_price
#                 print("dddddddddddddd",po_total)
#                 print("dddddddddddddd",po_tax.final_amount)
#                 self.assertEqual(po_tax.final_amount,po_total)
#                 _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::calculation is successful")

#     def test_total_origin_po(self):
#         freight_total=self.booking_no
#         po_total=0
#         for po_tax in freight_total.charges_line:
#             if po_tax.charges_type=="origin":
#                 # tax=po_tax.taxes_id.amount/100
#                 # print("gsdfgsdfgfdg",tax)
#                 po_total=po_total+po_tax.final_amount
#         self.assertEqual(freight_total.total_origin_charge,po_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::origin calculation is successful")

#     def test_total_freight_po(self):
#         freight_total=self.booking_no
#         po_total=0
#         for po_tax in freight_total.charges_line:
#             if po_tax.charges_type=="freight":
#                 # tax=po_tax.taxes_id.amount/100
#                 # print("gsdfgsdfgfdg",tax)
#                 po_total=po_total+po_tax.final_amount
#         self.assertEqual(freight_total.total_freight_charge,po_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::freight calculation is successful")
            
#     def test_total_destination_po(self):
#         freight_total=self.booking_no
#         po_total=0
#         for po_tax in freight_total.charges_line:
#             if po_tax.charges_type=="destination":
#                 # tax=po_tax.taxes_id.amount/100
#                 # print("gsdfgsdfgfdg",tax)
#                 po_total=po_total+po_tax.final_amount
#         self.assertEqual(freight_total.total_destination_charge,po_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::destination calculation is successful")

#     def test_total_charge_po(self):
#         freight_total=self.booking_no
#         po_total=freight_total.total_destination_charge+freight_total.total_origin_charge+freight_total.total_freight_charge
#         self.assertEqual(freight_total.total_charge,po_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::total charge calculation is successful")

#     def test_total_charge_for_loop_po(self):
#         freight_total=self.booking_no
#         po_total=po_total_destination=po_total_origin=po_total_freight=0
#         for po_tax in freight_total.charges_line:
#             if po_tax.charges_type=="destination":
#                 po_total_destination=po_total_destination+po_tax.final_amount
#             if po_tax.charges_type=="origin":
#                 po_total_origin=po_total_origin+po_tax.final_amount
#             if po_tax.charges_type=="freight":
#                 po_total_freight=po_total_freight+po_tax.final_amount
#         po_total=po_total_destination+po_total_origin+po_total_freight
#         self.assertEqual(freight_total.total_charge,po_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::total charge calculation inside for loop is successful")

#     def test_sum_of_final_amt_per_unit_po(self):
#         freight_total=self.booking_no
#         po_total=0
#         for po_tax in freight_total.charges_line:
#             po_total=po_total+po_tax.final_amount_per_unit
#         self.assertEqual(freight_total.total_final_amount_per_unit,po_total)
#         print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPpo_total",po_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::: sum of final amount per unit calculation is successful")
            

#     def test_sum_of_final_amt_per_unit_2_po(self):
#         freight_total=self.booking_no
#         po_total=po_prepaid_total=po_collect_total=0
#         for po_tax in freight_total.charges_line:
#             if po_tax.prepaid==True:
#                 tax=po_tax.taxes_id.amount/100*po_tax.unit_price
#                 po_prepaid_total=po_tax.unit_price+tax
#                 po_prepaid_total=po_prepaid_total+po_tax.final_amount_per_unit
#                 print("gsdfgsdfgfdg",po_prepaid_total)
#             if po_tax.collect==True:
#                 tax=po_tax.taxes_id.amount/100*po_tax.unit_price
#                 po_collect_total=po_tax.unit_price+tax
#                 print("gsdfgsdfgfdg",tax)
#                 print("gsdfgsdfgfdg",po_collect_total)
#                 # po_total=po_total+po_tax.final_amount_per_unit
#                 # print("gsdfgsdfgfdg",po_total)
#         po_total=po_prepaid_total+po_collect_total        
#         # self.assertEqual(freight_total.total_collect_charges,po_total)
#         self.assertEqual(freight_total.total_final_amount_per_unit,po_total)
#         print("PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPpo_total",po_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::: sum of final amount per unit calculation with if condition is successful")

#     def test_sum_of_final_amt_per_unit_3_po(self):
#         freight_total=self.booking_no
#         po_total=freight_total.total_prepaid_charges+freight_total.total_collect_charges
#         self.assertEqual(freight_total.total_final_amount_per_unit,po_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::total charge calculation using prepaid and collect charges is successful")    

#     def test_total_prepaid_po(self):
#         freight_total=self.booking_no
#         po_total=0
#         for po_tax in freight_total.charges_line:
#             if po_tax.prepaid==True:
#                 tax=po_tax.taxes_id.amount/100*po_tax.unit_price
#                 po_total=po_tax.unit_price+tax
#                 print("gsdfgsdfgfdg",tax)
#                 print("gsdfgsdfgfdg",po_total)
#                 po_total=po_total+po_tax.final_amount_per_unit
#         print("gsdfgsdfgfdg",po_total)
#         self.assertEqual(freight_total.total_prepaid_charges,po_total)
#         _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::prepaid calculation is successful")
            

#     def test_total_collect_po(self):
#         freight_total=self.booking_no
#         po_total=0
#         for po_tax in freight_total.charges_line:
#             if po_tax.collect==True:
#                 tax=po_tax.taxes_id.amount/100*po_tax.unit_price
#                 po_total=po_tax.unit_price+tax
#                 print("gsdfgsdfgfdg",tax)
#                 print("gsdfgsdfgfdg",po_total)
#                 # po_total=po_total+po_tax.final_amount_per_unit
#                 print("gsdfgsdfgfdg",po_total)
#                 self.assertEqual(freight_total.total_collect_charges,po_total)
#                 _logger.info(":::::::::::::::::::::::::::::::::::::::::::::::::::::prepaid calculation is successful")

#     def test__not_readonly(self):
#         po = Form(self.booking_no)
#         try:
#             po.floor="123"
#             _logger.info("floor is not readonly field")
#         except:
#             _logger.warning("floor is readonly field")

#     def test_readonly(self):
#         po = Form(self.booking_no)
#         try:
#             po.cargo_name="abc"
#             _logger.info("Cargo name is not readonly field")
#         except:
#             _logger.warning("cargo name is readonly")

    