# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import timedelta, datetime,date


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def create_invoices(self):
        sale_orders = self.env['sale.order'].browse(self._context.get('active_ids', []))
        super(SaleAdvancePaymentInv, self).create_invoices()
        se_rec = self.env['track.shipment.event'].create({
                'shipment_event': 'Shipment',
                'event_created': date.today(),
                'event_datetime': date.today(),
                'event_classifier_code': 'ACT',
                'shipment_event_type_code': 'RECE',
                'reason':'Customer Invoice Created',
                'booking_id':sale_orders.so_inquiry_id.id
            })
        for inv in sale_orders.invoice_ids:
            print("sssss")
            if sale_orders.charges_line:
                print("invvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv", inv)
                # inv.write()
                inv.write({
                    'sale_order_id': sale_orders.id,
                    'booking_id': sale_orders.booking_id,
                    'place_of_origin': sale_orders.place_of_origin,
                    'place_of_destination': sale_orders.final_port_of_destination,
                    'amount_tax': sale_orders.amount_tax,
                })
                for line in sale_orders.charges_line:
                    # if line.prepaid:
                    inv.update({

                            'charges_line': [(0, 0, {
                                'charges_id': line.charges_id.id,
                                'container_type': line.container_type.id,
                                'charges_type': line.charges_type,
                                'units': line.units,
                                'unit_price': line.unit_price,
                                'new_unit_price': line.new_unit_price,
                                'taxes_id': line.taxes_id.ids,
                                'prepaid': line.prepaid,
                                'collect': line.collect,
                                'comment': line.comment,
                                'invoice_order_id': inv.id,
                                'is_loaded_for_rfq': True,
                                'currency_id': line.currency_id.id,
                                'to_currency_id': line.to_currency_id.id,
                            })],
                    })
                for rates in inv.charges_line:
                    rates._onchange_charges()
