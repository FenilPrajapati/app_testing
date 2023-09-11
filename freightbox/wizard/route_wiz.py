# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class RouteTemplateWiz(models.Model):
    _name = 'route.templates.wiz'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Route Template Wizard"

    name = fields.Char(string='Name', required=True)
    route_id = fields.Many2one('route', string='Route', tracking=True)
    transport_id = fields.Many2one('transport', string='Transport', tracking=True)
    is_created_from_route = fields.Boolean("Created from Route", tracking=True)
    is_created_from_transport = fields.Boolean("Created from Transport", tracking=True)

    # def update_route_template(self):
    #     route_temp = self.env['route.templates']
    #     print("self.route_id", self)
    #     if self.is_created_from_route:
    #         rr = route_temp.search([])
    #         for r in rr:
    #             print("rrrrrrrrrrrrrrr", r.route_id)
    #         route_temp.sudo().search([('route_id', '=', 13)])
    #         print("R route_temp_obj", route_temp)
    #         route_lines = self.route_id.route_template_line
    #     if self.is_created_from_transport:
    #         route_temp.search([('transport_id', '=', self.transport_id.id)], limit=1)
    #         print("T route_temp_obj", route_temp)
    #         route_lines = self.transport_id.route_line
    #     print("C route_temp_obj", route_temp)
    #     print("self.route_id 8888:", self.route_id)
    #     rec = route_temp.write({
    #         'name': self.name,
    #         'route_template_line': route_lines,
    #     })
    #     print("reccccccccccccccccc", rec)
    #     # if self.transport_id:
    #     #     transport_id = transport.browse([(self._context['active_id'])])
    #     #     transport_temp_id = route_temp_obj.search([('transport_id', '=', transport_id.id)], limit=1)
    #     #     route_template_line = self.transport_id.route_line
    #     #     if transport_temp_id:
    #     #         transport_temp_id.write({
    #     #             'name': self.name,
    #     #             'route_template_line': route_template_line.ids,
    #     #         })
    #     return {
    #         'name': _('Updated'),
    #         'type': 'ir.actions.act_window',
    #         'views': [(self.env.ref('freightbox.message_wizard_route_form2').id, "form")],
    #         'view_mode': 'form',
    #         'res_model': 'message.wizard.route',
    #         'target': 'new'
    #     }

    def update_container_journey_template(self):
        print("selfff")
        cont_journey = self.env['route.template.container.journey']
        if self.transport_id:
            route_template_obj = self.env['route.templates']
            route_template_id = route_template_obj.search([('transport_id', '=', self.transport_id.id)],
                                                                  limit=1)
            if route_template_id:
                route_template_id.write({
                    'name': self.name,
                    'point_of_stuffing': self.transport_id.point_of_stuffing,
                    'point_of_destuffing': self.transport_id.point_of_destuffing,
                    'container_route_line': False,
                })

                for cj in self.transport_id.container_route_line:
                    print("selffff", self)
                    print("cjjjjj", cj)
                    print("route_template_id:", route_template_id)
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
                        'route_template_id': route_template_id.id,
                    }
                    cont_journey.sudo().create(cj_vals)
            return {
                    'name': _('Updated'),
                    'type': 'ir.actions.act_window',
                    'views': [(self.env.ref('freightbox.message_wizard_route_form2').id, "form")],
                    'view_mode': 'form',
                    'res_model': 'message.wizard.route',
                    'target': 'new'
            }

    def create_container_journey_template(self):
        print("self", self)
        transport_obj = self.env['transport']
        transport_id = transport_obj.browse([(self._context['current_id'])])
        print("transporttttttttttttttttttttt", transport_id)
        if transport_id.container_route_line:
            route_template_id = self.env['route.templates'].create({
                'name': self.name,
                'point_of_stuffing': transport_id.point_of_stuffing,
                'point_of_destuffing': transport_id.point_of_destuffing,
                'is_created_from_transport': True,
            })
            print("route_template_id", route_template_id)
            route_template_id.container_route_line = False
            route_list = []
            for cj in transport_id.container_route_line:
                route_list.append((0, 0, {
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
                    'route_template_id': route_template_id.id,
                }))
            route_template_id.container_route_line = route_list
        # route_template_id = self.env['transport.template'].create({
        # })
        return {
            'name': _('Successful'),
            'type': 'ir.actions.act_window',
            'views': [(self.env.ref('freightbox.message_wizard_route_form').id, "form")],
            'view_mode': 'form',
            'res_model': 'message.wizard.route',
            'target': 'new'
        }


    # def create_route_template(self):
    #     print("self", self.is_created_from_route)
    #     transport = self.env['transport']
    #     route = self.env['route']
    #     print("act", self._context['active_id'])
    #     transport_rec_id = route_rec_id = False
    #     if self.is_created_from_route:
    #         route_rec = route.browse([(self._context['active_id'])])
    #         if route_rec:
    #             route_rec_id = route_rec.id
    #         route_lines = route_rec.route_template_line
    #     if self.is_created_from_transport:
    #         transport_rec = transport.browse([(self._context['active_id'])])
    #         if transport_rec:
    #             transport_rec_id = transport_rec.id
    #         route_lines = transport_rec.route_line
    #     print("route_rec_id", route_rec_id)
    #     rec = self.env['route.templates'].create({
    #         'name': self.name,
    #         'transport_id': transport_rec_id,
    #         'route_id': route_rec_id,
    #         'is_created_from_transport': self.is_created_from_transport,
    #         'is_created_from_route': self.is_created_from_route,
    #         'route_template_line': route_lines,
    #     })
    #     print("reccccccccccccccccc", rec)
    #     return {
    #         'name': _('Successful'),
    #         'type': 'ir.actions.act_window',
    #         'views': [(self.env.ref('freightbox.message_wizard_route_form').id, "form")],
    #         'view_mode': 'form',
    #         'res_model': 'message.wizard.route',
    #         'target': 'new'
    #     }


class MessageWizardRoute(models.TransientModel):
    _name = 'message.wizard.route'
    _description = "Success or Update Wizard for Route"

    def action_ok(self):
        """ close wizard"""
        return {'type': 'ir.actions.act_window_close'}
