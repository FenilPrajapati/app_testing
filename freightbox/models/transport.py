from odoo import models, fields, _, api
from odoo.exceptions import UserError, ValidationError
from lxml import etree
from datetime import timedelta, datetime
import requests
import json
import math
import socket
# import re


class Transport(models.Model):
    _inherit = 'transport'
    # _inherit = ['mail.thread', 'mail.activity.mixin']
    # _description = "Transport"
    # _rec_name = 'cont_id'

    def get_coordinates(self):
        self.container_route_line.get_route_coordinates()
        # self.waypoint_coordinates = self.container_route_line[0].route_coordinates
        if self.container_route_line and self.container_route_line.mapped('route_coordinates'):
            new_waypoints = []
            mode_of_transport = 'road'
            for route_line in self.container_route_line:
                try:
                    route_waypoints = eval(route_line.route_coordinates) or []
                except:
                    route_waypoints = []

                try:
                    if route_line.transport_mode.name == 'Road':
                        mode_of_transport = 'road'
                    if route_line.transport_mode.name == 'Rail':
                        mode_of_transport = 'rail'
                    if route_line.transport_mode.name in ['Main Line', 'Feeder']:
                        mode_of_transport = 'ship'
                except:
                    mode_of_transport = 'road'


                if mode_of_transport and route_waypoints:
                    new_waypoints.append({mode_of_transport: route_waypoints})
            if new_waypoints and new_waypoints != []:
                self.waypoint_coordinates = new_waypoints
        return True

    @api.model
    def create(self, vals):
        if vals.get('cont_id', False) and len(vals.get('cont_id', [])) != 11:
            raise ValidationError("Container ID is invalide. Provide correct 11 digit Container ID.")

        # pattern = r'^[A-Z]{4}\d{7}$'
        # if not re.match(pattern, vals.get('cont_id', False)):
        #     raise ValidationError("Container ID is invalide")
        return super(Transport, self).create(vals)

    # def write(self, vals):
    #     if vals.get('cont_id', False) and len(vals.get('cont_id', [])) != 11:
    #         raise ValidationError("Container ID is invalide. Provide correct 11 digit Container ID.")

    #     pattern = r'^[A-Z]{4}\d{7}$'
    #     if vals.get('cont_id'):
    #         if not re.match(pattern, vals.get('cont_id')):
    #             raise ValidationError("Container ID is invalide")

    #     result = super(Transport, self).write(vals)
        
    #     return result

    def unlink(self):
        for rec in self:
            job_id = rec.job_id
            result = super(Transport, rec).unlink()
            if job_id:
                if not job_id.shipping_instruction_ids:
                    job_id.write({'state': 'draft'})
        return result

    def action_load_container_journey(self):
        port_obj = self.env['port']
        self.container_route_line = False
        container_route_lines = []

        if self.pickup_mode:
            container_route_lines.append((0, 0, {
                'start_point': self.pickup_loc_id.id,
                'end_point': self.point_of_stuffing.id,
                'transport_mode': self.pickup_mode.id,
                'planned_departure_time': self.planned_date,
                'speed': 30
            }))
        else:
            raise ValidationError("Please enter Mode of tranport from pickup")
        if self.stuffing_mode:
            container_route_lines.append((0, 0, {
                'start_point': self.point_of_stuffing.id,
                'end_point': self.port_of_origin_id.id,
                'transport_mode': self.stuffing_mode.id,
                'speed': 30
            }))
        else:
            raise ValidationError("Please enter Mode of tranport from Stuffing")
        if self.vessel_mode:
            if self.is_multi_modal==True:
                container_route_lines.append((0, 0, {
                    'start_point': self.port_of_origin_id.id,
                    'end_point': self.intermediate_pol_id.id,
                    'transport_mode': self.vessel_mode.id,
                    'speed': 30
                }))
            else:
                container_route_lines.append((0, 0, {
                    'start_point': self.port_of_origin_id.id,
                    'end_point': self.fpod_id.id,
                    'transport_mode': self.vessel_mode.id,
                    'speed': 30
                }))
        else:
            raise ValidationError("Please enter Mode of tranport from Port of Origin")
        if self.is_multi_modal==True:
            if self.second_vessel_mode and self.point_of_stuffing and self.point_of_destuffing:
                if self.is_another_ship_needed==True:
                    container_route_lines.append((0, 0, {
                        'start_point': self.intermediate_pol_id.id,
                        'end_point': self.second_intermediate_pol_id.id,
                        'transport_mode': self.second_vessel_mode.id,
                        'speed': 30
                    }))
                else:
                    container_route_lines.append((0, 0, {
                        'start_point': self.intermediate_pol_id.id,
                        'end_point': self.fpod_id.id,
                        'transport_mode': self.second_vessel_mode.id,
                        'speed': 30
                    }))
        if self.is_another_ship_needed==True:
            if self.third_vessel_mode:
                container_route_lines.append((0, 0, {
                    'start_point': self.second_intermediate_pol_id.id,
                    'end_point': self.fpod_id.id,
                    'transport_mode': self.third_vessel_mode.id,
                    'speed': 30
                }))
        if self.destuffing_mode:
            container_route_lines.append((0, 0, {
                'start_point': self.fpod_id.id,
                'end_point': self.point_of_destuffing.id,
                'transport_mode': self.destuffing_mode.id,
                'speed': 30
            }))
        else:
            raise ValidationError("Please enter Mode of transport from Destuffing Location")
        if self.dropoff_mode:
            container_route_lines.append((0, 0, {
                'start_point': self.point_of_destuffing.id,
                'end_point': self.dropoff_loc_id.id,
                'transport_mode': self.dropoff_mode.id,
                'speed': 30
            }))
        else:
            raise ValidationError("Please enter Mode of transport from Dropoff Location")
        self.container_route_line = container_route_lines
        self.action_update_route_dates()

    def action_delete_container_journey_template(self):
        self.container_route_line = False

    def action_create_or_update_container_route_template(self):
        ctx = {}
        self.ensure_one()
        if not self.container_route_line:
            raise UserError(_("There is no Route to create Route template"))
        routetemplate = self.env['route.templates'].search(
            [('transport_id', '=', self.id), ('is_created_from_transport', '=', True)], limit=1)
        name = "From " + self.point_of_stuffing.name + " To " + self.point_of_destuffing.name
        ctx = dict(
            default_transport_id=self.id,
            default_is_created_from_transport=False,
            default_name=name,
            current_id=self.id,
        )
        if routetemplate:
            ctx = dict(
                default_transport_id=self.id,
                default_name=routetemplate.name,
                default_is_created_from_transport=routetemplate.is_created_from_transport,
                current_id=self.id,
            )
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'route.templates.wiz',
            'view_mode': 'form',
            'views': [(self.env.ref('freightbox.route_template_form_wiz').id, "form")],
            # route_template_form_view2
            'context': ctx,
            'target': 'new',
        }

    def action_request_for_tnt(self):
        res_config_settings_obj = self.env['ir.config_parameter']
        if not self.actual_date:
            raise UserError("Actual Datetime needed to Request for Track Data. Go to 'Other Info' and provide Actual Datetime.")

        allowed_api_calls = int(self.env['ir.config_parameter'].sudo().get_param('odoo_v14_frieght.allowed_track_count')) or 0
        track_count = int(self.env['ir.config_parameter'].sudo().get_param('odoo_v14_frieght.track_count')) or 0

        if allowed_api_calls <= 0:
            allowed_api_calls = self.get_allowed_tnt_requests_from_motherserver()
            res_config_settings_obj.sudo().set_param('odoo_v14_frieght.allowed_track_count', allowed_api_calls)

        remaining_attemts = allowed_api_calls - track_count

        if remaining_attemts <= 0:
            confirm_message = """
                        You have used up all of your allowed tracks that us  %s. For more details / To get more tracks, 
                        contact Powerp Box IT Solutions Pvt. Ltd.""" % allowed_api_calls
            is_track_used_up = True

        else:
            confirm_message = """
                        You are allowed to track only %s shipments for free. You have %s time remaining. 
                        Want to track this shipment anyway?
                        """ % (allowed_api_calls, remaining_attemts)
            is_track_used_up = False
        if not self._context.get("confirmed", False):
            ctx = dict(self._context)



            ctx.update({
                "default_transport_id": self.id,
                "default_message": confirm_message,
                "default_is_track_used_up": is_track_used_up
            })
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'trace.confirm.wizard',
                'view_mode': 'form',
                'views': [(self.env.ref('freightbox.trace_confirm_wizard_form').id, "form")],
                'context': ctx,
                'target': 'new',
            }

        if self.no_of_api_calls > allowed_api_calls:
            raise ValidationError(_("You can not track more than %s containers." % allowed_api_calls))
        if self._context.get("confirmed", False):
            response =  self.create_transport_request_motherserver(self.cont_id, self.fb_transport_id)
            if response.status_code != 200:
                error_msg = "Could not complete transport reqiest due to following reasons : %s " % response.content
                raise ValidationError(error_msg)
            self.is_track_requested = True
        # import socket
        # import json
        # import requests
        # hostname = socket.gethostname()
        # transport_events = []
        # transport_name = "From " + self.point_of_stuffing + " To " + self.point_of_destuffing
        # dbuuid = self.env['ir.config_parameter'].sudo().get_param('database.uuid')
        # username = hostname + '_' + dbuuid
        # transport_vals = {
        #     'transport_user_name': username,
        #     'cont_id': self.cont_id,
        #     'transport_id': self.fb_transport_id,
        #     'vessel_operator_carrier_code': None,
        #     'transport_name': transport_name,
        #     'planned_date': str(self.planned_date),
        #     'actual_date': str(self.actual_date),
        #     'point_of_stuffing': self.point_of_stuffing,
        #     'point_of_destuffing': self.point_of_destuffing,
        # }
        # transport_events.append(transport_vals)
        # res = requests.post("https://mother.powerpbox.org/mother_odoo14/post_transport_from_freightbox",
        #                     data=json.dumps(transport_events))
        # print("res", res.status_code)
        #
        # if res.status_code == 200:
        #     res_config_settings_obj = self.env['ir.config_parameter']
        #     track_count = int(res_config_settings_obj.sudo().get_param('odoo_v14_frieght.track_count')) or 0
        #     res_config_settings_obj.sudo().set_param('odoo_v14_frieght.track_count', track_count+1)
        #     self.no_of_api_calls += 1
        #     print("self.no_of_api_calls", self.no_of_api_calls)

    def create_transport_request_motherserver(self, cont_id, fb_transport_id):
        hostname = socket.gethostname()
        transport_events = []
        point_of_stuffing = self.point_of_stuffing.name if self.point_of_stuffing else ''
        point_of_destuffing = self.point_of_destuffing.name if self.point_of_destuffing else ''
        transport_name = "From " + str(self.point_of_stuffing.name) + " To " + str(self.point_of_destuffing.name)
        dbuuid = self.env['ir.config_parameter'].sudo().get_param('database.uuid')
        username = hostname + '_' + dbuuid
        transport_vals = {
            'transport_user_name': username,
            'cont_id': cont_id,
            'transport_id': fb_transport_id,
            'vessel_operator_carrier_code': None,
            'transport_name': transport_name,
            'planned_date': str(self.planned_date or fields.Datetime.now()),
            'actual_date': str(self.actual_date or fields.Datetime.now()),
            'point_of_stuffing': self.point_of_stuffing.name if self.point_of_stuffing else '',
            'point_of_destuffing': self.point_of_destuffing.name if self.point_of_destuffing else ''
        }
        transport_events.append(transport_vals)
        api_rec = self.env['api.integration'].search([('name', '=', 'post_transport_from_freightbox')])[-1]
        if not api_rec:
            raise ValidationError("API Record does not exist for 'post_transport_from_freightbox'.")
        res = requests.post(api_rec.url, data=json.dumps(transport_events))
        if res.status_code == 200:
            res_config_settings_obj = self.env['ir.config_parameter']
            track_count = int(res_config_settings_obj.sudo().get_param('odoo_v14_frieght.track_count')) or 0
            res_config_settings_obj.sudo().set_param('odoo_v14_frieght.track_count', track_count + 1)
            self.no_of_api_calls += 1
        return res

    def get_allowed_tnt_requests_from_motherserver(self):
        allowed_api_calls = 0
        hostname = socket.gethostname()
        dbuuid = self.env['ir.config_parameter'].sudo().get_param('database.uuid')
        username = hostname + '_' + dbuuid
        api_rec = self.env['api.integration'].search([('name', '=', 'get_allowed_gh_api_calls')])[-1]
        if not api_rec:
            raise ValidationError("API Record does not exist for 'get_allowed_gh_api_calls'.")
        url = '%s/%s/1/0' % (api_rec.url, username)
        response = requests.get(url)
        if response.status_code == 200:
            response_data = json.loads(response.content)
            if response_data.get('data', {}).get('allowed_transport_requests', 0):
                allowed_api_calls = response_data.get('data', {}).get('allowed_transport_requests', 0)
        return allowed_api_calls

    def action_confirm_transportation(self):
        res = super(Transport, self).action_confirm_transportation()
        transport_lst = []
        # if not self.carrier_booking:
        #     raise UserError(_("Transportation cannot be confirmed without CARRIER BOOKING"))
        # if not self.job_id:
        #     raise UserError(_("Transportation cannot be confirmed without JOB"))
        # if not self.workorder:
        #     raise UserError(_("Transportation cannot be confirmed without WORK ORDER"))
        # if not self.transport_reference:
        #     raise UserError(_("Transportation cannot be confirmed without TRANSPORT REFERENCE"))
        # if not self.pickup_loc_id:
        #     raise UserError(_("Transportation cannot be confirmed without PICK UP LOCATION"))
        # if not self.planned_date:
        #     raise UserError(_("Transportation cannot be confirmed without PLANNED DATETIME"))
        # if not self.vessel_name:
        #     raise UserError(_("Transportation cannot be confirmed without VESSEL NAME"))
        # if not self.port_of_origin_id:
        #     raise UserError(_("Transportation cannot be confirmed without PORT OF ORIGIN"))
        # if not self.fpod_id:
        #     raise UserError(_("Transportation cannot be confirmed without FPOD"))

        # if self.pickup_loc_id == self.dropoff_loc_id:
        #     raise UserError(_("Pick up and Drop off locations cannot be same"))
        # If there are container route lines and equipment route lines, create planned track - trace records.
        self.create_estimated_track_trace()
        self.get_coordinates()
        # self.is_transportation_confirmed = True
        # self.write({'state': 'confirm'})
        se_rec = self.env['track.shipment.event'].create({
                'shipment_event': 'Shipment',
                'event_created': datetime.today(),
                'event_datetime': datetime.today(),
                'event_classifier_code': 'ACT',
                'shipment_event_type_code': 'RECE',
                'reason':'Transport Confirm',
                'booking_id':self.inquiry_id.id
            })
        tnt_rec = self.env['track.trace.event'].search([('transport_id','=',self.id)])
        se_rec_line = self.env['track.shipment.event'].search([('booking_id','=',self.inquiry_id.id)])
        for i in se_rec_line:
            i.track_trace_event_id = tnt_rec.id
            
        # Post transport to TNT API
        if self.fb_transport_id == _('New'):
            fb_trans = self.env['ir.sequence'].next_by_code('transport.seq') or _('New')
            client_id = self.env['ir.config_parameter'].sudo().get_param('database.uuid')
            self.fb_transport_id = fb_trans + '_' + client_id
        # if self.job_id:
        #     transport_lst = self.job_id.confirmed_transport_ids.ids
        #     transport_lst.append(self.id)
        #     self.job_id.confirmed_transport_ids = [(6, 0, transport_lst)]
        # If there are container route lines, create estimated track - trace records.
        # if self.container_route_line:
        #     self.create_estimated_track_trace()
        return True

    def action_create_shipping_instruction(self):
        view_id = self.env.ref('freightbox.shipping_instuction_form_view').id
        ctx = dict(
            default_transport_id=self.id,
            default_carrier_booking_reference=self.carrier_booking,
            # default_cont_id=self.cont_id,
            default_is_shipping_instruction=True,
            default_job_id=self.job_id.id,
            default_si_inquiry_no=self.inquiry_id.id,
            default_transport_container_id=self.cont_id,
            default_booking_user_id=self.booking_user_id.id,
        )
        return {
            'name': 'Shipping Instruction',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'shipping.instruction',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': ctx,
        }

    def action_create_or_update_transport_template(self):
        transport_template_obj = self.env['transport.template']
        transport_template_id = transport_template_obj.search(
            [('transport_id', '=', self.id), ('is_created_from_transport', '=', True)], limit=1)
        if transport_template_id:
            ctx = dict(
                default_transport_id=self.id,
                default_name=transport_template_id.name,
                default_is_created_from_transport=transport_template_id.is_created_from_transport,
            )
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'transport.template.wiz',
                'view_mode': 'form',
                'views': [(self.env.ref('freightbox.transport_template_form_view_wiz').id, "form")],
                'context': ctx,
                'target': 'new',
            }
        else:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'transport.template.wiz',
                'view_mode': 'form',
                'views': [(self.env.ref('freightbox.transport_template_form_view_wiz').id, "form")],
                'context': {'current_id': self.id},
                'target': 'new',
            }

    def action_transportation_send(self):
        """ Open a window to compose an email, with the edi invoice template
            message loaded by default
        """
        outmail_rec = self.env['ir.mail_server'].search([])
        if not outmail_rec:
            raise UserError("Outgoing mail server not set !!!")

        self.ensure_one()
        template = self.env.ref('freightbox.mail_template_freight_transport', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='transport',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template.id,
            default_composition_mode='comment',
            force_email=True,
        )
        return {
            'name': _('Compose Email'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form.id, 'form')],
            'view_id': compose_form.id,
            'target': 'new',
            'context': ctx,
        }

    def _get_si_count(self):
        for i in self:
            si_counts = self.env['shipping.instruction'].search([('transport_id', '=', i.id)])
            i.si_count = len(si_counts)
            if len(si_counts) > 0:
                i.si_state = "si_created"
            if si_counts.state == "accepted":
                i.si_state = "si_accepted"


    def _get_tnt_count(self):
        tnt_counts = self.env['track.trace.event'].search_count([('transport_id', '=', self.id)])
        self.tnt_count = tnt_counts

    def action_get_si(self):
        itemids = self.env['shipping.instruction'].search([('transport_id', '=', self.id)])
        itemids = itemids.ids
        return {
            'name': "Shipping Instruction",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'shipping.instruction',
            'view_id': False,
            'domain': [('id', 'in', itemids)],
            'target': 'current',
        }

    def action_get_tnt(self):
        itemids = self.env['track.trace.event'].search([('transport_id', '=', self.id)])
        itemids = itemids.ids
        return {
            'name': "Track n Trace",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'track.trace.event',
            'view_id': False,
            'domain': [('id', 'in', itemids)],
            'target': 'current',
        }

    @api.depends('route_template_line.service_line')
    def _get_service_count(self):
        service_count = len(self.route_template_line.service_line)
        for line in self:
            line.service_count = service_count
            service_ids = line.route_template_line.service_line.ids
            line.service_ids = service_ids

    def action_view_services(self):
        services = self.mapped('service_ids')
        action = self.env["ir.actions.actions"]._for_xml_id("freightbox.action_service_menu")
        if len(services) >= 1:
            action['domain'] = [('id', 'in', services.ids)]
        context = {
            'default_service_ids': services.ids,
        }
        action['context'] = context
        return action

    # name = fields.Char("Name")
    # workorder = fields.Char("Work Order*", tracking=True)
    # cont_id = fields.Char("Container ID", tracking=True)
    # planned_date = fields.Datetime("Planned Datetime*", tracking=True)
    # scheduled_date = fields.Datetime("Estimated Datetime*", tracking=True)
    # actual_date = fields.Datetime("Actual Datetime", tracking=True)
    # delay_reason = fields.Char("Delay Reason", tracking=True)
    # remarks = fields.Char("Remarks", tracking=True)
    # carrier_handover = fields.Many2one('port', string="Carrier Handover", tracking=True)
    # vessel_name = fields.Char("Vessel Name*", tracking=True)
    # imo_no = fields.Char("IMO No.", tracking=True)
    # voyage = fields.Char("Voyage", tracking=True)
    # rotation = fields.Char("Rotation", tracking=True)
    # proforma_schedule = fields.Binary("Proforma Schedule", tracking=True)
    # proforma_schedule_fname = fields.Char("Proforma Schedule Filename", tracking=True)
    # gate_cutoff = fields.Datetime("Gate Cut Off", tracking=True)
    # facility = fields.Many2one('port', string="Facility")
    # temparature = fields.Char("Temparature", tracking=True)
    # ventilation = fields.Char("Ventilation", tracking=True)
    # humidity = fields.Char("Humidity", tracking=True)
    # is_transportation_confirmed = fields.Boolean('Transportation Confirmed', tracking=True)
    route_template_id = fields.Many2one('route.templates', string='Route Template', tracking=True)
    route_line = fields.One2many('route.line', 'transport_id', string='Route', tracking=True)
    # container_route_line = fields.One2many('container.journey', 'transport_id', string='Container Journey', tracking=True)
    # equipment_journey_ids = fields.One2many('equipment.journey', 'transport_id', string='Equipment Journey', tracking=True)
    # state = fields.Selection([
    #     ('draft', 'Draft'),
    #     ('confirm', 'Transport Confirmed')
    #     ('cancelled', 'Cancelled')
    # ], default='draft', tracking=True, string='Status', readonly=True)

    # port_of_origin_id = fields.Many2one('port', string='Port of Origin*', tracking=True)
    # port_of_origin_facility_id = fields.Many2one('sub.port', string="Port of Origin Facility", tracking=True)

    # fpod_id = fields.Many2one('port', string='FPOD*', help="Final Port of Destination", tracking=True)
    # fpod_facility_id = fields.Many2one('sub.port', string="FPoD Facility", tracking=True,
    #                                    help="Final Port of Destination Facility")

    # point_of_stuffing = fields.Many2one('port', string='Point of Stuffing', tracking=True)
    # point_of_destuffing = fields.Many2one('port', string='Point of Destuffing', tracking=True)
    # carrier_booking = fields.Char(string='Carrier Booking*', tracking=True)
    # transport_reference = fields.Char(string='Transport Reference*', tracking=True)
    transport_template_id = fields.Many2one('transport.template', string='Transport Template', tracking=True)
    # cont_type = fields.Many2one("container.type", string="Container type", tracking=True)
    # special_type = fields.Selection(
    #     [('reefer_active', 'Reefer Active'), ('reefer_inactive', 'Reefer InActive'), ('pl', 'PL'), ('fr', 'FR'),
    #      ('ot', 'OT')], string="Special", tracking=True)
    # job_id = fields.Many2one('job', string='Job*', tracking=True, ondelete='cascade')
    # pickup_loc_id = fields.Many2one("port", string="Pick up Location*", tracking=True)
    # pickup_loc_facility_id = fields.Many2one('sub.port', string="Pick up Location Facility", tracking=True)
    # dropoff_loc_id = fields.Many2one("port", string="Drop Off Location", tracking=True)
    # dropoff_loc_facility_id = fields.Many2one('sub.port', string="Drop Off Location Facility", tracking=True)
    # shipping_instruction_id = fields.Many2one("shipping.instruction",
    #                                           string="Shipping Instruction", tracking=True)
    # inquiry_id = fields.Many2one('crm.lead', string="Inquiry ID", readonly=True, tracking=True)
    # pickup_mode = fields.Many2one('mode', string='Mode of transport from pickup', tracking=True)
    # dropoff_mode = fields.Many2one('mode', string='Mode of transport for Dropoff', tracking=True)
    # stuffing_mode = fields.Many2one('mode', string='Mode of transport from Stuffing Location', tracking=True)
    # destuffing_mode = fields.Many2one('mode', string='Mode of transport for Destuffing Location', tracking=True)
    # vessel_mode = fields.Many2one('mode', string='Mode of transport from Port', tracking=True)

    # equipment_event_line_ids = fields.One2many('equipment.event.line', 'equipment_line_id', string='Equipment Event')
    # shipment_event_line = fields.One2many('shipment.event', 'shipment_event_line_id', string='Shipment Event')
    # transport_event_line = fields.One2many('transport.event', 'transport_event_line_id', string='Transport Event')
    si_count = fields.Integer(string='SI Count', compute='_get_si_count', readonly=True, tracking=True)
    tnt_count = fields.Integer(string='TNT Count', compute='_get_tnt_count', readonly=True, tracking=True)
    # create_si_by_shipper = fields.Boolean("Allow Shipper to Create SI", tracking=True)
    is_multi_modal = fields.Boolean("Is Multi Modal", tracking=True)
    vessel_name1 = fields.Char("Vessel Name", tracking=True)
    voyage1 = fields.Char("Voyage", tracking=True)
    rotation1 = fields.Char("Rotation", tracking=True)
    imo_no1 = fields.Char("IMO No.", tracking=True)
    intermediate_pol_id = fields.Many2one("port", string="Intermediate port of loading", tracking=True)
    # fb_transport_id = fields.Text("FB Transport ID", default=lambda self: _('New'))
    no_of_api_calls = fields.Integer(string='Api Calls', readonly=True, tracking=True, default=0)
    is_track_requested = fields.Boolean("Is track Requested?", tracking=True)
    second_vessel_mode = fields.Many2one('mode', string='Mode of transport from Port', tracking=True)
    is_another_ship_needed = fields.Boolean("Is another ship needed?", tracking=True)
    vessel_name2 = fields.Char("Vessel Name", tracking=True)
    voyage2 = fields.Char("Voyage", tracking=True)
    rotation2 = fields.Char("Rotation", tracking=True)
    imo_no2 = fields.Char("IMO No.", tracking=True)
    second_intermediate_pol_id = fields.Many2one("port", string="Second Intermediate port of loading", tracking=True)
    third_vessel_mode = fields.Many2one('mode', string='Mode of transport from Port', tracking=True)
    # active = fields.Boolean(string='Active', default=True)
    # booking_user_id = fields.Many2one('res.users', string="Shipper/FF")
    # si_state = fields.Selection([
    #     ('yet_to_create', 'Yet To Create'),
    #     ('si_created', 'SI Created'),
    #     ('si_accepted', 'SI Accepted'),
    # ], default='yet_to_create', tracking=True, string='SI Status', readonly=True)
    waypoint_coordinates = fields.Text('Waypoint Coordinates')
    allow_get_waypoints = fields.Boolean("Allow Import Waypoints", compute="onchange_waypoint_coordinates", default=True)
    cont_jour_count = fields.Integer(string='Contain Jour', compute='_get_container_journy', readonly=True, tracking=True)

    def _get_container_journy(self):
        for i in self:
            i.cont_jour_count = len(i.container_route_line)

    def action_view_container_journy(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'container.journey',
            'view_mode': 'tree',
            # 'views': [(self.env.ref('freightbox.route_template_form_wiz').id, "form")],
            'domain':[('transport_id','=',self.id)],
            'context': {'default_transport_id':self.id},
            # 'target': 'new',
        }

    def onchange_waypoint_coordinates(self):
        for record in self:
            record.allow_get_waypoints = True
            if record.waypoint_coordinates and record.waypoint_coordinates.split() != "":
                record.allow_get_waypoints = False
            line_without_waypoints = False
            for route in record.container_route_line:
                if not route.route_coordinates or route.route_coordinates.split() == "":
                    line_without_waypoints = True
                    break
            if line_without_waypoints:
                record.allow_get_waypoints = True

    @api.onchange('transport_template_id')
    def _onchange_transport_template(self):
        container_journey_obj = self.env['container.journey']
        equipment_journey_obj = self.env['equipment.journey']
        port_obj = self.env['port']
        if not self.transport_template_id:
            self.container_route_line = False
            return
        if self.transport_template_id:
            self.workorder = self.transport_template_id.workorder or ''
            self.remarks = self.transport_template_id.remarks
            self.carrier_handover = self.transport_template_id.carrier_handover
            self.gate_cutoff = self.transport_template_id.gate_cutoff
            self.port_of_origin_id = self.transport_template_id.port_of_origin_id
            self.port_of_origin_facility_id = self.transport_template_id.port_of_origin_facility_id
            self.fpod_id = self.transport_template_id.fpod_id
            self.fpod_facility_id = self.transport_template_id.fpod_facility_id
            self.temparature = self.transport_template_id.temparature
            self.humidity = self.transport_template_id.humidity
            self.ventilation = self.transport_template_id.ventilation
            self.cont_type = self.transport_template_id.cont_type
            self.pickup_loc_id = self.transport_template_id.pickup_loc_id
            self.pickup_loc_facility_id = self.transport_template_id.pickup_loc_facility_id
            self.dropoff_loc_id = self.transport_template_id.dropoff_loc_id
            self.dropoff_loc_facility_id = self.transport_template_id.dropoff_loc_facility_id
            self.stuffing_mode = self.transport_template_id.stuffing_mode and self.transport_template_id.stuffing_mode.id or False
            self.destuffing_mode = self.transport_template_id.destuffing_mode and self.transport_template_id.destuffing_mode.id or False
            self.pickup_mode = self.transport_template_id.pickup_mode and self.transport_template_id.pickup_mode.id or False
            self.dropoff_mode = self.transport_template_id.dropoff_mode and self.transport_template_id.dropoff_mode.id or False
        transport_template_container_journey = self.transport_template_id.container_route_line
        self.container_route_line = False
        self.container_route_line.sudo().unlink()

        ptd = self.planned_date or self.transport_template_id.planned_date or fields.Datetime.now()
        pta = ptd
        for cj in transport_template_container_journey:

            distance_data = {}
            if cj.transport_mode and cj.transport_mode.name.lower().strip() in ['road', 'main_line', 'feeder']:
                #Getting Distance - Time data from mother server
                try:
                    start_point_name = cj.start_point
                    end_point_name = cj.end_point
                    transport_mode = 'road'
                    if cj.transport_mode.name.lower().strip() in ['main_line', 'feeder']:
                        transport_mode = 'sea'
                    if start_point_name and end_point_name:
                        if start_point_name.latitude and start_point_name.longitude and end_point_name.latitude and end_point_name.longitude:
                            start_point_country = start_point_name.country_id.name if start_point_name and start_point_name.country_id else False
                            end_point_country = end_point_name.country_id.name if end_point_name and end_point_name.country_id else False
                            api_rec = self.env['api.integration'].search([('name', '=', 'get_distance_time_from_geo_location')])[-1]
                            if not api_rec:
                                ValidationError("API Record does not exist for 'get_distance_time_from_geo_location'.")
                            url = "%s/%s/%s/(%s,%s)/(%s, %s)/%s/%s" % (
                            api_rec.url, start_point_name.name, end_point_name.name, start_point_name.latitude,
                            start_point_name.longitude, end_point_name.latitude, end_point_name.longitude, start_point_country, end_point_country)
                            response = requests.get(url)
                            if response.status_code == 200:
                                distance_data = json.loads(response.content)
                        else:
                            start_point_country = start_point_name.country_id.name if start_point_name and start_point_name.country_id else False
                            end_point_country = end_point_name.country_id.name if end_point_name and end_point_name.country_id else False
                            api_rec = self.env['api.integration'].search([('name', '=', 'get_distance_time')])[-1]
                            if not api_rec:
                                ValidationError("API Record does not exist for 'get_distance_time'.")
                            url = "%s%s/%s/%s/%s/%s" % (api_rec.url, start_point_name.name, end_point_name.name,start_point_country, end_point_country, transport_mode)
                            response = requests.get(url)
                            if response.status_code == 200:
                                distance_data = json.loads(response.content)
                            start_point_name.latitude = distance_data.get('Datas', {}).get('start_point_lat', '')
                            start_point_name.longitude = distance_data.get('Datas', {}).get('start_point_long', '')
                            end_point_name.latitude = distance_data.get('Datas', {}).get('end_point_lat', '')
                            end_point_name.longitude = distance_data.get('Datas', {}).get('end_point_long', '')
                    else:
                        start_point_name_str = start_point_name and start_point_name.name or cj.start_point.name
                        end_point_name_str = end_point_name and end_point_name.name or cj.end_point.name
                        if '/' in start_point_name_str:
                            start_point_name_str = start_point_name_str.replace('/', ' ')
                        if '/' in start_point_name_str:
                            start_point_name_str = start_point_name_str.replace('/', ' ')
                        start_point_country = start_point_name.country_id.name if start_point_name and start_point_name.country_id else False
                        end_point_country = end_point_name.country_id.name if end_point_name and end_point_name.country_id else False
                        api_rec = self.env['api.integration'].search([('name', '=', 'get_distance_time')])[-1]
                        if not api_rec:
                            ValidationError("API Record does not exist for 'get_distance_time'.")
                        url = "%s/%s/%s/%s/%s/%s" % (
                        api_rec.url, start_point_name_str, end_point_name_str, start_point_country, end_point_country, transport_mode)
                        response = requests.get(url)
                        if response.status_code != 200:
                            start_point_name_str = start_point_name and start_point_name.name or cj.start_point.name
                            end_point_name_str = end_point_name and end_point_name.name or cj.end_point.name
                            if '/' in start_point_name_str:
                                start_point_name_str = start_point_name_str.split('/')[-1]
                            if '/' in end_point_name_str:
                                end_point_name_str = end_point_name_str.split('/')[-1]
                            start_point_country = start_point_name.country_id.name if start_point_name and start_point_name.country_id else False
                            end_point_country = end_point_name.country_id.name if end_point_name and end_point_name.country_id else False
                            api_rec = self.env['api.integration'].search([('name', '=', 'get_distance_time')])[-1]
                            if not api_rec:
                                ValidationError("API Record does not exist for 'get_distance_time'.")
                            url = "%s/%s/%s/%s/%s/%s" % (
                                api_rec.url, start_point_name_str, end_point_name_str, start_point_country,
                                end_point_country, transport_mode)
                            response = requests.get(url)
                        if response.status_code == 200:
                            distance_data = json.loads(response.content)
                        if start_point_name:
                            start_point_name.latitude = distance_data.get('Datas', {}).get('start_point_lat', '')
                            start_point_name.longitude = distance_data.get('Datas', {}).get('start_point_long', '')
                        else:
                            start_point_name = port_obj.create({
                                'name': distance_data.get('Datas', {}).get('start_point', cj.start_point.name)
                            })

                        if end_point_name:
                            end_point_name.latitude = distance_data.get('Datas', {}).get('end_point_lat', '')
                            end_point_name.longitude = distance_data.get('Datas', {}).get('end_point_long', '')
                except:
                    ptd = pta + timedelta(hours=cj.yard_time)
                    pta = ptd + timedelta(hours=cj.gate_out_wait_time) + timedelta(hours=cj.gate_in_wait_time) + timedelta(hours=cj.travel_time) + timedelta(hours=cj.buffer_time)
                    new_cj = container_journey_obj.create({
                        'start_point': cj.start_point.id,
                        'end_point': cj.end_point.id,
                        'transport_mode': cj.transport_mode.id,
                        'planned_departure_time': ptd,
                        'planned_arrival_time': pta,
                        'transport_id': self.id,
                        'distance': distance_data.get('Datas', {}).get('distance', cj.distance),
                        'speed': cj.speed,
                        'fuel': cj.fuel,
                        'co2_emmision': cj.co2_emmision,
                        'gate_in_wait_time': distance_data.get('Datas', {}).get('gate_in_wait_time', cj.gate_in_wait_time),
                        'gate_out_wait_time': distance_data.get('Datas', {}).get('gate_out_wait_time', cj.gate_out_wait_time),
                        'travel_time': distance_data.get('Datas', {}).get('travel_time', cj.travel_time),
                        'buffer_time': distance_data.get('Datas', {}).get('buffer_time', cj.buffer_time),
                        'yard_time': distance_data.get('Datas', {}).get('yard_time', cj.yard_time),
                    })
                    new_cj.onchange_distance_traveltime_speed()
                    continue
            gate_in_wait_time = distance_data.get('Datas', {}).get('gate_in_wait_time', cj.gate_in_wait_time)
            gate_out_wait_time = distance_data.get('Datas', {}).get('gate_out_wait_time', cj.gate_out_wait_time)
            travel_time = distance_data.get('Datas', {}).get('travel_time', cj.travel_time)
            buffer_time = distance_data.get('Datas', {}).get('buffer_time', cj.buffer_time)
            yard_time = distance_data.get('Datas', {}).get('yard_time', cj.yard_time)

            ptd = pta
            if yard_time:
                ptd += timedelta(hours=yard_time)
            pta = ptd
            if gate_out_wait_time:
                pta += timedelta(hours=gate_out_wait_time)
            if gate_in_wait_time:
                pta += timedelta(hours=gate_in_wait_time)
            if travel_time:
                pta += timedelta(hours=travel_time)
            if buffer_time:
                pta += timedelta(hours=buffer_time)

            new_cj = container_journey_obj.create({
                'start_point': cj.start_point.id,
                'end_point': cj.end_point.id,
                'transport_mode': cj.transport_mode.id,
                'planned_departure_time': ptd,
                'planned_arrival_time': pta,
                'transport_id': self.id,
                'distance': distance_data.get('Datas', {}).get('distance', cj.distance),
                'speed': distance_data.get('Datas', {}).get('speed_kmph', cj.speed),
                'fuel': cj.fuel,
                'co2_emmision': cj.co2_emmision,
                'gate_in_wait_time': gate_in_wait_time,
                'gate_out_wait_time': gate_out_wait_time,
                'travel_time': travel_time,
                'buffer_time': buffer_time,
                'yard_time': yard_time,
            })
            new_cj.onchange_distance_traveltime_speed()
        self.equipment_journey_ids.sudo().unlink()
        for equipment_route in self.transport_template_id.equipment_route_line:
            equipment_journey_obj.create({
                'transport_id': self.id,
                'track_trace_event_id': equipment_route.track_trace_event_id,
                'equip_event_id': equipment_route.equip_event_id,
                'event_created_datetime': equipment_route.event_created_datetime,
                'estimated_event_time': equipment_route.estimated_event_time,
                'event_classifier_code':equipment_route.event_classifier_code or 'PLN',
                'equip_event_type_code': equipment_route.equip_event_type_code,
                'equip_reference': equipment_route.equip_reference,
                'iso_equip_code': equipment_route.iso_equip_code,
                'empty_indicator_code': equipment_route.empty_indicator_code,
                'shipment_id': equipment_route.shipment_id,
                'transport_call': equipment_route.transport_call,
                'event_location': equipment_route.event_location,
                'document_references': equipment_route.document_references,
                'references_type_code': equipment_route.references_type_code,
                'reference_values': equipment_route.reference_values,
                'seal_no': equipment_route.seal_no,
                'seal_source': equipment_route.seal_source,
                'seal_type': equipment_route.seal_type,
                'event_type': equipment_route.event_type,
                'event_description': equipment_route.event_description,
                'locode': equipment_route.locode,
                'location_name': equipment_route.location_name,
                'country': equipment_route.country,
                'timezone': equipment_route.timezone,
                'latitude': equipment_route.latitude,
                'longitude': equipment_route.longitude,
                'transport_call_type': equipment_route.transport_call_type
            })

        # transport_route_line = self.transport_template_id.transport_template_route_line
        # for line in transport_route_line:
        #     self.route_line.create({
        #         'port_of_origin': line.port_of_origin,
        #         'fpod': line.fpod,
        #         'mode_id': line.mode_id.id,
        #         'transport_id': self.id,
        #         'planned_departure_time': line.planned_departure_time,
        #         'planned_arrival_time': line.planned_arrival_time,
        #         'estimated_departure_time': line.estimated_departure_time,
        #         'estimated_arrival_time': line.estimated_arrival_time,
        #         'actual_departure_time': line.actual_departure_time,
        #         'actual_arrival_time': line.actual_arrival_time,
        #         'delay_reason': line.delay_reason,
        #     })

    def get_port_from_locode(self, locode):
        try:
            api_rec = self.env['api.integration'].search([('name', '=', 'get_port_details_from_locode')])[-1]
            if not api_rec:
                ValidationError("API Record does not exist for 'get_port_details_from_locode'.")
            url = "%s/%s" % (api_rec.url, locode)
            response = requests.get(url)
            if response.status_code == 200:
                distance_data = json.loads(response.content).get('Datas', {})
                port_vals = {
                    'unloc_code': distance_data.get('locode', locode),
                    'name': distance_data.get('locode', ''),
                    'latitude': distance_data.get('latitude', ''),
                    'longitude': distance_data.get('longitude', ''),
                }
                return self.env['port'].create(port_vals)
        except:
            return False
        return False

    def action_create_route_template(self):
        ctx = {}
        self.ensure_one()
        if not self.route_line:
            raise UserError(_("There is no Route to create Route template"))
        transporttemplate = self.env['route.templates'].search(
            [('transport_id', '=', self.id), ('is_created_from_transport', '=', True)], limit=1)
        ctx = dict(
            default_transport_id=self.id,
            default_is_created_from_transport=True,
            current_id=self.id,
        )
        if transporttemplate:
            ctx = dict(
                default_transport_id=self.id,
                default_name=transporttemplate.name,
                default_is_created_from_transport=transporttemplate.is_created_from_transport,
                current_id=self.id,
            )
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'route.templates.wiz',
            'view_mode': 'form',
            'views': [(self.env.ref('freightbox.route_template_form_wiz').id, "form")],
            # route_template_form_view2
            'context': ctx,
            'target': 'new',
        }

    def action_load_route_template(self):
        self.container_route_line = False
        route_lst = []
        if self.route_template_id:
            for r in self.route_template_id.container_route_line:
                route_lst.append((0, 0, {
                    'start_point': r.start_point.id,
                    'end_point': r.end_point,
                    'transport_mode': r.transport_mode.id,
                    'estimated_departure_time': r.estimated_departure_time,
                    'estimated_arrival_time': r.estimated_arrival_time,
                    'planned_departure_time': r.planned_departure_time,
                    'planned_arrival_time': r.planned_arrival_time,
                    'actual_departure_time': r.actual_departure_time,
                    'actual_arrival_time': r.actual_arrival_time,
                    'delay_reason': r.delay_reason,
                    'change_remark': r.change_remark,
                }))
            self.container_route_line = route_lst

        # self.route_line = False
        # route_list = []
        # vals_start = {}
        # vals_end = {}
        # vals_start_tup = ()
        # vals_end_tup = ()
        # for line in self.route_template_id.route_template_line:
        #     route_list.append((0, 0, {'port_of_origin_id': line.port_of_origin_id.id,
        #                               'fpod_id': line.fpod_id.id,
        #                               'port_of_origin': line.port_of_origin,
        #                               'fpod': line.fpod,
        #                               'point_of_stuffing': line.point_of_stuffing,
        #                               'point_of_destuffing': line.point_of_destuffing,
        #                               'mode_id': line.mode_id.id,
        #                               'estimated_departure_time': line.estimated_departure_time,
        #                               'estimated_arrival_time': line.estimated_arrival_time,
        #                               'actual_departure_time': line.actual_departure_time,
        #                               'actual_arrival_time': line.actual_arrival_time,
        #                               'delay_reason': line.delay_reason,
        #                               }))
        # if route_list != []:
        #     vals_start.update({'port_of_origin': route_list[0][2]['point_of_stuffing'],
        #                        'fpod': route_list[0][2]['port_of_origin'],
        #                        })
        #     vals_start_tup = (0, 0, vals_start)
        #     vals_end.update({'port_of_origin': route_list[-1][2]['fpod'],
        #                      'fpod': route_list[-1][2]['point_of_destuffing'],
        #                      })
        #     vals_end_tup = (0, 0, vals_end)
        #     route_list.insert(0, vals_start_tup)
        #     route_list.append(vals_end_tup)
        # self.route_line = route_list

    def action_delete_route_template(self):
        self.route_line = False

    def create_estimated_track_trace(self):
        track_trace_event = self.env["track.trace.event"].search(
            [('transport_id', '=', self.id),
             ('carrier_booking', '=', self.carrier_booking)],
            order="id", limit=1
        )
        if not track_trace_event:
            bol_id = self.env['bill.of.lading'].search([('carrier_booking_reference', '=', self.carrier_booking), ('is_master_bill_of_lading', '=', True)])

            track_trace_event = self.env["track.trace.event"].create({
                "carrier_booking": self.carrier_booking,
                "cont_id": self.cont_id,
                "cont_type": self.cont_type.id,
                "transport_document_reference": bol_id.transport_document_reference,
                "party_name_id": self.job_id.po_id.party_name_id.id,
                "partner_id": self.job_id.po_id.partner_id.id,
                "transport_id": self.id,
                "port_of_origin_id": self.port_of_origin_id.id,
                "fpod_id": self.fpod_id.id
            })
        self.create_estimated_transport_events(track_trace_event)
        self.create_estimated_equipment_events(track_trace_event)

    def create_estimated_transport_events(self, track_trace_event):
        track_transport_event_obj = self.env["track.transport.event"]
        seq_no = track_transport_event_obj.search([], order="sequence desc", limit=1).sequence or 0
        for record in self.container_route_line:
            seq_no += 5
            desc = "Vehicle will leave location %s at %s" % (record.start_point.name, record.estimated_departure_time)
            event_datetime = record.planned_departure_time
            event_classifier_code = 'PLN'
            if record.estimated_departure_time:
                event_datetime = record.estimated_departure_time
                event_classifier_code = 'EST'
            depa_event_vals = {
                "sequence": seq_no,
                "track_trace_event_id": track_trace_event.id,
                "event_created_datetime": fields.Datetime.now(),
                "event_datetime": event_datetime,
                "event_classifier_code": event_classifier_code,
                "event_type": "TRANSPORT",
                "event_description": desc,
                "transport_event_id": self.fb_transport_id,
                "transport_event_type_code": "DEPA",
                "change_remark": record.change_remark,
                "transport_id": self.id,
                "transport_reference":self.transport_reference,
                "container_id": self.cont_id,
                "transport_name": self.cont_id,
                "mode_of_transport_code": record.transport_mode.name,
                "vessel_imo_number": self.imo_no,
                "carrier_voyage_number": self.voyage,
                "un_location_code": record.start_point.unloc_code,
                "facility_code": self.pickup_loc_facility_id.unloc_code or "",
                "location": record.start_point.name,
                "vessel_name": self.vessel_name,
            }
            track_transport_event_obj.create(depa_event_vals)
            seq_no += 5
            desc = "Vehicle will arrive at location %s at %s" % (record.end_point, record.estimated_arrival_time)
            event_datetime = record.planned_arrival_time
            event_classifier_code = 'PLN'
            if record.estimated_arrival_time:
                event_datetime = record.estimated_arrival_time
                event_classifier_code = 'EST'
            arr_event_vals = {
                "sequence": seq_no,
                "track_trace_event_id": track_trace_event.id,
                "event_created_datetime": fields.Datetime.now(),
                "event_datetime": event_datetime,
                "event_classifier_code": event_classifier_code,
                "event_type": "TRANSPORT",
                "event_description": desc,
                "transport_event_id": self.fb_transport_id,
                "transport_event_type_code": "ARRI",
                "change_remark": record.change_remark,
                "transport_id": self.id,
                "transport_reference": self.transport_reference,
                "container_id": self.cont_id,
                "transport_name": self.cont_id,
                "mode_of_transport_code": record.transport_mode.name,
                "vessel_imo_number": self.imo_no,
                "carrier_voyage_number": self.voyage,
                "un_location_code": record.end_point.unloc_code,
                "facility_code": self.dropoff_loc_facility_id.unloc_code or "",
                "location": record.end_point.name,
                "vessel_name": self.vessel_name,
                'distance': record.distance,
                'speed': record.speed,
                'fuel': record.fuel,
                'co2_emmision': record.co2_emmision
            }
            track_transport_event_obj.create(arr_event_vals)

    def create_estimated_equipment_events(self, track_trace_event):
        track_equipment_event_obj = self.env["track.equipment.event"]
        for record in self.equipment_journey_ids:
            equip_event_vals = {
                'track_trace_event_id': track_trace_event.id,
                'equip_event_id': record.equip_event_id,
                'event_created_datetime': record.event_created_datetime,
                'event_datetime': record.estimated_event_time or fields.Datetime.now(),
                'event_classifier_code':record.event_classifier_code or 'PLN',
                'equip_event_type_code': record.equip_event_type_code,
                'equip_reference': record.equip_reference,
                'iso_equip_code': record.iso_equip_code,
                'empty_indicator_code': record.empty_indicator_code,
                'shipment_id': record.shipment_id,
                'transport_call': record.transport_call,
                'event_location': record.event_location,
                'document_references': record.document_references,
                'references_type_code': record.references_type_code,
                'reference_values': record.reference_values,
                'seal_no': record.seal_no,
                'seal_source': record.seal_source,
                'seal_type': record.seal_type,
                'event_type': record.event_type,
                'event_description': record.event_description,
                'locode': record.locode,
                'location_name': record.location_name,
                'country': record.country,
                'timezone': record.timezone,
                'latitude': record.latitude,
                'longitude': record.longitude,
                'transport_call_type': record.transport_call_type,
            }
            track_equipment_event_obj.create(equip_event_vals)

    def action_import_tnt(self):
        api_obj = self.env["api.integration"]
        return api_obj.import_tnt_cron(transports=self)

    def transport_tutorial_video_new_tab(self):
        url = self.env['ir.config_parameter'].sudo().get_param('freightbox.complete_tutorial_video_start_to_end',
                                                               "/freightbox/static/src/img/index_file_images/not_found.png")
        return {
            'type': 'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }

    @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    def get_view(self, view_id=None, view_type='form', **options):
        # result = super().fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        result = super().get_view(view_id, view_type, **options)
        if view_id == self.env.ref("freightbox.transport_form_view").id:
            url = self.env['ir.config_parameter'].sudo().get_param('freightbox.transport_tutorial_video',
                                                                   "/freightbox/static/src/img/index_file_images/not_found.png")
            doc = etree.XML(result['arch'])
            for node in doc.xpath("//iframe[@id='transport_tutorial_video']"):
                node.set('src', url)
            result['arch'] = etree.tostring(doc)
        return result

    @api.onchange('planned_date')
    def onchange_planned_date(self):
        for record in self:
            ptd = self.planned_date
            pta = ptd
            for cj in record.container_route_line:
                ptd = pta + timedelta(hours=cj.yard_time)
                pta = ptd + timedelta(hours=cj.gate_out_wait_time) + timedelta(hours=cj.gate_in_wait_time) + timedelta(hours=cj.travel_time) + timedelta(hours=cj.buffer_time)
                cj.write({
                    'planned_departure_time': ptd,
                    'planned_arrival_time': pta
                })
        self.container_route_line.onchange_planned_dates()
        self.container_route_line.onchange_scheduled_dates()

    @api.onchange('scheduled_date')
    def onchange_scheduled_date(self):
        for record in self:
            if record.scheduled_date:
                etd = record.scheduled_date
                eta = etd
                for cj in record.container_route_line:
                    etd = eta + timedelta(hours=cj.yard_time)
                    eta = etd + timedelta(hours=cj.gate_out_wait_time) + timedelta(hours=cj.gate_in_wait_time) + timedelta(
                        hours=cj.travel_time) + timedelta(hours=cj.buffer_time)
                    cj.write({
                        'estimated_departure_time': etd,
                        'estimated_arrival_time': eta
                    })
                record.container_route_line.onchange_planned_dates()
                record.container_route_line.onchange_scheduled_dates()

    def action_updated_pta_ptd_eta_etd(self):
        return True

    def action_update_route_dates(self):
        for record in self:
            ptd = self.planned_date
            pta = ptd
            for cj in record.container_route_line:
                if cj.start_point and not cj.start_point.country_id:
                    raise ValidationError('Country not set in port : %s. Please configure and try again.' % cj.start_point.name)
                if cj.end_point and not cj.end_point.country_id:
                    raise ValidationError('Country not set in port : %s. Please configure and try again.' % cj.end_point.name)

                if cj.transport_mode.name.strip().lower() in ['road', 'mainline', 'main line', 'feeder']:
                    response = False
                    distance_data = {}
                    if cj.start_point.latitude and cj.start_point.longitude and cj.end_point.latitude and cj.end_point.longitude and cj.transport_mode.name.strip().lower() == 'road':
                        api_rec = self.env['api.integration'].search([('name', '=', 'get_distance_time_from_geo_location')])[-1]
                        if not api_rec:
                            ValidationError("API Record does not exist for 'get_distance_time_from_geo_location'.")
                        url = "%s/%s/%s/(%s,%s)/(%s, %s)/%s/%s" % (
                            api_rec.url, cj.start_point.name, cj.end_point.name, cj.start_point.latitude,
                            cj.start_point.longitude, cj.end_point.latitude, cj.end_point.longitude, cj.start_point.country_id.name, cj.end_point.country_id.name)
                        response = requests.get(url)
                        if response.status_code == 200:
                            distance_data = json.loads(response.content)
                        else:
                            origin_geo_data = self.get_geo_location_from_port(cj.start_point)
                            dest_geo_data = self.get_geo_location_from_port(cj.end_point)
                            start_lon = origin_geo_data.get('lon', False)
                            start_lat = origin_geo_data.get('lat', False)
                            end_lon = dest_geo_data.get('lon', False)
                            end_lat = dest_geo_data.get('lat', False)
                            if start_lon and start_lat and end_lon and end_lat:
                                api_rec = self.env['api.integration'].search([('name', '=', 'get_distance_time_from_geo_location')])[-1]
                                if not api_rec:
                                    ValidationError(
                                        "API Record does not exist for 'get_distance_time_from_geo_location'.")
                                url = "%s/%s/%s/(%s,%s)/(%s, %s)/%s/%s" % (
                                    api_rec.url, cj.start_point.name, cj.end_point.name, start_lat,
                                    start_lon, end_lat, end_lon,
                                    cj.start_point.country_id.name, cj.end_point.country_id.name)
                                response = requests.get(url)
                                if response.status_code == 200:
                                    distance_data = json.loads(response.content)
                                    cj.start_point.sudo().write({
                                        'latitude': start_lat,
                                        'longitude': start_lon
                                    })
                                    cj.end_point.sudo().write({
                                        'latitude': end_lat,
                                        'longitude': end_lon
                                    })


                    else:
                        start_point_geo_data = self.get_geo_location_from_port(cj.start_point)
                        if start_point_geo_data.get('status_code', 0) == 200:
                            if not cj.start_point.latitude:
                                cj.start_point.latitude = start_point_geo_data.get('lat', '')
                            if not cj.start_point.longitude:
                                cj.start_point.longitude = start_point_geo_data.get('lon', '')
                        end_point_geo_data = self.get_geo_location_from_port(cj.end_point)
                        if end_point_geo_data.get('status_code', 0) == 200:
                            if not cj.end_point.latitude:
                                cj.end_point.latitude = end_point_geo_data.get('lat', '')
                            if not cj.end_point.longitude:
                                cj.end_point.longitude = end_point_geo_data.get('lon', '')
                        api_rec = self.env['api.integration'].search([('name', '=', 'get_distance_time_from_geo_location')])[-1]
                        if not api_rec:
                            ValidationError("API Record does not exist for 'get_distance_time_from_geo_location'.")
                        url = "%s/%s/%s/(%s,%s)/(%s, %s)/%s/%s" % (
                            api_rec.url, cj.start_point.name.strip(), cj.end_point.name.strip(), cj.start_point.latitude,
                            cj.start_point.longitude, cj.end_point.latitude, cj.end_point.longitude, cj.start_point.country_id.name.strip(), cj.end_point.country_id.name.strip())
                        response = requests.get(url)
                        if response.status_code == 200:
                            distance_data = json.loads(response.content)

                    if response and response.status_code == 200:
                        distance_res_data = distance_data.get('Datas', {})
                        distance_update_vals = {
                            'distance': distance_res_data.get('distance', 0),
                            'gate_in_wait_time': distance_res_data.get('gate_in_wait_time', 0),
                            'gate_out_wait_time': distance_res_data.get('gate_out_wait_time', 0),
                            'travel_time': distance_res_data.get('travel_time', 0),
                            'buffer_time': distance_res_data.get('buffer_time', 0),
                            'yard_time': distance_res_data.get('yard_time', 0),
                        }
                        cj.write(distance_update_vals)
                    if response.status_code != 200 or distance_data.get('Datas') == {}:
                        transport_mode = 'road'
                        start_point_name_str = cj.start_point.name
                        end_point_name_str = cj.end_point.name
                        speed = 30
                        fuel = 'motor_gasoline'
                        if cj.transport_mode.name.strip().lower() in ['mainline', 'main line', 'feeder']:
                            transport_mode = 'sea'
                            start_point_name_str = cj.start_point.unloc_code or cj.start_point.name
                            end_point_name_str = cj.end_point.unloc_code or cj.end_point.name
                            speed = 33.5
                            fuel = 'residual_fuel_oil'

                        if '/' in start_point_name_str:
                            start_point_name_str = start_point_name_str.split('/')[-1]
                        if '/' in end_point_name_str:
                            end_point_name_str = end_point_name_str.split('/')[-1]
                        start_point_country = cj.start_point.country_id.name if cj.start_point and cj.start_point.country_id else False
                        end_point_country = cj.end_point.country_id.name if cj.end_point and cj.end_point.country_id else False
                        api_rec = self.env['api.integration'].search([('name', '=', 'get_distance_time')])[-1]
                        if not api_rec:
                            ValidationError("API Record does not exist for 'get_distance_time'.")
                        url = "%s/%s/%s/%s/%s/%s" % (
                            api_rec.url, start_point_name_str, end_point_name_str, start_point_country, end_point_country, transport_mode)
                        response = requests.get(url)
                        distance_res_data = {}
                        if response.status_code == 200:
                            distance_res_data = json.loads(response.content)
                        distance_update_vals = {
                            'distance': distance_res_data.get('Datas', {}).get('distance', 0),
                            'gate_in_wait_time': distance_res_data.get('Datas', {}).get('gate_in_wait_time', 0),
                            'gate_out_wait_time': distance_res_data.get('Datas', {}).get('gate_out_wait_time', 0),
                            'travel_time': distance_res_data.get('Datas', {}).get('travel_time', 0),
                            'buffer_time': distance_res_data.get('Datas', {}).get('buffer_time', 0),
                            'yard_time': distance_res_data.get('Datas', {}).get('yard_time', 0),
                            'speed': speed,
                            'fuel': fuel
                        }
                        cj.write(distance_update_vals)
        self.onchange_planned_date()
        self.onchange_scheduled_date()
        return True

    def get_geo_location_from_port(self, port):
        if port.geo_codes_updated_from_api and port.latitude and port.longitude:
            return {
                'status_code': 200,
                'lat': port.latitude,
                'lon': port.longitude
            }
        api_rec = self.env['api.integration'].search([('name', '=', 'forward_reverse_geo_coding')])[-1]
        if not api_rec:
            raise Warning("API record doesn't exist for 'forward_reverse_geo_coding' process.")

        url = api_rec.url

        city = port.name.replace('/', ',')
        querystring = {"format": "json", "city": city, "accept-language": "en", "polygon_threshold": "0.0"}

        headers = {
            "X-RapidAPI-Key": api_rec.key,
            "X-RapidAPI-Host": api_rec.host
        }

        if port and port.country_id:
            querystring.update({'country': port.country_id.name})

        geo_loc_response = requests.request("GET", url, headers=headers, params=querystring)

        response_content = json.loads(geo_loc_response.content)
        if response_content and geo_loc_response.status_code == 200:
            data_dict = response_content[0]
            data_dict.update({'status_code': geo_loc_response.status_code})
            if data_dict.get('lat', 0) and data_dict.get('lon', 0):
                port.write({
                    'geo_codes_updated_from_api': True,
                    'latitude': data_dict.get('lat', 0),
                    'longitude': data_dict.get('lon', 0)
                })
            return data_dict

        else:

            url = api_rec.url

            querystring = {"format": "json", "street": port.name, "accept-language": "en", "polygon_threshold": "0.0"}

            headers = {
                "X-RapidAPI-Key": api_rec.key,
                "X-RapidAPI-Host": api_rec.host
            }

            geo_loc_response = requests.request("GET", url, headers=headers, params=querystring)

            response_content = json.loads(geo_loc_response.content)
            if response_content and geo_loc_response.status_code == 200:
                data_dict = response_content[0]
                data_dict.update({'status_code': geo_loc_response.status_code})
                if data_dict.get('lat', 0) and data_dict.get('lon', 0):
                    port.write({
                        'geo_codes_updated_from_api': True,
                        'latitude': data_dict.get('lat', 0),
                        'longitude': data_dict.get('lon', 0)
                    })
                return data_dict

            else:

                api_rec = self.env['api.integration'].search([('name', '=', 'get_unloc_code_details')])[-1]
                if not api_rec:
                    raise Warning("API record doesn't exist for 'get_unloc_code_details' process.")

                url = api_rec.url

                querystring = {"unlocode": port.unloc_code}

                headers = {
                    "X-RapidAPI-Key": api_rec.key,
                    "X-RapidAPI-Host": api_rec.host
                }

                response = requests.request("GET", url, headers=headers, params=querystring)
                if response.status_code == 200:
                    data_dict = json.loads(response.content)
                    data_dict.update({'status_code': response.status_code})
                    if data_dict.get('lat', 0) and data_dict.get('lon', 0):
                        port.write({
                            'geo_codes_updated_from_api': True,
                            'latitude': data_dict.get('lat', 0),
                            'longitude': data_dict.get('lon', 0)
                        })
                    return data_dict
                else:
                    return {'status_code': geo_loc_response.status_code}

    def get_container_track_details(self, cont_id):
        transport_rec = self.search([('cont_id', '=', cont_id)], order="id desc", limit=1)
        response = {'container_id': cont_id,
                    'route': [],
                    'map_markers_list': []}
        if transport_rec:
            if transport_rec.waypoint_coordinates:
                route_list = eval(transport_rec.waypoint_coordinates)
                map_markers_list = []
                previouse_transport_mode = ''
                for route in route_list:
                    added_in_list = False
                    key = list(route.keys())[0]
                    if previouse_transport_mode != key:
                        map_markers_list.append(route.get(key, [{}])[0])
                        previouse_transport_mode = key
                        added_in_list = True
                    if route == route_list[-1] and not added_in_list:
                        map_markers_list.append(route.get(key, [{}])[-1])
                response.update({'route': route_list, 'map_markers_list': map_markers_list})
        return response


class ContainerJourney(models.Model):
    _inherit = 'container.journey'
    _description = "Container Journey"
    # _order = 'id asc'

    # @api.onchange('start_point', 'end_point')
    # def _onchange_end_point(self):
    #     if self.end_point:
    #         fpod_vals.update({'end_point': self.end_point})
    #         # fpod = self.fpod_id.unloc_code + ' ' + self.fpod_id.name
    #         # self.end_point = fpod
    #     # if self.port_of_origin_id:
    #     #     port_of_origin = self.port_of_origin_id.unloc_code + ' ' + self.port_of_origin_id.name
    #     #     self.port_of_origin = port_of_origin

    # def _get_default_start_point(self):
    #     print("self", self)
    #     parent_id = self.env.context.get('parent_id')
    #     print("parent_id:", parent_id)
    #     transport_rec = self.env['transport'].browse(parent_id)
    #     print("transsss", transport_rec)
    #     if transport_rec:
    #         container_journey = transport_rec.container_route_line.ids
    #         print("connnnnn", container_journey)
    #         print("last", container_journey[-1])
    #         latest_journey = self.browse(container_journey[-1])
    #         print("latest_journey:", latest_journey.end_point)
    #         # self.start_point = latest_journey.end_point
    #         # print("self.start_point ", self.start_point )
    #     return latest_journey.end_point


    # transport_id = fields.Many2one('transport', string='Transport')
    # transport_template_id = fields.Many2one('transport.template', string='Transport Template')
    # end_point = fields.Char(string='End Point')
    # start_point = fields.Many2one('port', string='Start Point')
    # end_point = fields.Many2one('port', string='End Point')
    # transport_mode = fields.Many2one('mode', string='Mode of Transport')
    # estimated_departure_time = fields.Datetime("ETD")
    # estimated_arrival_time = fields.Datetime("ETA")
    # planned_departure_time = fields.Datetime("PTD")
    # planned_arrival_time = fields.Datetime("PTA")
    # actual_departure_time = fields.Datetime("ATD")
    # actual_arrival_time = fields.Datetime("ATA")
    # delay_reason = fields.Char('Reason for Delay')
    # change_remark = fields.Text('Change Remark')
    # Temporary fields to show in template
    # distance = fields.Char("Distance (KM)")
    # speed = fields.Char("Speed", default=30)
    # fuel = fields.Selection([('motor_gasoline', 'Motor Gasoline / Patrol'),
    #                          ('diesel_oil', 'Diesel Oil'),
    #                          ('gas_oil', 'Gas Oil'),
    #                          ('lpg', 'Liquefied Petroleum Gas (LPG)'),
    #                          ('cng', 'Compressed Natural Gas (CNG)'),
    #                          ('jet_kerosene', 'Jet Kerosene'),
    #                          ('residual_fuel_oil', 'Residual Fuel Oil'),
    #                          ('biogasoline', 'Biogasoline'),
    #                          ('biodiesel', 'Biodiesel')],
    #                         string="Fuel Type",
    #                         default='motor_gasoline',
    #                         required=True)
    # fuel_consumption = fields.Float('Fuel Consumption')
    # co2_emmision = fields.Float("CO2 Emmision", store=True, readonly=True, compute='_calculate_co2_emmision')
    # transport_mode = fields.Many2one('mode', string='Mode of Transport')
    # gate_in_wait_time = fields.Float("Gate In Waiting Time (hr)", default=24)
    # gate_out_wait_time = fields.Float("Gate Out Waiting Time (hr)", default=24)
    # travel_time = fields.Float("Time in hr")
    # buffer_time = fields.Float("Buffer Time (hr)")
    # yard_time = fields.Float("Yard Time (hr)")
    # ptd_updated = fields.Boolean("PTD Updated", default=False)
    # pta_updated = fields.Boolean("PTA Updated", default=False)
    # etd_updated = fields.Boolean("ETD Updated", default=False)
    # eta_updated = fields.Boolean("ETA Updated", default=False)
    # route_coordinates = fields.Text('Route Coordinates')

    def get_route_coordinates(self):
        for record in self:
            por_geo_data = self.get_geo_location_from_city(record.start_point)
            pod_geo_data = self.get_geo_location_from_city(record.end_point)
            startpoint_unloc = record.start_point.unloc_code
            endpoint_unloc = record.end_point.unloc_code
            startpoint_name = record.start_point.name
            endpoint_name = record.end_point.name
            startpoint_lon = por_geo_data.get('lon', record.start_point.longitude)
            startpoint_lat = por_geo_data.get('lat', record.start_point.latitude)
            endpoint_lon = pod_geo_data.get('lon', record.end_point.longitude)
            endpoint_lat = pod_geo_data.get('lat', record.end_point.latitude)
            if record.transport_mode.name.strip().lower() in ['mainline', 'main line', 'feeder']:
                response = False
                api_rec = self.env['api.integration'].search([('name', '=', 'get_routes_by_loccode')])[-1]
                if not api_rec:
                    raise Warning("API record doesn't exist for 'get_routes_by_loccode' process.")
                if startpoint_unloc and endpoint_unloc:
                    url = '%s/%s/%s/0/0/0/0' % (api_rec.url, startpoint_unloc, endpoint_unloc)
                    response = requests.get(url)
                else:
                    if startpoint_lon and startpoint_lat and endpoint_lon and endpoint_lat:
                        api_rec = self.env['api.integration'].search([('name', '=', 'get_routes_by_geocode')])[-1]
                        if not api_rec:
                            raise Warning("API record doesn't exist for 'get_routes_by_geocode' process.")
                        url = '%s/%s/%s/%s/%s/0/0/0/0' % (
                        api_rec.url, startpoint_lon, startpoint_lat, endpoint_lon, endpoint_lat)
                        response = requests.get(url)
                if response.status_code != 200 and startpoint_lon and startpoint_lat and endpoint_lon and endpoint_lat:
                    if startpoint_lon and startpoint_lat and endpoint_lon and endpoint_lat:
                        api_rec = self.env['api.integration'].search([('name', '=', 'get_routes_by_geocode')])[-1]
                        if not api_rec:
                            raise Warning("API record doesn't exist for 'get_routes_by_geocode' process.")
                    url = '%s/%s/%s/%s/%s/0/0/0/0' % (
                    api_rec.url, startpoint_lon, startpoint_lat, endpoint_lon, endpoint_lat)
                    response = requests.get(url)
                route_data = {}
                try:
                    if response and response.status_code == 200:
                        route_data = json.loads(response.content)
                    else:
                        route_data.update({'route': [
                            {
                                'lon': por_geo_data.get('lon', False) if por_geo_data.get('status_code',
                                                                                          0) == 200 else False,
                                'lat': por_geo_data.get('lat', False) if por_geo_data.get('status_code',
                                                                                          0) == 200 else False
                            },
                            {
                                'lon': pod_geo_data.get('lon', False) if pod_geo_data.get('status_code',
                                                                                          0) == 200 else False,
                                'lat': pod_geo_data.get('lat', False) if pod_geo_data.get('status_code',
                                                                                          0) == 200 else False
                            }
                        ]
                        })
                except:
                    route_data.update({'route': [
                        {
                            'lon': por_geo_data.get('lon', False) if por_geo_data.get('status_code',
                                                                                      0) == 200 else False,
                            'lat': por_geo_data.get('lat', False) if por_geo_data.get('status_code',
                                                                                      0) == 200 else False
                        },
                        {
                            'lon': pod_geo_data.get('lon', False) if pod_geo_data.get('status_code',
                                                                                      0) == 200 else False,
                            'lat': pod_geo_data.get('lat', False) if pod_geo_data.get('status_code',
                                                                                      0) == 200 else False
                        }
                    ]
                    })
                # prepared_route = ""
                # for route_point in route_data.get('route', []):
                #     if prepared_route:
                #         prepared_route = "%s/%s,%s" % (prepared_route, route_point.get('lon'), route_point.get('lat'))
                #     else:
                #         prepared_route = "%s,%s" % (route_point.get('lon'), route_point.get('lat'))
                record.route_coordinates = route_data.get('route', [])
            if record.transport_mode.name.strip().lower() == 'road':
                api_rec = self.env['api.integration'].search([('name', '=', 'get_road_routes')])[-1]
                if not api_rec:
                    ValidationError("API Record does not exist for 'get_road_routes'.")
                url = '%s/%s/%s/%s/%s/%s/%s' % (api_rec.url, startpoint_name, endpoint_name, startpoint_lon, startpoint_lat, endpoint_lon, endpoint_lat)
                response = requests.get(url)
                print('eq_response :%s ' % response.content)
                route_data = {}
                if response and response.status_code == 200:
                    route_data = json.loads(response.content)
                # prepared_route = ""
                # for route_point in route_data.get('route', []):
                #     if prepared_route:
                #         prepared_route = "%s/%s,%s" % (prepared_route, route_point.get('lon'), route_point.get('lat'))
                #     else:
                #         prepared_route = "%s,%s" % (route_point.get('lon'), route_point.get('lat'))
                record.route_coordinates = route_data.get('route', [])

    def get_geo_location_from_city(self, port_rec):
        if port_rec.geo_codes_updated_from_api and port_rec.latitude and port_rec.longitude:
            return {
                'status_code': 200,
                'lat': port_rec.latitude,
                'lon': port_rec.longitude
            }
        api_rec = self.env['api.integration'].search([('name', '=', 'forward_reverse_geo_coding')])[-1]
        if not api_rec:
            raise Warning("API record doesn't exist for 'forward_reverse_geo_coding' process.")
        url = "%s/forward" % api_rec.url
        querystring = {"format": "json", "city": port_rec.name, "accept-language": "en", "polygon_threshold": "0.0"}
        if port_rec.country_id:
            querystring.update({'country': port_rec.country_id.name})
        headers = {
            "X-RapidAPI-Key": "bf6da40350msh8328c98e9927978p17e8b8jsn1a66b4c0ed12",
            "X-RapidAPI-Host": "forward-reverse-geocoding.p.rapidapi.com"
        }

        geo_loc_response = requests.request("GET", url, headers=headers, params=querystring)

        response_content = json.loads(geo_loc_response.content)
        if response_content and geo_loc_response.status_code == 200:
            data_dict = response_content[0]
            data_dict.update({'status_code': geo_loc_response.status_code})
            if data_dict.get('lat', 0) and data_dict.get('lon', 0):
                port_rec.write({
                    'geo_codes_updated_from_api': True,
                    'latitude': data_dict.get('lat', 0),
                    'longitude': data_dict.get('lon', 0)
                })
            return data_dict

        else:
            api_rec = self.env['api.integration'].search([('name', '=', 'forward_reverse_geo_coding')])[-1]
            if not api_rec:
                raise Warning("API record doesn't exist for 'forward_reverse_geo_coding' process.")
            url = "%s/forward" % api_rec.url

            querystring = {"format": "json", "street": port_rec.name, "accept-language": "en", "polygon_threshold": "0.0"}

            headers = {
                "X-RapidAPI-Key": "bf6da40350msh8328c98e9927978p17e8b8jsn1a66b4c0ed12",
                "X-RapidAPI-Host": "forward-reverse-geocoding.p.rapidapi.com"
            }

            geo_loc_response = requests.request("GET", url, headers=headers, params=querystring)

            response_content = json.loads(geo_loc_response.content)
            if response_content and geo_loc_response.status_code == 200:
                data_dict = response_content[0]
                data_dict.update({'status_code': geo_loc_response.status_code})
                if data_dict.get('lat', 0) and data_dict.get('lon', 0):
                    port_rec.write({
                        'geo_codes_updated_from_api': True,
                        'latitude': data_dict.get('lat', 0),
                        'longitude': data_dict.get('lon', 0)
                    })
                return data_dict

            else:
                return {'status_code': geo_loc_response.status_code}

    @api.depends('fuel','fuel_consumption')
    def _calculate_co2_emmision(self):
        for record in self:
            if record.fuel == 'motor_gasoline':
                record.co2_emmision = record.fuel_consumption * 2.8 if record.fuel_consumption else 0
            if record.fuel in ['diesel_oil', 'gas_oil']:
                record.co2_emmision = record.fuel_consumption * 2.9 if record.fuel_consumption else 0
            if record.fuel in ['lpg', 'biodiesel']:
                record.co2_emmision = record.fuel_consumption * 1.9 if record.fuel_consumption else 0
            if record.fuel == 'cng':
                record.co2_emmision = record.fuel_consumption * 3.3 if record.fuel_consumption else 0
            if record.fuel in ['jet_kerosene', 'residual_fuel_oil']:
                record.co2_emmision = record.fuel_consumption * 3.5 if record.fuel_consumption else 0
                if record.fuel == 'biogasoline':
                    record.co2_emmision = record.fuel_consumption * 1.8 if record.fuel_consumption else 0


    @api.onchange('planned_departure_time', 'planned_arrival_time', 'gate_in_wait_time', 'gate_out_wait_time',
                  'travel_time', 'buffer_time', 'yard_time')
    def onchange_planned_dates(self):
        planned_scheduled_date_updated = False
        for record in self:
            db_current_rec = self.search([('id', '=', record._origin.id)])
            first_line = True
            for cj in record.transport_id.container_route_line.filtered(lambda line: line._origin.id >= record._origin.id):
                planned_scheduled_date_updated = True
                if first_line:
                    pta_updated = False
                    gate_out_wait_time = cj.gate_out_wait_time or 0
                    gate_in_wait_time = cj.gate_in_wait_time or 0
                    travel_time = cj.travel_time or 0
                    buffer_time = cj.buffer_time or 0
                    yard_time = cj.yard_time or 0
                    if cj.planned_departure_time != db_current_rec.planned_departure_time:
                        ptd = cj.planned_departure_time
                        pta = ptd
                        if gate_out_wait_time :
                            pta += timedelta(hours=gate_out_wait_time)
                        if gate_in_wait_time:
                            pta +=timedelta(hours=gate_in_wait_time)
                        if travel_time:
                            pta += timedelta(hours=travel_time)
                        if gate_out_wait_time:
                            pta +=timedelta(hours=buffer_time)
                    else:
                        if cj.planned_arrival_time != db_current_rec.planned_arrival_time:
                            ptd = db_current_rec.planned_departure_time
                            pta = cj.planned_arrival_time

                        else:
                            ptd = db_current_rec.planned_departure_time
                            pta = ptd
                            if pta and gate_out_wait_time:
                                pta += timedelta(hours=gate_out_wait_time)
                            if pta and gate_in_wait_time:
                                pta += timedelta(hours=gate_in_wait_time)
                            if pta and travel_time:
                                pta += timedelta(hours=travel_time)
                            if pta and buffer_time:
                                pta += timedelta(hours=buffer_time)

                    first_line = False

                else:
                    gate_out_wait_time = cj.gate_out_wait_time or 0
                    gate_in_wait_time = cj.gate_in_wait_time or 0
                    travel_time = cj.travel_time or 0
                    buffer_time = cj.buffer_time or 0
                    yard_time = cj.yard_time or 0
                    ptd = pta
                    if yard_time:
                        ptd += timedelta(hours=yard_time)
                    pta = ptd
                    if pta and gate_out_wait_time:
                        pta += timedelta(hours=gate_out_wait_time)
                    if pta and gate_in_wait_time:
                        pta += timedelta(hours=gate_in_wait_time)
                    if pta and travel_time:
                        pta += timedelta(hours=travel_time)
                    if pta and buffer_time:
                        pta += timedelta(hours=buffer_time)

                cj_vals = {
                        'planned_departure_time': ptd,
                        'planned_arrival_time': pta,
                        'gate_in_wait_time': cj.gate_in_wait_time,
                        'gate_out_wait_time': cj.gate_out_wait_time,
                        'travel_time': cj.travel_time,
                        'buffer_time': cj.buffer_time,
                        'yard_time': cj.yard_time,
                    }
                container_journey = self.browse(cj._origin.id)
                container_journey.write(cj_vals)
        # self._origin.transport_id.planned_scheduled_date_updated = planned_scheduled_date_updated
        # self._origin.transport_id.with_context(planned_scheduled_date_updated=True).action_update_route_dates()
        # return {
        #     'name': _('Transport'),
        #     'view_mode': 'form',
        #     'res_model': 'transport',
        #     'res_id': self._origin.transport_id.id,
        #     'view_id': self.env.ref('freightbox.transport_form_view').id,
        #     'type': 'ir.actions.act_window',
        # }

    @api.onchange('gate_in_wait_time', 'gate_out_wait_time', 'travel_time', 'buffer_time', 'yard_time',
                  'estimated_departure_time', 'estimated_arrival_time')
    def onchange_scheduled_dates(self):
        planned_scheduled_date_updated = False
        for record in self:
            db_current_rec = self.search([('id', '=', record._origin.id)])
            first_line = True
            for cj in record.transport_id.container_route_line.filtered(lambda line: line._origin.id >= record._origin.id):
                planned_scheduled_date_updated = True
                if first_line:
                    gate_out_wait_time = cj.gate_out_wait_time or 0
                    gate_in_wait_time = cj.gate_in_wait_time or 0
                    travel_time = cj.travel_time or 0
                    buffer_time = cj.buffer_time or 0
                    yard_time = cj.yard_time or 0

                    eta = False
                    etd = False
                    if cj.estimated_departure_time or cj.estimated_departure_time:
                        if cj.estimated_departure_time != db_current_rec.estimated_departure_time:
                            etd = cj.estimated_departure_time
                            eta = etd
                            if gate_out_wait_time:
                                eta += timedelta(hours=gate_out_wait_time)
                            if gate_in_wait_time:
                                eta += timedelta(hours=gate_in_wait_time)
                            if travel_time:
                                eta += timedelta(hours=travel_time)
                            if buffer_time:
                                eta += timedelta(hours=buffer_time)
                        else:
                            if cj.estimated_arrival_time != db_current_rec.estimated_arrival_time:
                                etd = db_current_rec.estimated_departure_time
                                eta = cj.estimated_arrival_time

                            else:
                                etd = db_current_rec.estimated_departure_time
                                eta = etd
                                if gate_out_wait_time:
                                    eta += timedelta(hours=gate_out_wait_time)
                                if gate_in_wait_time:
                                    eta += timedelta(hours=gate_in_wait_time)
                                if travel_time:
                                    eta += timedelta(hours=travel_time)
                                if buffer_time:
                                    eta += timedelta(hours=buffer_time)
                    first_line = False

                else:
                    gate_out_wait_time = cj.gate_out_wait_time or 0
                    gate_in_wait_time = cj.gate_in_wait_time or 0
                    travel_time = cj.travel_time or 0
                    buffer_time = cj.buffer_time or 0
                    yard_time = cj.yard_time or 0

                    if eta or etd:
                        etd = eta
                        if yard_time:
                            etd += timedelta(hours=yard_time)
                        eta = etd
                        if gate_out_wait_time:
                            eta += timedelta(hours=gate_out_wait_time)
                        if gate_in_wait_time:
                            eta += timedelta(hours=gate_in_wait_time)
                        if travel_time:
                            eta += timedelta(hours=travel_time)
                        if buffer_time:
                            eta += timedelta(hours=buffer_time)
                cj_vals = {
                    'gate_in_wait_time': cj.gate_in_wait_time,
                    'gate_out_wait_time': cj.gate_out_wait_time,
                    'travel_time': cj.travel_time,
                    'buffer_time': cj.buffer_time,
                    'yard_time': cj.yard_time,
                }
                if eta:
                    cj_vals.update({
                        'estimated_arrival_time': eta
                    })
                if etd:
                    cj_vals.update({
                        'estimated_departure_time': etd
                    })
                container_journey = self.browse(cj._origin.id)
                container_journey.write(cj_vals)
        # self._origin.transport_id.planned_scheduled_date_updated = planned_scheduled_date_updated
        # self._origin.transport_id.with_context(planned_scheduled_date_updated=True).action_update_route_dates()
        # return {
        #     'name': _('Transport'),
        #     'view_mode': 'form',
        #     'res_model': 'transport',
        #     'res_id': self._origin.transport_id.id,
        #     'view_id': self.env.ref('freightbox.transport_form_view').id,
        #     'type': 'ir.actions.act_window',
        # }
        

    @api.onchange('start_point', 'end_point', 'transport_mode')
    def onchange_start_end_point(self):
        port_obj = self.env['port']
        distance_data = {}
        for record in self:
            if record.transport_mode.name and record.transport_mode.name.lower().strip() in ['road', 'mainline', 'main line', 'feeder'] and record.start_point and record.end_point:
                # Getting Distance - Time data from mother server
                transport_mode = 'road'
                if record.transport_mode.name.lower().strip() in ['mainline', 'feeder']:
                    transport_mode = 'sea'
                try:
                    start_point_name = record.start_point
                    end_point_name = record.end_point
                    if start_point_name and end_point_name:
                        if start_point_name.latitude and start_point_name.longitude and end_point_name.latitude and end_point_name.longitude:
                            start_point_country = start_point_name.country_id.name if start_point_name and start_point_name.country_id else False
                            end_point_country = end_point_name.country_id.name if end_point_name and end_point_name.country_id else False
                            api_rec = self.env['api.integration'].search([('name', '=', 'get_distance_time_from_geo_location')])[-1]
                            if not api_rec:
                                ValidationError("API Record does not exist for 'get_distance_time_from_geo_location'.")
                            url = "%s/%s/%s/(%s,%s)/(%s, %s)/%s/%s" % (
                                api_rec.url, start_point_name.name, end_point_name.name, start_point_name.latitude,
                                start_point_name.longitude, end_point_name.latitude, end_point_name.longitude, start_point_country, end_point_country)
                            response = requests.get(url)
                            if response.status_code != 200:
                                start_point_name_str = start_point_name and start_point_name.name or record.start_point.name
                                end_point_name_str = end_point_name and end_point_name.name or record.end_point.name
                                if '/' in start_point_name_str:
                                    start_point_name_str = start_point_name_str.replace('/', ' ')
                                if '/' in start_point_name_str:
                                    start_point_name_str = start_point_name_str.replace('/', ' ')
                                start_point_country = start_point_name.country_id.name if start_point_name and start_point_name.country_id else False
                                end_point_country = end_point_name.country_id.name if end_point_name and end_point_name.country_id else False
                                api_rec = self.env['api.integration'].search([('name', '=', 'get_distance_time')])[-1]
                                if not api_rec:
                                    ValidationError(
                                        "API Record does not exist for 'get_distance_time'.")
                                url = "%s/%s/%s/%s/%s/%s" % (
                                    api_rec.url, start_point_name_str, end_point_name_str, start_point_country, end_point_country, transport_mode)
                                response = requests.get(url)
                                if response.status_code != 200:
                                    start_point_name_str = start_point_name and start_point_name.name or record.start_point.name
                                    end_point_name_str = end_point_name and end_point_name.name or record.end_point.name
                                    if '/' in start_point_name_str:
                                        start_point_name_str = start_point_name_str.split('/')[-1]
                                    if '/' in end_point_name_str:
                                        end_point_name_str = end_point_name_str.split('/')[-1]
                                    start_point_country = start_point_name.country_id.name if start_point_name and start_point_name.country_id else False
                                    end_point_country = end_point_name.country_id.name if end_point_name and end_point_name.country_id else False
                                    api_rec = self.env['api.integration'].search([('name', '=', 'get_distance_time')])[-1]
                                    if not api_rec:
                                        ValidationError(
                                            "API Record does not exist for 'get_distance_time'.")
                                    url = "%s/%s/%s/%s/%s/%s" % (
                                        api_rec.url, start_point_name_str, end_point_name_str, start_point_country, end_point_country, transport_mode)
                                    response = requests.get(url)
                                if response.status_code == 200:
                                    distance_data = json.loads(response.content)
                                if start_point_name:
                                    start_point_name.latitude = distance_data.get('Datas', {}).get('start_point_lat',
                                                                                                   '')
                                    start_point_name.longitude = distance_data.get('Datas', {}).get('start_point_long',
                                                                                                    '')
                                else:
                                    start_point_name = port_obj.create({
                                        'name': distance_data.get('Datas', {}).get('start_point', record.start_point.name)
                                    })

                                if end_point_name:
                                    end_point_name.latitude = distance_data.get('Datas', {}).get('end_point_lat', '')
                                    end_point_name.longitude = distance_data.get('Datas', {}).get('end_point_long', '')
                            else:
                                distance_data = json.loads(response.content)
                        else:
                            start_point_country = start_point_name.country_id.name if start_point_name and start_point_name.country_id else False
                            end_point_country = end_point_name.country_id.name if end_point_name and end_point_name.country_id else False
                            start_point_name_str = start_point_name.name
                            end_point_name_str = end_point_name.name
                            api_rec = self.env['api.integration'].search([('name', '=', 'get_distance_time')])[-1]
                            if not api_rec:
                                ValidationError(
                                    "API Record does not exist for 'get_distance_time'.")
                            url = "%s/%s/%s/%s/%s/%s" % (
                                api_rec.url, start_point_name_str, end_point_name_str, start_point_country, end_point_country, transport_mode)
                            response = requests.get(url)
                            if response.status_code == 200:
                                distance_data = json.loads(response.content)
                        start_point_name.latitude = distance_data.get('Datas', {}).get('start_point_lat', '')
                        start_point_name.longitude = distance_data.get('Datas', {}).get('start_point_long', '')
                        end_point_name.latitude = distance_data.get('Datas', {}).get('end_point_lat', '')
                        end_point_name.longitude = distance_data.get('Datas', {}).get('end_point_long', '')
                    else:
                        start_point_name_str = start_point_name and start_point_name.name or record.start_point.name
                        end_point_name_str = end_point_name and end_point_name.name or record.end_point.name
                        if '/' in start_point_name_str:
                            start_point_name_str = start_point_name_str.replace('/', ' ')
                        if '/' in start_point_name_str:
                            start_point_name_str = start_point_name_str.replace('/', ' ')
                        start_point_country = start_point_name.country_id.name if start_point_name and start_point_name.country_id else False
                        end_point_country = end_point_name.country_id.name if end_point_name and end_point_name.country_id else False
                        api_rec = self.env['api.integration'].search([('name', '=', 'get_distance_time')])[-1]
                        if not api_rec:
                            ValidationError(
                                "API Record does not exist for 'get_distance_time'.")
                        url = "%s/%s/%s/%s/%s/%s" % (
                            api_rec.url, start_point_name_str, end_point_name_str, start_point_country, end_point_country, transport_mode)
                        response = requests.get(url)
                        if response.status_code != 200:
                            start_point_name_str = start_point_name and start_point_name.name or record.start_point.name
                            end_point_name_str = end_point_name and end_point_name.name or record.end_point.name
                            if '/' in start_point_name_str:
                                start_point_name_str = start_point_name_str.split('/')[-1]
                            if '/' in end_point_name_str:
                                end_point_name_str = end_point_name_str.split('/')[-1]
                            start_point_country = start_point_name.country_id.name if start_point_name and start_point_name.country_id else False
                            end_point_country = end_point_name.country_id.name if end_point_name and end_point_name.country_id else False
                            api_rec = self.env['api.integration'].search([('name', '=', 'get_distance_time')])[-1]
                            if not api_rec:
                                ValidationError(
                                    "API Record does not exist for 'get_distance_time'.")
                            url = "%s/%s/%s/%s/%s/%s" % (
                                api_rec.url, start_point_name_str, end_point_name_str, start_point_country, end_point_country, transport_mode)
                            response = requests.get(url)
                        if response.status_code == 200:
                            distance_data = json.loads(response.content)
                        if start_point_name:
                            start_point_name.latitude = distance_data.get('Datas', {}).get('start_point_lat', '')
                            start_point_name.longitude = distance_data.get('Datas', {}).get('start_point_long', '')

                        if end_point_name:
                            end_point_name.latitude = distance_data.get('Datas', {}).get('end_point_lat', '')
                            end_point_name.longitude = distance_data.get('Datas', {}).get('end_point_long', '')

                    record.distance = distance_data.get('Datas', {}).get('distance', 0.0)
                    record.gate_in_wait_time = distance_data.get('Datas', {}).get('gate_in_wait_time', 0.0)
                    record.gate_out_wait_time = distance_data.get('Datas', {}).get('gate_out_wait_time', 0.0)
                    record.travel_time = distance_data.get('Datas', {}).get('Datas', {}).get('travel_time', 0.0)
                    record.buffer_time = distance_data.get('Datas', {}).get('buffer_time', 0.0)
                    record.yard_time = distance_data.get('Datas', {}).get('yard_time', 0.0)
                except:
                    record.distance = 0.0
                    record.gate_in_wait_time = 0.0
                    record.gate_out_wait_time = 0.0
                    record.travel_time = 0.0
                    record.buffer_time = 0.0
                    record.yard_time = 0.0

    def get_port_from_locode(self, locode):
        try:
            api_rec = self.env['api.integration'].search([('name', '=', 'get_port_details_from_locode')])[-1]
            if not api_rec:
                ValidationError("API Record does not exist for 'get_port_details_from_locode'.")
            url = "%s/%s" % (api_rec.url, locode)
            response = requests.get(url)
            if response.status_code == 200:
                distance_data = json.loads(response.content).get('Datas', {})
                port_vals = {
                    'unloc_code': distance_data.get('locode', locode),
                    'name': distance_data.get('locode', ''),
                    'latitude': distance_data.get('latitude', ''),
                    'longitude': distance_data.get('longitude', ''),

                }
                return self.env['port'].create(port_vals)
        except:
            return False
        return False

    @api.onchange('planned_departure_time')
    def onchange_planned_departure_time(self):
        self.ptd_updated = True

    @api.onchange('planned_arrival_time')
    def onchange_planned_arrival_time(self):
        self.pta_updated = True

    @api.onchange('estimated_departure_time')
    def onchange_estimated_departure_time(self):
        self.etd_updated = True

    @api.onchange('estimated_arrival_time')
    def onchange_estimated_arrival_timeself(self):
        self.eta_updated = True

    @api.onchange('distance', 'speed')
    def onchange_distance_traveltime_speed(self):
        for record in self:
            if record.distance:
                if record.speed:
                    try:
                        record.travel_time = math.ceil(float(record.distance) / float(record.speed))
                    except:
                        record.travel_time = 0.0
                else:
                    record.travel_time = 0.0
            record.onchange_planned_dates()
            record.onchange_scheduled_dates()


# class EquipmentJourney(models.Model):
#         _inherit = 'equipment.journey'
#         _description = "Equipment Journey"
#         _order = 'id'

        # transport_id = fields.Many2one('transport', string='Transport')
        # track_trace_event_id = fields.Many2one('track.trace.event', string='Track Trace Event')
        # equip_event_id = fields.Char("Equipment Event ID", help="Unique identifier for the equipment event captured.")
        # event_created_datetime = fields.Datetime("Event Created DateTime",
        #                                          help="The date and time when the event entry was created.")
        # estimated_event_time = fields.Datetime("ETA", help="Estimated Time of Action")
        # event_classifier_code = fields.Text("Event Classifier Code",
        #                                     help="The code for the event classifier, e.g.,Actual.")
        # equip_event_type_code = fields.Text("Equipment Event Type Code",
        #                                     help="The code to identify an equipmentrelated event type")
        # equip_reference = fields.Text("Container ID",
        #                               help="Reference that uniquely identifies the equipment involved in the event.")
        # iso_equip_code = fields.Text("ISO Equipment Code",
        #                              help="Unique code for the different equipment size/type used for transporting commodities.")
        # empty_indicator_code = fields.Text("Empty Indicator Code",
        #                                    help="Code to denote whether the equipment is empty or laden.")
        # shipment_id = fields.Char("Shipment ID", help="Unique identifier for the shipment")
        # transport_call = fields.Text("Transport Call", help="Specifies the transport call involved in the event.")
        # event_location = fields.Text("Event Location", help="The location where the event takes place")
        # document_references = fields.Char("Document References",
        #                                   help="Field is used to describe where the documentReferenceValue-field is pointing to.")
        # references_type_code = fields.Text("References Type Code", help="e.g, BKG")
        # reference_values = fields.Text("Reference Values", help="e.g, ABC123123123")
        # seal_no = fields.Text("Seal NO.", help="Identifies a seal affixed to the container.")
        # seal_source = fields.Text("Seal Source", help="The source of the seal, namely who has affixed the seal.")
        # seal_type = fields.Text("Seal Type",
        #                         help="The type of seal.This attribute links to the Seal Type ID defined in the Seal Type reference data entity.")
        # event_type = fields.Text("Event Type", tracking=True)
        # event_description = fields.Text("Event Description", tracking=True)
        # locode = fields.Text("Locode", tracking=True)
        # location_name = fields.Text("Location Name", tracking=True)
        # country = fields.Text("Country", tracking=True)
        # timezone = fields.Text("Timezone", tracking=True)
        # latitude = fields.Text("Latitude", tracking=True)
        # longitude = fields.Text("Longitude", tracking=True)
        # transport_call_type = fields.Text("Transport Call Type", tracking=True)
