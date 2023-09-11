# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class TransportMessageWizard(models.TransientModel):
    _name = 'transport.message.wizard'
    _description = "Success or Update Wizard"

    def action_close(self):
        """ close wizard"""
        return {'type': 'ir.actions.act_window_close'}


class TransportTrackWizard(models.TransientModel):
    _name = 'transport.track.wizard'
    _description = "Proceed or Cancel Wizard"

    track_user_count = fields.Integer("")

    def action_proceed_tracking(self):
        return True

    def action_cancel_tracking(self):
        """ close wizard"""
        return {'type': 'ir.actions.act_window_close'}


class TransportTemplateWiz(models.Model):
    _name = 'transport.template.wiz'
    _description = "Transport Template Wizard"

    name = fields.Char(string='Name', required=True)
    transport_id = fields.Many2one('transport', string='Transport')
    is_created_from_transport = fields.Boolean(string='Is created from Transport')

    def update_transport_template(self):
        route_list = []
        cont_journey = self.env['trans.temp.container.journey']
        if self.transport_id:
            transport_template_obj = self.env['transport.template']
            transport_template_id = transport_template_obj.search([('transport_id', '=', self.transport_id.id)],
                                                                  limit=1)
            if transport_template_id:
                # transport_template_id.transport_template_route_line = False
                transport_template_id.write({
                    'name': self.name,
                    'workorder': self.transport_id.workorder,
                    'carrier_booking': self.transport_id.carrier_booking,
                    'planned_date': self.transport_id.planned_date,
                    'remarks': self.transport_id.remarks,
                    'carrier_handover': self.transport_id.carrier_handover.id,
                    'vessel_name': self.transport_id.vessel_name,
                    'imo_no': self.transport_id.imo_no,
                    'voyage': self.transport_id.voyage,
                    'rotation': self.transport_id.rotation,
                    'gate_cutoff': self.transport_id.gate_cutoff,
                    'port_of_origin_facility_id': self.transport_id.port_of_origin_facility_id.id,
                    'fpod_facility_id': self.transport_id.fpod_facility_id.id,
                    'pickup_loc_id': self.transport_id.pickup_loc_id.id,
                    'pickup_loc_facility_id': self.transport_id.pickup_loc_facility_id.id,
                    'dropoff_loc_id': self.transport_id.dropoff_loc_id.id,
                    'dropoff_loc_facility_id': self.transport_id.dropoff_loc_facility_id.id,
                    'port_of_origin_id': self.transport_id.port_of_origin_id.id,
                    'fpod_id': self.transport_id.fpod_id.id,
                    'point_of_stuffing': self.transport_id.point_of_stuffing,
                    'point_of_destuffing': self.transport_id.point_of_destuffing,
                    'temparature': self.transport_id.temparature,
                    'humidity': self.transport_id.humidity,
                    'ventilation': self.transport_id.ventilation,
                    'cont_type': self.transport_id.cont_type.id,

                    'pickup_mode': self.transport_id.pickup_mode.id,
                    'dropoff_mode': self.transport_id.dropoff_mode.id,
                    'stuffing_mode': self.transport_id.stuffing_mode.id,
                    'destuffing_mode': self.transport_id.destuffing_mode.id,
                    'vessel_mode': self.transport_id.vessel_mode.id,
                    'is_multi_modal': self.transport_id.is_multi_modal,
                    'vessel_name1': self.transport_id.vessel_name1,
                    'voyage1': self.transport_id.voyage1,
                    'rotation1': self.transport_id.rotation1,
                    'imo_no1': self.transport_id.imo_no1,
                    'intermediate_pol_id': self.transport_id.intermediate_pol_id.id,
                    'transport_template_route_line': False,
                    'container_route_line': False,

                })
                for cj in self.transport_id.container_route_line:
                    print("selffff", self)
                    print("cjjjjj", cj)
                    print("transport_template_id:", transport_template_id)
                    cj_vals = {
                        'start_point': cj.start_point.id,
                        'end_point': cj.end_point.id,
                        'transport_mode': cj.transport_mode.id,
                        'estimated_departure_time': cj.estimated_departure_time,
                        'estimated_arrival_time': cj.estimated_arrival_time,
                        'planned_departure_time': cj.planned_departure_time,
                        'planned_arrival_time': cj.planned_arrival_time,
                        'actual_departure_time': cj.actual_departure_time,
                        'actual_arrival_time': cj.actual_arrival_time,
                        'delay_reason': cj.delay_reason,
                        'change_remark': cj.change_remark,
                        'transport_template_id': transport_template_id.id,
                        'distance': cj.distance,
                        'speed': cj.speed,
                        'fuel': cj.fuel,
                        'co2_emmision': cj.co2_emmision,
                        'gate_in_wait_time': cj.gate_in_wait_time,
                        'gate_out_wait_time': cj.gate_out_wait_time,
                        'travel_time': cj.travel_time,
                        'buffer_time': cj.buffer_time,
                        'yard_time': cj.yard_time,

                    }
                    cont_journey.sudo().create(cj_vals)

                for line in self.transport_id.route_line:
                    print("`")
                    route_list.append((0, 0, {
                        'port_of_origin': line.port_of_origin,
                        'fpod': line.fpod,
                        'mode_id': line.mode_id.id,
                        'transport_template_id': transport_template_id.id,
                        'planned_departure_time': line.planned_departure_time,
                        'planned_arrival_time': line.planned_arrival_time,
                        'estimated_departure_time': line.estimated_departure_time,
                        'estimated_arrival_time': line.estimated_arrival_time,
                        'actual_departure_time': line.actual_departure_time,
                        'actual_arrival_time': line.actual_arrival_time,
                        'delay_reason': line.delay_reason,
                    }))
                transport_template_id.transport_template_route_line = route_list


        return {
            'name': _('Updated'),
            'type': 'ir.actions.act_window',
            'views': [(self.env.ref('freightbox.transport_message_wizard_form_for_update_msg').id, "form")],
            'view_mode': 'form',
            'res_model': 'message.wizard',
            'target': 'new'
        }

    def create_transport_template(self):
        route_list = []
        transport_obj = self.env['transport']
        transport_id = transport_obj.browse([(self._context['current_id'])])
        print("transporttttttttttttttttttttt", transport_id.carrier_booking)
        print("ccccccc", transport_id.pickup_loc_id)
        # print(sdf)
        transport_template_id = self.env['transport.template'].create({
            'name': self.name,
            'transport_id': transport_id.id,
            'is_created_from_transport': True,
            'workorder': transport_id.workorder,
            'carrier_booking': transport_id.carrier_booking,
            'planned_date': transport_id.planned_date,
            'remarks': transport_id.remarks,
            'carrier_handover': transport_id.carrier_handover.id,
            'vessel_name': transport_id.vessel_name,
            'imo_no': transport_id.imo_no,
            'voyage': transport_id.voyage,
            'rotation': transport_id.rotation,
            'gate_cutoff': transport_id.gate_cutoff,
            'port_of_origin_facility_id': transport_id.port_of_origin_facility_id.id,
            'fpod_facility_id': transport_id.fpod_facility_id.id,
            'pickup_loc_id': transport_id.pickup_loc_id.id,
            'pickup_loc_facility_id': transport_id.pickup_loc_facility_id.id,
            'dropoff_loc_id': transport_id.dropoff_loc_id.id,
            'dropoff_loc_facility_id': transport_id.dropoff_loc_facility_id.id,
            'port_of_origin_id': transport_id.port_of_origin_id.id,
            'fpod_id': transport_id.fpod_id.id,
            'point_of_stuffing': transport_id.point_of_stuffing.id,
            'point_of_destuffing': transport_id.point_of_destuffing.id,
            'temparature': transport_id.temparature,
            'humidity': transport_id.humidity,
            'ventilation': transport_id.ventilation,
            'cont_type': transport_id.cont_type.id,

            'pickup_mode': transport_id.pickup_mode.id,
            'dropoff_mode': transport_id.dropoff_mode.id,
            'stuffing_mode': transport_id.stuffing_mode.id,
            'destuffing_mode': transport_id.destuffing_mode.id,
            'vessel_mode': transport_id.vessel_mode.id,
            'is_multi_modal': transport_id.is_multi_modal,
            'vessel_name1': transport_id.vessel_name1,
            'voyage1': transport_id.voyage1,
            'rotation1': transport_id.rotation1,
            'imo_no1': transport_id.imo_no1,
            'intermediate_pol_id': self.transport_id.intermediate_pol_id.id,


        })
        cj_list = []
        transport_template_id.container_route_line = False
        for cj in transport_id.container_route_line:
            cj_list.append((0, 0, {
                'start_point': cj.start_point.id,
                'end_point': cj.end_point.id,
                'transport_mode': cj.transport_mode.id,
                'estimated_departure_time': cj.estimated_departure_time,
                'estimated_arrival_time': cj.estimated_arrival_time,
                'planned_departure_time': cj.planned_departure_time,
                'planned_arrival_time': cj.planned_arrival_time,
                'actual_departure_time': cj.actual_departure_time,
                'actual_arrival_time': cj.actual_arrival_time,
                'delay_reason': cj.delay_reason,
                'change_remark': cj.change_remark,
                'transport_template_id': transport_template_id.id,
                'distance': cj.distance,
                'speed': cj.speed,
                'fuel': cj.fuel,
                'co2_emmision': cj.co2_emmision,
                'gate_in_wait_time': cj.gate_in_wait_time,
                'gate_out_wait_time': cj.gate_out_wait_time,
                'travel_time': cj.travel_time,
                'buffer_time': cj.buffer_time,
                'yard_time': cj.yard_time,
            }))
        transport_template_id.container_route_line = cj_list

        for line in transport_id.route_line:
            route_list.append((0, 0, {
                'port_of_origin': line.port_of_origin,
                'fpod': line.fpod,
                'mode_id': line.mode_id.id,
                'transport_template_id': transport_template_id.id,
                'planned_departure_time': line.planned_departure_time,
                'planned_arrival_time': line.planned_arrival_time,
                'estimated_departure_time': line.estimated_departure_time,
                'estimated_arrival_time': line.estimated_arrival_time,
                'actual_departure_time': line.actual_departure_time,
                'actual_arrival_time': line.actual_arrival_time,
                'delay_reason': line.delay_reason,
            }))
        transport_template_id.transport_template_route_line = False
        transport_template_id.transport_template_route_line = route_list

        return {
            'name': _('Successful'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'views': [(self.env.ref('freightbox.transport_message_wizard_form').id, "form")],
            'res_model': 'message.wizard',
            'target': 'new'
        }
