from odoo import http, fields, _
from odoo.http import request
from odoo.exceptions import ValidationError
import requests
import json
import pytz


class TrackTraceController(http.Controller):

    @http.route('/track_trace', type='http', auth='public', website=True)
    def track_trace(self, **post):
        container_data = []
        logged_in_user = True
        if request.env.user.id == request.env.ref('base.public_user').id:
            logged_in_user = False
        transport_obj = request.env['transport']
        port_obj = request.env['port']
        por_lat = 0
        por_lon = 0
        pod_lat = 0
        pod_lon = 0
        track_trace_event_ids = request.env['track.trace.event'].sudo().search([('standalone_user_id','=',request.env.user.id)])
        print("-------------track_trace_event_ids",track_trace_event_ids)
        if track_trace_event_ids:
            track_trace_event_ids.import_tnt_from_mother_server()
            track_trace_event_ids.sudo().get_route_waypoints()
            done_cont_ids = []
            tnt_container_ids = []
            for tnt_event in track_trace_event_ids:
                if tnt_event.cont_id not in done_cont_ids:
                    done_cont_ids.append(tnt_event.cont_id)
                    if tnt_event.cont_id:
                        tnt_container_ids.append(
                            {tnt_event.cont_id: (tnt_event.carrier_booking, tnt_event.id)})
                    else:
                        tnt_container_ids.append(
                            {tnt_event.carrier_booking: (tnt_event.carrier_booking, tnt_event.id)})
                tnt_container_events = []
                if len(tnt_event.transport_event_line) > 0:
                    origin_port_unlocode = tnt_event.transport_event_line[0].un_location_code or \
                                           tnt_event.transport_event_line[0].locode or False
                    origin_port_name = tnt_event.transport_event_line[0].location or tnt_event.transport_event_line[
                        0].location_name or False
                    destination_port_unlocode = tnt_event.transport_event_line[-1].un_location_code or \
                                                tnt_event.transport_event_line[-1].locode or False
                    destination_port_name = tnt_event.transport_event_line[-1].location or \
                                            tnt_event.transport_event_line[-1].location_name or False

                    if origin_port_name or origin_port_unlocode:
                        origin_port_domain = []
                        if origin_port_unlocode:
                            origin_port_domain.append(('unloc_code', '=', origin_port_unlocode))
                        if origin_port_name:
                            origin_port_domain.append(('name', '=', origin_port_name))
                        origin_port = port_obj.sudo().search(origin_port_domain)
                        origin_geo_data = origin_port and transport_obj.sudo().get_geo_location_from_port(origin_port) or {}
                        por_lat = origin_geo_data.get('lat', 0)
                        por_lon = origin_geo_data.get('lon', 0)

                    if destination_port_unlocode or destination_port_name:
                        destination_port_domain = []
                        if destination_port_unlocode:
                            destination_port_domain.append(('unloc_code', '=', destination_port_unlocode))
                        if destination_port_name:
                            destination_port_domain.append(('name', '=', destination_port_name))
                        destination_port = port_obj.sudo().search(destination_port_domain)
                        destination_geo_data = destination_port and transport_obj.sudo().get_geo_location_from_port(
                            destination_port) or {}
                        pod_lat = destination_geo_data.get('lat', 0)
                        pod_lon = destination_geo_data.get('lon', 0)

                for transport_event in tnt_event.transport_event_line:
                    msg = ""
                    event_occurred = False
                    if transport_event.event_classifier_code == 'ACT':
                        if transport_event.transport_event_type_code == "DEPA":
                            msg = "Left"
                            if transport_event.location:
                                msg = "%s from %s" % (msg, transport_event.location)
                            if transport_event.mode_of_transport_code:
                                msg = "%s by %s " % (msg, transport_event.mode_of_transport_code)
                        if transport_event.transport_event_type_code == "ARRI":
                            msg = "Arrived"
                            if transport_event.location:
                                msg = "%s at %s" % (msg, transport_event.location)
                            if transport_event.mode_of_transport_code:
                                msg = "%s by %s " % (msg, transport_event.mode_of_transport_code)
                    else:
                        if transport_event.transport_event_type_code == "DEPA":
                            msg = "Will Leave"
                            if transport_event.location:
                                msg = "%s from %s" % (msg, transport_event.location)
                            if transport_event.mode_of_transport_code:
                                msg = "%s by %s " % (msg, transport_event.mode_of_transport_code)
                        if transport_event.transport_event_type_code == "ARRI":
                            msg = "Will arrive"
                            if transport_event.location:
                                msg = "%s at %s" % (msg, transport_event.location)
                            if transport_event.mode_of_transport_code:
                                msg = "%s by %s " % (msg, transport_event.mode_of_transport_code)
                    event_due_passed = False
                    reason_for_dealy = False
                    if not transport_event.transport_event_occured:
                        if transport_event.event_datetime and transport_event.event_datetime < fields.Datetime.now():
                            reason_for_dealy = True
                            if transport_event.delay_reason:
                                reason_for_dealy = transport_event.delay_reason

                    if transport_event.event_classifier_code == 'ACT':
                        event_occurred = True

                    if not msg and transport_event:
                        msg = transport_event.event_description

                    tnt_container_events.append(
                        (
                            transport_event.event_datetime,
                            transport_event.event_type,
                            transport_event.event_classifier_code,
                            transport_event.transport_event_type_code,
                            transport_event.mode_of_transport_code,
                            msg,
                            transport_event.distance,
                            transport_event.speed,
                            transport_event.co2_emmision
                        )
                    )
                for equipment_event in tnt_event.equipment_event_line:
                    msg = ""
                    event_occurred = False
                    reason_for_delay = False
                    if equipment_event.equip_event_type_code == "LOAD" and equipment_event.empty_indicator_code == "EMPTY":
                        if equipment_event.event_classifier_code == "ACT":
                            msg = " %s Container is %sED at %s" % (equipment_event.empty_indicator_code,
                                                                   equipment_event.equip_event_type_code,
                                                                   equipment_event.event_location)
                            event_occurred = True
                            reason_for_delay = False
                        else:
                            msg = "Preparing to %s the %s container at %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)

                    elif equipment_event.equip_event_type_code == "OTHR" and equipment_event.empty_indicator_code == "LADEN":
                        if equipment_event.event_classifier_code == "ACT":
                            msg = " %s of %s container at %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                            event_occurred = True
                        else:
                            msg = "Preparing to %s the %s container at %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                    elif equipment_event.equip_event_type_code == "GTOT" and equipment_event.empty_indicator_code == "LADEN":
                        if equipment_event.event_classifier_code == "ACT":
                            msg = " Gate Out of %s container at %s" % (
                                equipment_event.empty_indicator_code, equipment_event.event_location)
                            event_occurred = True
                        else:
                            msg = "Preparing to %s the %s container at %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                    elif equipment_event.equip_event_type_code == "GTIN" and equipment_event.empty_indicator_code == "EMPTY":
                        if equipment_event.event_classifier_code == "ACT":
                            msg = " Gate In of %s container at %s" % (
                                equipment_event.empty_indicator_code, equipment_event.event_location)
                            event_occurred = True
                        else:
                            msg = "Preparing to %s the %s container at %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                    elif equipment_event.equip_event_type_code == "STUF" and equipment_event.empty_indicator_code == "EMPTY":
                        if equipment_event.event_classifier_code == "ACT":
                            msg = "%sFED, %s Container at %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                            event_occurred = True
                        else:
                            msg = "Preparing to %sF, %s container at %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                    elif equipment_event.equip_event_type_code == "PICK" and equipment_event.empty_indicator_code == "LADEN":
                        if equipment_event.event_classifier_code == "ACT":
                            msg = "%s Container is %sED up from %s" % (
                                equipment_event.empty_indicator_code, equipment_event.equip_event_type_code,
                                equipment_event.event_location)
                            event_occurred = True
                        else:
                            msg = "Preparing to  %s UP,  %s container from %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                    elif equipment_event.equip_event_type_code == "PICK" and equipment_event.empty_indicator_code == "EMPTY":
                        if equipment_event.event_classifier_code == "ACT":
                            msg = "%s Container is %sED UP from %s" % (
                                equipment_event.empty_indicator_code, equipment_event.equip_event_type_code,
                                equipment_event.event_location)
                            event_occurred = True
                        else:
                            msg = "Preparing to %s UP, %s Container from %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                    elif equipment_event.equip_event_type_code == "LOAD" and equipment_event.empty_indicator_code == "LADEN":
                        if equipment_event.event_classifier_code == "ACT":
                            msg = "%s Container is %sED at %s" % (
                                equipment_event.empty_indicator_code, equipment_event.equip_event_type_code,
                                equipment_event.event_location)
                            event_occurred = True
                        else:
                            msg = "Preparing to %s, %s container at %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                    elif equipment_event.equip_event_type_code == "DROP" and equipment_event.empty_indicator_code == "LADEN":
                        if equipment_event.event_classifier_code == "ACT":
                            msg = "%s Container is %sPED OFF at %s" % (
                                equipment_event.empty_indicator_code, equipment_event.equip_event_type_code,
                                equipment_event.event_location)
                            event_occurred = True
                        else:
                            msg = "Preparing to %s OFF, %s container at %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                    elif equipment_event.equip_event_type_code == "DISC" and equipment_event.empty_indicator_code == "LADEN":
                        if equipment_event.event_classifier_code == "ACT":
                            msg = "%sHARGED, %s Container at %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                            event_occurred = True
                        else:
                            msg = "Preparing to %sHARGE, %s Container at %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                    elif equipment_event.equip_event_type_code == "STRIP" and equipment_event.empty_indicator_code == "LADEN":
                        if equipment_event.event_classifier_code == "ACT":
                            msg = "%s Container is %sPED at %s" % (
                                equipment_event.empty_indicator_code, equipment_event.equip_event_type_code,
                                equipment_event.event_location)
                            event_occurred = True
                        else:
                            msg = "Preparing to %s, %s Container at %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                            event_occurred = False
                            reason_for_delay = False
                    elif equipment_event.equip_event_type_code == "GTOT" and equipment_event.empty_indicator_code == "EMPTY":
                        if equipment_event.event_classifier_code == "ACT":
                            msg = "Gate Out of %s container at %s" % (
                                equipment_event.empty_indicator_code, equipment_event.event_location)
                            event_occurred = True
                        else:
                            msg = "Preparing to %s, %s Container at %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                            event_occurred = False
                            reason_for_delay = False

                    elif equipment_event.equip_event_type_code == "GTIN" and equipment_event.empty_indicator_code == "LADEN":
                        if equipment_event.event_classifier_code == "ACT":
                            msg = "%s Container Received, %s Container at %s" % (
                                equipment_event.empty_indicator_code, equipment_event.equip_reference,
                                equipment_event.event_location)
                            event_occurred = True
                        else:
                            msg = "About to receive %s Container with reference %s at %s" % (
                                equipment_event.empty_indicator_code, equipment_event.equip_reference,
                                equipment_event.event_location)
                            event_occurred = False
                            reason_for_delay = False

                    elif equipment_event.equip_event_type_code == "DISC" and equipment_event.empty_indicator_code == "LADEN":
                        if equipment_event.event_classifier_code == "ACT":
                            msg = "%sHARGED, %s Container at %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                            event_occurred = True
                        else:
                            msg = "Preparing to %sHARGE, %s Container at %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                            event_occurred = False
                            reason_for_delay = False

                    if not equipment_event.equipment_event_occured:
                        if equipment_event.event_datetime and equipment_event.event_datetime < fields.Datetime.now():
                            reason_for_delay = True

                    if not msg and equipment_event:
                        msg = equipment_event.event_description

                    tnt_container_events.append(
                        (
                            equipment_event.event_datetime,
                            equipment_event.event_type,
                            equipment_event.event_classifier_code,
                            equipment_event.equip_event_type_code,
                            equipment_event.empty_indicator_code,
                            msg
                        )
                    )
                current_eta = tnt_event.destination_eta
                if current_eta:
                    user_tz = pytz.timezone(request.env.user.tz)
                    destination_eta = current_eta.replace(tzinfo=pytz.utc)
                    destination_eta = destination_eta.replace(tzinfo=pytz.utc).astimezone(user_tz)
                    destination_eta = destination_eta.replace(tzinfo=None)
                else:
                    destination_eta = current_eta

                container_data.append((tnt_event.id, tnt_event.cont_id, destination_eta, tnt_container_events))

            # for container_id in container_ids:
            #     import datetime
            #     fb_trans = request.env['ir.sequence'].sudo().next_by_code('transport.seq') or _('New')
            #     client_id = request.env['ir.config_parameter'].sudo().sudo().get_param('database.uuid')
            #     fb_transport_id = fb_trans + '_' + client_id
            #     if container_id not in track_trace_event_ids.mapped('cont_id'):
            #         res = request.env['transport'].sudo().create_transport_request_motherserver(container_id,
            #                                                                                     fb_transport_id)
            #         if res and res.status_code == 200:
            #             new_tnt_event = tnt_obj.sudo().create({
            #                 'is_standalone_tnt': True,
            #                 'carrier_booking': carrier_booking_ref,
            #                 'cont_id': container_id,
            #                 'standalone_user_id': user.id
            #             })
            #             equip = json.loads(res.content)
            #             if cont_id:
            #                 body_msg = """
            #                                 Hello,

            #                                 A track n trace standalone request has been made to mother server for Container ID : %s and Carrier Booking ref. : %s.

            #                                 Kindly look into it.

            #                                 Regards.
            #                                 (System Generated Email From Freightbox Backend)
            #                                 """ % (cont_id, carrier_booking_ref)
            #             admin_user = request.env['res.users'].sudo().search([('id', '=', 2)])
            #             email = request.env['mail.mail'].sudo().create({
            #                 'author_id': admin_user.partner_id.id,
            #                 'email_from': admin_user.partner_id.email,
            #                 'body_html': body_msg,
            #                 'subject': "Track n Trace Standalone Request",
            #                 'email_to': 'bhargavi@powerpbox.org',
            #                 'auto_delete': False,
            #                 'state': 'outgoing'

            #             })
            #             email.sudo().send()
            #         if new_tnt_event.cont_id not in done_cont_ids:
            #             done_cont_ids.append(new_tnt_event.cont_id)
            #             if tnt_event.cont_id:
            #                 tnt_container_ids.append(
            #                     {tnt_event.cont_id: (carrier_booking_ref, tnt_event.id, transport_document_ref)})
            #             else:
            #                 tnt_container_ids.append(
            #                     {carrier_booking_ref: (carrier_booking_ref, tnt_event.id, transport_document_ref)})
            print("------------ container_data",container_data)
            
        r = request.render('freightbox.track_trace', {
            'container_list': 0,
            'container_ids': [],
            'container_data': container_data,
            'logged_in_user':logged_in_user,
            'show_on_load':True
        })
        return r

    @http.route('/track_gmap', type='http', auth='public', website=True)
    def track_gmap(self, **post):
        r = request.render('freightbox.track_gmap')
        return r

    def get_track_trace_events(self, carrier_booking_ref, container_ids, transport_document_ref):

        tnt_obj = request.env['track.trace.event']
        tnt_event_domain = []
        if carrier_booking_ref:
            tnt_event_domain.append(('carrier_booking', '=', carrier_booking_ref))
        if container_ids:
            tnt_event_domain.append(('cont_id', 'in', container_ids))
        if not carrier_booking_ref and transport_document_ref:
            bol_rec = request.env['bill.of.lading'].sudo().search([('transport_document_reference', '=', transport_document_ref)],
                                                        limit=1)
            booking_ref = bol_rec.job_id.carrier_booking
            tnt_event_domain.append(('carrier_booking', '=', booking_ref))
        track_trace_event_ids = tnt_obj.sudo().search(tnt_event_domain, order="id desc")

        if not track_trace_event_ids:

            tnt_event_domain = []
            if carrier_booking_ref:
                tnt_event_domain.append(('carrier_booking', '=', carrier_booking_ref))
            if container_ids:
                tnt_event_domain.append(('cont_id', 'in', container_ids))
            if transport_document_ref:
                tnt_event_domain.append(('bol_ref', '=', transport_document_ref))

            track_trace_event_ids = tnt_obj.sudo().search(tnt_event_domain, order="id desc")
        return track_trace_event_ids

    @http.route(['/standalone_list_of_containers/<string:carrier_booking_ref>/tdr/<string:transport_document_ref>/container/<string:cont_id>'],
                type='http', auth="public", website=True)
    def standalone_list_of_containers(self, carrier_booking_ref, transport_document_ref, cont_id, access_token=None,
                                       **kw):
        if carrier_booking_ref == 'null':
            carrier_booking_ref = False
        if transport_document_ref == 'null':
            transport_document_ref = False
        if cont_id == 'null':
            cont_id = False
        user = request.env.user
        logged_in_user = True
        if user.id == request.env.ref('base.public_user').id:
            logged_in_user = False
        transport_obj = request.env['transport']
        port_obj = request.env['port']
        container_ids = []
        if cont_id:
            container_ids = cont_id.split(',')
        container_data = []
        transport_obj = request.env['transport']
        por_lat = 0
        por_lon = 0
        pod_lat = 0
        pod_lon = 0
        # api_rec = request.env['api.integration'].sudo().search([('name', '=', 'track_trace_ref')])
        # url = ""
        # headers = {}
        # if api_rec:
        #     url = str(api_rec.url) + str(carrier_booking_ref)
        #     headers = {'Tnt-Access-Token': api_rec.token,
        #                'username': api_rec.username,
        #                'passwd': api_rec.password}
        #
        # eq_response = requests.get(url, headers=headers)
        # tnt_event_created = False
        # transport_obj = request.env['transport']
        # container_data = []
        # por_lat = 0
        # por_lon = 0
        # pod_lat = 0
        # pod_lon = 0
        #
        # if eq_response.status_code == 200:
        #     equip = json.loads(eq_response.content)
        #     tnt_obj = request.env['track.trace.event']
        #     track_equipment_event = request.env['track.equipment.event']
        #     track_transport_event = request.env['track.transport.event']
        #     if 'Datas' in equip:
        #         track_trace_event_id = tnt_obj.sudo().search([('carrier_booking', '=', carrier_booking_ref)],
        #                                                      order='id desc', limit=1)
        #         if not track_trace_event_id:
        #             track_trace_event_id = tnt_obj.sudo().create({'carrier_booking': carrier_booking_ref,
        #                                                           'standalone_user_id': user.id})
        #             if track_trace_event_id:
        #                 tnt_event_created = True
        #         for eq in equip['Datas'][0]['eq']:
        #             import datetime
        #             if len(eq['event_created_datetime']) > 20:
        #                 event_created_datetime = datetime.datetime.strptime(eq['event_created_datetime'],
        #                                                                     "%Y-%m-%d %H:%M:%S.%f")
        #             else:
        #                 event_created_datetime = eq['event_created_datetime']
        #             if len(eq['event_datetime']) > 20:
        #                 final_event_datetime = datetime.datetime.strptime(eq['event_datetime'],
        #                                                                   "%Y-%m-%d %H:%M:%S.%f")
        #             else:
        #                 final_event_datetime = eq['event_datetime']
        #             equip_event_domain = [
        #                 ('equip_reference', '=', eq['equip_reference']),
        #                 ('locode', '=', eq['locode']),
        #                 ('equip_event_type_code', '=', eq['equip_event_type_code'])
        #             ]
        #             track_equipment_event_id = track_equipment_event.sudo().search(equip_event_domain)
        #             equip_events_vals = {
        #                 'track_trace_event_id': track_trace_event_id.id,
        #                 'equip_event_type_code': eq['equip_event_type_code'],
        #                 'equip_event_id': eq['equip_event_id'],
        #                 'event_created_datetime': event_created_datetime,
        #                 'event_classifier_code': eq['event_classifier_code'] or 'ACT',
        #                 'event_datetime': final_event_datetime,
        #                 'transport_call': eq['transport_call'],
        #                 'equip_reference': eq['equip_reference'],
        #                 'iso_equip_code': eq['iso_equip_code'],
        #                 'empty_indicator_code': eq['empty_indicator_code'],
        #                 'event_type': eq['event_type'],
        #                 'event_description': eq['event_description'],
        #                 'locode': eq['locode'],
        #                 'location_name': eq['location_name'],
        #                 'country': eq['country'],
        #                 'timezone': eq['timezone'],
        #                 'latitude': eq['latitude'],
        #                 'longitude': eq['longitude'],
        #                 'event_location': eq['location_name'],
        #             }
        #             if track_equipment_event_id:
        #                 if track_trace_event_id and track_trace_event_id.cont_id == eq['equip_reference']:
        #                     track_equipment_event_id.sudo().write(equip_events_vals)
        #             else:
        #                 if track_trace_event_id and track_trace_event_id.cont_id == eq.get('equip_reference', '0'):
        #                     track_equipment_event.sudo().create(equip_events_vals)
        #         for transport in equip['Datas'][0]['transport']:
        #             import datetime
        #             if len(transport['event_created_datetime']) > 20:
        #                 event_created_datetime = datetime.datetime.strptime(transport['event_created_datetime'],
        #                                                                     "%Y-%m-%d %H:%M:%S.%f")
        #             else:
        #                 event_created_datetime = transport['event_created_datetime']
        #             if len(transport['event_datetime']) > 20:
        #                 final_event_datetime = datetime.datetime.strptime(transport['event_datetime'],
        #                                                                   "%Y-%m-%d %H:%M:%S.%f")
        #             else:
        #                 final_event_datetime = transport['event_datetime']
        #             transport_event_domain = [
        #                 ('container_id', '=', transport['container_id']),
        #                 ('transport_event_type_code', '=', transport['transport_event_type_code']),
        #                 ('locode', '=', transport['locode'])
        #             ]
        #             track_transport_event_id = track_transport_event.sudo().search(transport_event_domain)
        #             transport_events_vals = {
        #                 'track_trace_event_id': track_trace_event_id.id,
        #                 'transport_event_type_code': transport['transport_event_type_code'],
        #                 'transport_event_id': transport['transport_event_id'],
        #                 'event_created_datetime': event_created_datetime,
        #                 'event_classifier_code': transport['event_classifier_code'] or 'ACT',
        #                 'event_datetime': final_event_datetime,
        #                 'delay_reason': transport['delay_reason'],
        #                 'change_remark': transport['change_remark'],
        #                 'transport_call_id': transport['transport_call_id'],
        #                 'carrier_service_code': transport['carrier_service_code'],
        #                 'carrier_voyage_number': transport['carrier_voyage_number'],
        #                 'un_location_code': transport['un_location_code'],
        #                 'mode_of_transport_code': transport['mode_of_transport_code'],
        #                 'vessel_imo_number': transport['vessel_imo_number'],
        #                 'vessel_name': transport['vessel_name'],
        #                 'vessel_operator_carrier_code': transport['vessel_operator_carrier_code'],
        #                 'vessel_operator_carrier_code_list_provider': transport[
        #                     'vessel_operator_carrier_code_list_provider'],
        #                 'container_id': transport['container_id'],
        #                 'event_type': transport['event_type'],
        #                 'event_description': transport['event_description'],
        #                 'locode': transport['locode'],
        #                 'location_name': transport['location_name'],
        #                 'country': transport['country'],
        #                 'timezone': transport['timezone'],
        #                 'latitude': transport['latitude'],
        #                 'longitude': transport['longitude'],
        #                 'location': transport['location'],
        #             }
        #             if track_transport_event_id:
        #                 if track_trace_event_id and track_trace_event_id.cont_id == transport.get('container_id', '0'):
        #                     track_transport_event_id.sudo().write(transport_events_vals)
        #             else:
        #                 if track_trace_event_id and track_trace_event_id.cont_id == transport.get('container_id', '0'):
        #                     track_transport_event.sudo().create(transport_events_vals)

        # if not carrier_booking_ref:
        #     raise ValidationError("Provide Carrier Booking Reference / Transport Document Reference to proceed.")
        tnt_obj = request.env['track.trace.event']

        track_trace_event_ids = self.get_track_trace_events(carrier_booking_ref, container_ids, transport_document_ref)

        if not track_trace_event_ids:
            transport_domain = []
            if carrier_booking_ref:
                transport_domain.append(('carrier_booking', '=', carrier_booking_ref))
            if container_ids:
                transport_domain.append(('cont_id', 'in', container_ids))
            if not carrier_booking_ref and transport_document_ref:
                bol_rec = request.env['bill.of.lading'].sudo().search(
                    [('transport_document_reference', '=', transport_document_ref)],
                    limit=1)
                booking_ref = bol_rec.job_id.carrier_booking
                transport_domain.append(('carrier_booking', '=', booking_ref))
            transport = transport_obj.sudo().search(transport_domain, order="id desc")
            if transport:
                tnt_event_domain = [('transport_id', 'in', transport.ids)]
                if len(container_ids) > 0:
                    tnt_event_domain.append(('cont_id', 'in', container_ids))
                track_trace_event_ids = tnt_obj.sudo().search(tnt_event_domain, order="id desc")
            else:
                track_trace_event_ids = False
        if not track_trace_event_ids:
            import datetime
            fb_trans = request.env['ir.sequence'].sudo().next_by_code('transport.seq') or _('New')
            client_id = request.env['ir.config_parameter'].sudo().sudo().get_param('database.uuid')
            fb_transport_id = fb_trans + '_' + client_id
            done_cont_ids = []
            tnt_container_ids = []
            for container_id in container_ids:
                res = request.env['transport'].sudo().create_transport_request_motherserver(container_id,
                                                                                            fb_transport_id)
                if res and res.status_code == 200:
                    tnt_event = tnt_obj.sudo().create({
                        'is_standalone_tnt': True,
                        'carrier_booking': carrier_booking_ref or '',
                        'bol_ref': transport_document_ref or '',
                        'cont_id': container_id or '',
                        'standalone_user_id': user.id
                    })
                    if container_id not in done_cont_ids:
                        done_cont_ids.append(container_id)
                        tnt_container_ids.append({tnt_event.cont_id: tnt_event.id})
                    equip = json.loads(res.content)
                    if cont_id:
                        body_msg = """
                                        Hello,

                                        A track n trace standalone request has been made to mother server for Container ID : %s and Carrier Booking ref. : %s.

                                        Kindly look into it.

                                        Regards.
                                        (System Generated Email From Freightbox Backend)
                                        """ % (cont_id, carrier_booking_ref)
                    admin_user = request.env['res.users'].sudo().search([('id', '=', 2)])
                    email = request.env['mail.mail'].sudo().create({
                        'author_id': admin_user.partner_id.id,
                        'email_from': admin_user.partner_id.email,
                        'body_html': body_msg,
                        'subject': "Track n Trace Standalone Request",
                        'email_to': 'bhargavi@powerpbox.org',
                        'auto_delete': False,
                        'state': 'outgoing'
                    })
                    email.sudo().send()

                    tnt_obj = request.env['track.trace.event']
                    track_equipment_event = request.env['track.equipment.event']
                    track_transport_event = request.env['track.transport.event']
                    if 'Datas' in equip:
                        track_trace_event_id = tnt_obj.sudo().search([('carrier_booking', '=', carrier_booking_ref)],
                                                                     order='id desc', limit=1)
                        if not track_trace_event_id:
                            track_trace_event_id = tnt_obj.sudo().create({'carrier_booking': carrier_booking_ref,
                                                                          'standalone_user_id': user.id})
                        for eq in equip['Datas'][0]['eq']:
                            import datetime
                            print("eq['event_created_datetime']", eq['event_created_datetime'])
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
                                'track_trace_event_id': track_trace_event_id.id,
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
                                if track_equipment_event_id and track_trace_event_id.equip_reference == eq[
                                    'equip_reference']:
                                    track_equipment_event_id.sudo().write(equip_events_vals)
                            else:
                                if track_equipment_event_id and track_trace_event_id.equip_reference == eq[
                                    'equip_reference']:
                                    track_equipment_event.sudo().create(equip_events_vals)
                        for transport in equip['Datas'][0]['transport']:
                            print("trans--", transport)
                            print("EVENT", transport['event_created_datetime'])
                            import datetime
                            if len(transport['event_created_datetime']) > 20:

                                event_created_datetime = datetime.datetime.strptime(transport['event_created_datetime'],
                                                                                    "%Y-%m-%d %H:%M:%S.%f")
                            else:
                                event_created_datetime = transport['event_created_datetime']
                            if len(eq['event_datetime']) > 20:
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
                                'track_trace_event_id': track_trace_event_id.id,
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
                                if track_transport_event_id and track_trace_event_id.container_id == transport['container_id']:
                                    track_transport_event_id.sudo().write(transport_events_vals)
                            else:
                                if track_transport_event_id and track_trace_event_id.container_id == transport['container_id']:
                                    track_transport_event.sudo().create(transport_events_vals)
                        track_trace_event_id.onchange_transport_event_code()
        track_trace_event_ids = self.get_track_trace_events(carrier_booking_ref, container_ids, transport_document_ref)
        if track_trace_event_ids:
            track_trace_event_ids.import_tnt_from_mother_server()
            track_trace_event_ids.sudo().get_route_waypoints()
            done_cont_ids = []
            tnt_container_ids = []
            for tnt_event in track_trace_event_ids:
                if tnt_event.cont_id not in done_cont_ids:
                    done_cont_ids.append(tnt_event.cont_id)
                    if tnt_event.cont_id:
                        tnt_container_ids.append(
                            {tnt_event.cont_id: (carrier_booking_ref, tnt_event.id, transport_document_ref)})
                    else:
                        tnt_container_ids.append(
                            {carrier_booking_ref: (carrier_booking_ref, tnt_event.id, transport_document_ref)})
                tnt_container_events = []
                if len(tnt_event.transport_event_line) > 0:
                    origin_port_unlocode = tnt_event.transport_event_line[0].un_location_code or \
                                           tnt_event.transport_event_line[0].locode or False
                    origin_port_name = tnt_event.transport_event_line[0].location or tnt_event.transport_event_line[
                        0].location_name or False
                    destination_port_unlocode = tnt_event.transport_event_line[-1].un_location_code or \
                                                tnt_event.transport_event_line[-1].locode or False
                    destination_port_name = tnt_event.transport_event_line[-1].location or \
                                            tnt_event.transport_event_line[-1].location_name or False

                    if origin_port_name or origin_port_unlocode:
                        origin_port_domain = []
                        if origin_port_unlocode:
                            origin_port_domain.append(('unloc_code', '=', origin_port_unlocode))
                        if origin_port_name:
                            origin_port_domain.append(('name', '=', origin_port_name))
                        origin_port = port_obj.sudo().search(origin_port_domain)
                        origin_geo_data = origin_port and transport_obj.sudo().get_geo_location_from_port(origin_port) or {}
                        por_lat = origin_geo_data.get('lat', 0)
                        por_lon = origin_geo_data.get('lon', 0)

                    if destination_port_unlocode or destination_port_name:
                        destination_port_domain = []
                        if destination_port_unlocode:
                            destination_port_domain.append(('unloc_code', '=', destination_port_unlocode))
                        if destination_port_name:
                            destination_port_domain.append(('name', '=', destination_port_name))
                        destination_port = port_obj.sudo().search(destination_port_domain)
                        destination_geo_data = destination_port and transport_obj.sudo().get_geo_location_from_port(
                            destination_port) or {}
                        pod_lat = destination_geo_data.get('lat', 0)
                        pod_lon = destination_geo_data.get('lon', 0)

                for transport_event in tnt_event.transport_event_line:
                    msg = ""
                    event_occurred = False
                    if transport_event.event_classifier_code == 'ACT':
                        if transport_event.transport_event_type_code == "DEPA":
                            msg = "Left"
                            if transport_event.location:
                                msg = "%s from %s" % (msg, transport_event.location)
                            if transport_event.mode_of_transport_code:
                                msg = "%s by %s " % (msg, transport_event.mode_of_transport_code)
                        if transport_event.transport_event_type_code == "ARRI":
                            msg = "Arrived"
                            if transport_event.location:
                                msg = "%s at %s" % (msg, transport_event.location)
                            if transport_event.mode_of_transport_code:
                                msg = "%s by %s " % (msg, transport_event.mode_of_transport_code)
                    else:
                        if transport_event.transport_event_type_code == "DEPA":
                            msg = "Will Leave"
                            if transport_event.location:
                                msg = "%s from %s" % (msg, transport_event.location)
                            if transport_event.mode_of_transport_code:
                                msg = "%s by %s " % (msg, transport_event.mode_of_transport_code)
                        if transport_event.transport_event_type_code == "ARRI":
                            msg = "Will arrive"
                            if transport_event.location:
                                msg = "%s at %s" % (msg, transport_event.location)
                            if transport_event.mode_of_transport_code:
                                msg = "%s by %s " % (msg, transport_event.mode_of_transport_code)
                    event_due_passed = False
                    reason_for_dealy = False
                    if not transport_event.transport_event_occured:
                        if transport_event.event_datetime and transport_event.event_datetime < fields.Datetime.now():
                            reason_for_dealy = True
                            if transport_event.delay_reason:
                                reason_for_dealy = transport_event.delay_reason

                    if transport_event.event_classifier_code == 'ACT':
                        event_occurred = True

                    if not msg and transport_event:
                        msg = transport_event.event_description

                    tnt_container_events.append(
                        (
                            transport_event.event_datetime,
                            transport_event.event_type,
                            transport_event.event_classifier_code,
                            transport_event.transport_event_type_code,
                            transport_event.mode_of_transport_code,
                            msg,
                            transport_event.distance,
                            transport_event.speed,
                            transport_event.co2_emmision
                        )
                    )
                for equipment_event in tnt_event.equipment_event_line:
                    msg = ""
                    event_occurred = False
                    reason_for_delay = False
                    if equipment_event.equip_event_type_code == "LOAD" and equipment_event.empty_indicator_code == "EMPTY":
                        if equipment_event.event_classifier_code == "ACT":
                            msg = " %s Container is %sED at %s" % (equipment_event.empty_indicator_code,
                                                                   equipment_event.equip_event_type_code,
                                                                   equipment_event.event_location)
                            event_occurred = True
                            reason_for_delay = False
                        else:
                            msg = "Preparing to %s the %s container at %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)

                    elif equipment_event.equip_event_type_code == "OTHR" and equipment_event.empty_indicator_code == "LADEN":
                        if equipment_event.event_classifier_code == "ACT":
                            msg = " %s of %s container at %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                            event_occurred = True
                        else:
                            msg = "Preparing to %s the %s container at %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                    elif equipment_event.equip_event_type_code == "GTOT" and equipment_event.empty_indicator_code == "LADEN":
                        if equipment_event.event_classifier_code == "ACT":
                            msg = " Gate Out of %s container at %s" % (
                                equipment_event.empty_indicator_code, equipment_event.event_location)
                            event_occurred = True
                        else:
                            msg = "Preparing to %s the %s container at %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                    elif equipment_event.equip_event_type_code == "GTIN" and equipment_event.empty_indicator_code == "EMPTY":
                        if equipment_event.event_classifier_code == "ACT":
                            msg = " Gate In of %s container at %s" % (
                                equipment_event.empty_indicator_code, equipment_event.event_location)
                            event_occurred = True
                        else:
                            msg = "Preparing to %s the %s container at %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                    elif equipment_event.equip_event_type_code == "STUF" and equipment_event.empty_indicator_code == "EMPTY":
                        if equipment_event.event_classifier_code == "ACT":
                            msg = "%sFED, %s Container at %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                            event_occurred = True
                        else:
                            msg = "Preparing to %sF, %s container at %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                    elif equipment_event.equip_event_type_code == "PICK" and equipment_event.empty_indicator_code == "LADEN":
                        if equipment_event.event_classifier_code == "ACT":
                            msg = "%s Container is %sED up from %s" % (
                                equipment_event.empty_indicator_code, equipment_event.equip_event_type_code,
                                equipment_event.event_location)
                            event_occurred = True
                        else:
                            msg = "Preparing to  %s UP,  %s container from %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                    elif equipment_event.equip_event_type_code == "PICK" and equipment_event.empty_indicator_code == "EMPTY":
                        if equipment_event.event_classifier_code == "ACT":
                            msg = "%s Container is %sED UP from %s" % (
                                equipment_event.empty_indicator_code, equipment_event.equip_event_type_code,
                                equipment_event.event_location)
                            event_occurred = True
                        else:
                            msg = "Preparing to %s UP, %s Container from %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                    elif equipment_event.equip_event_type_code == "LOAD" and equipment_event.empty_indicator_code == "LADEN":
                        if equipment_event.event_classifier_code == "ACT":
                            msg = "%s Container is %sED at %s" % (
                                equipment_event.empty_indicator_code, equipment_event.equip_event_type_code,
                                equipment_event.event_location)
                            event_occurred = True
                        else:
                            msg = "Preparing to %s, %s container at %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                    elif equipment_event.equip_event_type_code == "DROP" and equipment_event.empty_indicator_code == "LADEN":
                        if equipment_event.event_classifier_code == "ACT":
                            msg = "%s Container is %sPED OFF at %s" % (
                                equipment_event.empty_indicator_code, equipment_event.equip_event_type_code,
                                equipment_event.event_location)
                            event_occurred = True
                        else:
                            msg = "Preparing to %s OFF, %s container at %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                    elif equipment_event.equip_event_type_code == "DISC" and equipment_event.empty_indicator_code == "LADEN":
                        if equipment_event.event_classifier_code == "ACT":
                            msg = "%sHARGED, %s Container at %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                            event_occurred = True
                        else:
                            msg = "Preparing to %sHARGE, %s Container at %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                    elif equipment_event.equip_event_type_code == "STRIP" and equipment_event.empty_indicator_code == "LADEN":
                        if equipment_event.event_classifier_code == "ACT":
                            msg = "%s Container is %sPED at %s" % (
                                equipment_event.empty_indicator_code, equipment_event.equip_event_type_code,
                                equipment_event.event_location)
                            event_occurred = True
                        else:
                            msg = "Preparing to %s, %s Container at %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                            event_occurred = False
                            reason_for_delay = False
                    elif equipment_event.equip_event_type_code == "GTOT" and equipment_event.empty_indicator_code == "EMPTY":
                        if equipment_event.event_classifier_code == "ACT":
                            msg = "Gate Out of %s container at %s" % (
                                equipment_event.empty_indicator_code, equipment_event.event_location)
                            event_occurred = True
                        else:
                            msg = "Preparing to %s, %s Container at %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                            event_occurred = False
                            reason_for_delay = False

                    elif equipment_event.equip_event_type_code == "GTIN" and equipment_event.empty_indicator_code == "LADEN":
                        if equipment_event.event_classifier_code == "ACT":
                            msg = "%s Container Received, %s Container at %s" % (
                                equipment_event.empty_indicator_code, equipment_event.equip_reference,
                                equipment_event.event_location)
                            event_occurred = True
                        else:
                            msg = "About to receive %s Container with reference %s at %s" % (
                                equipment_event.empty_indicator_code, equipment_event.equip_reference,
                                equipment_event.event_location)
                            event_occurred = False
                            reason_for_delay = False

                    elif equipment_event.equip_event_type_code == "DISC" and equipment_event.empty_indicator_code == "LADEN":
                        if equipment_event.event_classifier_code == "ACT":
                            msg = "%sHARGED, %s Container at %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                            event_occurred = True
                        else:
                            msg = "Preparing to %sHARGE, %s Container at %s" % (
                                equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                                equipment_event.event_location)
                            event_occurred = False
                            reason_for_delay = False

                    if not equipment_event.equipment_event_occured:
                        if equipment_event.event_datetime and equipment_event.event_datetime < fields.Datetime.now():
                            reason_for_delay = True

                    if not msg and equipment_event:
                        msg = equipment_event.event_description

                    tnt_container_events.append(
                        (
                            equipment_event.event_datetime,
                            equipment_event.event_type,
                            equipment_event.event_classifier_code,
                            equipment_event.equip_event_type_code,
                            equipment_event.empty_indicator_code,
                            msg
                        )
                    )
                current_eta = tnt_event.destination_eta
                if current_eta:
                    user_tz = pytz.timezone(user.tz)
                    destination_eta = current_eta.replace(tzinfo=pytz.utc)
                    destination_eta = destination_eta.replace(tzinfo=pytz.utc).astimezone(user_tz)
                    destination_eta = destination_eta.replace(tzinfo=None)
                else:
                    destination_eta = current_eta

                container_data.append((tnt_event.id, tnt_event.cont_id, destination_eta, tnt_container_events))

            for container_id in container_ids:
                import datetime
                fb_trans = request.env['ir.sequence'].sudo().next_by_code('transport.seq') or _('New')
                client_id = request.env['ir.config_parameter'].sudo().sudo().get_param('database.uuid')
                fb_transport_id = fb_trans + '_' + client_id
                if container_id not in track_trace_event_ids.mapped('cont_id'):
                    res = request.env['transport'].sudo().create_transport_request_motherserver(container_id,
                                                                                                fb_transport_id)
                    if res and res.status_code == 200:
                        new_tnt_event = tnt_obj.sudo().create({
                            'is_standalone_tnt': True,
                            'carrier_booking': carrier_booking_ref,
                            'cont_id': container_id,
                            'standalone_user_id': user.id
                        })
                        equip = json.loads(res.content)
                        if cont_id:
                            body_msg = """
                                            Hello,

                                            A track n trace standalone request has been made to mother server for Container ID : %s and Carrier Booking ref. : %s.

                                            Kindly look into it.

                                            Regards.
                                            (System Generated Email From Freightbox Backend)
                                            """ % (cont_id, carrier_booking_ref)
                        admin_user = request.env['res.users'].sudo().search([('id', '=', 2)])
                        email = request.env['mail.mail'].sudo().create({
                            'author_id': admin_user.partner_id.id,
                            'email_from': admin_user.partner_id.email,
                            'body_html': body_msg,
                            'subject': "Track n Trace Standalone Request",
                            'email_to': 'bhargavi@powerpbox.org',
                            'auto_delete': False,
                            'state': 'outgoing'

                        })
                        email.sudo().send()
                    if new_tnt_event.cont_id not in done_cont_ids:
                        done_cont_ids.append(new_tnt_event.cont_id)
                        if tnt_event.cont_id:
                            tnt_container_ids.append(
                                {tnt_event.cont_id: (carrier_booking_ref, tnt_event.id, transport_document_ref)})
                        else:
                            tnt_container_ids.append(
                                {carrier_booking_ref: (carrier_booking_ref, tnt_event.id, transport_document_ref)})
            res = request.render('freightbox.track_trace', {
                'container_ids': tnt_container_ids,
                'trace_trace_event_rec': track_trace_event_ids,
                'cont_id': cont_id or carrier_booking_ref,
                'container_list': 1,
                'container_data': container_data,
                'logged_in_user': logged_in_user,
                'show_on_load':False
            })
            return res
        # else:
        #     import datetime
        #     fb_trans = request.env['ir.sequence'].sudo().next_by_code('transport.seq') or _('New')
        #     client_id = request.env['ir.config_parameter'].sudo().sudo().get_param('database.uuid')
        #     fb_transport_id = fb_trans + '_' + client_id
        #     done_cont_ids = []
        #     tnt_container_ids = []
        #     for container_id in container_ids:
        #         res = request.env['transport'].sudo().create_transport_request_motherserver(container_id,
        #                                                                                     fb_transport_id)
        #         if res and res.status_code == 200:
        #             tnt_event = tnt_obj.sudo().create({
        #                 'is_standalone_tnt': True,
        #                 'carrier_booking': carrier_booking_ref,
        #                 'cont_id': container_id,
        #                 'standalone_user_id': user.id
        #             })
        #             if container_id not in done_cont_ids:
        #                 done_cont_ids.append(container_id)
        #                 tnt_container_ids.append({tnt_event.cont_id: tnt_event.id})
        #             equip = json.loads(res.content)
        #             if cont_id:
        #                 body_msg = """
        #                     Hello,
        #
        #                     A track n trace standalone request has been made to mother server for Container ID : %s and Carrier Booking ref. : %s.
        #
        #                     Kindly look into it.
        #
        #                     Regards.
        #                     (System Generated Email From Freightbox Backend)
        #                     """ % (cont_id, carrier_booking_ref)
        #             admin_user = request.env['res.users'].sudo().search([('id', '=', 2)])
        #             email = request.env['mail.mail'].sudo().create({
        #                 'author_id': admin_user.partner_id.id,
        #                 'email_from': admin_user.partner_id.email,
        #                 'body_html': body_msg,
        #                 'subject': "Track n Trace Standalone Request",
        #                 'email_to': 'bhargavi@powerpbox.org',
        #                 'auto_delete': False,
        #                 'state': 'outgoing'
        #             })
        #             email.sudo().send()
        #
        #             tnt_obj = request.env['track.trace.event']
        #             track_equipment_event = request.env['track.equipment.event']
        #             track_transport_event = request.env['track.transport.event']
        #             if 'Datas' in equip:
        #                 track_trace_event_id = tnt_obj.sudo().search([('carrier_booking', '=', carrier_booking_ref)],
        #                                                              order='id desc', limit=1)
        #                 if not track_trace_event_id:
        #                     track_trace_event_id = tnt_obj.sudo().create({'carrier_booking': carrier_booking_ref,
        #                                                                   'standalone_user_id': user.id})
        #                 for eq in equip['Datas'][0]['eq']:
        #                     import datetime
        #                     print("eq['event_created_datetime']", eq['event_created_datetime'])
        #                     if len(eq['event_created_datetime']) > 20:
        #                         event_created_datetime = datetime.datetime.strptime(eq['event_created_datetime'],
        #                                                                             "%Y-%m-%d %H:%M:%S.%f")
        #                     else:
        #                         event_created_datetime = eq['event_created_datetime']
        #                     if len(eq['event_datetime']) > 20:
        #                         final_event_datetime = datetime.datetime.strptime(eq['event_datetime'],
        #                                                                           "%Y-%m-%d %H:%M:%S.%f")
        #                     else:
        #                         final_event_datetime = eq['event_datetime']
        #                     equip_event_domain = [
        #                         ('equip_reference', '=', eq['equip_reference']),
        #                         ('locode', '=', eq['locode']),
        #                         ('equip_event_type_code', '=', eq['equip_event_type_code'])
        #                     ]
        #                     track_equipment_event_id = track_equipment_event.sudo().search(equip_event_domain)
        #                     equip_events_vals = {
        #                         'track_trace_event_id': track_trace_event_id.id,
        #                         'equip_event_type_code': eq['equip_event_type_code'],
        #                         'equip_event_id': eq['equip_event_id'],
        #                         'event_created_datetime': event_created_datetime,
        #                         'event_classifier_code': eq['event_classifier_code'] or 'ACT',
        #                         'event_datetime': final_event_datetime,
        #                         'transport_call': eq['transport_call'],
        #                         'equip_reference': eq['equip_reference'],
        #                         'iso_equip_code': eq['iso_equip_code'],
        #                         'empty_indicator_code': eq['empty_indicator_code'],
        #                         'event_type': eq['event_type'],
        #                         'event_description': eq['event_description'],
        #                         'locode': eq['locode'],
        #                         'location_name': eq['location_name'],
        #                         'country': eq['country'],
        #                         'timezone': eq['timezone'],
        #                         'latitude': eq['latitude'],
        #                         'longitude': eq['longitude'],
        #                         'event_location': eq['location_name'],
        #                     }
        #                     if track_equipment_event_id:
        #                         if track_equipment_event_id and track_trace_event_id.equip_reference == eq[
        #                             'equip_reference']:
        #                             track_equipment_event_id.sudo().write(equip_events_vals)
        #                     else:
        #                         if track_equipment_event_id and track_trace_event_id.equip_reference == eq[
        #                             'equip_reference']:
        #                             track_equipment_event.sudo().create(equip_events_vals)
        #                 for transport in equip['Datas'][0]['transport']:
        #                     print("trans--", transport)
        #                     print("EVENT", transport['event_created_datetime'])
        #                     import datetime
        #                     if len(transport['event_created_datetime']) > 20:
        #
        #                         event_created_datetime = datetime.datetime.strptime(transport['event_created_datetime'],
        #                                                                             "%Y-%m-%d %H:%M:%S.%f")
        #                     else:
        #                         event_created_datetime = transport['event_created_datetime']
        #                     if len(eq['event_datetime']) > 20:
        #                         final_event_datetime = datetime.datetime.strptime(transport['event_datetime'],
        #                                                                           "%Y-%m-%d %H:%M:%S.%f")
        #                     else:
        #                         final_event_datetime = transport['event_datetime']
        #                     transport_event_domain = [
        #                         ('container_id', '=', transport['container_id']),
        #                         ('transport_event_type_code', '=', transport['transport_event_type_code']),
        #                         ('locode', '=', transport['locode'])
        #                     ]
        #                     track_transport_event_id = track_transport_event.sudo().search(transport_event_domain)
        #                     transport_events_vals = {
        #                         'track_trace_event_id': track_trace_event_id.id,
        #                         'transport_event_type_code': transport['transport_event_type_code'],
        #                         'transport_event_id': transport['transport_event_id'],
        #                         'event_created_datetime': event_created_datetime,
        #                         'event_classifier_code': transport['event_classifier_code'] or 'ACT',
        #                         'event_datetime': final_event_datetime,
        #                         'delay_reason': transport['delay_reason'],
        #                         'change_remark': transport['change_remark'],
        #                         'transport_call_id': transport['transport_call_id'],
        #                         'carrier_service_code': transport['carrier_service_code'],
        #                         'carrier_voyage_number': transport['carrier_voyage_number'],
        #                         'un_location_code': transport['un_location_code'],
        #                         'mode_of_transport_code': transport['mode_of_transport_code'],
        #                         'vessel_imo_number': transport['vessel_imo_number'],
        #                         'vessel_name': transport['vessel_name'],
        #                         'vessel_operator_carrier_code': transport['vessel_operator_carrier_code'],
        #                         'vessel_operator_carrier_code_list_provider': transport[
        #                             'vessel_operator_carrier_code_list_provider'],
        #                         'container_id': transport['container_id'],
        #                         'event_type': transport['event_type'],
        #                         'event_description': transport['event_description'],
        #                         'locode': transport['locode'],
        #                         'location_name': transport['location_name'],
        #                         'country': transport['country'],
        #                         'timezone': transport['timezone'],
        #                         'latitude': transport['latitude'],
        #                         'longitude': transport['longitude'],
        #                         'location': transport['location'],
        #                     }
        #                     if track_transport_event_id:
        #                         if track_transport_event_id and track_trace_event_id.container_id == transport[
        #                             'container_id']:
        #                             track_transport_event_id.sudo().write(transport_events_vals)
        #                     else:
        #                         if track_transport_event_id and track_trace_event_id.container_id == transport[
        #                             'container_id']:
        #                             track_transport_event.sudo().create(transport_events_vals)
        #                 track_trace_event_id.onchange_transport_event_code()
        #
        #     res = request.render('freightbox.track_trace', {
        #         'container_ids': tnt_container_ids,
        #         'trace_trace_event_rec': track_trace_event_ids,
        #         'cont_id': cont_id or carrier_booking_ref,
        #         'container_list': 1,
        #         'logged_in_user': logged_in_user
        #     })
        #     return res
        return request.render('freightbox.tnt_standalone_msg')

    @http.route(
        ['/tracktrace_containerforstandalone/<int:trace_trace_event_rec>/<string:cont_id>/<string:container_id>'],
        type='http', auth="public", website=True)
    def tracktrace_containerforstandalone(self, trace_trace_event_rec, container_id,
                                          cont_id, access_token=None, **kw):
        transport_event_tb = request.env['track.transport.event']
        track_trace_event_obj = request.env['track.trace.event']
        track_trace_event = track_trace_event_obj.sudo().search([('id', '=', trace_trace_event_rec)])
        transport_events = track_trace_event.transport_event_line
        eq_events = track_trace_event.equipment_event_line
        shipment_event = request.env['track.shipment.event'].sudo().search(
            [('track_trace_event_id', '=', trace_trace_event_rec)], order='event_datetime asc')
        if cont_id != "null":
            transport_event = False
            shipment_event = False
        tnt_container_events = []
        msg = ""
        event_occurred = False
        event_delay_reason = ""
        delay_reason = False
        if eq_events:
            for equipment_event in eq_events:
                msg = ""
                event_occurred = False
                reason_for_delay = False
                if equipment_event.equip_event_type_code == "LOAD" and equipment_event.empty_indicator_code == "EMPTY":
                    if equipment_event.event_classifier_code == "ACT":
                        msg = " %s Container is %sED at %s" % (equipment_event.empty_indicator_code,
                                                               equipment_event.equip_event_type_code,
                                                               equipment_event.event_location)
                        event_occurred = True
                        reason_for_delay = False
                    else:
                        msg = "Preparing to %s the %s container at %s" % (
                            equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                            equipment_event.event_location)

                elif equipment_event.equip_event_type_code == "OTHR" and equipment_event.empty_indicator_code == "LADEN":
                    if equipment_event.event_classifier_code == "ACT":
                        msg = " %s of %s container at %s" % (
                            equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                            equipment_event.event_location)
                        event_occurred = True
                    else:
                        msg = "Preparing to %s the %s container at %s" % (
                            equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                            equipment_event.event_location)
                elif equipment_event.equip_event_type_code == "GTOT" and equipment_event.empty_indicator_code == "LADEN":
                    if equipment_event.event_classifier_code == "ACT":
                        msg = " Gate Out of %s container at %s" % (
                            equipment_event.empty_indicator_code, equipment_event.event_location)
                        event_occurred = True
                    else:
                        msg = "Preparing to %s the %s container at %s" % (
                            equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                            equipment_event.event_location)
                elif equipment_event.equip_event_type_code == "GTIN" and equipment_event.empty_indicator_code == "EMPTY":
                    if equipment_event.event_classifier_code == "ACT":
                        msg = " Gate In of %s container at %s" % (
                            equipment_event.empty_indicator_code, equipment_event.event_location)
                        event_occurred = True
                    else:
                        msg = "Preparing to %s the %s container at %s" % (
                            equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                            equipment_event.event_location)
                elif equipment_event.equip_event_type_code == "STUF" and equipment_event.empty_indicator_code == "EMPTY":
                    if equipment_event.event_classifier_code == "ACT":
                        msg = "%sFED, %s Container at %s" % (
                            equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                            equipment_event.event_location)
                        event_occurred = True
                    else:
                        msg = "Preparing to %sF, %s container at %s" % (
                            equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                            equipment_event.event_location)
                elif equipment_event.equip_event_type_code == "PICK" and equipment_event.empty_indicator_code == "LADEN":
                    if equipment_event.event_classifier_code == "ACT":
                        msg = "%s Container is %sED up from %s" % (
                            equipment_event.empty_indicator_code, equipment_event.equip_event_type_code,
                            equipment_event.event_location)
                        event_occurred = True
                    else:
                        msg = "Preparing to  %s UP,  %s container from %s" % (
                            equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                            equipment_event.event_location)
                elif equipment_event.equip_event_type_code == "PICK" and equipment_event.empty_indicator_code == "EMPTY":
                    if equipment_event.event_classifier_code == "ACT":
                        msg = "%s Container is %sED UP from %s" % (
                            equipment_event.empty_indicator_code, equipment_event.equip_event_type_code,
                            equipment_event.event_location)
                        event_occurred = True
                    else:
                        msg = "Preparing to %s UP, %s Container from %s" % (
                            equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                            equipment_event.event_location)
                elif equipment_event.equip_event_type_code == "LOAD" and equipment_event.empty_indicator_code == "LADEN":
                    if equipment_event.event_classifier_code == "ACT":
                        msg = "%s Container is %sED at %s" % (
                            equipment_event.empty_indicator_code, equipment_event.equip_event_type_code,
                            equipment_event.event_location)
                        event_occurred = True
                    else:
                        msg = "Preparing to %s, %s container at %s" % (
                            equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                            equipment_event.event_location)
                elif equipment_event.equip_event_type_code == "DROP" and equipment_event.empty_indicator_code == "LADEN":
                    if equipment_event.event_classifier_code == "ACT":
                        msg = "%s Container is %sPED OFF at %s" % (
                            equipment_event.empty_indicator_code, equipment_event.equip_event_type_code,
                            equipment_event.event_location)
                        event_occurred = True
                    else:
                        msg = "Preparing to %s OFF, %s container at %s" % (
                            equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                            equipment_event.event_location)
                elif equipment_event.equip_event_type_code == "DISC" and equipment_event.empty_indicator_code == "LADEN":
                    if equipment_event.event_classifier_code == "ACT":
                        msg = "%sHARGED, %s Container at %s" % (
                            equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                            equipment_event.event_location)
                        event_occurred = True
                    else:
                        msg = "Preparing to %sHARGE, %s Container at %s" % (
                            equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                            equipment_event.event_location)
                elif equipment_event.equip_event_type_code == "STRIP" and equipment_event.empty_indicator_code == "LADEN":
                    if equipment_event.event_classifier_code == "ACT":
                        msg = "%s Container is %sPED at %s" % (
                            equipment_event.empty_indicator_code, equipment_event.equip_event_type_code,
                            equipment_event.event_location)
                        event_occurred = True
                    else:
                        msg = "Preparing to %s, %s Container at %s" % (
                            equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                            equipment_event.event_location)
                        event_occurred = False
                        reason_for_delay = False
                elif equipment_event.equip_event_type_code == "GTOT" and equipment_event.empty_indicator_code == "EMPTY":
                    if equipment_event.event_classifier_code == "ACT":
                        msg = "Gate Out of %s container at %s" % (
                            equipment_event.empty_indicator_code, equipment_event.event_location)
                        event_occurred = True
                    else:
                        msg = "Preparing to %s, %s Container at %s" % (
                            equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                            equipment_event.event_location)
                        event_occurred = False
                        reason_for_delay = False

                elif equipment_event.equip_event_type_code == "GTIN" and equipment_event.empty_indicator_code == "LADEN":
                    if equipment_event.event_classifier_code == "ACT":
                        msg = "%s Container Received, %s Container at %s" % (
                            equipment_event.empty_indicator_code, equipment_event.equip_reference,
                            equipment_event.event_location)
                        event_occurred = True
                    else:
                        msg = "About to receive %s Container with reference %s at %s" % (
                            equipment_event.empty_indicator_code, equipment_event.equip_reference,
                            equipment_event.event_location)
                        event_occurred = False
                        reason_for_delay = False

                elif equipment_event.equip_event_type_code == "DISC" and equipment_event.empty_indicator_code == "LADEN":
                    if equipment_event.event_classifier_code == "ACT":
                        msg = "%sHARGED, %s Container at %s" % (
                            equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                            equipment_event.event_location)
                        event_occurred = True
                    else:
                        msg = "Preparing to %sHARGE, %s Container at %s" % (
                            equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                            equipment_event.event_location)
                        event_occurred = False
                        reason_for_delay = False

                if not equipment_event.equipment_event_occured:
                    if equipment_event.event_datetime and equipment_event.event_datetime < fields.fields.Datetime.now():
                        reason_for_delay = True

                if not msg and equipment_event:
                    msg = equipment_event.event_description

                tnt_container_events.append({
                    'event_datetime': equipment_event.event_datetime,
                    'id': equipment_event.id,
                    'event_type': "equipment",
                    'msg': msg,
                    'event_occurred': event_occurred,
                    'reason_for_dealy': reason_for_delay,
                    'event_delay_reason': "",
                    'distance': 0,
                    'speed': 0,
                    'co2_emmision': 0,
                    'event_code': equipment_event.event_classifier_code
                })

        if transport_events:
            for transport_event in transport_events:
                msg = ""
                event_occurred = False
                if transport_event.event_classifier_code == 'ACT':
                    if transport_event.transport_event_type_code == "DEPA":
                        msg = "Left"
                        if transport_event.location:
                            msg = "%s from %s" % (msg, transport_event.location)
                        if transport_event.mode_of_transport_code:
                            msg = "%s by %s " % (msg, transport_event.mode_of_transport_code)
                    if transport_event.transport_event_type_code == "ARRI":
                        msg = "Arrived"
                        if transport_event.location:
                            msg = "%s at %s" % (msg, transport_event.location)
                        if transport_event.mode_of_transport_code:
                            msg = "%s by %s " % (msg, transport_event.mode_of_transport_code)
                else:
                    if transport_event.transport_event_type_code == "DEPA":
                        msg = "Will Leave"
                        if transport_event.location:
                            msg = "%s from %s" % (msg, transport_event.location)
                        if transport_event.mode_of_transport_code:
                            msg = "%s by %s " % (msg, transport_event.mode_of_transport_code)
                    if transport_event.transport_event_type_code == "ARRI":
                        msg = "Will arrive"
                        if transport_event.location:
                            msg = "%s at %s" % (msg, transport_event.location)
                        if transport_event.mode_of_transport_code:
                            msg = "%s by %s " % (msg, transport_event.mode_of_transport_code)
                event_due_passed = False
                reason_for_dealy = False
                if not transport_event.transport_event_occured:
                    if transport_event.event_datetime and transport_event.event_datetime < fields.fields.Datetime.now():
                        reason_for_dealy = True
                        if transport_event.delay_reason:
                            reason_for_dealy = transport_event.delay_reason

                if transport_event.event_classifier_code == 'ACT':
                    event_occurred = True

                if not msg and transport_event:
                    msg = equipment_event.event_description

                transport_event_data = {
                    'event_datetime': transport_event.event_datetime,
                    'id': transport_event.id,
                    'event_type': "transport",
                    'msg': msg,
                    'event_occurred': event_occurred,
                    'reason_for_dealy': reason_for_dealy,
                    'event_delay_reason': reason_for_dealy,
                    'event_due_passed': event_due_passed,
                    'mode': transport_event.mode_of_transport_code,
                    'distance': transport_event.distance or 0,
                    'speed': transport_event.speed or 0,
                    'co2_emmision': transport_event.co2_emmision or 0,
                    'event_code': transport_event.event_classifier_code
                }
                tnt_container_events.append(transport_event_data)
        if shipment_event:
            for s in shipment_event:
                # print("SSSSSSSSSSSSs", s)
                if s.shipment_event_type_code == "RECE" and s.document_type_code == "BKG":
                    if s.event_classifier_code == "ACT":
                        msg = "Booking Received"
                        event_occurred = True
                        reason_for_delay = False
                    elif s.event_datetime and s.event_datetime < fields.fields.Datetime.now():
                        event_occurred = False
                        reason_for_delay = True
                    else:
                        msg = "To Receive booking"
                        event_occurred = False
                        reason_for_delay = False
                    tnt_container_events.append({
                        'event_datetime': s.event_datetime,
                        'id': s.id,
                        'event_type': "shipment",
                        'msg': msg,
                        'event_occurred': event_occurred,
                        'reason_for_dealy': reason_for_delay,
                        'event_delay_reason': "",
                    })
                if s.shipment_event_type_code == "CONF" and s.document_type_code == "BKG":
                    if s.event_classifier_code == "ACT":
                        msg = "Booking Confirmed"
                        event_occurred = True
                        reason_for_delay = False
                    else:
                        msg = "Booking is under Process"
                        event_occurred = False
                        reason_for_delay = False
                    tnt_container_events.append({
                        'event_datetime': s.event_datetime,
                        'id': s.id,
                        'event_type': "shipment",
                        'msg': msg,
                        'event_occurred': event_occurred,
                        'reason_for_dealy': reason_for_delay,
                        'event_delay_reason': "",
                    })
                if s.shipment_event_type_code == "RECE" and s.document_type_code == "SHI":
                    if s.event_classifier_code == "ACT":
                        msg = "Shipping Instruction Received"
                        event_occurred = True
                        reason_for_delay = False
                    else:
                        msg = "Shipping Instruction is yet to be Prepared"
                        event_occurred = False
                        reason_for_delay = False
                    tnt_container_events.append({
                        'event_datetime': s.event_datetime,
                        'id': s.id,
                        'event_type': "shipment",
                        'msg': msg,
                        'event_occurred': event_occurred,
                        'reason_for_dealy': reason_for_delay,
                        'event_delay_reason': "",
                    })
                if s.shipment_event_type_code == "APPR" and s.document_type_code == "SHI":
                    if s.event_classifier_code == "ACT":
                        msg = "Shipping Instruction Approved"
                        event_occurred = True
                        reason_for_delay = False
                    else:
                        msg = "Shipping Instruction is under Process"
                        event_occurred = False
                        reason_for_delay = False
                    tnt_container_events.append({
                        'event_datetime': s.event_datetime,
                        'id': s.id,
                        'event_type': "shipment",
                        'msg': msg,
                        'event_occurred': event_occurred,
                        'reason_for_dealy': reason_for_delay,
                        'event_delay_reason': "",
                    })
                if s.shipment_event_type_code == "ISSU" and s.document_type_code == "TRD":
                    if s.event_classifier_code == "ACT":
                        msg = "Transport Document Issued"
                        event_occurred = True
                        reason_for_delay = False
                    else:
                        msg = "Transport Document is under Process"
                        event_occurred = False
                        reason_for_delay = False
                    tnt_container_events.append({
                        'event_datetime': s.event_datetime,
                        'id': s.id,
                        'event_type': "shipment",
                        'msg': msg,
                        'event_occurred': event_occurred,
                        'reason_for_dealy': reason_for_delay,
                        'event_delay_reason': "",
                    })
                if s.shipment_event_type_code == "ISSU" and s.document_type_code == "SRM":
                    if s.event_classifier_code == "ACT":
                        msg = "Shipment Release Message Issued"
                        event_occurred = True
                        reason_for_delay = False
                    else:
                        msg = "Shipment Release Message yet to be issued"
                        event_occurred = False
                    tnt_container_events.append({
                        'event_datetime': s.event_datetime,
                        'id': s.id,
                        'event_type': "shipment",
                        'msg': msg,
                        'event_occurred': event_occurred,
                        'reason_for_dealy': reason_for_delay,
                        'event_delay_reason': "",
                    })
                if s.shipment_event_type_code == "HOLD" and s.document_type_code == "CUS":
                    if s.event_classifier_code == "ACT":
                        msg = "Laden Equipment is ON HOLD at Customs Inspection"
                        event_occurred = True
                        reason_for_delay = False
                    else:
                        msg = "Laden Equipment is Under Customs Inspection"
                        event_occurred = False
                        reason_for_delay = False
                    tnt_container_events.append({
                        'event_datetime': s.event_datetime,
                        'id': s.id,
                        'event_type': "shipment",
                        'msg': msg,
                        'event_occurred': event_occurred,
                        'reason_for_dealy': reason_for_delay,
                        'event_delay_reason': "",
                    })
                if s.shipment_event_type_code == "RELS" and s.document_type_code == "CUS":
                    if s.event_classifier_code == "ACT":
                        msg = "Laden Equipment is Released from Customs Inspection"
                        event_occurred = True
                        reason_for_delay = False
                    else:
                        msg = "Laden Equipment is yet to be released by Customs"
                        event_occurred = False
                        reason_for_delay = False
                    tnt_container_events.append({
                        'event_datetime': s.event_datetime,
                        'id': s.id,
                        'event_type': "shipment",
                        'msg': msg,
                        'event_occurred': event_occurred,
                        'reason_for_dealy': reason_for_delay,
                        'event_delay_reason': "",
                    })
                if s.shipment_event_type_code == "REJE" and s.document_type_code == "BKG":
                    if s.event_classifier_code == "ACT":
                        msg = "Booking Rejected"
                        event_occurred = True
                        reason_for_delay = False
                    else:
                        msg = "Booking is under Process"
                        event_occurred = False
                        reason_for_delay = False
                    tnt_container_events.append({
                        'event_datetime': s.event_datetime,
                        'id': s.id,
                        'event_type': "shipment",
                        'msg': msg,
                        'event_occurred': event_occurred,
                        'reason_for_dealy': reason_for_delay,
                        'event_delay_reason': "",
                    })
                if s.shipment_event_type_code == "REJE" and s.document_type_code == "SHI":
                    if s.event_classifier_code == "ACT":
                        msg = "Shipping Instruction Rejected"
                        event_occurred = True
                        reason_for_delay = False
                    else:
                        msg = "Shipping Instruction is under Process"
                        event_occurred = False
                        reason_for_delay = False
                    tnt_container_events.append({
                        'event_datetime': s.event_datetime,
                        'id': s.id,
                        'event_type': "shipment",
                        'msg': msg,
                        'event_occurred': event_occurred,
                        'reason_for_dealy': reason_for_delay,
                        'event_delay_reason': "",
                    })
                if s.shipment_event_type_code == "RECE" and s.document_type_code == "VGM":
                    if s.event_classifier_code == "ACT":
                        msg = "VGM Received"
                        event_occurred = True
                        reason_for_delay = False
                    else:
                        msg = "VGM is yet to be recieved"
                        event_occurred = False
                        reason_for_delay = False
                    tnt_container_events.append({
                        'event_datetime': s.event_datetime,
                        'id': s.id,
                        'event_type': "shipment",
                        'msg': msg,
                        'event_occurred': event_occurred,
                        'reason_for_dealy': reason_for_delay,
                        'event_delay_reason': "",
                    })
        res = []
        moves_with_event_datetime = []
        moves_without_event_datetime = []
        for data in tnt_container_events:
            if data.get('event_datetime'):
                if data not in moves_with_event_datetime:
                    moves_with_event_datetime.append(data)
            else:
                if data not in moves_without_event_datetime:
                    moves_without_event_datetime.append(data)
        sorted_moves_with_event_datetime = []
        sorted_moves_without_event_datetime = []
        for move in sorted(moves_with_event_datetime, key=lambda move: move['event_datetime']):
            sorted_moves_with_event_datetime.append(move)
        for move in sorted(moves_without_event_datetime, key=lambda move: move['id']):
            sorted_moves_without_event_datetime.append(move)
        sorted_container_events = sorted_moves_with_event_datetime + sorted_moves_without_event_datetime
        width = len(sorted_container_events) * 30
        if len(sorted_container_events) == 0:
            width = 100
        res = request.render('freightbox.track_trace', {
            'transport_rec': 'false',
            'sorted_events': sorted_container_events,
            'width': width,
            'show_container_track': 1
        })
        return res

    @http.route(['/tracktrace_for_user/<int:transport_id>'], type='http', auth="public", website=True)
    def tracktrace_for_user(self, transport_id, access_token=None, **kw):
        transport = request.env['transport']
        transport_rec = transport.sudo().search([('id', '=', transport_id)])
        container_id = transport_rec.cont_id
        track_trace_event_obj = request.env['track.trace.event']

        api_rec = request.env['api.integration'].search([('name', '=', 'track_trace_ref')])[-1]
        url = ""
        headers = {}
        if not api_rec:
            raise ValidationError("API Record does not exist for 'track_trace_ref'.")
        url = str(api_rec.url) + str(container_id)
        headers = {'Tnt-Access-Token': api_rec.token,
                   'username': api_rec.username,
                   'passwd': api_rec.password}
        # url = "https://mother.powerpbox.org/mother_odoo14/get_track_trace_events_gh/%s" % container_id
        # headers = {'Tnt-Access-Token': "447b2d295a113f7c784bf1e7528a76123ab1a6d0",
        #            'username': "indra",
        #            'passwd': "indra"}
        # eb2bc2e3560da2130d8e6210c38f5de909fd3ed
        eq_response = requests.get(url, headers=headers)
        if eq_response.status_code == 200:
            equip = json.loads(eq_response.content)
            tnt_obj = request.env['track.trace.event']
            track_equipment_event = request.env['track.equipment.event']
            track_transport_event = request.env['track.transport.event']
            if 'Datas' in equip:
                track_trace_event_domain = [('carrier_booking', '=', transport_rec.carrier_booking)]
                if transport_rec:
                    track_trace_event_domain.append(('transport_id', '=', transport_rec.id))
                track_trace_event_id = tnt_obj.sudo().search(track_trace_event_domain)
                if not track_trace_event_id:
                    track_trace_event_vals = {'carrier_booking': transport_rec.carrier_booking}
                    if transport_rec:
                        track_trace_event_vals.update({'transport_id': transport_rec.id})
                    track_trace_event_id = tnt_obj.sudo().create(track_trace_event_vals)
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
                        'track_trace_event_id': track_trace_event_id.id,
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
                        if track_trace_event_id and track_trace_event_id.transport_id and track_trace_event_id.transport_id.cont_id == \
                                eq['equip_reference']:
                            track_equipment_event_id.sudo().write(equip_events_vals)
                    else:
                        if track_trace_event_id and track_trace_event_id.transport_id and track_trace_event_id.transport_id.cont_id == \
                                eq['equip_reference']:
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
                        'track_trace_event_id': track_trace_event_id.id,
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
                        if track_trace_event_id and track_trace_event_id.transport_id and track_trace_event_id.transport_id.cont_id == \
                                transport['container_id']:
                            track_transport_event_id.sudo().write(transport_events_vals)
                    else:
                        if track_trace_event_id and track_trace_event_id.transport_id and track_trace_event_id.transport_id.cont_id == \
                                transport['container_id']:
                            track_transport_event.sudo().create(transport_events_vals)
        #         transport_event = track_transport_event.sudo().search(
        #                 [('track_trace_event_id', '=', track_trace_event_id.id),
        #                  ('container_id', '=', container_id)], order='event_datetime asc')
        #         eq_event = track_equipment_event.sudo().search(
        #                 [('track_trace_event_id', '=', track_trace_event_id.id),
        #                  ('equip_reference', '=', container_id)], order='event_datetime asc')
        #         shipment_event = request.env['track.shipment.event'].sudo().search(
        #                 [('track_trace_event_id', '=', track_trace_event_id.id)], order='event_datetime asc')
        #
        #         msg = ""
        #         event_occurred = False
        #         event_delay_reason = ""
        #         delay_reason = False
        #         if eq_event:
        #             for eq in eq_event:
        #                 if eq.equip_event_type_code == "LOAD" and eq.empty_indicator_code == "EMPTY":
        #                     if eq.event_classifier_code == "ACT":
        #                         msg = " %s Container is %sED at %s" % (eq.empty_indicator_code,
        #                                                                eq.equip_event_type_code, eq.event_location)
        #                         event_occurred = True
        #                         reason_for_delay = False
        #                     else:
        #                         msg = "Preparing to %s the %s container at %s" % (
        #                             eq.equip_event_type_code, eq.empty_indicator_code, eq.event_location)
        #                         event_occurred = False
        #                         reason_for_delay = False
        #                     print("transport_tnt_events", tnt_container_events)
        #                     tnt_container_events.append({
        #                         'event_datetime': eq.event_datetime,
        #                         'id': eq.id,
        #                         'event_type': "shipment",
        #                         'msg': msg,
        #                         'event_occurred': event_occurred,
        #                         'reason_for_dealy': reason_for_delay,
        #                         'event_delay_reason': "",
        #                     })
        #                 if eq.equip_event_type_code == "OTHR" and eq.empty_indicator_code == "LADEN":
        #                     if eq.event_classifier_code == "ACT":
        #                         msg = " %s of %s container at %s" % (eq.equip_event_type_code, eq.empty_indicator_code, eq.event_location)
        #                         event_occurred = True
        #                         reason_for_delay = False
        #                         event_occurred = True
        #                         reason_for_delay = False
        #                     else:
        #                         msg = "Preparing to %s the %s container at %s" % (
        #                             eq.equip_event_type_code, eq.empty_indicator_code, eq.event_location)
        #                         event_occurred = False
        #                         reason_for_delay = False
        #                     print("transport_tnt_events", tnt_container_events)
        #                     tnt_container_events.append({
        #                         'event_datetime': eq.event_datetime,
        #                         'id': eq.id,
        #                         'event_type': "shipment",
        #                         'msg': msg,
        #                         'event_occurred': event_occurred,
        #                         'reason_for_dealy': reason_for_delay,
        #                         'event_delay_reason': "",
        #                     })
        #                 if eq.equip_event_type_code == "GTOT" and eq.empty_indicator_code == "LADEN":
        #                     if eq.event_classifier_code == "ACT":
        #                         msg = " Gate Out of %s container at %s" % (eq.empty_indicator_code, eq.event_location)
        #                         event_occurred = True
        #                         reason_for_delay = False
        #                         event_occurred = True
        #                         reason_for_delay = False
        #                     else:
        #                         msg = "Preparing to %s the %s container at %s" % (
        #                             eq.equip_event_type_code, eq.empty_indicator_code, eq.event_location)
        #                         event_occurred = False
        #                         reason_for_delay = False
        #                     print("transport_tnt_events", tnt_container_events)
        #                     tnt_container_events.append({
        #                         'event_datetime': eq.event_datetime,
        #                         'id': eq.id,
        #                         'event_type': "shipment",
        #                         'msg': msg,
        #                         'event_occurred': event_occurred,
        #                         'reason_for_dealy': reason_for_delay,
        #                         'event_delay_reason': "",
        #                     })
        #                 if eq.equip_event_type_code == "GTIN" and eq.empty_indicator_code == "EMPTY":
        #                     if eq.event_classifier_code == "ACT":
        #                         # msg = " %s Container is %sED at %s" % (eq.empty_indicator_code,
        #                         #                                        eq.equip_event_type_code, eq.event_location)
        #                         msg = " Gate In of %s container at %s" % (eq.empty_indicator_code, eq.event_location)
        #                         event_occurred = True
        #                         reason_for_delay = False
        #                     else:
        #                         msg = "Preparing to %s the %s container at %s" % (
        #                             eq.equip_event_type_code, eq.empty_indicator_code, eq.event_location)
        #                         event_occurred = False
        #                         reason_for_delay = False
        #                     print("transport_tnt_events", tnt_container_events)
        #                     tnt_container_events.append({
        #                         'event_datetime': eq.event_datetime,
        #                         'id': eq.id,
        #                         'event_type': "shipment",
        #                         'msg': msg,
        #                         'event_occurred': event_occurred,
        #                         'reason_for_dealy': reason_for_delay,
        #                         'event_delay_reason': "",
        #                     })
        #                 if eq.equip_event_type_code == "STUF" and eq.empty_indicator_code == "EMPTY":
        #                     if eq.event_classifier_code == "ACT":
        #                         msg = "%sFED, %s Container at %s" % (
        #                             eq.equip_event_type_code, eq.empty_indicator_code, eq.event_location)
        #                         event_occurred = True
        #                         reason_for_delay = False
        #                     else:
        #                         msg = "Preparing to %sF, %s container at %s" % (
        #                             eq.equip_event_type_code, eq.empty_indicator_code, eq.event_location)
        #                         event_occurred = False
        #                         reason_for_delay = False
        #                     print("transport_tnt_events", tnt_container_events)
        #                     tnt_container_events.append({
        #                         'event_datetime': eq.event_datetime,
        #                         'id': eq.id,
        #                         'event_type': "shipment",
        #                         'msg': msg,
        #                         'event_occurred': event_occurred,
        #                         'reason_for_dealy': reason_for_delay,
        #                         'event_delay_reason': "",
        #                     })
        #                 if eq.equip_event_type_code == "PICK" and eq.empty_indicator_code == "LADEN":
        #                     if eq.event_classifier_code == "ACT":
        #                         msg = "%s Container is %sED up from %s" % (
        #                             eq.empty_indicator_code, eq.equip_event_type_code, eq.event_location)
        #                         event_occurred = True
        #                         reason_for_delay = False
        #                     else:
        #                         msg = "Preparing to  %s UP,  %s container from %s" % (
        #                             eq.equip_event_type_code, eq.empty_indicator_code, eq.event_location)
        #                         event_occurred = False
        #                         reason_for_delay = False
        #                     print("transport_tnt_events", tnt_container_events)
        #                     tnt_container_events.append({
        #                         'event_datetime': eq.event_datetime,
        #                         'id': eq.id,
        #                         'event_type': "shipment",
        #                         'msg': msg,
        #                         'event_occurred': event_occurred,
        #                         'reason_for_dealy': reason_for_delay,
        #                         'event_delay_reason': "",
        #                     })
        #                 if eq.equip_event_type_code == "PICK" and eq.empty_indicator_code == "EMPTY":
        #                     if eq.event_classifier_code == "ACT":
        #                         msg = "%s Container is %sED UP from %s" % (
        #                             eq.empty_indicator_code, eq.equip_event_type_code, eq.event_location)
        #                         event_occurred = True
        #                         reason_for_delay = False
        #                     else:
        #                         msg = "Preparing to %s UP, %s Container from %s" % (
        #                             eq.equip_event_type_code, eq.empty_indicator_code, eq.event_location)
        #                         event_occurred = False
        #                         reason_for_delay = False
        #                     print("transport_tnt_events", tnt_container_events)
        #                     tnt_container_events.append({
        #                         'event_datetime': eq.event_datetime,
        #                         'id': eq.id,
        #                         'event_type': "shipment",
        #                         'msg': msg,
        #                         'event_occurred': event_occurred,
        #                         'reason_for_dealy': reason_for_delay,
        #                         'event_delay_reason': "",
        #                     })
        #                 if eq.equip_event_type_code == "LOAD" and eq.empty_indicator_code == "LADEN":
        #                     if eq.event_classifier_code == "ACT":
        #                         msg = "%s Container is %sED at %s" % (
        #                             eq.empty_indicator_code, eq.equip_event_type_code, eq.event_location)
        #                         event_occurred = True
        #                         reason_for_delay = False
        #                     else:
        #                         msg = "Preparing to %s, %s container at %s" % (
        #                             eq.equip_event_type_code, eq.empty_indicator_code, eq.event_location)
        #                         event_occurred = False
        #                         reason_for_delay = False
        #                     print("transport_tnt_events", tnt_container_events)
        #                     tnt_container_events.append({
        #                         'event_datetime': eq.event_datetime,
        #                         'id': eq.id,
        #                         'event_type': "shipment",
        #                         'msg': msg,
        #                         'event_occurred': event_occurred,
        #                         'reason_for_dealy': reason_for_delay,
        #                         'event_delay_reason': "",
        #                     })
        #                 if eq.equip_event_type_code == "DROP" and eq.empty_indicator_code == "LADEN":
        #                     if eq.event_classifier_code == "ACT":
        #                         msg = "%s Container is %sPED OFF at %s" % (
        #                             eq.empty_indicator_code, eq.equip_event_type_code, eq.event_location)
        #                         event_occurred = True
        #                         reason_for_delay = False
        #                     else:
        #                         msg = "Preparing to %s OFF, %s container at %s" % (
        #                             eq.equip_event_type_code, eq.empty_indicator_code, eq.event_location)
        #                         event_occurred = False
        #                         reason_for_delay = False
        #                     print("transport_tnt_events", tnt_container_events)
        #                     tnt_container_events.append({
        #                         'event_datetime': eq.event_datetime,
        #                         'id': eq.id,
        #                         'event_type': "shipment",
        #                         'msg': msg,
        #                         'event_occurred': event_occurred,
        #                         'reason_for_dealy': reason_for_delay,
        #                         'event_delay_reason': "",
        #                     })
        #                 if eq.equip_event_type_code == "DISC" and eq.empty_indicator_code == "LADEN":
        #                     if eq.event_classifier_code == "ACT":
        #                         msg = "%sHARGED, %s Container at %s" % (
        #                             eq.equip_event_type_code, eq.empty_indicator_code, eq.event_location)
        #                         event_occurred = True
        #                         reason_for_delay = False
        #                     else:
        #                         msg = "Preparing to %sHARGE, %s Container at %s" % (
        #                             eq.equip_event_type_code, eq.empty_indicator_code, eq.event_location)
        #                         event_occurred = False
        #                         reason_for_delay = False
        #                     print("transport_tnt_events", tnt_container_events)
        #                     tnt_container_events.append({
        #                         'event_datetime': eq.event_datetime,
        #                         'id': eq.id,
        #                         'event_type': "shipment",
        #                         'msg': msg,
        #                         'event_occurred': event_occurred,
        #                         'reason_for_dealy': reason_for_delay,
        #                         'event_delay_reason': "",
        #                     })
        #                 if eq.equip_event_type_code == "STRIP" and eq.empty_indicator_code == "LADEN":
        #                     if eq.event_classifier_code == "ACT":
        #                         msg = "%s Container is %sPED at %s" % (
        #                             eq.empty_indicator_code, eq.equip_event_type_code, eq.event_location)
        #                         event_occurred = True
        #                         reason_for_delay = False
        #                     else:
        #                         msg = "Preparing to %s, %s Container at %s" % (
        #                             eq.equip_event_type_code, eq.empty_indicator_code, eq.event_location)
        #                         event_occurred = False
        #                         reason_for_delay = False
        #                     print("transport_tnt_events", tnt_container_events)
        #                     tnt_container_events.append({
        #                         'event_datetime': eq.event_datetime,
        #                         'id': eq.id,
        #                         'event_type': "shipment",
        #                         'msg': msg,
        #                         'event_occurred': event_occurred,
        #                         'reason_for_dealy': reason_for_delay,
        #                         'event_delay_reason': "",
        #                     })
        #
        #         if transport_event:
        #             for t in transport_event:
        #                 if t.transport_event_type_code == "DEPA":
        #                     if t.event_classifier_code == "ACT":
        #                         msg = "Departed from %s by %s" % (t.location, t.mode_of_transport_code)
        #                         event_occurred = True
        #                         reason_for_delay = False
        #                     else:
        #                         if t.delay_reason:
        #                             delay_reason = True
        #                         else:
        #                             delay_reason = False
        #                         msg = "Preparing to depart from %s by %s " % (t.location, t.mode_of_transport_code)
        #                         event_occurred = False
        #                         reason_for_delay = delay_reason
        #                     print("transport_tnt_events", tnt_container_events)
        #                     tnt_container_events.append({
        #                         'event_datetime': t.event_datetime,
        #                         'id': t.id,
        #                         'event_type': "shipment",
        #                         'msg': msg,
        #                         'event_occurred': event_occurred,
        #                         'reason_for_dealy': reason_for_delay,
        #                         'event_delay_reason': t.delay_reason,
        #                     })
        #                 if t.transport_event_type_code == "ARRI":
        #                     if t.event_classifier_code == "ACT":
        #                         msg = "Arrived at %s by %s" % (t.location, t.mode_of_transport_code)
        #                         event_occurred = True
        #                         reason_for_delay = False
        #                     else:
        #                         if t.delay_reason:
        #                             delay_reason = True
        #                         else:
        #                             delay_reason = False
        #                         msg = "On the Way to %s by %s" % (t.location, t.mode_of_transport_code)
        #                         event_occurred = False
        #                         reason_for_delay = delay_reason
        #                     tnt_container_events.append({
        #                         'event_datetime': t.event_datetime,
        #                         'id': t.id,
        #                         'event_type': "shipment",
        #                         'msg': msg,
        #                         'event_occurred': event_occurred,
        #                         'reason_for_dealy': reason_for_delay,
        #                         'event_delay_reason': t.delay_reason,
        #                     })
        #         if shipment_event:
        #             for s in shipment_event:
        #                 # print("SSSSSSSSSSSSs", s)
        #                 if s.shipment_event_type_code == "RECE" and s.document_type_code == "BKG":
        #                     if s.event_classifier_code == "ACT":
        #                         msg = "Booking Received"
        #                         event_occurred = True
        #                         reason_for_delay = False
        #                     else:
        #                         msg = "To Receive booking"
        #                         event_occurred = False
        #                         reason_for_delay = False
        #                     tnt_container_events.append({
        #                         'event_datetime': s.event_datetime,
        #                         'id': s.id,
        #                         'event_type': "shipment",
        #                         'msg': msg,
        #                         'event_occurred': event_occurred,
        #                         'reason_for_dealy': reason_for_delay,
        #                         'event_delay_reason': "",
        #                     })
        #                 if s.shipment_event_type_code == "CONF" and s.document_type_code == "BKG":
        #                     if s.event_classifier_code == "ACT":
        #                         msg = "Booking Confirmed"
        #                         event_occurred = True
        #                         reason_for_delay = False
        #                     else:
        #                         msg = "Booking is under Process"
        #                         event_occurred = False
        #                         reason_for_delay = False
        #                     tnt_container_events.append({
        #                         'event_datetime': s.event_datetime,
        #                         'id': s.id,
        #                         'event_type': "shipment",
        #                         'msg': msg,
        #                         'event_occurred': event_occurred,
        #                         'reason_for_dealy': reason_for_delay,
        #                         'event_delay_reason': "",
        #                     })
        #                 if s.shipment_event_type_code == "RECE" and s.document_type_code == "SHI":
        #                     if s.event_classifier_code == "ACT":
        #                         msg = "Shipping Instruction Received"
        #                         event_occurred = True
        #                         reason_for_delay = False
        #                     else:
        #                         msg = "Shipping Instruction is yet to be Prepared"
        #                         event_occurred = False
        #                         reason_for_delay = False
        #                     tnt_container_events.append({
        #                         'event_datetime': s.event_datetime,
        #                         'id': s.id,
        #                         'event_type': "shipment",
        #                         'msg': msg,
        #                         'event_occurred': event_occurred,
        #                         'reason_for_dealy': reason_for_delay,
        #                         'event_delay_reason': "",
        #                     })
        #                 if s.shipment_event_type_code == "APPR" and s.document_type_code == "SHI":
        #                     if s.event_classifier_code == "ACT":
        #                         msg = "Shipping Instruction Approved"
        #                         event_occurred = True
        #                         reason_for_delay = False
        #                     else:
        #                         msg = "Shipping Instruction is under Process"
        #                         event_occurred = False
        #                         reason_for_delay = False
        #                     tnt_container_events.append({
        #                         'event_datetime': s.event_datetime,
        #                         'id': s.id,
        #                         'event_type': "shipment",
        #                         'msg': msg,
        #                         'event_occurred': event_occurred,
        #                         'reason_for_dealy': reason_for_delay,
        #                         'event_delay_reason': "",
        #                     })
        #                 if s.shipment_event_type_code == "ISSU" and s.document_type_code == "TRD":
        #                     if s.event_classifier_code == "ACT":
        #                         msg = "Transport Document Issued"
        #                         event_occurred = True
        #                         reason_for_delay = False
        #                     else:
        #                         msg = "Transport Document is under Process"
        #                         event_occurred = False
        #                         reason_for_delay = False
        #                     tnt_container_events.append({
        #                         'event_datetime': s.event_datetime,
        #                         'id': s.id,
        #                         'event_type': "shipment",
        #                         'msg': msg,
        #                         'event_occurred': event_occurred,
        #                         'reason_for_dealy': reason_for_delay,
        #                         'event_delay_reason': "",
        #                     })
        #                 if s.shipment_event_type_code == "ISSU" and s.document_type_code == "SRM":
        #                     if s.event_classifier_code == "ACT":
        #                         msg = "Shipment Release Message Issued"
        #                         event_occurred = True
        #                         reason_for_delay = False
        #                     else:
        #                         msg = "Shipment Release Message yet to be issued"
        #                         event_occurred = False
        #                     tnt_container_events.append({
        #                         'event_datetime': s.event_datetime,
        #                         'id': s.id,
        #                         'event_type': "shipment",
        #                         'msg': msg,
        #                         'event_occurred': event_occurred,
        #                         'reason_for_dealy': reason_for_delay,
        #                         'event_delay_reason': "",
        #                     })
        #                 if s.shipment_event_type_code == "HOLD" and s.document_type_code == "CUS":
        #                     if s.event_classifier_code == "ACT":
        #                         msg = "Laden Equipment is ON HOLD at Customs Inspection"
        #                         event_occurred = True
        #                         reason_for_delay = False
        #                     else:
        #                         msg = "Laden Equipment is Under Customs Inspection"
        #                         event_occurred = False
        #                         reason_for_delay = False
        #                     tnt_container_events.append({
        #                         'event_datetime': s.event_datetime,
        #                         'id': s.id,
        #                         'event_type': "shipment",
        #                         'msg': msg,
        #                         'event_occurred': event_occurred,
        #                         'reason_for_dealy': reason_for_delay,
        #                         'event_delay_reason': "",
        #                     })
        #                 if s.shipment_event_type_code == "RELS" and s.document_type_code == "CUS":
        #                     if s.event_classifier_code == "ACT":
        #                         msg = "Laden Equipment is Released from Customs Inspection"
        #                         event_occurred = True
        #                         reason_for_delay = False
        #                     else:
        #                         msg = "Laden Equipment is yet to be released by Customs"
        #                         event_occurred = False
        #                         reason_for_delay = False
        #                     tnt_container_events.append({
        #                         'event_datetime': s.event_datetime,
        #                         'id': s.id,
        #                         'event_type': "shipment",
        #                         'msg': msg,
        #                         'event_occurred': event_occurred,
        #                         'reason_for_dealy': reason_for_delay,
        #                         'event_delay_reason': "",
        #                     })
        #                 if s.shipment_event_type_code == "REJE" and s.document_type_code == "BKG":
        #                     if s.event_classifier_code == "ACT":
        #                         msg = "Booking Rejected"
        #                         event_occurred = True
        #                         reason_for_delay = False
        #                     else:
        #                         msg = "Booking is under Process"
        #                         event_occurred = False
        #                         reason_for_delay = False
        #                     tnt_container_events.append({
        #                         'event_datetime': s.event_datetime,
        #                         'id': s.id,
        #                         'event_type': "shipment",
        #                         'msg': msg,
        #                         'event_occurred': event_occurred,
        #                         'reason_for_dealy': reason_for_delay,
        #                         'event_delay_reason': "",
        #                     })
        #                 if s.shipment_event_type_code == "REJE" and s.document_type_code == "SHI":
        #                     if s.event_classifier_code == "ACT":
        #                         msg = "Shipping Instruction Rejected"
        #                         event_occurred = True
        #                         reason_for_delay = False
        #                     else:
        #                         msg = "Shipping Instruction is under Process"
        #                         event_occurred = False
        #                         reason_for_delay = False
        #                     tnt_container_events.append({
        #                         'event_datetime': s.event_datetime,
        #                         'id': s.id,
        #                         'event_type': "shipment",
        #                         'msg': msg,
        #                         'event_occurred': event_occurred,
        #                         'reason_for_dealy': reason_for_delay,
        #                         'event_delay_reason': "",
        #                     })
        #                 if s.shipment_event_type_code == "RECE" and s.document_type_code == "VGM":
        #                     if s.event_classifier_code == "ACT":
        #                         msg = "VGM Received"
        #                         event_occurred = True
        #                         reason_for_delay = False
        #                     else:
        #                         msg = "VGM is yet to be recieved"
        #                         event_occurred = False
        #                         reason_for_delay = False
        #                     tnt_container_events.append({
        #                         'event_datetime': s.event_datetime,
        #                         'id': s.id,
        #                         'event_type': "shipment",
        #                         'msg': msg,
        #                         'event_occurred': event_occurred,
        #                         'reason_for_dealy': reason_for_delay,
        #                         'event_delay_reason': "",
        #                     })

        tnt_container_events = []

        # Creating tracking response from tracking events
        track_trace_event = track_trace_event_obj.sudo().search([
            ('transport_id', '=', transport_rec.id)
        ], order='id desc', limit=1)
        count = 0
        for transport_event in track_trace_event.transport_event_line:
            msg = ""
            event_occurred = False
            if transport_event.event_classifier_code == 'ACT':
                if transport_event.transport_event_type_code == "DEPA":
                    msg = "Left"
                    if transport_event.location:
                        msg = "%s from %s" % (msg, transport_event.location)
                    if transport_event.mode_of_transport_code:
                        msg = "%s by %s " % (msg, transport_event.mode_of_transport_code)
                if transport_event.transport_event_type_code == "ARRI":
                    msg = "Arrived"
                    if transport_event.location:
                        msg = "%s at %s" % (msg, transport_event.location)
                    if transport_event.mode_of_transport_code:
                        msg = "%s by %s " % (msg, transport_event.mode_of_transport_code)
            else:
                if transport_event.transport_event_type_code == "DEPA":
                    msg = "Will Leave"
                    if transport_event.location:
                        msg = "%s from %s" % (msg, transport_event.location)
                    if transport_event.mode_of_transport_code:
                        msg = "%s by %s " % (msg, transport_event.mode_of_transport_code)
                if transport_event.transport_event_type_code == "ARRI":
                    msg = "Will arrive"
                    if transport_event.location:
                        msg = "%s at %s" % (msg, transport_event.location)
                    if transport_event.mode_of_transport_code:
                        msg = "%s by %s " % (msg, transport_event.mode_of_transport_code)
            event_due_passed = False
            reason_for_dealy = False
            if not transport_event.transport_event_occured:
                if transport_event.event_datetime and transport_event.event_datetime < fields.fields.Datetime.now():
                    reason_for_dealy = True
                    if transport_event.delay_reason:
                        reason_for_dealy = transport_event.delay_reason

            if transport_event.event_classifier_code == 'ACT':
                event_occurred = True

            if not msg and transport_event:
                msg = transport_event.event_description

            transport_event_data = {
                'event_datetime': transport_event.event_datetime,
                'id': transport_event.id,
                'event_type': "transport",
                'msg': msg,
                'event_occurred': event_occurred,
                'reason_for_dealy': reason_for_dealy,
                'event_delay_reason': reason_for_dealy,
                'event_due_passed': event_due_passed,
                'mode': transport_event.mode_of_transport_code,
                'distance': transport_event.distance or 0,
                'speed': transport_event.speed or 0,
                'co2_emmision': transport_event.co2_emmision or 0,
                'event_code': transport_event.event_classifier_code
            }
            tnt_container_events.append(transport_event_data)
        for equipment_event in track_trace_event.equipment_event_line:
            msg = ""
            event_occurred = False
            reason_for_delay = False
            if equipment_event.equip_event_type_code == "LOAD" and equipment_event.empty_indicator_code == "EMPTY":
                if equipment_event.event_classifier_code == "ACT":
                    msg = " %s Container is %sED at %s" % (equipment_event.empty_indicator_code,
                                                           equipment_event.equip_event_type_code,
                                                           equipment_event.event_location)
                    event_occurred = True
                    reason_for_delay = False
                else:
                    msg = "Preparing to %s the %s container at %s" % (
                        equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                        equipment_event.event_location)

            elif equipment_event.equip_event_type_code == "OTHR" and equipment_event.empty_indicator_code == "LADEN":
                if equipment_event.event_classifier_code == "ACT":
                    msg = " %s of %s container at %s" % (
                        equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                        equipment_event.event_location)
                    event_occurred = True
                else:
                    msg = "Preparing to %s the %s container at %s" % (
                        equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                        equipment_event.event_location)
            elif equipment_event.equip_event_type_code == "GTOT" and equipment_event.empty_indicator_code == "LADEN":
                if equipment_event.event_classifier_code == "ACT":
                    msg = " Gate Out of %s container at %s" % (
                    equipment_event.empty_indicator_code, equipment_event.event_location)
                    event_occurred = True
                else:
                    msg = "Preparing to %s the %s container at %s" % (
                        equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                        equipment_event.event_location)
            elif equipment_event.equip_event_type_code == "GTIN" and equipment_event.empty_indicator_code == "EMPTY":
                if equipment_event.event_classifier_code == "ACT":
                    msg = " Gate In of %s container at %s" % (
                    equipment_event.empty_indicator_code, equipment_event.event_location)
                    event_occurred = True
                else:
                    msg = "Preparing to %s the %s container at %s" % (
                        equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                        equipment_event.event_location)
            elif equipment_event.equip_event_type_code == "STUF" and equipment_event.empty_indicator_code == "EMPTY":
                if equipment_event.event_classifier_code == "ACT":
                    msg = "%sFED, %s Container at %s" % (
                        equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                        equipment_event.event_location)
                    event_occurred = True
                else:
                    msg = "Preparing to %sF, %s container at %s" % (
                        equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                        equipment_event.event_location)
            elif equipment_event.equip_event_type_code == "PICK" and equipment_event.empty_indicator_code == "LADEN":
                if equipment_event.event_classifier_code == "ACT":
                    msg = "%s Container is %sED up from %s" % (
                        equipment_event.empty_indicator_code, equipment_event.equip_event_type_code,
                        equipment_event.event_location)
                    event_occurred = True
                else:
                    msg = "Preparing to  %s UP,  %s container from %s" % (
                        equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                        equipment_event.event_location)
            elif equipment_event.equip_event_type_code == "PICK" and equipment_event.empty_indicator_code == "EMPTY":
                if equipment_event.event_classifier_code == "ACT":
                    msg = "%s Container is %sED UP from %s" % (
                        equipment_event.empty_indicator_code, equipment_event.equip_event_type_code,
                        equipment_event.event_location)
                    event_occurred = True
                else:
                    msg = "Preparing to %s UP, %s Container from %s" % (
                        equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                        equipment_event.event_location)
            elif equipment_event.equip_event_type_code == "LOAD" and equipment_event.empty_indicator_code == "LADEN":
                if equipment_event.event_classifier_code == "ACT":
                    msg = "%s Container is %sED at %s" % (
                        equipment_event.empty_indicator_code, equipment_event.equip_event_type_code,
                        equipment_event.event_location)
                    event_occurred = True
                else:
                    msg = "Preparing to %s, %s container at %s" % (
                        equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                        equipment_event.event_location)
            elif equipment_event.equip_event_type_code == "DROP" and equipment_event.empty_indicator_code == "LADEN":
                if equipment_event.event_classifier_code == "ACT":
                    msg = "%s Container is %sPED OFF at %s" % (
                        equipment_event.empty_indicator_code, equipment_event.equip_event_type_code,
                        equipment_event.event_location)
                    event_occurred = True
                else:
                    msg = "Preparing to %s OFF, %s container at %s" % (
                        equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                        equipment_event.event_location)
            elif equipment_event.equip_event_type_code == "DISC" and equipment_event.empty_indicator_code == "LADEN":
                if equipment_event.event_classifier_code == "ACT":
                    msg = "%sHARGED, %s Container at %s" % (
                        equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                        equipment_event.event_location)
                    event_occurred = True
                else:
                    msg = "Preparing to %sHARGE, %s Container at %s" % (
                        equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                        equipment_event.event_location)
            elif equipment_event.equip_event_type_code == "STRIP" and equipment_event.empty_indicator_code == "LADEN":
                if equipment_event.event_classifier_code == "ACT":
                    msg = "%s Container is %sPED at %s" % (
                        equipment_event.empty_indicator_code, equipment_event.equip_event_type_code,
                        equipment_event.event_location)
                    event_occurred = True
                else:
                    msg = "Preparing to %s, %s Container at %s" % (
                        equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                        equipment_event.event_location)
                    event_occurred = False
                    reason_for_delay = False
            elif equipment_event.equip_event_type_code == "GTOT" and equipment_event.empty_indicator_code == "EMPTY":
                if equipment_event.event_classifier_code == "ACT":
                    msg = "Gate Out of %s container at %s" % (
                        equipment_event.empty_indicator_code, equipment_event.event_location)
                    event_occurred = True
                else:
                    msg = "Preparing to %s, %s Container at %s" % (
                        equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                        equipment_event.event_location)
                    event_occurred = False
                    reason_for_delay = False

            elif equipment_event.equip_event_type_code == "GTIN" and equipment_event.empty_indicator_code == "LADEN":
                if equipment_event.event_classifier_code == "ACT":
                    msg = "%s Container Received, %s Container at %s" % (
                        equipment_event.empty_indicator_code, equipment_event.equip_reference,
                        equipment_event.event_location)
                    event_occurred = True
                else:
                    msg = "About to receive %s Container with reference %s at %s" % (
                        equipment_event.empty_indicator_code, equipment_event.equip_reference,
                        equipment_event.event_location)
                    event_occurred = False
                    reason_for_delay = False

            elif equipment_event.equip_event_type_code == "DISC" and equipment_event.empty_indicator_code == "LADEN":
                if equipment_event.event_classifier_code == "ACT":
                    msg = "%sHARGED, %s Container at %s" % (
                        equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                        equipment_event.event_location)
                    event_occurred = True
                else:
                    msg = "Preparing to %sHARGE, %s Container at %s" % (
                        equipment_event.equip_event_type_code, equipment_event.empty_indicator_code,
                        equipment_event.event_location)
                    event_occurred = False
                    reason_for_delay = False

            if not equipment_event.equipment_event_occured:
                if equipment_event.event_datetime and equipment_event.event_datetime < fields.fields.Datetime.now():
                    reason_for_delay = True

            if not msg and equipment_event:
                msg = equipment_event.event_description

            tnt_container_events.append({
                'event_datetime': equipment_event.event_datetime,
                'id': equipment_event.id,
                'event_type': "equipment",
                'msg': msg,
                'event_occurred': event_occurred,
                'reason_for_dealy': reason_for_delay,
                'event_delay_reason': "",
                'distance': 0,
                'speed': 0,
                'co2_emmision': 0,
                'event_code': equipment_event.event_classifier_code
            })

        moves_with_event_datetime = []
        moves_without_event_datetime = []
        for data in tnt_container_events:
            if data.get('event_datetime'):
                if data not in moves_with_event_datetime:
                    moves_with_event_datetime.append(data)
            else:
                if data not in moves_without_event_datetime:
                    moves_without_event_datetime.append(data)
        sorted_moves_with_event_datetime = []
        sorted_moves_without_event_datetime = []
        for move in sorted(moves_with_event_datetime, key=lambda move: move['event_datetime']):
            sorted_moves_with_event_datetime.append(move)
        for move in sorted(moves_without_event_datetime, key=lambda move: move['id']):
            sorted_moves_without_event_datetime.append(move)
        sorted_container_events = sorted_moves_with_event_datetime + sorted_moves_without_event_datetime
        if sorted_container_events:
            width = len(sorted_container_events) * 30
        else:
            width = 100
        res = request.render('freightbox.track_user_own_shipment_form', {
            'transport_rec': transport_rec,
            'sorted_events': sorted_container_events,
            'width': width
        })
        return res

    # @http.route('/track_trace_brief', type='http', auth='public', website=True)
    # def track_trace_brief(self, **post):
    #     job_obj = request.env['job']
    #     rfq_obj = request.env['request.for.quote']
    #     sq_obj = request.env['shipment.quote']
    #     transport_obj = request.env['transport']
    #     si_obj = request.env['shipping.instruction']
    #     bol_obj = request.env['bill.of.lading']
    #     jobs = job_obj.search([('state', 'not in', ['draft', 'hold', 'inactive'])], order='id')
    #     tnt_brief_data=[]
    #     for job in jobs:
    #         job_data = []
    #         job_data.append(job.carrier_booking or 'N/A')
    #         rc_counts = rfq_obj.search_count([('booking_id', '=', job.id)])
    #         if rc_counts > 0:
    #             job_data.append('true')
    #         else:
    #             job_data.append('false')
    #
    #         if job.po_id:
    #             job_data.append('true')
    #         else:
    #             job_data.append('false')
    #
    # sq_rec = sq_obj.search([('po_id', "=", job.po_id.id)])
    #         if sq_rec:
    #             job_data.append('true')
    #         else:
    #             job_data.append('false')
    #
    #         if job.so_id:
    #             job_data.append('true')
    #         else:
    #             job_data.append('false')
    #
    #         if job.job_no:
    #             job_data.append('true')
    #         else:
    #             job_data.append('false')
    #
    #         transport_rec = transport_obj.search([('job_id', '=', job.id)])
    #         if transport_rec:
    #             job_data.append('true')
    #         else:
    #             job_data.append('false')
    #
    #         si_rec = si_obj.search([('job_id', '=', job.id)])
    #         if si_rec:
    #             job_data.append('true')
    #         else:
    #             job_data.append('false')
    #
    #         bol_rec = bol_obj.search([('job_id', '=', job.id)])
    #         if bol_rec:
    #             job_data.append('true')
    #         else:
    #             job_data.append('false')
    #         final_data = tuple(job_data)
    #         tnt_brief_data.append(final_data)
    #
    #
    #     res = request.render('freightbox.track_trace_brief', {
    #         'tnt_brief_data': tnt_brief_data
    #     })
    #     return res
    #
    # @http.route(['/tracktrace_brief_details/<string:booking_id>'],
    #             type='http', auth="public", website=True)
    # def tracktrace_brief_details(self, booking_id, **kw):
    #     if not booking_id:
    #         return "Provide Carrier Booking Reference / Transport Document Reference to proceed."
    #     job_obj = request.env['job']
    #     transport_obj = request.env['transport']
    #     tnt_obj = request.env['track.trace.event']
    #
    #     job = job_obj.search([('carrier_booking', '=', booking_id)])
    #     transport_domain = [
    #         ('job_id', '=', job.id)
    #     ]
    #     transport = transport_obj.sudo().search(transport_domain, order="id desc")
    #     track_trace_event_ids = tnt_obj.sudo().search([
    #         ('transport_id', 'in', transport.ids)
    #     ], order="id")
    #     if track_trace_event_ids:
    #         done_cont_ids = []
    #         container_ids = []
    #         for tnt_event in track_trace_event_ids:
    #             if tnt_event.transport_id.cont_id not in done_cont_ids:
    #                 done_cont_ids.append(tnt_event.transport_id.cont_id)
    #                 container_ids.append({tnt_event.transport_id.cont_id: tnt_event.id})
    #         res = request.render('freightbox.track_trace_equipment_reference_list', {
    #             'container_ids': container_ids,
    #             'trace_trace_event_rec': track_trace_event_ids,
    #             'transport_ref': None,
    #             'cont_id': None,
    #         })
    #         return res
    #     else:
    #         return "Tracking Event Doesn't Exist with carrier booking ref. "
    #
