from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
import requests
import json
import pytz


class TrackTraceEvent(models.Model):
    _name = 'track.trace.event'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Track Trace Event"
    _rec_name = 'carrier_booking'
    _order = 'sequence, id'

    carrier_booking = fields.Char(string='Carrier Booking/ Transport Document Reference', tracking=True)
    equipment_event_line = fields.One2many('track.equipment.event', 'track_trace_event_id', string='Equipment Event',
                                           tracking=True)
    shipment_event_line = fields.One2many('track.shipment.event', 'track_trace_event_id', string='Shipment Event',
                                          tracking=True)
    transport_event_line = fields.One2many('track.transport.event', 'track_trace_event_id', string='Transport Event',
                                           tracking=True)
    transport_id = fields.Many2one('transport', string='Transport ID', tracking=True)
    # transport_document_reference = fields.Text(string='Transport Document Reference')
    is_standalone_tnt = fields.Boolean("Is Stand Alone TNT?", tracking=True)
    sequence = fields.Integer(string='Sequence')
    event_stage = fields.Selection([('pln', 'Plan'),
                                    ('est', 'Estimated'),
                                    ('act', 'Actual'),
                                    ('late', 'Late')],
                                   onchange='onchange_transport_event_code',
                                   string="Event Stage")
    is_delayed = fields.Boolean("Is Delayed?", tracking=True)
    under_detention = fields.Boolean("under detention?", tracking=True)
    under_demurrage = fields.Boolean("under demurrage?", tracking=True)
    at_origin = fields.Boolean("At Origin?", tracking=True)
    at_destination = fields.Boolean("At Destination?", tracking=True)
    in_transit = fields.Boolean("In Transit?", tracking=True)
    at_ts_port = fields.Boolean("At Transshipment Port?", tracking=True)
    gt_tracked = fields.Boolean("Gatehouse Tracked?", tracking=True)
    port_of_origin_id = fields.Many2one('port', string='Port of Origin*', tracking=True)
    fpod_id = fields.Many2one('port', string='FPOD*', help="Final Port of Destination", tracking=True)
    cont_id = fields.Char("Container ID", tracking=True)
    transport_document_reference = fields.Text("B/L Number", tracking=True)
    cont_type = fields.Many2one("container.type", string="Container type", tracking=True)
    party_name_id = fields.Many2one('res.partner', string="Consignee")
    partner_id = fields.Many2one('res.partner', string='Shipping Line', domain="[('supplier_rank', '>', 0)]")
    at_origin_time = fields.Datetime("At origin Datetime", tracking=True)
    at_dest_time = fields.Datetime("At Destination Datetime", tracking=True)
    waypoint_coordinates = fields.Text('Waypoint Coordinates')
    allow_import_waypoints = fields.Boolean("Allow import Waypoints", compute="get_allow_import_waypoint", store=True)
    standalone_user_id = fields.Many2one("res.users", "Standalone User", help="TnT Standalone User for TnT Standalone Events Only.")
    destination_eta = fields.Datetime("Destination ETA", help="Estimated Arrival Time at Destination Location.")
    bol_ref = fields.Char("BOL Reference", help="BOL Reference in case of standalone track trace event.")

    @api.depends('waypoint_coordinates')
    def get_allow_import_waypoint(self):
        transport_events_obj = self.env['track.transport.event']
        for record in self:
            record.allow_import_waypoints = False
            if record.waypoint_coordinates.strip() == "" if record.waypoint_coordinates else False:
                record.allow_import_waypoints = True
            elif not record.waypoint_coordinates:
                record.allow_import_waypoints = True
            else:
                transport_arrival_recs = transport_events_obj.search([
                    ('track_trace_event_id', '=', record.id),
                    ('transport_event_type_code', '=', 'ARRI')
                ], order='id')
                for transport_arr_rec in transport_arrival_recs:
                    if transport_arr_rec.route_waypoint.strip() == "" if transport_arr_rec.route_waypoint else False:
                        record.allow_import_waypoints = True
                        break
    def get_route_waypoints(self):
        transport_events_obj = self.env['track.transport.event']
        port_obj = self.env['port']
        transport_obj = self.env['transport']
        for record in self:
            if record.allow_import_waypoints:
                if record.transport_id and record.transport_id.waypoint_coordinates:
                    record.waypoint_coordinates = record.transport_id.waypoint_coordinates
                else:
                    transport_events = transport_events_obj.search([
                        ('track_trace_event_id', '=', record.id),
                    ], order="id")

                    origin_rec = False
                    combined_route = []
                    for transport_event in transport_events:
                        if transport_event.transport_event_type_code == "DEPA":
                            origin_rec = transport_event
                            continue
                        if origin_rec and transport_event.transport_event_type_code == "ARRI":
                            startpoint_unloc = origin_rec.un_location_code or origin_rec.locode or False
                            startpoint_name = origin_rec.location or origin_rec.location_name or False
                            endpoint_unloc = transport_event.un_location_code or transport_event.locode or False
                            endpoint_name = transport_event.location or transport_event.location_name or False
                            por_geo_data = {}
                            pod_geo_data = {}

                            if startpoint_name or startpoint_unloc:
                                origin_port_domain = []
                                if startpoint_unloc:
                                    origin_port_domain.append(('unloc_code', '=', startpoint_unloc))
                                if startpoint_name:
                                    origin_port_domain.append(('name', '=', startpoint_name))
                                origin_port = port_obj.search(origin_port_domain)
                                por_geo_data = origin_port and transport_obj.get_geo_location_from_port(
                                    origin_port) or {}

                            if endpoint_unloc or endpoint_name:
                                destination_port_domain = []
                                if endpoint_unloc:
                                    destination_port_domain.append(('unloc_code', '=', endpoint_unloc))
                                if endpoint_name:
                                    destination_port_domain.append(('name', '=', endpoint_name))
                                destination_port = port_obj.search(destination_port_domain)
                                pod_geo_data = destination_port and transport_obj.get_geo_location_from_port(
                                    destination_port) or {}

                            startpoint_lon = por_geo_data.get('lon', origin_rec.longitude)
                            startpoint_lat = por_geo_data.get('lat', origin_rec.latitude)
                            endpoint_lon = pod_geo_data.get('lon', transport_event.longitude)
                            endpoint_lat = pod_geo_data.get('lat', transport_event.latitude)
                            if transport_event.mode_of_transport_code.strip().lower() in ['mainline', 'main line',
                                                                                          'feeder']:
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
                                            raise Warning(
                                                "API record doesn't exist for 'get_routes_by_geocode' process.")
                                        url = '%s/%s/%s/%s/%s/0/0/0/0' % (
                                            api_rec.url, startpoint_lon, startpoint_lat, endpoint_lon, endpoint_lat)
                                        response = requests.get(url)
                                if response.status_code != 200 and startpoint_lon and startpoint_lat and endpoint_lon and endpoint_lat:
                                    if startpoint_lon and startpoint_lat and endpoint_lon and endpoint_lat:
                                        api_rec = self.env['api.integration'].search([('name', '=', 'get_routes_by_geocode')])[-1]
                                        if not api_rec:
                                            raise Warning(
                                                "API record doesn't exist for 'get_routes_by_geocode' process.")
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
                                #         prepared_route = "%s/%s,%s" % (
                                #             prepared_route, route_point.get('lon'), route_point.get('lat'))
                                #     else:
                                #         prepared_route = "%s,%s" % (route_point.get('lon'), route_point.get('lat'))
                                # if combined_route:
                                #     combined_route = "%s/%s" % (combined_route, prepared_route)
                                # else:
                                #     combined_route = prepared_route
                                if route_data.get('route', []):
                                    combined_route.append({'ship': route_data.get('route', [])})
                                transport_event.route_waypoint = route_data.get('route', [])
                            if transport_event.mode_of_transport_code.strip().lower() == 'road':
                                api_rec = self.env['api.integration'].search([('name', '=', 'get_road_routes')])[-1]
                                if not api_rec:
                                    ValidationError("API Record does not exist for 'get_road_routes'.")
                                url = '%s/%s/%s/%s/%s/%s/%s' % (
                                    api_rec.url, startpoint_name, endpoint_name, startpoint_lon, startpoint_lat,
                                    endpoint_lon,
                                    endpoint_lat)
                                response = requests.get(url)
                                print('eq_response :%s ' % response.content)
                                route_data = {}
                                if response and response.status_code == 200:
                                    route_data = json.loads(response.content)
                                # prepared_route = ""
                                # for route_point in route_data.get('route', []):
                                #     if prepared_route:
                                #         prepared_route = "%s/%s,%s" % (
                                #             prepared_route, route_point.get('lon'), route_point.get('lat'))
                                #     else:
                                #         prepared_route = "%s,%s" % (route_point.get('lon'), route_point.get('lat'))
                                # if combined_route:
                                #     combined_route = "%s/%s" % (combined_route, prepared_route)
                                # else:
                                #     combined_route = prepared_route
                                if route_data.get('route', []):
                                    combined_route.append({'road': route_data.get('route', [])})
                                transport_event.route_waypoint = route_data.get('route', [])

                    record.waypoint_coordinates = combined_route

        return True

    def get_route_waypoints_cron(self):
        records_to_process = self.search([('allow_import_waypoints', '=', True)])
        return records_to_process.get_route_waypoints()


    @api.onchange('transport_event_line', 'transport_event_line.event_classifier_code')
    def onchange_transport_event_code(self):
        for record in self:
            if any(rec.event_classifier_code == 'ACT' for rec in record.transport_event_line):
                record.event_stage = 'act'
                record.gt_tracked = True
            elif any(rec.event_classifier_code == 'EST' for rec in record.transport_event_line):
                record.event_stage = 'est'
            elif any(rec.event_classifier_code == 'PLN' for rec in record.transport_event_line):
                record.event_stage = 'pln'
            # elif any(rec.delay_reason != False for rec in record.transport_event_line):
            #     record.event_stage = 'late'
                
    @api.onchange('transport_event_line', 'transport_event_line.delay_reason')
    def onchange_transport_delay_reason(self):
        for record in self:
            if any(rec.delay_reason != False for rec in record.transport_event_line):
                record.is_delayed = True

    @api.onchange('transport_event_line', 'transport_event_line.location')
    def onchange_transport_location(self):
        for record in self:
            print("rrrrrrrrrrrrrrrrrrrrrrrrrrrrrr",record.fpod_id.name)
            for rec in record.transport_event_line:
                if rec.location == record.port_of_origin_id.name:
                    record.at_origin_time = rec.event_datetime
                    record.at_origin = True
                    print("tttttttttttttttttttttttttttttttttt",rec.event_datetime)
                elif rec.location == record.fpod_id.name:
                    record.at_dest_time = rec.event_datetime
                    record.at_destination = True
                    print("tttttttttttttttttttttttttttttttttt",rec.event_datetime)
                # elif rec.location == record.fpod_id.name:
                #     record.at_dest_time = rec.event_datetime
                #     print("tttttttttttttttttttttttttttttttttt",rec.event_datetime)
                
    # @api.onchange('transport_event_line', 'transport_event_line.event_classifier_code')
    # def onchange_transport_event_code(self):
    #     for record in self:
    #         if any(rec.event_classifier_code == 'ACT' for rec in record.transport_event_line):
    #             record.gt_tracked = True

    def _schedule_auto_vacuum_standalone_tnt(self):
        today = fields.Date.today()
        tnt_rec = self.search([('is_standalone_tnt', '=', True)])
        for rec in tnt_rec:
            diff_date = today - rec.create_date.date()
            if diff_date.days > 15:
                rec.sudo().unlink()

    @api.model
    def retrieve_dashboard(self):
        """ This function returns the values to populate the custom dashboard in
            the purchase order views.
        """
        self.check_access_rights('read')

        result = {
            'planned': 0,
            'estimated': 0,
            'actual': 0,
            'delayed': 0,
            'under_detention': 0,
            'under_demurrage': 0,
            'at_origin': 0,
            'at_destination': 0,
            'in_transit': 0,
            'at_ts_port': 0,
            'gt_tracked': 0
        }

        result['planned'] = self.search_count([('event_stage', '=', 'pln')])
        result['estimated'] = self.search_count([('event_stage', '=', 'est')])
        result['actual'] = self.search_count([('event_stage', '=', 'act')])
        result['delayed'] = self.search_count([('is_delayed', '=', True)])
        result['under_detention'] = self.search_count([('under_detention', '=', True)])
        result['under_demurrage'] = self.search_count([('under_demurrage', '=', True)])
        result['at_origin'] = self.search_count([('at_origin', '=', True)])
        result['at_destination'] = self.search_count([('at_destination', '=', True)])
        result['in_transit'] = self.search_count([('in_transit', '=', True)])
        result['at_ts_port'] = self.search_count([('at_ts_port', '=', True)])
        result['gt_tracked'] = self.search_count([('gt_tracked', '=', True)])

        return result
    
    def tnt_auto_mail_cron(self):
        super_user = self.env['res.users'].browse(2)
        tnt_rec = self.search([('transport_event_line.mail_sent', '=', False)])
        print("-------------- call tnt_rec ",tnt_rec)
        for record in tnt_rec:
            delay_reason = ""
            ext_detail = ""
            new_shippment = False
            for i in record.transport_event_line:

                if not i.mail_sent:
                    if i.delay_reason:
                        delay_reason += "<p> Mode of Transport - " + str(i.mode_of_transport_code) + "</p>"
                        delay_reason += "<p> Location - " + str(i.location) + "</p>"
                        delay_reason += "<p>" + str(i.delay_reason) + "</p>"
                    else:
                        new_shippment = True
                        ext_detail += "<p> Mode of Transport - " + str(i.mode_of_transport_code) + "</p>"
                        ext_detail += "<p> Location - " + str(i.location) + "</p>"


                    i.mail_sent = True

            if delay_reason:
                mail_dict = {
                    "subject": 'Shipment Delayed',
                    "email_from": super_user.partner_id.email_formatted,
                    # currently email_to is project manager later it will be changed to sales team.
                    "email_to": record.partner_id.email,
                    "author_id": super_user.partner_id.id,
                    "body_html": "<br>"+
                    "<span>Greetings  </span>" + str(record.partner_id.name) +
                    "<p> Kindly note this is a notification of Delay in Shipment, Please find the details below. </p>"+
                    "<p> Carrier Booking - "+ record.carrier_booking +"</P>"+
                    "<p> Container ID - "+ record.cont_id +"</P>"+
                    "<p> Delay Reason - </P>"+
                    delay_reason +
                    "<p>Do not hesitate to contact us if you have any questions.</p>"
                    "<p>With Warm Regards, </p>"+super_user.company_id.name+"<p></p>"+super_user.company_id.phone+"<p></p>"+super_user.company_id.website
                    }
                print("------------ call ----------- Delay ")
                if mail_dict:
                    mail_create = self.env['mail.mail'].create(mail_dict)
                    # mail_create.send()

            if new_shippment:
                mail_dict = {
                    "subject": 'Shipment On Time',
                    "email_from": super_user.partner_id.email_formatted,
                    # currently email_to is project manager later it will be changed to sales team.
                    "email_to": record.partner_id.email,
                    "author_id": super_user.partner_id.id,
                    "body_html": "<br>"+
                    "<span>Greetings </span>" + str(record.partner_id.name) +
                    "<p> This is to notify that your shipment is on time, Please find the details below. </p>"+
                    "<p> Carrier Booking - "+ record.carrier_booking +"</P>"+
                    "<p> Container ID - "+ record.cont_id +"</P>"+
                    ext_detail + 
                    "<p>Do not hesitate to contact us if you have any questions.</p>"
                    "<p>With Warm Regards, </p>"+super_user.company_id.name+"<p></p>"+super_user.company_id.phone+"<p></p>"+super_user.company_id.website
                    }
                print("------------ call ----------- new ")
                if mail_dict:
                    mail_create = self.env['mail.mail'].create(mail_dict)
                    # mail_create.send()

    def update_estination_eta(self, cont_id, destination_eta):
        try:
            return_message = "Method Call Successfull with Container ID : %s and Destination ETA : %s " % (
            cont_id, destination_eta)
            track_trace_event_rec = self.sudo().search([('cont_id', '=', cont_id)])
            try:
                eta_datetime = datetime.strptime(destination_eta.replace('T', ' '), "%Y-%m-%d %H:%M:%S")
            except:
                eta_datetime = datetime.strptime(destination_eta.replace('T', ' '), "%Y-%m-%d %H:%M")
            if self.env.user:
                user_timezone = pytz.timezone(self.env.user.tz)
                eta_datetime = user_timezone.localize(eta_datetime).astimezone(pytz.utc)
                eta_datetime = eta_datetime.replace(tzinfo=None)
            if track_trace_event_rec:
                res = track_trace_event_rec.sudo().write({'destination_eta' : eta_datetime})
                print(res)
        except:
            return_message = "Something went wrong, Please try again after a while with Container ID : %s and " \
                             "Destination ETA : %s " % (cont_id, destination_eta)

        return return_message

    def import_tnt_from_mother_server(self):
        for record in self:
            api_rec = self.env['api.integration'].search([('name', '=', 'track_trace_ref')])[-1]
            url = ""
            headers = {}

            if api_rec:
                url = str(api_rec.url) + str(record.carrier_booking)
                headers = {'Tnt-Access-Token': api_rec.token,
                           'username': api_rec.username,
                           'passwd': api_rec.password}

            eq_response = requests.get(url, headers=headers)

            tnt_event_created = False
            transport_obj = self.env['transport']
            container_data = []
            por_lat = 0
            por_lon = 0
            pod_lat = 0
            pod_lon = 0

            if eq_response.status_code == 200:
                equip = json.loads(eq_response.content)
                tnt_obj = self.env['track.trace.event']
                track_equipment_event = self.env['track.equipment.event']
                track_transport_event = self.env['track.transport.event']
                if 'Datas' in equip:
                    # track_trace_event_id = tnt_obj.sudo().search([('carrier_booking', '=', carrier_booking_ref)],
                    #                                             order='id desc', limit=1)
                    # if not track_trace_event_id:
                    #     track_trace_event_id = tnt_obj.sudo().create({'carrier_booking': carrier_booking_ref})
                    #     if track_trace_event_id:
                    #         tnt_event_created = True
                    for eq in equip['Datas'][0]['eq']:
                        import datetime
                        if len(eq['event_created_datetime']) > 20:
                            event_created_datetime = datetime.datetime.strptime(eq['event_created_datetime'],
                                                                                "%Y-%m-%d %H:%M:%S.%f")
                        else:
                            event_created_datetime = eq['event_created_datetime']
                        if len(eq['event_datetime']) > 20:
                            final_event_datetime = datetime.datetime.strptime(eq['event_datetime'],
                                                                              "%Y-%m-%d %H:%M:%S.%f")
                        else:
                            final_event_datetime = eq['event_datetime']
                        equip_event_domain = [
                            ('equip_reference', '=', eq['equip_reference']),
                            ('locode', '=', eq['locode']),
                            ('equip_event_type_code', '=', eq['equip_event_type_code'])
                        ]
                        track_equipment_event_id = track_equipment_event.sudo().search(equip_event_domain)
                        equip_events_vals = {
                            'track_trace_event_id': record.id,
                            'equip_event_type_code': eq['equip_event_type_code'],
                            'equip_event_id': eq['equip_event_id'],
                            'event_created_datetime': event_created_datetime,
                            'event_classifier_code': eq['event_classifier_code'] or 'ACT',
                            'event_datetime': final_event_datetime,
                            'transport_call': eq['transport_call'],
                            'equip_reference': eq['equip_reference'],
                            'iso_equip_code': eq['iso_equip_code'],
                            'empty_indicator_code': eq['empty_indicator_code'],
                            'event_type': eq['event_type'],
                            'event_description': eq['event_description'],
                            'locode': eq['locode'],
                            'location_name': eq['location_name'],
                            'country': eq['country'],
                            'timezone': eq['timezone'],
                            'latitude': eq['latitude'],
                            'longitude': eq['longitude'],
                            'event_location': eq['location_name'],
                        }
                        if track_equipment_event_id:
                            if record and record.cont_id == eq['equip_reference']:
                                track_equipment_event_id.sudo().write(equip_events_vals)
                        else:
                            if record and record.cont_id == eq.get('equip_reference', '0'):
                                track_equipment_event.sudo().create(equip_events_vals)
                    for transport in equip['Datas'][0]['transport']:
                        import datetime
                        if len(transport['event_created_datetime']) > 20:
                            event_created_datetime = datetime.datetime.strptime(transport['event_created_datetime'],
                                                                                "%Y-%m-%d %H:%M:%S.%f")
                        else:
                            event_created_datetime = transport['event_created_datetime']
                        if len(transport['event_datetime']) > 20:
                            final_event_datetime = datetime.datetime.strptime(transport['event_datetime'],
                                                                              "%Y-%m-%d %H:%M:%S.%f")
                        else:
                            final_event_datetime = transport['event_datetime']
                        transport_event_domain = [
                            ('container_id', '=', transport['container_id']),
                            ('transport_event_type_code', '=', transport['transport_event_type_code']),
                            ('locode', '=', transport['locode'])
                        ]
                        track_transport_event_id = track_transport_event.sudo().search(transport_event_domain)
                        transport_events_vals = {
                            'track_trace_event_id': record.id,
                            'transport_event_type_code': transport['transport_event_type_code'],
                            'transport_event_id': transport['transport_event_id'],
                            'event_created_datetime': event_created_datetime,
                            'event_classifier_code': transport['event_classifier_code'] or 'ACT',
                            'event_datetime': final_event_datetime,
                            'delay_reason': transport['delay_reason'],
                            'change_remark': transport['change_remark'],
                            'transport_call_id': transport['transport_call_id'],
                            'carrier_service_code': transport['carrier_service_code'],
                            'carrier_voyage_number': transport['carrier_voyage_number'],
                            'un_location_code': transport['un_location_code'],
                            'mode_of_transport_code': transport['mode_of_transport_code'],
                            'vessel_imo_number': transport['vessel_imo_number'],
                            'vessel_name': transport['vessel_name'],
                            'vessel_operator_carrier_code': transport['vessel_operator_carrier_code'],
                            'vessel_operator_carrier_code_list_provider': transport[
                                'vessel_operator_carrier_code_list_provider'],
                            'container_id': transport['container_id'],
                            'event_type': transport['event_type'],
                            'event_description': transport['event_description'],
                            'locode': transport['locode'],
                            'location_name': transport['location_name'],
                            'country': transport['country'],
                            'timezone': transport['timezone'],
                            'latitude': transport['latitude'],
                            'longitude': transport['longitude'],
                            'location': transport['location'],
                        }
                        if track_transport_event_id:
                            if record and record.cont_id == transport.get('container_id', '0'):
                                track_transport_event_id.sudo().write(transport_events_vals)
                        else:
                            if record and record.cont_id == transport.get('container_id', '0'):
                                track_transport_event.sudo().create(transport_events_vals)

    def get_event_track_details(self, rec_id):
        transport_rec = self.search([('id', '=', rec_id)])
        response = {'container_id': transport_rec.cont_id,
                    'route': [],
                    'por_lat': 0,
                    'por_lon': 0,
                    'pod_lat': 0,
                    'pod_lon': 0}
        if transport_rec:
            if transport_rec.waypoint_coordinates:
                route_list = eval(transport_rec.waypoint_coordinates)
                por_lat = 0
                por_lon = 0
                pod_lat = 0
                pod_lon = 0
                if len(route_list) > 0:
                    first_coordinate = route_list[0].get(list(route_list[0].keys())[0], [{}])[0]
                    por_lat = first_coordinate.get('lat', 0)
                    por_lon = first_coordinate.get('lon', 0)
                    last_coordinate = route_list[-1].get(list(route_list[-1].keys())[0], [{}])[-1]
                    pod_lat = last_coordinate.get('lat', 0)
                    pod_lon = last_coordinate.get('lon', 0)

                response.update({'route': route_list,
                                 'por_lat': por_lat,
                                 'por_lon': por_lon,
                                 'pod_lat': pod_lat,
                                 'pod_lon': pod_lon
                                 })

        return response


class TrackTransportEvent(models.Model):
    _name = 'track.transport.event'
    _description = "Transport Event"
    _order = 'event_datetime, sequence'

    # port_of_origin = fields.Char(string='Intermediate POL')
    # fpod = fields.Char(string='Intermediate POD')
    mail_sent = fields.Boolean(string="Mail Sent")
    event_created_datetime = fields.Datetime("Event Created DateTime",
                                             help="The date and time when the event entry was created")
    event_datetime = fields.Datetime("Event DateTime", required=True, help="The date and time when the event occurred or will occur.")

    # estimated_departure_time = fields.Datetime("ETD")
    # estimated_arrival_time = fields.Datetime("ETA")
    # planned_departure_time = fields.Datetime("PTD")
    # planned_arrival_time = fields.Datetime("PTA")
    # actual_departure_time = fields.Datetime("ATD")
    # actual_arrival_time = fields.Datetime("ATA")
    delay_reason = fields.Char('Reason for Delay', help="Code for the delay reason as provided by SMDG.")
    change_remark = fields.Text('Change Remark', help="Free text description of the reason for the change in schedule.")

    track_trace_event_id = fields.Many2one('track.trace.event', string='Track Trace Event')
    transport_event_id = fields.Char(string='Transport Event ID',
                                     help="Unique identifier for the transport event captured.")
    event_classifier_code = fields.Text("Event Classifier Code",
                                        help="Specifies the code for the classifier of the event, e.g. Actual.")
    transport_event_type_code = fields.Text("Transport Event Type Code",
                                            help="The code to identify the type of event that is related to transport")

    transport_id = fields.Char(string='Transport ID', help="The unique identifier for the transport.")
    transport_reference = fields.Text(string='Transport Reference',
                                      help="When the mode of transport is a vessel,the Transport Reference will be the vessel IMO number.")
    transport_name = fields.Text(string='Transport Name',
                                 help="The name of the transport instance, e.g. or a vessel, this is the vessel name.")
    mode_of_transport_code = fields.Text(string='Mode of Transport code',
                                         help="The code specifying the mode of transport.")
    load_transport_call_id = fields.Text(string='Load Transport Call ID',
                                         help="Identifies the departure transport call of the shipment.")
    discharge_transport_call_id = fields.Text(string='Discharge Transport Call ID',
                                              help="Identifies the arrival transport call of the shipment.")
    vessel_imo_number = fields.Text(string='Vessel IMO Number',
                                    help="The vessel carrying out the transport identified by its IMO number.")

    transport_call_id = fields.Char("Transport Call ID", help="The unique identifier for a transport call.")
    carrier_service_code = fields.Char("Carrier Service Code",
                                       help="The code of the service for which the schedule details are published")
    carrier_voyage_number = fields.Text("Carrier Voyage Number",
                                        help="The vessel operator-specific identifier of the Voyage.")
    un_location_code = fields.Char("UN Location Code",
                                   help="The UN Location code specifying where the place is located.")
    facility_code = fields.Char("Facility Code",
                                help="The code used for identifying the specific facility. This code does not include the UN Location Code.")
    facility_code_list_provider = fields.Char("Facility Code List Provider",
                                              help="The provider used for identifying the facility Code.")
    facility_type_code = fields.Text("Facility Type Code", help="The code to identify the specific type of facility.")
    other_facility = fields.Text("Other Facility",
                                 help="An alternative way to capture the facility when no standardized DCSA facility code can be found")
    # mode_of_transport = fields.Text("Mode of Transport")
    location = fields.Char("Location",
                           help="Location of the facility. Can often be omitted when it is just repeating the contents of the UNLocationCode field.")
    vessel_imo_number = fields.Char("Vessel IMO Number",
                                    help="The vessel carrying out the transport identified by its IMO number.")
    vessel_name = fields.Char("Vessel Name", help="e.g, King of seas")
    vessel_flag = fields.Char("Vessel Flag", help="e.g, DE")
    vessel_call_sign_number = fields.Char("Vessel Call sign Number", help="e.g,NCVV")
    vessel_operator_carrier_code = fields.Char("Vessel Operator carrier code", help="e.g,MAEU")
    vessel_operator_carrier_code_list_provider = fields.Char("Vessel Operator Carrier Code List Provider",
                                                             help="e.g, NMFTA")

    document_reference_line = fields.One2many('track.document.reference', 'transport_event_id',
                                              string='Document References')
    reference_line = fields.One2many('track.reference', 'transport_event_id', string='References')
    container_id = fields.Text("Container ID",
                               help="Reference that uniquely identifies the equipment involved in the event.")
    event_type = fields.Text("Event Type", tracking=True)
    event_description = fields.Text("Event Description", tracking=True)
    locode = fields.Text("Locode", tracking=True)
    location_name = fields.Text("Location Name", tracking=True)
    country = fields.Text("Country", tracking=True)
    timezone = fields.Text("Timezone", tracking=True)
    latitude = fields.Text("Latitude", tracking=True)
    longitude = fields.Text("Longitude", tracking=True)
    transport_call_type = fields.Text("Transport Call Type", tracking=True)
    sequence = fields.Integer(string='Sequence')
    type = fields.Selection([('est', 'Estimated'),
                             ('rl', 'Real')],
                            string="Type", default='est', required=True)
    transport_event_occured = fields.Boolean("Transport Event Occurred", default=False)
    distance = fields.Char("Distance (KM)")
    speed = fields.Char("Speed (KM/H)")
    fuel = fields.Selection([('motor_gasoline', 'Motor Gasoline / Patrol'),
                             ('diesel_oil', 'Diesel Oil'),
                             ('gas_oil', 'Gas Oil'),
                             ('lpg', 'Liquefied Petroleum Gas (LPG)'),
                             ('cng', 'Compressed Natural Gas (CNG)'),
                             ('jet_kerosene', 'Jet Kerosene'),
                             ('residual_fuel_oil', 'Residual Fuel Oil'),
                             ('biogasoline', 'Biogasoline'),
                             ('biodiesel', 'Biodiesel')],
                            string="Fuel Type",
                            default='motor_gasoline',
                            required=True)
    fuel_consumption = fields.Float('Fuel Consumption')
    co2_emmision = fields.Char("CO2 Emmision")
    route_waypoint = fields.Text("Route Waypoint")


class TrackDocumentReference(models.Model):
    _name = 'track.document.reference'
    _description = "Document References"

    transport_event_id = fields.Many2one('track.transport.event', string='Transport Event')
    document_reference_type = fields.Char("Document Reference Type", help="e.g,BKG")
    document_reference_value = fields.Char("Document Reference Value", help="e.g, ABC123123123")


class TrackReference(models.Model):
    _name = 'track.reference'
    _description = "References"

    transport_event_id = fields.Many2one('track.transport.event', string='Transport Event')
    reference_type = fields.Char("Reference Type", help="The reference type codes defined by DCSA.")
    reference_value = fields.Char("Reference Value", help="The actual value of the reference.")


class TrackEquipmentEvent(models.Model):
    _name = 'track.equipment.event'
    _description = "Equipment Event"
    _order = "event_datetime, id"

    track_trace_event_id = fields.Many2one('track.trace.event', string='Track Trace Event')
    equip_event_id = fields.Char("Equipment Event ID", help="Unique identifier for the equipment event captured.")
    event_created_datetime = fields.Datetime("Event Created DateTime",
                                             help="The date and time when the event entry was created.")
    event_datetime = fields.Datetime("Event DateTime", required=True, help="The date and time when the event occurred or will occur.")
    event_classifier_code = fields.Text("Event Classifier Code", help="The code for the event classifier, e.g.,Actual.")
    equip_event_type_code = fields.Text("Equipment Event Type Code",
                                        help="The code to identify an equipmentrelated event type")
    equip_reference = fields.Text("Container ID",
                                  help="Reference that uniquely identifies the equipment involved in the event.")
    iso_equip_code = fields.Text("ISO Equipment Code",
                                 help="Unique code for the different equipment size/type used for transporting commodities.")
    empty_indicator_code = fields.Text("Empty Indicator Code",
                                       help="Code to denote whether the equipment is empty or laden.")
    shipment_id = fields.Char("Shipment ID", help="Unique identifier for the shipment")
    transport_call = fields.Text("Transport Call", help="Specifies the transport call involved in the event.")
    event_location = fields.Text("Event Location", help="The location where the event takes place")
    document_references = fields.Char("Document References",
                                      help="Field is used to describe where the documentReferenceValue-field is pointing to.")
    references_type_code = fields.Text("References Type Code", help="e.g, BKG")
    reference_values = fields.Text("Reference Values", help="e.g, ABC123123123")
    seal_no = fields.Text("Seal NO.", help="Identifies a seal affixed to the container.")
    seal_source = fields.Text("Seal Source", help="The source of the seal, namely who has affixed the seal.")
    seal_type = fields.Text("Seal Type",
                            help="The type of seal.This attribute links to the Seal Type ID defined in the Seal Type reference data entity.")
    event_type = fields.Text("Event Type", tracking=True)
    event_description = fields.Text("Event Description", tracking=True)
    locode = fields.Text("Locode", tracking=True)
    location_name = fields.Text("Location Name", tracking=True)
    country = fields.Text("Country", tracking=True)
    timezone = fields.Text("Timezone", tracking=True)
    latitude = fields.Text("Latitude", tracking=True)
    longitude = fields.Text("Longitude", tracking=True)
    transport_call_type = fields.Text("Transport Call Type", tracking=True)
    equipment_event_occured = fields.Boolean("Equipment Event Occurred", default=False)


class TrackShipmentEvent(models.Model):
    _name = 'track.shipment.event'
    _description = "Shipment Event"

    track_trace_event_id = fields.Many2one('track.trace.event', string='Track Trace Event')
    shipment_event = fields.Char('Shipment Event', help="A unique identifier for the shipment event captured.")
    event_created = fields.Datetime('Event Created Date Time',
                                    help="The date and time when the event entry was created.")
    event_datetime = fields.Datetime('Event Date Time', required=True, help="The date and time when the event occurred or will occur.")
    event_classifier_code = fields.Text('Event Classifier Code',
                                        help="Code for the event classifier (PLN, ACT or EST).")
    shipment_event_type_code = fields.Text('Shipment Event Type Code',
                                           help="The code to identify the event that is related to the shipment.")
    document_type_code = fields.Text('Document Type code',
                                     help="The code to identify the type of information that is related to the shipment.")
    document_id = fields.Text('Document ID', help="The id of the object defined by the documentTypeCode")
    reason = fields.Text('Reason', help="This field can be used to explain why a specific event has been sent")
    booking_id = fields.Many2one('crm.lead',string="Booking")