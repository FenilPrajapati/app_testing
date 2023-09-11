# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class SiTemplateWiz(models.Model):
    _name = 'si.templates.wiz'
    _description = "Si Template Wizard"

    name = fields.Char(string='Name', required=True)
    si_id = fields.Many2one('si.templates', string='Shipping Instruction')
    created_from_si = fields.Boolean("Created from SI")

    def action_create_si_template(self):
        ShippingInstruction = self.env['shipping.instruction']
        si_rec = ShippingInstruction.browse([(self._context['current_id'])])
        si_template_rec = self.env['si.templates'].create({
            'name': self.name,
            'transport_document_type_code': si_rec.transport_document_type_code,
            'is_shipped_onboard_type': si_rec.is_shipped_onboard_type,
            'number_of_originals': si_rec.number_of_originals,
            'number_of_copies': si_rec.number_of_copies,
            'pre_carriage_under_shippers_responsibility': si_rec.pre_carriage_under_shippers_responsibility,
            'is_electronic': si_rec.is_electronic,
            'carrier_booking_reference': si_rec.carrier_booking_reference,
            'is_charges_displayed': si_rec.is_charges_displayed,
            'location_name': si_rec.location_name,
            'un_location_code': si_rec.un_location_code,
            'city_name': si_rec.city_name,
            'state_region': si_rec.state_region,
            'country': si_rec.country,
            'si_user_id': self.env.user.id,
        })
        if si_template_rec and si_rec.cargo_items_line:
            for cl in si_rec.cargo_items_line:
                si_template_rec.si_template_cargo_items_line.create({
                    'si_template_cargo_line_id': si_template_rec.id,
                    'cargo_line_items_id': cl.cargo_line_items_id,
                    'shipping_marks': cl.shipping_marks,
                    'carrier_booking_reference': cl.carrier_booking_reference,
                    'description_of_goods': cl.description_of_goods,
                    'hs_code': cl.hs_code,
                    'number_of_packages': cl.number_of_packages,
                    'weight': cl.weight,
                    'volume': cl.volume,
                    'weight_unit': cl.weight_unit,
                    'volume_unit': cl.volume_unit,
                    'package_code': cl.package_code,
                    'equipment_reference': cl.equipment_reference,
                    'cargo_array_created_by': cl.cargo_array_created_by,
                })
        if si_template_rec and si_rec.transport_equipment_line:
            for tq in si_rec.transport_equipment_line:
                si_template_rec.si_template_transport_equipment_line.create({
                    'si_template_transport_equipment_line_id': si_template_rec.id,
                    'equipment_reference_id': tq.equipment_reference_id,
                    'weight_unit': tq.weight_unit,
                    'cargo_gross_weight': tq.cargo_gross_weight,
                    'container_tare_weight': tq.container_tare_weight,
                    'iso_equipment_code': tq.iso_equipment_code,
                    'is_shipper_owned': tq.is_shipper_owned,
                    'temperature_min': tq.temperature_min,
                    'temperature_max': tq.temperature_max,
                    'temperature_unit': tq.temperature_unit,
                    'humidity_min': tq.humidity_min,
                    'humidity_max': tq.humidity_max,
                    'ventilation_min': tq.ventilation_min,
                    'ventilation_max': tq.ventilation_max,
                    'seal_number': tq.seal_number,
                    'seal_source': tq.seal_source,
                    'seal_type': tq.seal_type,
                    'transport_equipment_array_created_by': tq.transport_equipment_array_created_by,
                })
        if si_template_rec and si_rec.document_parties_line:
            for dp in si_rec.document_parties_line:
                si_template_rec.si_template_document_parties_line.create({
                    'si_template_document_parties_line_id': si_template_rec.id,
                    'party_name_id': dp.party_name_id,
                    'tax_reference_1': dp.tax_reference_1,
                    'public_key': dp.public_key,
                    'street': dp.street,
                    'street_number': dp.street_number,
                    'floor': dp.floor,
                    'post_code': dp.post_code,
                    'city': dp.city,
                    'state_region': dp.state_region,
                    'country': dp.country,
                    'tax_reference_2': dp.tax_reference_2,
                    'nmfta_code': dp.nmfta_code,
                    'party_function': dp.party_function,
                    'address_line': dp.address_line,
                    'name': dp.name,
                    'email': dp.email,
                    'phone': dp.phone,
                    'is_to_be_notified': dp.is_to_be_notified,
                    'document_parties_array_created_by': dp.document_parties_array_created_by,
                })
        if si_template_rec and si_rec.shipment_location_line:
            for sl in si_rec.shipment_location_line:
                print("sl.location_type", sl.location_type)
                si_template_rec.si_template_shipment_location_line.create({
                    'si_template_shipment_location_line_id': si_template_rec.id,
                    'location_type': sl.location_type.id,
                    'displayed_name': sl.displayed_name,
                    'location_name': sl.location_name,
                    'latitude': sl.latitude,
                    'longitude': sl.longitude,
                    'un_location_code': sl.un_location_code,
                    'street_name': sl.street_name,
                    'street_number': sl.street_number,
                    'floor': sl.floor,
                    'post_code': sl.post_code,
                    'city_name': sl.city_name,
                    'state_region': sl.state_region,
                    'country': sl.country,
                    'shipment_location_array_created_by': sl.shipment_location_array_created_by,
                })
        if si_template_rec and si_rec.references_line:
            for rc in si_rec.references_line:
                si_template_rec.si_template_references_line.create({
                    'si_template_references_line_id': si_template_rec.id,
                    'reference_type': rc.reference_type,
                    'reference_value': rc.reference_value,
                    'references_array_created_by': rc.references_array_created_by,
                })
