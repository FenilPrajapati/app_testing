from odoo import http, fields, SUPERUSER_ID
from odoo.http import request
from odoo.exceptions import AccessError, MissingError, ValidationError, UserError
from odoo import _
import requests
import json
import socket
from odoo.osv import expression
from datetime import timedelta, datetime,date
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager
from odoo.addons.portal.controllers.mail import _message_post_helper
from odoo.addons.account.controllers.portal import PortalAccount
import qrcode
import os
import base64

GROUP_SYSTEM = 'base.group_system'


class ShippingInstructionController(http.Controller):

    @http.route(['/list_of_containers/<string:carrier_booking_ref>/tr/<string:transport_ref>'
                 '/tdr/<string:transport_document_ref>/container/<string:cont_id>'],
                type='http', auth="public", website=True)
    def list_of_containers(self, carrier_booking_ref, transport_ref,
                           cont_id, access_token=None, **kw):

        api_rec = request.env['api.integration'].search([('name','=','track_trace_ref')])[-1]
        if not api_rec:
            raise Warning("API record doesn't exist for 'track_trace_ref' process.")
        url = ""
        headers ={}
        if api_rec:
            # url = "https://mother.powerpbox.org/mother_odoo14/get_track_trace_events_gh/%s" % carrier_booking_ref
            # headers = {'Tnt-Access-Token': "447b2d295a113f7c784bf1e7528a76123ab1a6d0",
            #         'username': "indra",
            #         'passwd': "indra"}
            url = str(api_rec.url) + str(carrier_booking_ref)
            headers = {'Tnt-Access-Token': api_rec.token,
                        'username': api_rec.username,
                        'passwd': api_rec.password}
                        
        eq_response = requests.get(url, headers=headers)
        tnt_event_created = False
        if eq_response.status_code == 200:
            equip = json.loads(eq_response.content)
            tnt_obj = request.env['track.trace.event']
            track_equipment_event = request.env['track.equipment.event']
            track_transport_event = request.env['track.transport.event']
            if 'Datas' in equip:
                track_trace_event_id = tnt_obj.sudo().search([('carrier_booking', '=', carrier_booking_ref)], order='id desc', limit=1)
                if not track_trace_event_id:
                    track_trace_event_id = tnt_obj.sudo().create({'carrier_booking': carrier_booking_ref})
                    if track_trace_event_id:
                        tnt_event_created = True
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
                        track_equipment_event_id.sudo().write(equip_events_vals)
                    else:
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
                        'vessel_operator_carrier_code_list_provider': transport['vessel_operator_carrier_code_list_provider'],
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
                        track_transport_event_id.sudo().write(transport_events_vals)
                    else:
                        track_transport_event.sudo().create(transport_events_vals)

                # track_trace_event_id.sudo().write({'is_standalone_tnt': True})
                # print("track_transport_event", track_trace_event_id.transport_event_line,  order='event_datetime asc')
        #         eq_event = request.env['track.equipment.event'].sudo().search(
        #             [('track_trace_event_id', '=', track_trace_event_id.id)], order='event_datetime asc')
        #         print("eq_event 1 ::::::::::::::::::", eq_event)
        #         request.cr.execute(
        #             """SELECT DISTINCT eq.equip_reference FROM track_equipment_event eq where eq.id in %s  """,
        #             (tuple(eq_event.ids),))
        #         events_rec = request.cr.fetchall()
        #         print("333333", events_rec)
        #         if transport_ref != "null":
        #             transport_events = request.env['track.transport.event'].sudo().search(
        #                 [('track_trace_event_id', '=', track_trace_event_id.id),
        #                  ('transport_reference', '=', transport_ref)], order='event_datetime asc')
        #             if transport_events:
        #                 request.cr.execute(
        #                     """SELECT DISTINCT eq.container_id FROM track_transport_event eq where eq.id in %s  """,
        #                     (tuple(transport_events.ids),))
        #                 events_rec = request.cr.fetchall()
        #                 print("444444", events_rec)
        #         elif cont_id != "null":
        #             eq_event = request.env['track.equipment.event'].sudo().search(
        #                 [('track_trace_event_id', '=', track_trace_event_id.id),
        #                  ('equip_reference', '=', cont_id)], order='event_datetime asc')
        #             print("eq_event 2 ", eq_event)
        #             if eq_event:
        #                 request.cr.execute(
        #                     """ select DISTINCT eq.equip_reference FROM track_equipment_event eq where eq.id in %s  """,
        #                     (tuple(eq_event.ids),))
        #
        #                 events_rec = request.cr.fetchall()
        #                 print("555555", events_rec)
        #             # else:
        #         container_ids = []
        #         for d in events_rec:
        #             if d[0] != None:
        #                 container_ids.append(d[0])
        #         print("container_ids", container_ids)
        #         res = request.render('freightbox.track_trace_equipment_reference_list', {
        #             'container_ids': container_ids,
        #             'trace_trace_event_rec': track_trace_event_id,
        #             'transport_ref': transport_ref,
        #             'transport_document_ref': transport_document_ref,
        #             'cont_id': cont_id,
        #         })
        #         return res
        #     else:
        #         print("ELSE:", equip)
        #         raise UserError(_(equip['message']))
        #         return
        # else:
        #     resp = eq_response.text
        #     raise UserError(resp)
        #     return


    # @http.route(['/xxlist_of_containers/<string:carrier_booking_ref>/tr/<string:transport_ref>'
    #              '/tdr/<string:transport_document_ref>/container/<string:cont_id>'],
    #             type='http', auth="public", website=True)
    # def xxlist_of_containers(self, carrier_booking_ref, transport_ref,
    #                        transport_document_ref, cont_id, access_token=None, **kw):
    #     url = 'http://mother.powerpbox.org:8069/api/api_all_transport_event/'
    #     values = {"carrier_booking": carrier_booking_ref}
    #     data = json.dumps(values)
    #     headers = {
    #         'content-type': 'application/json',
    #     }
    #     response = requests.post(url, data=data, headers=headers)
    #     result = response.json()
    #     result = result.get('result')
    #     result = result.get('Event')
    #     print("list_of_containers result::::::", result)
    #     if result != None:
    #         for key, value in result.items():
    #             track_trace_event_ids = request.env['track.trace.event'].sudo().search([('carrier_booking', '=', key)])
    #             track_trace_event_ids.transport_event_line.sudo().unlink()
    #             track_trace_event_ids.equipment_event_line.sudo().unlink()
    #             track_trace_event_ids.shipment_event_line.sudo().unlink()
    #             if track_trace_event_ids:
    #                 for key1, value1 in value.items():
    #                     if key1 == 'TranportEvent':
    #                         track_trace_event_ids.transport_event_line = value1
    #                     if key1 == 'EquipmentEvent':
    #                         track_trace_event_ids.equipment_event_line = value1
    #                     if key1 == 'ShipmentEvent':
    #                         track_trace_event_ids.shipment_event_line = value1
    #             else:
    #                 track_trace_event_ids = request.env['track.trace.event'].sudo().create({'carrier_booking': key})
    #                 track_trace_event_ids.sudo().write({'is_standalone_tnt': True})
    #                 for key1, value1 in value.items():
    #                     if key1 == 'TranportEvent':
    #                         track_trace_event_ids.transport_event_line = value1
    #                     if key1 == 'EquipmentEvent':
    #                         track_trace_event_ids.equipment_event_line = value1
    #                     if key1 == 'ShipmentEvent':
    #                         track_trace_event_ids.shipment_event_line = value1
    #
    #     track_trace_event = request.env['track.trace.event']
    #     trace_trace_event_rec = track_trace_event.sudo().search(
    #         [('carrier_booking', '=', carrier_booking_ref)])
    #     print("trace_trace_event_rec", trace_trace_event_rec)
    #     if trace_trace_event_rec:
    #         eq_event = request.env['track.equipment.event'].sudo().search(
    #             [('track_trace_event_id', '=', trace_trace_event_rec.id)], order='event_datetime asc')
    #         print("eq_event 1 ::::::::::::::::::", eq_event)
    #         request.cr.execute("""SELECT DISTINCT eq.equip_reference FROM track_equipment_event eq where eq.id in %s  """,(tuple(eq_event.ids),))
    #         events_rec = request.cr.fetchall()
    #         print("333333", events_rec)
    #         if transport_ref != "null":
    #             transport_events = request.env['track.transport.event'].sudo().search(
    #                 [('track_trace_event_id', '=', trace_trace_event_rec.id),
    #                  ('transport_reference', '=', transport_ref)], order='event_datetime asc')
    #             if transport_events:
    #                 request.cr.execute("""SELECT DISTINCT eq.container_id FROM track_transport_event eq where eq.id in %s  """,(tuple(transport_events.ids),))
    #                 events_rec = request.cr.fetchall()
    #                 print("444444", events_rec)
    #         elif cont_id != "null":
    #             eq_event = request.env['track.equipment.event'].sudo().search(
    #                 [('track_trace_event_id', '=', trace_trace_event_rec.id),
    #                  ('equip_reference', '=', cont_id)], order='event_datetime asc')
    #             print("eq_event 2 ", eq_event)
    #             if eq_event:
    #                 request.cr.execute(""" select DISTINCT eq.equip_reference FROM track_equipment_event eq where eq.id in %s  """,(tuple(eq_event.ids),))
    #
    #                 events_rec = request.cr.fetchall()
    #                 print("555555", events_rec)
    #             # else:
    #         container_ids = []
    #         for d in events_rec:
    #             if d[0] != None:
    #                 container_ids.append(d[0])
    #         print("container_ids", container_ids)
    #         res = request.render('freightbox.track_trace_equipment_reference_list', {
    #             'container_ids': container_ids,
    #             'trace_trace_event_rec': trace_trace_event_rec,
    #             'transport_ref': transport_ref,
    #             'transport_document_ref': transport_document_ref,
    #             'cont_id': cont_id,
    #         })
    #     else:
    #         raise UserError(_("No Records found in our System to trace your shipment. Please check your Inputs"))
    #     return res
        if not carrier_booking_ref:
            raise UserError("Provide Carrier Booking Reference / Transport Document Reference to proceed.")
        transport_obj = request.env['transport']
        tnt_obj = request.env['track.trace.event']
        track_trace_event_ids = False
        if tnt_event_created:
            track_trace_event_ids = tnt_obj.sudo().search([
                ('carrier_booking', '=', carrier_booking_ref)
            ], order="id desc")
        else:
            transport_domain = [
                ('carrier_booking', '=', carrier_booking_ref)
            ]
            if cont_id and cont_id != 'null':
                transport_domain.append(('cont_id', '=', cont_id))
            transport = transport_obj.sudo().search(transport_domain, order="id desc")
            if transport:
                track_trace_event_ids = tnt_obj.sudo().search([
                    ('transport_id', 'in', transport.ids)
                ], order="id desc")
            else:
                track_trace_event_ids = tnt_obj.sudo().search([
                    ('carrier_booking', '=', carrier_booking_ref)
                ], order="id desc")
        if track_trace_event_ids:
            # track_trace_event_ids.sudo().write({'is_standalone_tnt': True})
            # print("track_transport_event", track_trace_event_id.transport_event_line,  order='event_datetime asc')
            # eq_event = sorted(track_trace_event_ids.mapped('equipment_event_line').ids)
            # print("eq_event 1 ::::::::::::::::::", eq_event)
            # request.cr.execute(
            #     """SELECT DISTINCT eq.equip_reference FROM track_equipment_event eq where eq.id in %s  """,
            #     (tuple(eq_event),))
            # events_rec = request.cr.fetchall()
            # print("333333", events_rec)
            # if transport_ref != "null":
            #     transport_events = sorted(track_trace_event_ids.mapped('transport_event_line').ids)
            #     if transport_events:
            #         request.cr.execute(
            #             """SELECT DISTINCT eq.container_id FROM track_transport_event eq where eq.id in %s  """,
            #             (tuple(transport_events),))
            #         events_rec = request.cr.fetchall()
            # elif cont_id != "null":
            #     transport_domain.append(('cont_id', '=', cont_id))
            #     transport = transport_obj.sudo().search(transport_domain, order="id desc", limit=1)
            #     eq_event = request.env['track.equipment.event'].sudo().search(
            #         [('track_trace_event_id', 'in', track_trace_event_ids.ids),
            #          ('equip_reference', '=', cont_id)], order='event_datetime asc')
            #     if eq_event:
            #         request.cr.execute(
            #             """ select DISTINCT eq.equip_reference FROM track_equipment_event eq where eq.id in %s  """,
            #             (tuple(eq_event.ids),))
            #
            #         events_rec = request.cr.fetchall()
            #     # else:
            # container_ids = []
            # for d in events_rec:
            #     if d[0] != None:
            #         track_trace_event_rec=track_trace_event_ids.filtered(lambda x: x.transpsort_id.cont_id == d[0])
            #         if track_trace_event_rec:
            #             container_ids.append({d[0]: track_trace_event_rec.id})

            done_cont_ids = []
            container_ids = []
            for tnt_event in track_trace_event_ids:
                if tnt_event.transport_id.cont_id not in done_cont_ids:
                    done_cont_ids.append(tnt_event.transport_id.cont_id)
                    if tnt_event.transport_id and tnt_event.transport_id.cont_id:
                        container_ids.append({tnt_event.transport_id.cont_id: tnt_event.id})
                    else:
                        container_ids.append({carrier_booking_ref: tnt_event.id})
            res = request.render('freightbox.track_trace_equipment_reference_list', {
                'container_ids': container_ids,
                'trace_trace_event_rec': track_trace_event_ids,
                'transport_ref': transport_ref,
                'cont_id': cont_id or carrier_booking_ref,
            })
            return res
        else:
            import datetime
            hostname = socket.gethostname()
            transport_events = []
            dbuuid = request.env['ir.config_parameter'].sudo().get_param('database.uuid')
            username = hostname + '_' + dbuuid
            # transport_vals = {
            #     'transport_user_name': username,
            #     'cont_id': cont_id,
            # }
            transport_name = "From " + kw.get('point_of_stuffing', '') + " To " + kw.get('point_of_destuffing', '')
            fb_trans = request.env['ir.sequence'].sudo().next_by_code('transport.seq') or _('New')
            client_id = request.env['ir.config_parameter'].sudo().sudo().get_param('database.uuid')
            fb_transport_id = fb_trans + '_' + client_id
            res = False
            if cont_id:
                res = request.env['transport'].sudo().create_transport_request_motherserver(cont_id,fb_transport_id)
            else:
                res = request.env['transport'].sudo().create_transport_request_motherserver(carrier_booking_ref, fb_transport_id)
            if res and res.status_code == 200:
                equip = json.loads(res.content)
                if cont_id:
                    body_msg = """
                    Hello,
                    
                    A track n trace standalone request has been made to mother server for Container ID : %s and Carrier Booking ref. : %s.
                    
                    Kindly look into it.
                    
                    Regards.
                    (System Generated Email From Freightbox Backend)
                    """ % (cont_id, carrier_booking_ref)
                else:
                    body_msg = """
                    Hello,

                    A track n trace standalone request has been made to mother server for Container ID : %s and Carrier Booking ref. : %s.

                    Kindly look into it.

                    Regards.
                    (System Generated Email From Freightbox Backend)
                    """ % (carrier_booking_ref, carrier_booking_ref)
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
                print("equip--------------", equip)
                if 'Datas' in equip:
                    print("EQQQ::", equip['Datas'])
                    track_trace_event_id = tnt_obj.sudo().search([('carrier_booking', '=', carrier_booking_ref)],
                                                                 order='id desc', limit=1)
                    if not track_trace_event_id:
                        track_trace_event_id = tnt_obj.sudo().create({'carrier_booking': carrier_booking_ref})
                    print("track_trace_event_id", track_trace_event_id)
                    # track_trace_event_id.transport_event_line.sudo().unlink()
                    # track_trace_event_id.equipment_event_line.sudo().unlink()
                    # track_trace_event_id.shipment_event_line.sudo().unlink()
                    print("EQUIP:::", equip['Datas'][0]['eq'])
                    print("111111:::", len(equip['Datas'][0]['eq']))
                    # print("2222:::", len(eq['Datas'][0]['eq'][0]))
                    for eq in equip['Datas'][0]['eq']:
                        # print("e--", eq)
                        # print("EVENT", eq['equip_event_type_code'])
                        # event_created_datetime = eq['event_created_datetime']
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
                            track_equipment_event_id.sudo().write(equip_events_vals)
                        else:
                            track_equipment_event.sudo().create(equip_events_vals)
                    for transport in equip['Datas'][0]['transport']:
                        print("trans--", transport)
                        print("EVENT", transport['event_created_datetime'])
                        # event_created_datetime = eq['event_created_datetime']
                        import datetime
                        # event_created_datetime = datetime.datetime.strptime(transport['event_created_datetime'],
                        #                                                     "%Y-%m-%d %H:%M:%S.%f")
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
                            track_transport_event_id.sudo().write(transport_events_vals)
                        else:
                            track_transport_event.sudo().create(transport_events_vals)
                    track_trace_event_id.onchange_transport_event_code()
                transport_obj = request.env['transport']
                tnt_obj = request.env['track.trace.event']

                transport_domain = [
                    ('carrier_booking', '=', carrier_booking_ref)
                ]
                if cont_id and cont_id != 'null':
                    transport_domain.append(('cont_id', '=', cont_id))
                transport = transport_obj.sudo().search(transport_domain, order="id desc")
                track_trace_event_ids = tnt_obj.sudo().search([
                    ('transport_id', 'in', transport.ids)
                ], order="id")
                if track_trace_event_ids:
                    done_cont_ids = []
                    container_ids = []
                    for tnt_event in track_trace_event_ids:
                        if tnt_event.transport_id.cont_id not in done_cont_ids:
                            done_cont_ids.append(tnt_event.transport_id.cont_id)
                            if tnt_event.transport_id and tnt_event.transport_id.cont_id:
                                container_ids.append({tnt_event.transport_id.cont_id: tnt_event.id})
                            else:
                                container_ids.append({carrier_booking_ref: tnt_event.id})
                    res = request.render('freightbox.track_trace_equipment_reference_list', {
                        'container_ids': container_ids,
                        'trace_trace_event_rec': track_trace_event_ids,
                        'transport_ref': transport_ref,
                        'cont_id': cont_id or carrier_booking_ref,
                    })
                    return res
                else:
                    return request.render('freightbox.tnt_standalone_msg')
            else:
                raise UserError("Tracking Event Doesn't Exist with carrier booking ref. provide Carrier Booking Ref. and Container ID both and try againg.")
            return

    @http.route(['/shipper_equipment_reference/<int:job_id>'], type='http', auth="public", website=True)
    def shipper_equipment_reference(self, job_id, access_token=None, **kw):
        Job = request.env['job']
        tnt_evnt_obj = request.env['track.trace.event']
        job_rec = Job.sudo().search([('id', '=', job_id)])
        transport_data = []
        por_lat = 0
        por_lon = 0
        pod_lat = 0
        pod_lon = 0
        for transport in job_rec.confirmed_transport_ids:
            por_coords = transport.waypoint_coordinates.split('/')[0] if transport.waypoint_coordinates else '0, 0'
            pod_coords = transport.waypoint_coordinates.split('/')[-1] if transport.waypoint_coordinates else '0, 0'
            por_lat = por_coords.split(',')[1] if por_coords else 0
            por_lon = por_coords.split(',')[0] if por_coords else 0
            pod_lat = pod_coords.split(',')[1] if pod_coords else 0
            pod_lon = pod_coords.split(',')[0] if pod_coords else 0

            # tnt_data = []
            # tnt_event = tnt_evnt_obj.search([('transport_id', '=', transport.id)], order='id desc', limit=1)
            # if tnt_event:
            #     for event in tnt_event.transport_event_line:
            #         msg = ""
            #         if event.transport_event_type_code == "DEPA":
            #             msg = "Will Leave"
            #             if event.location:
            #                 msg = "%s from %s" % (msg, event.location)
            #             if event.mode_of_transport_code:
            #                 msg = "%s by %s " % (msg, event.mode_of_transport_code)
            #         if event.transport_event_type_code == "ARRI":
            #             msg = "Will arrive"
            #             if event.location:
            #                 msg = "%s at %s" % (msg, event.location)
            #             if event.mode_of_transport_code:
            #                 msg = "%s by %s " % (msg, event.mode_of_transport_code)
            #
            #         tnt_data.append(
            #             (
            #                 event.event_datetime,
            #                 event.event_type,
            #                 event.event_classifier_code,
            #                 event.transport_event_type_code,
            #                 event.mode_of_transport_code,
            #                 msg
            #             )
            #         )

            tnt_container_events = []

            # Creating tracking response from tracking events
            track_trace_event = tnt_evnt_obj.sudo().search([('transport_id', '=', transport.id)], order='id desc', limit=1)
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
                    if transport_event.event_datetime and transport_event.event_datetime < datetime.now():
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
                        transport_event.distance or 0,
                        transport_event.speed or 0,
                        transport_event.co2_emmision or 0
                    )
                )
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
                    if equipment_event.event_datetime and equipment_event.event_datetime < datetime.now():
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
            transport_data.append((transport.cont_id, transport.id, tnt_container_events))
        res = request.render('freightbox.track_trace_equipment_reference_form', {
            'transport_data': transport_data,
        })
        return res

    @http.route(['/view_or_update_bol/<int:job_id>'], type='http', auth="public", website=True)
    def view_or_update_bol(self, job_id, access_token=None, **kw):
        hbol_rec = request.env['bill.of.lading'].sudo().search([('job_id', '=', job_id), ('is_house_bill_of_lading', '=', True)], limit=1)
        bol_rec = request.env['bill.of.lading'].sudo().search([('job_id', '=', job_id), ('is_master_bill_of_lading', '=', True)], limit=1)
        qr_image_path = False

        try:

            payment_due = bol_rec.job_id.so_id.partner_id.is_due_exceeded
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            qr_path = "%s/pdf/%s" % (base_url, bol_rec.id)
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
            qr.add_data(qr_path)
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="black", back_color="white")
            file_path = os.path.dirname(__file__)
            qr_image.save(file_path + "/../static/src/img/bol_qr/" + "/%s.jpg" % bol_rec.id)
            qr_image_path = "/freightbox/static/src/img/bol_qr/%s.jpg" % bol_rec.id

        except:
            payment_due = False
        if hbol_rec:
            r = request.render('freightbox.view_or_update_bol_form', {
                'bol_rec': hbol_rec,
                'payment_due': payment_due,
                'qr_image_path': qr_image_path
            })
        else:
            r = request.render('freightbox.view_or_update_bol_form', {
                'bol_rec': bol_rec,
                'payment_due': payment_due,
                'qr_image_path': qr_image_path
            })
        return r

    # @http.route(['/track_trace_brief/<int:job_id>'], type='http', auth="public", website=True)
    # def track_trace_brief(self, job_id, access_token=None, **kw):
    #     job_obj = request.env['job']
    #     rfq_obj = request.env['request.for.quote']
    #     sq_obj = request.env['shipment.quote']
    #     transport_obj = request.env['transport']
    #     si_obj = request.env['shipping.instruction']
    #     bol_obj = request.env['bill.of.lading']
    #     jobs = job_obj.search([('id', '=', job_id)])
    #     tnt_brief_data = []
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
    #         sq_rec = sq_obj.search([('po_id', "=", job.po_id.id)])
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
    #         job_data.append(job and job.inquiry_id and job.inquiry_id.id or False)
    #         final_data = tuple(job_data)
    #         tnt_brief_data.append(final_data)
    #
    #     res = request.render('freightbox.track_trace_brief', {
    #         'tnt_brief_data': tnt_brief_data
    #     })
    #     return res


    @http.route(['/accept_or_reject_sq/<int:sq_id>'], type='http', auth="public", website=True)
    def accept_or_reject_sq(self, sq_id, access_token=None, **kw):
        sq_rec = request.env['shipment.quote'].sudo().browse(sq_id)
        action = request.env.ref('freightbox.action_shipment_quote')
        r = request.render('freightbox.accept_or_reject_sq_form', {
            'sq_rec': sq_rec,
            'action': action,
        })
        return r

    @http.route(['/thank-accept/<int:sq_rec>'], type='http', auth="public", website=True)
    def thanks_accept_sq(self, sq_rec, access_token=None, **kw):
        sq_rec_accept = request.env['shipment.quote'].sudo().browse(sq_rec)
        sq_rec_accept.state = "accepted"
        sq_rec_accept.button_accept()
        return request.render('freightbox.sq_accepted')

    @http.route(['/thank-reject'], type='http', methods=['POST'], auth="public", website=True, csrf=False)
    def thanks_reject_sq(self, **post):
        sq_rec_reject = request.env['shipment.quote'].sudo().search([('id', '=', post['sq_id'])])
        request.env['reject.reason'].sudo().create({
            'sq_id': post['sq_id'],
            'name': post['reason_for_reject'],
        })
        se_rec = request.env['track.shipment.event'].create({
            'shipment_event': 'Shipment',
            'event_created': date.today(),
            'event_datetime': date.today(),
            'event_classifier_code': 'ACT',
            'shipment_event_type_code': 'RECE',
            'reason':'Shipment Quote Reject',
            'booking_id':sq_rec_reject.inquiry_id.id
        })
        # sq_rec_reject.state = "rejected"
        sq_rec_reject.write({'reject_reason': post['reason_for_reject'], 'reject_bool': True, 'state': 'rejected'})
        return request.render('freightbox.sq_rejected')
    
    def _order_get_page_view_values(self, order, access_token, **kwargs):
        print("------------------------ last Call ------------------------")
        values = {
            'sale_order': order,
            'token': access_token,
            'return_url': '/shop/payment/validate',
            'bootstrap_formatting': True,
            'partner_id': order.partner_id.id,
            'report_type': 'html',
            'action': order._get_portal_return_action(),
        }
        if order.company_id:
            values['res_company'] = order.company_id

        if order._has_to_be_paid():
            domain = expression.AND([
                ['&', ('state', 'in', ['enabled', 'test']), ('company_id', '=', order.company_id.id)],
                ['|', ('country_ids', '=', False), ('country_ids', 'in', [order.partner_id.country_id.id])]
            ])
            acquirers = request.env['payment.acquirer'].sudo().search(domain)

            values['acquirers'] = acquirers.filtered(lambda acq: (acq.payment_flow == 'form' and acq.view_template_id) or
                                                     (acq.payment_flow == 's2s' and acq.registration_view_template_id))
            values['pms'] = request.env['payment.token'].search([('partner_id', '=', order.partner_id.id)])
            values['acq_extra_fees'] = acquirers.get_acquirer_extra_fees(order.amount_total, order.currency_id, order.partner_id.country_id.id)

        if order.state in ('draft', 'sent', 'cancel'):
            history = request.session.get('my_quotations_history', [])
        else:
            history = request.session.get('my_orders_history', [])
        values.update(get_records_pager(history, order))

        return values

    @http.route(['/my/orders/<int:order_id>'], type='http', auth="public", website=True)
    def portal_order_page(self, order_id, report_type=None, access_token=None, message=False, download=False, **kw):
        try:
            order_sudo = self._document_check_access('sale.order', order_id, access_token=access_token)
        except (AccessError, MissingError):
            return request.redirect('/my')

        if report_type in ('html', 'pdf', 'text'):
            return self._show_report(model=order_sudo, report_type=report_type,
                                     report_ref='sale.action_report_saleorder', download=download)

        if request.env.user.share and access_token:
            # If a public/portal user accesses the order with the access token
            # Log a note on the chatter.
            today = fields.Date.today().isoformat()
            session_obj_date = request.session.get('view_quote_%s' % order_sudo.id)
            if session_obj_date != today:
                # store the date as a string in the session to allow serialization
                request.session['view_quote_%s' % order_sudo.id] = today
                # The "Quotation viewed by customer" log note is an information
                # dedicated to the salesman and shouldn't be translated in the customer/website lgg
                context = {'lang': order_sudo.user_id.partner_id.lang or order_sudo.company_id.partner_id.lang}
                msg = _('Quotation viewed by customer %s', order_sudo.partner_id.name)
                del context
                _message_post_helper(
                    "sale.order",
                    order_sudo.id,
                    message=msg,
                    token=order_sudo.access_token,
                    message_type="notification",
                    subtype_xmlid="mail.mt_note",
                    partner_ids=order_sudo.user_id.sudo().partner_id.ids,
                )

        backend_url = f'/web#model={order_sudo._name}' \
                      f'&id={order_sudo.id}' \
                      f'&action={order_sudo._get_portal_return_action().id}' \
                      f'&view_type=form'
        values = {
            'sale_order': order_sudo,
            'message': message,
            'report_type': 'html',
            'backend_url': backend_url,
            'res_company': order_sudo.company_id,  # Used to display correct company logo
        }

        # Payment values
        if order_sudo._has_to_be_paid():
            values.update(self._get_payment_values(order_sudo))

        if order_sudo.state in ('draft', 'sent', 'cancel'):
            history_session_key = 'my_quotations_history'
        else:
            history_session_key = 'my_orders_history'

        values = self._get_page_view_values(
            order_sudo, access_token, values, history_session_key, False)

        return request.render('sale.sale_order_portal_template', values)

    def _get_page_view_values(self, document, access_token, values, session_history, no_breadcrumbs, **kwargs):
        """Include necessary values for portal chatter & pager setup (see template portal.message_thread).

        :param document: record to display on portal
        :param str access_token: provided document access token
        :param dict values: base dict of values where chatter rendering values should be added
        :param str session_history: key used to store latest records browsed on the portal in the session
        :param bool no_breadcrumbs:
        :return: updated values
        :rtype: dict
        """
        values['object'] = document

        if access_token:
            # if no_breadcrumbs = False -> force breadcrumbs even if access_token to `invite` users to register if they click on it
            values['no_breadcrumbs'] = no_breadcrumbs
            values['access_token'] = access_token
            values['token'] = access_token  # for portal chatter

        # Those are used notably whenever the payment form is implied in the portal.
        if kwargs.get('error'):
            values['error'] = kwargs['error']
        if kwargs.get('warning'):
            values['warning'] = kwargs['warning']
        if kwargs.get('success'):
            values['success'] = kwargs['success']
        # Email token for posting messages in portal view with identified author
        if kwargs.get('pid'):
            values['pid'] = kwargs['pid']
        if kwargs.get('hash'):
            values['hash'] = kwargs['hash']

        history = request.session.get(session_history, [])
        values.update(get_records_pager(history, document))

        return values

    def _document_check_access(self, model_name, document_id, access_token=None):
        """Check if current user is allowed to access the specified record.

        :param str model_name: model of the requested record
        :param int document_id: id of the requested record
        :param str access_token: record token to check if user isn't allowed to read requested record
        :return: expected record, SUDOED, with SUPERUSER context
        :raise MissingError: record not found in database, might have been deleted
        :raise AccessError: current user isn't allowed to read requested document (and no valid token was given)
        """
        document = request.env[model_name].browse([document_id])
        document_sudo = document.with_user(SUPERUSER_ID).exists()
        if not document_sudo:
            raise MissingError(_("This document does not exist."))
        try:
            document.check_access_rights('read')
            document.check_access_rule('read')
        except AccessError:
            if not access_token or not document_sudo.access_token or not consteq(document_sudo.access_token, access_token):
                raise
        return document_sudo

    # @http.route(['/my/orders/<int:order_id>'], type='http', auth="public", website=True)
    # def portal_order_page(self, order_id, report_type=None, access_token=None, message=False, download=False, **kw):
    #     order_sudo = request.env['sale.order'].sudo().browse(order_id)
    #     values = {
    #         'sale_order': order_sudo,
    #         'token': access_token,
    #         'return_url': '/shop/payment/validate',
    #         'bootstrap_formatting': True,
    #         'partner_id': order_sudo.partner_id.id,
    #         'report_type': 'html',
    #         'action': order_sudo._get_portal_return_action(),
    #     }
    #     values = self._order_get_page_view_values(order_sudo, access_token, **kw)
    #     values['message'] = message
    #     return request.render('sale.sale_order_portal_template', values)

    @http.route(['/create_si/transportations-/<int:transport_id>'], type='http', auth="public", website=True)
    def create_si_transportations(self, transport_id, access_token=None, **kw):
        transport = request.env['transport']
        user = request.env.user
        transport_rec = transport.sudo().browse(transport_id)
        job_rec = transport_rec.job_id
        si_template_ids = request.env['si.templates'].sudo().search(['|', ('si_user_id', '=', user.id), ('is_data_template', '=', True)])
        res = request.render('freightbox.create_new_si', {
            'job_rec': job_rec,
            'transport_rec': transport_rec,
            'user_name': user,
            'si_template_ids': si_template_ids,
        })
        return res

    @http.route(['/create_new_bol/<int:job_id>'], type='http', auth="public", website=True)
    def create_new_bol(self, job_id, access_token=None, **kw):
        hbol_rec = request.env['bill.of.lading'].sudo().search([('job_id', '=', job_id), ('is_house_bill_of_lading', '=', True)], limit=1)
        bol_rec = request.env['bill.of.lading'].sudo().search([('job_id', '=', job_id), ('is_master_bill_of_lading', '=', True)], limit=1)
        qr_image_path = False

        try:

            payment_due = bol_rec.job_id.so_id.partner_id.is_due_exceeded
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            qr_path = "%s/pdf/%s" % (base_url, bol_rec.id)
            qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=10, border=4)
            qr.add_data(qr_path)
            qr.make(fit=True)
            qr_image = qr.make_image(fill_color="black", back_color="white")
            file_path = os.path.dirname(__file__)
            qr_image.save(file_path + "/../static/src/img/bol_qr/" + "/%s.jpg" % bol_rec.id)
            qr_image_path = "/freightbox/static/src/img/bol_qr/%s.jpg" % bol_rec.id

        except:
            payment_due = False

        if hbol_rec:
            r = request.render('freightbox.create_bol_form', {
                'bol_rec': hbol_rec,
                'payment_due': payment_due,
                'qr_image_path': qr_image_path
            })
        else:
            r = request.render('freightbox.create_bol_form', {
                'bol_rec': bol_rec,
                'payment_due': payment_due,
                'qr_image_path': qr_image_path
            })
        return r

    @http.route(['/view_inquiry_form/<int:inquiry_id>'], type='http', auth="public", website=True)
    def view_inquiry(self, inquiry_id, access_token=None, **kw):
        crm = request.env['crm.lead']
        enquiry_rec = crm.sudo().browse(inquiry_id)
        res = request.render('freightbox.view_enquiry_form', {
            'enquiry_rec': enquiry_rec,
        })
        return res

    @http.route(['/si_template_values'], type='json', auth="public", method=['POST'], website=True)
    def si_template_values(self, si_template, **kwargs):
        si_template_obj = request.env['si.templates']
        si_template_rec = si_template_obj.sudo().search([('id', '=', si_template)])
        count_cargo_items = len(si_template_rec.si_template_cargo_items_line)
        cargo_line_values = []
        for c in si_template_rec.si_template_cargo_items_line:
            cargo_line_values.append({
                'cargo_line_items_id': c.cargo_line_items_id,
                'shipping_marks': c.shipping_marks,
                'carrier_booking_reference': c.carrier_booking_reference,
                'description_of_goods': c.description_of_goods,
                'hs_code': c.hs_code,
                'number_of_packages': c.number_of_packages,
                'weight': c.weight,
                'volume': c.volume,
                'weight_unit': c.weight_unit,
                'volume_unit': c.volume_unit,
                # 'equipment_reference': c.equipment_reference,
                'package_code': c.package_code,
            })
        count_tq_items = len(si_template_rec.si_template_transport_equipment_line)
        tq_line_values = []
        for tq in si_template_rec.si_template_transport_equipment_line:
            tq_line_values.append({
                'equipment_reference': tq.equipment_reference_id,
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

        count_dp_items = len(si_template_rec.si_template_document_parties_line)
        dp_line_values = []
        for dp in si_template_rec.si_template_document_parties_line:
            dp_line_values.append({
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
        count_sl_items = len(si_template_rec.si_template_shipment_location_line)
        sl_line_values = []
        for sl in si_template_rec.si_template_shipment_location_line:
            sl_line_values.append({
                'location_type': sl.location_type.name,
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
                'displayed_name': sl.displayed_name,
                'shipment_location_array_created_by': sl.shipment_location_array_created_by,
            })
        count_rc_items = len(si_template_rec.si_template_references_line)
        rc_line_values = []
        for rc in si_template_rec.si_template_references_line:
            rc_line_values.append({
                'reference_type': rc.reference_type,
                'reference_value': rc.reference_value,
                'references_array_created_by': rc.references_array_created_by,
            })
        si_template_rec_values = {
            'si_template_id': si_template_rec.id,
            'name': si_template_rec.name,
            'transport_document_type_code': si_template_rec.transport_document_type_code,
            'number_of_originals': si_template_rec.number_of_originals,
            'number_of_copies': si_template_rec.number_of_copies,
            'pre_carriage_under_shippers_responsibility': si_template_rec.pre_carriage_under_shippers_responsibility,
            'carrier_booking_reference': si_template_rec.carrier_booking_reference,
            'location_name': si_template_rec.location_name,
            'un_location_code': si_template_rec.un_location_code,
            'city_name': si_template_rec.city_name,
            'state_region': si_template_rec.state_region,
            'country': si_template_rec.country,
            'count_cargo_items': count_cargo_items,
            'cargo_line_values': cargo_line_values,
            'count_tq_items': count_tq_items,
            'tq_line_values': tq_line_values,
            'count_dp_items': count_dp_items,
            'dp_line_values': dp_line_values,
            'count_sl_items': count_sl_items,
            'sl_line_values': sl_line_values,
            'count_rc_items': count_rc_items,
            'rc_line_values': rc_line_values,
        }
        return si_template_rec_values

    @http.route(['/open_si-/<int:job_si_id>/job-/<int:job_id>'], type='http', auth="public", website=True)
    def open_si(self, job_si_id, job_id, access_token=None, **kw):
        vals = {}
        shipping_instruction = request.env['shipping.instruction']
        rec = shipping_instruction.sudo().browse(job_si_id)
        transport_rec = rec.transport_id
        job_rec = request.env['job'].sudo().browse(job_id)
        si_template_ids = request.env['si.templates'].sudo().search([])
        user = request.env.user
        vals.update({
            'si_rec': rec,
            'job_rec': job_rec,
            'transport_rec': transport_rec,
            'user_name': user,
            'si_template_ids': si_template_ids,
        })
        res = request.render('freightbox.create_new_si', vals)
        return res

    @http.route(['/update_prev_sent_si/<int:si_id>'], type='http', auth="public", website=True)
    def update_si(self, si_id, access_token=None, **kw):
        vals = {}
        shipping_instruction = request.env['shipping.instruction']
        rec = shipping_instruction.sudo().browse(si_id)
        vals.update({
            'si_rec': rec,
        })
        res = request.render('freightbox.shipping_instruction_si_update', vals)
        return res

    @http.route(['/view_prev_sent_si/<int:si_id>'], type='http', auth="public", website=True)
    def update_si_view(self, si_id, access_token=None, **kw):
        vals = {}
        shipping_instruction = request.env['shipping.instruction']
        rec = shipping_instruction.sudo().browse(si_id)
        vals.update({
            'si_rec': rec,
        })
        res = request.render('freightbox.view_update_si', vals)
        return res

    @http.route(['/view_or_update_si/<int:job_id>'], type='http', auth="public", website=True)
    def create_si_for_transport(self, job_id, access_token=None, **kw):
        job_rec = request.env['job'].sudo().browse(job_id)
        r = request.render('freightbox.view_or_update_si_form', {
            'job_rec': job_rec,
        })
        return r

    @http.route('/shipment_information', type='http', auth='public', website=True)
    def shipment_information(self, **post):
        values = {}
        user = request.env.user
        user_logged = True
        if user.name == 'Public user':
            user_logged = False
        if request.session.uid:
            partner = request.env.user.partner_id
            if partner:
                # sq = request.env['crm.lead'].sudo().search([('partner_id', '=', partner.id)])

                # if request.env.user.has_group(GROUP_SYSTEM):
                #     inquiry_ids = request.env['crm.lead'].sudo().search([('is_freight_box_crm', '=', True)])
                #     # job_ids = request.env['job'].sudo().search([('job_status', 'not in', ['inactive'])])
                #     job_ids = request.env['job'].sudo().search([])
                #     si_ids = request.env['shipping.instruction'].sudo().search(
                #         [('is_shipping_instruction', '=', True)])
                # else:
                #     job_ids = request.env['job'].sudo().search(
                #         [('shipper_id', '=', partner.id)])
                #     si_ids = request.env['shipping.instruction'].sudo().search(
                #         [('is_shipping_instruction', '=', True), ('shipper_id', '=', partner.id)])
                #     inquiry_ids = request.env['crm.lead'].sudo().search([('partner_id', '=', partner.id)])
                # print("job_ids:::::::::", job_ids)
                # # job_ids.reverse()
                # print("afterrrr", job_ids)
                # values.update({
                #     'inquiry_ids': inquiry_ids,
                #     'si_ids': si_ids,
                #     'job_ids': job_ids,
                #     'user_logged': user_logged,
                # })
                page_vals = []
                if request.env.user.has_group(GROUP_SYSTEM):
                    inquiry_ids = request.env['crm.lead'].sudo().search([('is_freight_box_crm', '=', True)])
                else:
                    job_ids = request.env['job'].sudo().search(
                        [('shipper_id', '=', partner.id)])
                    si_ids = request.env['shipping.instruction'].sudo().search(
                        [('is_shipping_instruction', '=', True), ('shipper_id', '=', partner.id)])
                    inquiry_ids = request.env['crm.lead'].sudo().search([('partner_id', '=', partner.id)])
                vals_list  = []
                for inquiry in inquiry_ids:
                    so_ids = request.env['sale.order'].sudo().search([('so_inquiry_id', '=', inquiry.id)], order="id desc", limit=1)
                    si_ids = request.env['shipping.instruction'].sudo().search([('si_inquiry_no', '=', inquiry.id)])
                    # sq_ids = request.env['shipment.quote'].sudo().search([('inquiry_id', "=", inquiry.id), ('allow_shipper_to_approve', '=', True)], order="id desc", limit=1)
                    sq_id = request.env['shipment.quote'].sudo().search([('inquiry_id', "=", inquiry.id)], order="id desc", limit=1)
                    job_ids = request.env['job'].sudo().search([('inquiry_id', '=', inquiry.id)])
                    bol_ids = request.env['bill.of.lading'].sudo().search([('job_id', 'in', job_ids.ids)], order='id desc')
                    transport_ids = request.env['transport'].sudo().search([('inquiry_id', "=", inquiry.id)])
                    confirmed_transport_ids = request.env['transport'].sudo().search([('id', 'in', transport_ids.ids), ('state', '=', 'confirm')])
                    hold_jobs = job_ids.filtered(lambda job: job.state == 'hold')
                    hold_bols = bol_ids.filtered(lambda job: job.state == 'hold')
                    allow_create_si = confirmed_transport_ids.filtered(lambda ct: ct.create_si_by_shipper)

                    invoice_ids = request.env['account.move'].sudo().search([('booking_id', "=", inquiry.booking_id)])

                    si_color = "grey"
                    si_message = "grey_1"
                    # si_to_attend = si_ids.filtered(lambda si_rec: si_rec.state in ['open', 'update in progress'])
                    # rejected_si = si_ids.filtered(lambda si_line: si_line.state in ['rejected', 'cancelled'])
                    missing_si = False
                    for transport in transport_ids:
                        transport_si = request.env['shipping.instruction'].search([('transport_id', '=', transport.id)])
                        if not transport_si:
                            missing_si = True

                    if not si_ids and missing_si:
                        if allow_create_si:
                            si_color = "amber"
                            si_message = "At least one or more Shipping Instruction(s) need to be created / accepted."
                        else:
                            si_color = "grey"
                            si_message = "grey_2"
                    elif si_ids and missing_si:
                        si_color = "amber"
                        si_message = "One or more Shipping Instruction(s) created."
                    else:
                        not_created_si = False
                        for conf_transport_id in confirmed_transport_ids:
                            if conf_transport_id not in si_ids.mapped('transport_id'):
                                not_created_si = True
                                break
                        if not_created_si:
                            si_color = "grey"
                            si_message = "grey_3"
                        if si_ids and any(si_id.state == 'rejected' for si_id in si_ids):
                            si_color = "red"
                            si_message = "At least one or more Shipping Instruction(s) rejected."
                        elif si_ids and any(si_id.state != 'accepted' for si_id in si_ids):
                            si_color = "amber"
                            si_message = "At least one or more Shipping Instruction(s) need to be accepted."
                        elif si_ids and all(si_id.state == 'accepted' for si_id in si_ids):
                            si_color = "green"
                            si_message = "All Shipping Instructions are accepted."


                    vals_list_tmp = [inquiry]
                    if sq_id:
                        vals_list_tmp.append(sq_id)
                    else:
                        vals_list_tmp.append('false')
                    if so_ids:
                        vals_list_tmp.append(so_ids)
                    else:
                        vals_list_tmp.append('false')
                    if si_ids:
                        vals_list_tmp.append(si_ids)
                    else:
                        vals_list_tmp.append('false')
                    if bol_ids:
                        vals_list_tmp.append(bol_ids[0])
                    else:
                        vals_list_tmp.append('false')
                    if inquiry.job_id:
                        vals_list_tmp.append(inquiry.job_id)
                    else:
                        vals_list_tmp.append('false')
                    if allow_create_si:
                        vals_list_tmp.append('true')
                    else:
                        vals_list_tmp.append('false')
                    if confirmed_transport_ids:
                        vals_list_tmp.append('true')
                    else:
                        vals_list_tmp.append('false')
                    vals_list_tmp.append(si_color)
                    vals_list_tmp.append(si_message)
                    if hold_jobs:
                        vals_list_tmp.append('true')
                    else:
                        vals_list_tmp.append('false')
                    if hold_bols:
                        vals_list_tmp.append('true')
                    else:
                        vals_list_tmp.append('false')
                    vals_list_tmp.append(len(transport_ids.ids))
                    if bol_ids:
                        mbol_ids = bol_ids.filtered(lambda bol: bol.is_master_bill_of_lading)
                        if mbol_ids:
                            vals_list_tmp.append(mbol_ids[0].transport_document_reference)
                        else:
                            vals_list_tmp.append(bol_ids[0].transport_document_reference)
                    else:
                        vals_list_tmp.append('false')
                    if inquiry.job_id:
                        vals_list_tmp.append(inquiry.job_id.carrier_booking)
                    else:
                        vals_list_tmp.append('false')
                    if inquiry.job_id:
                        vals_list_tmp.append(int(inquiry.job_id.confirmed_no_of_container))
                    else:
                        vals_list_tmp.append(0)
                    
                    # if si_to_attend:
                    #     vals_list_tmp.append('true')
                    # else:
                    #     vals_list_tmp.append('false')
                    # if rejected_si:
                    #     vals_list_tmp.append('true')
                    # else:
                    #     vals_list_tmp.append('false')
                    # if not_created_si:
                    #     vals_list_tmp.append('true')
                    # else:
                    #     vals_list_tmp.append('false')
                    vals_list.append(vals_list_tmp)
                    if sq_id and sq_id.state:
                        vals_list_tmp.append(sq_id.state)
                    else:
                        vals_list_tmp.append("")
                    if so_ids:
                        vals_list_tmp.append(so_ids.state)
                    else:
                        vals_list_tmp.append("")
                    if bol_ids:
                        vals_list_tmp.append(bol_ids[0].state)
                    else:
                        vals_list_tmp.append('false')
                    if job_ids:
                        vals_list_tmp.append(job_ids[0].id)
                    else:
                        vals_list_tmp.append('false')

                    #For Invoice List	
                    if invoice_ids:	
                        vals_list_tmp.append(invoice_ids)	
                    else:	
                        vals_list_tmp.append('false')	
                    #For Payment Status	
                    paid = True	
                    for pay in invoice_ids:	
                        if pay.payment_state != 'paid':	
                            paid = False	
                    vals_list_tmp.append(paid)

                value_tuple = tuple(vals_list)
                values.update({
                    'user_logged': user_logged,
                    'value_tuple': value_tuple
                })
        print("values SI", values)
        r = request.render('freightbox.shipping_instruction', values)
        return r

    @http.route(['/si_update_vals'], type='json', auth="public", method=['POST'], website=True)
    def si_update_vals(self, update_parent_vals, updated_cargo_vals, updated_tq_vals, updated_dp_vals, updated_sl_vals,
                       updated_rc_vals, **kwargs):
        ShippingInstruction = request.env['shipping.instruction']
        current_si = update_parent_vals[0]['current_si_id']
        si_rec = ShippingInstruction.sudo().search([('id', '=', current_si)])
        rec = si_rec.sudo().write({
            'transport_document_type_code': update_parent_vals[0]['transport_document_type_code'],
            'is_shipped_onboard_type': update_parent_vals[0]['is_shipper_owned'],
            'number_of_originals': update_parent_vals[0]['number_of_originals'],
            'number_of_copies': update_parent_vals[0]['number_of_copies'],
            'pre_carriage_under_shippers_responsibility': update_parent_vals[0][
                'pre_carriage_under_shippers_responsibility'],
            'is_electronic': update_parent_vals[0]['is_electronic'],
            'carrier_booking_reference': update_parent_vals[0]['carrier_booking_reference'],
            'is_charges_displayed': update_parent_vals[0]['is_charges_displayed'],
            'location_name': update_parent_vals[0]['inv_payable_location_name'],
            'un_location_code': update_parent_vals[0]['inv_payable_un_location_code'],
            'city_name': update_parent_vals[0]['inv_payable_city_name_update'],
            'state_region': update_parent_vals[0]['inv_payable_state_region_update'],
            'country': update_parent_vals[0]['inv_payable_country_update'],
            'si_updated_by': update_parent_vals[0]['update_si_created_by'],
            'is_shipping_instruction': True,
            'update_si': False,
            'state': "updated"
        })
        cargo_update_table_count = update_parent_vals[0]['cargo_table_update_count']
        if cargo_update_table_count > 0:
            si_rec.cargo_items_line.unlink()
            for c in updated_cargo_vals:
                si_rec.cargo_items_line.sudo().create({
                    'cargo_line_id': si_rec.id,
                    'cargo_line_items_id': c['cargo_line_item_id'],
                    'shipping_marks': c['shipping_marks'],
                    'carrier_booking_reference': c['carrier_booking_reference'],
                    'description_of_goods': c['description_of_goods'],
                    'hs_code': c['hs_code'],
                    'number_of_packages': c['no_of_packages'],
                    'weight': c['weight'],
                    'volume': c['volume'],
                    'weight_unit': c['weight_unit'],
                    'volume_unit': c['volume_unit'],
                    'package_code': c['package_code'],
                    'equipment_reference': c['equipment_reference'],
                    'cargo_array_created_by': c['cargo_array_created_by'],
                })
        tq_update_table_count = update_parent_vals[0]['tq_table_update_count']
        if tq_update_table_count > 0:
            si_rec.transport_equipment_line.unlink()
            for tq in updated_tq_vals:
                si_rec.transport_equipment_line.sudo().create({
                    'transport_equipment_line_id': si_rec.id,
                    'equipment_reference_id': tq['equipment_reference'],
                    'weight_unit': tq['new_wt_unit_update_tq'],
                    'cargo_gross_weight': tq['new_cgw_update_tq'],
                    'container_tare_weight': tq['new_ctw_update_tq'],
                    'iso_equipment_code': tq['new_iso_eq_code_update_tq'],
                    'is_shipper_owned': tq['new_is_shipper_owned_update_tq'],
                    'temperature_min': tq['new_temp_min_update_tq'],
                    'temperature_max': tq['new_temp_max_update_tq'],
                    'temperature_unit': tq['new_temp_unit_update_tq'],
                    'humidity_min': tq['new_humidity_min_update_tq'],
                    'humidity_max': tq['new_humidity_max_update_tq'],
                    'ventilation_min': tq['new_ventilation_min_update_tq'],
                    'ventilation_max': tq['new_ventilation_max_update_tq'],
                    'seal_number': tq['new_seal_no_update_tq'],
                    'seal_source': tq['new_seal_source_update_tq'],
                    'seal_type': tq['new_seal_type_update_tq'],
                    'transport_equipment_array_created_by': tq['transport_equipment_array_created_by'],
                })
        dp_table_update_count = update_parent_vals[0]['dp_table_update_count']
        if dp_table_update_count > 0:
            si_rec.document_parties_line.unlink()
            for dp in updated_dp_vals:
                si_rec.document_parties_line.sudo().create({
                    'document_parties_line_id': si_rec.id,
                    'party_name_id': dp['new_party_name_update_dp'],
                    'tax_reference_1': dp['new_tax_reference_1_update_dp'],
                    'public_key': dp['new_public_key_update_dp'],
                    'street': dp['new_street_update_dp'],
                    'street_number': dp['new_street_number_update_dp'],
                    'floor': dp['new_floor_update_dp'],
                    'post_code': dp['new_post_code_update_dp'],
                    'city': dp['new_city_update_dp'],
                    'state_region': dp['new_state_region_update_dp'],
                    'country': dp['new_country_update_dp'],
                    'tax_reference_2': dp['new_tax_reference_2_update_dp'],
                    'nmfta_code': dp['new_nmfta_code_update_dp'],
                    'party_function': dp['new_party_function_update_dp'],
                    'address_line': dp['new_address_line_update_dp'],
                    'name': dp['new_name_update_dp'],
                    'email': dp['new_email_update_dp'],
                    'phone': dp['new_phone_update_dp'],
                    'is_to_be_notified': dp['new_is_to_be_notified_update_dp'],
                    'document_parties_array_created_by': dp['document_parties_array_created_by'],
                })
        sl_table_update_count = update_parent_vals[0]['sl_table_update_count']
        if sl_table_update_count > 0:
            si_rec.shipment_location_line.unlink()
            for sl in updated_sl_vals:
                location_type_rec = request.env['location.type'].sudo().search([
                    ('name', '=', sl['new_location_type_update_sl'])])
                si_rec.shipment_location_line.sudo().create({
                    'shipment_location_line_id': si_rec.id,
                    'location_type': location_type_rec.id,
                    'location_name': sl['new_location_name_update_sl'],
                    'latitude': sl['new_latitude_update_sl'],
                    'longitude': sl['new_longitude_update_sl'],
                    'un_location_code': sl['new_un_location_code_update_sl'],
                    'street_name': sl['new_street_name_code_update_sl'],
                    'street_number': sl['new_street_number_code_update_sl'],
                    'floor': sl['new_floor_update_sl'],
                    'post_code': sl['new_post_code_update_sl'],
                    'city_name': sl['new_city_name_update_sl'],
                    'state_region': sl['new_state_region_update_sl'],
                    'country': sl['new_country_update_sl'],
                    'displayed_name': sl['new_displayed_name_update_sl'],
                    'shipment_location_array_created_by': sl['shipment_location_array_created_by'],
                })
        rc_table_update_count = update_parent_vals[0]['rc_table_update_count']
        if rc_table_update_count > 0:
            si_rec.references_line.unlink()
            for rc in updated_rc_vals:
                si_rec.references_line.sudo().create({
                    'references_line_id': si_rec.id,
                    'reference_type': rc['new_reference_type_update_rc'],
                    'reference_value': rc['new_reference_value_update_rc'],
                    'references_array_created_by': rc['references_array_created_by'],
                })
        vals = {
            'cargo_items_line': si_rec.cargo_items_line,
            'transport_equipment_line': si_rec.transport_equipment_line,
            'document_parties_line': si_rec.document_parties_line,
            'shipment_location_line': si_rec.shipment_location_line,
            'references_line': si_rec.references_line,
        }
        si_rec.sudo().write(vals)
        if rec:
            return True
        else:
            return False

    @http.route(['/si_vals'], type='json', auth="public", method=['POST'], website=True)
    def si_vals(self, parent_vals, cargo_vals, tq_vals, dp_vals, sl_vals, rc_vals, **kwargs):
        ShippingInstruction = request.env['shipping.instruction']
        cargo_table_count = parent_vals[0]['cargo_table_count']
        si_saved_id = parent_vals[0]['saved_si_id']
        inquiry_rec = False
        si_create_inquiry_no = parent_vals[0]['si_create_inquiry_no']
        if si_create_inquiry_no:
            inquiry_rec = request.env['crm.lead'].sudo().search([('booking_id', '=', si_create_inquiry_no)]).id
        if si_saved_id:
            si_rec = ShippingInstruction.sudo().search([('id', '=', si_saved_id)])
            si_rec.sudo().write({
                'transport_document_type_code': parent_vals[0]['transport_document_type_code'],
                'is_shipped_onboard_type': parent_vals[0]['is_shipper_owned'],
                'number_of_originals': parent_vals[0]['number_of_originals'],
                'number_of_copies': parent_vals[0]['number_of_copies'],
                'pre_carriage_under_shippers_responsibility': parent_vals[0][
                    'pre_carriage_under_shippers_responsibility'],
                'is_electronic': parent_vals[0]['is_electronic'],
                'carrier_booking_reference': parent_vals[0]['carrier_booking_reference'],
                'is_charges_displayed': parent_vals[0]['is_charges_displayed'],
                'location_name': parent_vals[0]['inv_payable_location_name'],
                'un_location_code': parent_vals[0]['inv_payable_un_location_code'],
                'city_name': parent_vals[0]['inv_payable_city_name'],
                'state_region': parent_vals[0]['inv_payable_state_region'],
                'country': parent_vals[0]['inv_payable_country'],
                'is_shipping_instruction': True,
                'si_created_by': parent_vals[0]['si_created_by_parent_val'],
                'si_inquiry_no': inquiry_rec,
                'is_saved': parent_vals[0]['is_saved'],
                'state': parent_vals[0]['state'],
                'saved_si_name': parent_vals[0]['saved_si_name'],
                'shipper_id': request.env.user.partner_id.id,
                # 'si_sequence_id': _('New'),
                'transport_container_id': parent_vals[0]['saved_cont_id'],
            })
        else:
            si_rec = ShippingInstruction.sudo().create({
                'transport_document_type_code': parent_vals[0]['transport_document_type_code'],
                'is_shipped_onboard_type': parent_vals[0]['is_shipper_owned'],
                'number_of_originals': parent_vals[0]['number_of_originals'],
                'number_of_copies': parent_vals[0]['number_of_copies'],
                'pre_carriage_under_shippers_responsibility': parent_vals[0][
                    'pre_carriage_under_shippers_responsibility'],
                'is_electronic': parent_vals[0]['is_electronic'],
                'carrier_booking_reference': parent_vals[0]['carrier_booking_reference'],
                'is_charges_displayed': parent_vals[0]['is_charges_displayed'],
                'location_name': parent_vals[0]['inv_payable_location_name'],
                'un_location_code': parent_vals[0]['inv_payable_un_location_code'],
                'city_name': parent_vals[0]['inv_payable_city_name'],
                'state_region': parent_vals[0]['inv_payable_state_region'],
                'country': parent_vals[0]['inv_payable_country'],
                'is_shipping_instruction': True,
                'si_created_by': parent_vals[0]['si_created_by_parent_val'],
                'si_inquiry_no': inquiry_rec,
                'is_saved': parent_vals[0]['is_saved'],
                'state': parent_vals[0]['state'],
                'saved_si_name': parent_vals[0]['saved_si_name'],
                'shipper_id': request.env.user.partner_id.id,
                'si_sequence_id':  _('New'),
                'transport_container_id': parent_vals[0]['saved_cont_id'],
            })
        job_id = parent_vals[0]['si_create_job_id']
        if job_id:
            job_rec = request.env['job'].sudo().search([('id', '=', job_id)])
            created_si_ids = job_rec.shipping_instruction_ids.ids
            created_si_ids.append(si_rec.id)
            if created_si_ids:
                job_rec.sudo().write({'state': 'si_created'})
            job_rec.sudo().write({'shipping_instruction_ids': [(6, 0, created_si_ids)]})
            si_rec.sudo().write({'job_id': job_rec.id,
                                 'booking_user_id': job_rec.booking_user_id.id})
        si_transport_id = parent_vals[0]['si_create_transport_id']
        if si_transport_id:
            transport_rec = request.env['transport'].sudo().search([('id', '=', si_transport_id)])
            if transport_rec:
                transport_rec.sudo().write({'shipping_instruction_id': si_rec.id})
                si_rec.sudo().write({'transport_id': transport_rec.id})
        if si_rec:
            si_rec.cargo_items_line.sudo().unlink()
            if cargo_table_count > 0:
                for line in cargo_vals:
                    si_rec.cargo_items_line.sudo().create({
                        'cargo_line_id': si_rec.id,
                        'cargo_line_items_id': line['cargo_line_item_id'],
                        'shipping_marks': line['shipping_marks'],
                        'carrier_booking_reference': line['carrier_booking_reference'],
                        'description_of_goods': line['description_of_goods'],
                        'hs_code': line['hs_code'],
                        'number_of_packages': line['no_of_packages'],
                        'weight': line['weight'],
                        'volume': line['volume'],
                        'weight_unit': line['weight_unit'],
                        'volume_unit': line['volume_unit'],
                        'package_code': line['package_code'],
                        'equipment_reference': line['equipment_reference'],
                        'cargo_array_created_by': line['cargo_array_created_by'],
                        'cargo_line_items_row_id': line['row_count_cargo'],
                    })
            tq_table_count = parent_vals[0]['tq_table_count']
            si_rec.transport_equipment_line.sudo().unlink()
            if tq_table_count > 0:
                for tq in tq_vals:
                    si_rec.transport_equipment_line.sudo().create({
                        'transport_equipment_line_id': si_rec.id,
                        'equipment_reference_id': tq['equipment_reference'],
                        'weight_unit': tq['weight_unit_tq'],
                        'cargo_gross_weight': tq['cargo_gross_weight'],
                        'container_tare_weight': tq['container_tare_weight'],
                        'iso_equipment_code': tq['iso_equipment_code'],
                        'is_shipper_owned': tq['is_shipper_owned'],
                        'temperature_min': tq['temperature_min'],
                        'temperature_max': tq['temperature_max'],
                        'temperature_unit': tq['temperature_unit'],
                        'humidity_min': tq['humidity_min'],
                        'humidity_max': tq['humidity_max'],
                        'ventilation_min': tq['ventilation_min'],
                        'ventilation_max': tq['ventilation_max'],
                        'seal_number': tq['seal_number'],
                        'seal_source': tq['seal_source'],
                        'seal_type': tq['seal_type'],
                        'transport_equipment_array_created_by': tq['tq_array_created_by'],
                        'transport_equipment_row_id': tq['row_count_tq'],
                    })
            dp_table_count = parent_vals[0]['dp_table_count']
            si_rec.document_parties_line.sudo().unlink()
            if dp_table_count > 0:
                for dp in dp_vals:
                    si_rec.document_parties_line.sudo().create({
                        'document_parties_line_id': si_rec.id,
                        'party_name_id': dp['party_name'],
                        'tax_reference_1': dp['tax_reference_1_dp'],
                        'public_key': dp['public_key'],
                        'street': dp['street'],
                        'street_number': dp['street_number'],
                        'floor': dp['floor'],
                        'post_code': dp['post_code'],
                        'city': dp['city'],
                        'state_region': dp['state_region'],
                        'country': dp['country'],
                        'tax_reference_2': dp['tax_reference_2'],
                        'nmfta_code': dp['nmfta_code'],
                        'party_function': dp['party_function'],
                        'address_line': dp['address_line'],
                        'name': dp['name'],
                        'email': dp['email'],
                        'phone': dp['phone'],
                        'is_to_be_notified': dp['is_to_be_notified'],
                        'document_parties_array_created_by': dp['dp_array_created_by'],
                        'document_parties_row_id': dp['row_count_dp'],
                    })
            sl_table_count = parent_vals[0]['sl_table_count']
            si_rec.shipment_location_line.sudo().unlink()
            if sl_table_count > 0:
                for sl in sl_vals:
                    location_type_rec = request.env['location.type'].sudo().search([('name', '=', sl['location_type'])])
                    si_rec.shipment_location_line.sudo().create({
                        'shipment_location_line_id': si_rec.id,
                        'location_type': location_type_rec.id,
                        'displayed_name': sl['displayed_name'],
                        'location_name': sl['location_name'],
                        'latitude': sl['latitude'],
                        'longitude': sl['longitude'],
                        'un_location_code': sl['un_location_code'],
                        'street_name': sl['street_name'],
                        'street_number': sl['street_number'],
                        'floor': sl['floor'],
                        'post_code': sl['post_code'],
                        'city_name': sl['city_name'],
                        'state_region': sl['state_region'],
                        'country': sl['country'],
                        'shipment_location_array_created_by': sl['sl_array_created_by'],
                        'shipment_location_row_id': sl['row_count_sl'],
                    })
            rc_table_count = parent_vals[0]['rc_table_count']
            si_rec.references_line.sudo().unlink()
            if rc_table_count > 0:
                for rc in rc_vals:
                    si_rec.references_line.sudo().create({
                        'references_line_id': si_rec.id,
                        'reference_type': rc['reference_type'],
                        'reference_value': rc['reference_value'],
                        'references_array_created_by': rc['ref_array_created_by'],
                        'shipping_references_row_id': rc['row_count_rc'],
                    })
            return {'si_rec_id': si_rec.id}
        else:
            return False

    @http.route(['/bol_vals'], type='json', auth="public", method=['POST'], website=True)
    def bol_vals(self, parent_vals, **kwargs):
        print("............................ in",parent_vals)
        print("............................ in",parent_vals[0])
        ShippingInstruction = request.env['bill.of.lading']
        
        bol_rec = ShippingInstruction.sudo().search([('id', '=', parent_vals[0]['id'])])
        print("............................ bol_rec",bol_rec)
        print("----------------------- parent_vals[0]['pre_longitude']",parent_vals[0]['pre_longitude'])
        if bol_rec:
            print("............................ in")
            vals = {
                'transport_document_type_code': parent_vals[0]['transport_document_type_code'],
                'number_of_originals': parent_vals[0]['number_of_originals'],
                'carrier_booking_reference': parent_vals[0]['carrier_booking_reference'],
                'is_electronic': parent_vals[0]['is_electronic'],
                'number_of_copies': parent_vals[0]['number_of_copies'],
                'is_shipped_onboard_type': parent_vals[0]['is_shipped_onboard_type'],
                'is_charges_displayed': parent_vals[0]['is_charges_displayed'],
                'location_name': parent_vals[0]['location_name'],
                'city_name': parent_vals[0]['city_name'],
                'un_location_code': parent_vals[0]['un_location_code'],
                'state_region': parent_vals[0]['state_region'],
                'country': parent_vals[0]['country'],
                'shipping_instruction_ID': parent_vals[0]['shipping_instruction_ID'],
                'transport_document_reference': parent_vals[0]['transport_document_reference'],
                'reciept_or_deliverytype_at_origin': parent_vals[0]['reciept_or_deliverytype_at_origin'],
                'reciept_or_deliverytype_at_dest': parent_vals[0]['reciept_or_deliverytype_at_dest'],
                'shipped_onboard_date': parent_vals[0]['shipped_onboard_date'],
                'issue_date': parent_vals[0]['issue_date'],
                'cargo_movement_type_at_origin': parent_vals[0]['cargo_movement_type_at_origin'],
                'cargo_movement_type_at_dest': parent_vals[0]['cargo_movement_type_at_dest'],
                'terms_and_conditions': parent_vals[0]['terms_and_conditions'],
                'received_for_shipment_date': parent_vals[0]['received_for_shipment_date'],
                'declared_value': parent_vals[0]['declared_value'],
                'service_contract_reference': parent_vals[0]['service_contract_reference'],
                'declared_value_currency': parent_vals[0]['declared_value_currency'],
                'issuer_code': parent_vals[0]['issuer_code'],
                'issuer_code_list_provider': parent_vals[0]['issuer_code_list_provider'],
                'no_of_rider_pages': parent_vals[0]['no_of_rider_pages'],
                'planned_arrival_date': parent_vals[0]['planned_arrival_date'],
                'planned_departure_date': parent_vals[0]['planned_departure_date'],
                'document_hash': parent_vals[0]['document_hash'],
                'pre_carried_by': parent_vals[0]['pre_carried_by'],

                'poi_location_name': parent_vals[0]['poi_location_name'],
                'poi_post_code': parent_vals[0]['poi_post_code'],
                'poi_un_location_code': parent_vals[0]['poi_un_location_code'],
                'poi_city_name': parent_vals[0]['poi_city_name'],
                'poi_street_name': parent_vals[0]['poi_street_name'],
                'poi_state_region': parent_vals[0]['poi_state_region'],
                'poi_street_number': parent_vals[0]['poi_street_number'],
                'poi_country': parent_vals[0]['poi_country'],
                'poi_floor': parent_vals[0]['poi_floor'],
                'por_location_name': parent_vals[0]['por_location_name'],
                'por_post_code': parent_vals[0]['por_post_code'],
                'por_un_location_code': parent_vals[0]['por_un_location_code'],
                'por_city_name': parent_vals[0]['por_city_name'],
                'por_street_name': parent_vals[0]['por_street_name'],
                'por_state_region': parent_vals[0]['por_state_region'],
                'por_street_number': parent_vals[0]['por_street_number'],
                'por_country': parent_vals[0]['por_country'],
                'por_floor': parent_vals[0]['por_floor'],
                'pol_location_name': parent_vals[0]['pol_location_name'],
                # 'pol_post_code': parent_vals[0]['pol_post_code'],
                'pol_un_location_code': parent_vals[0]['pol_un_location_code'],
                'pol_city_name': parent_vals[0]['pol_city_name'],
                # 'pol_street_name': parent_vals[0]['pol_street_name'],
                'pol_state_region': parent_vals[0]['pol_state_region'],
                # 'pol_street_number': parent_vals[0]['pol_street_number'],
                'pol_country': parent_vals[0]['pol_country'],
                # 'pol_floor': parent_vals[0]['pol_floor'],
                'pod_location_name': parent_vals[0]['pod_location_name'],
                # 'pod_post_code': parent_vals[0]['pod_post_code'],
                'pod_un_location_code': parent_vals[0]['pod_un_location_code'],
                'pod_city_name': parent_vals[0]['pod_city_name'],
                # 'pod_street_name': parent_vals[0]['pod_street_name'],
                'pod_state_region': parent_vals[0]['pod_state_region'],
                # 'pod_street_number': parent_vals[0]['pod_street_number'],
                'pod_country': parent_vals[0]['pod_country'],
                # 'pod_floor': parent_vals[0]['pod_floor'],
                'plod_location_name': parent_vals[0]['plod_location_name'],
                'plod_post_code': parent_vals[0]['plod_post_code'],
                'plod_un_location_code': parent_vals[0]['plod_un_location_code'],
                'plod_city_name': parent_vals[0]['plod_city_name'],
                'plod_street_name': parent_vals[0]['plod_street_name'],
                'plod_state_region': parent_vals[0]['plod_state_region'],
                'plod_street_number': parent_vals[0]['plod_street_number'],
                'plod_country': parent_vals[0]['plod_country'],
                'plod_floor': parent_vals[0]['plod_floor'],
                'oir_location_name': parent_vals[0]['oir_location_name'],
                'oir_post_code': parent_vals[0]['oir_post_code'],
                'oir_un_location_code': parent_vals[0]['oir_un_location_code'],
                'oir_city_name': parent_vals[0]['oir_city_name'],
                'oir_street_name': parent_vals[0]['oir_street_name'],
                'oir_state_region': parent_vals[0]['oir_state_region'],
                'oir_street_number': parent_vals[0]['oir_street_number'],
                'oir_country': parent_vals[0]['oir_country'],
                'oir_floor': parent_vals[0]['oir_floor'],
                'pre_location_name': parent_vals[0]['pre_location_name'],
                'pre_post_code': parent_vals[0]['pre_post_code'],
                'pre_latitude': parent_vals[0]['pre_latitude'],
                'pre_longitude': str(parent_vals[0]['pre_longitude']),
                'pre_un_location_code': parent_vals[0]['pre_un_location_code'],
                'pre_city_name': parent_vals[0]['pre_city_name'],
                'pre_street_name': parent_vals[0]['pre_street_name'],
                'pre_state_region': parent_vals[0]['pre_state_region'],
                'pre_street_number': parent_vals[0]['pre_street_number'],
                'pre_country': parent_vals[0]['pre_country'],
                'pre_floor': parent_vals[0]['pre_floor'],
                'is_shipped_onboard_type': parent_vals[0]['is_shipped_onboard_type'],
                'number_of_originals': parent_vals[0]['number_of_originals'],
            }
            print("------------------------- vals",vals)
            bol_rec.sudo().write(vals)
        return {'bol':bol_rec.id}
        print("..............bol_rec...............",bol_rec)
        

    @http.route(['/si_template_values_for_create'], type='json', auth="public", method=['POST'], website=True)
    def si_template_values_for_create(self, parent_vals, cargo_vals, tq_vals, dp_vals, sl_vals, rc_vals, **kwargs):
        SiTemplate = request.env['si.templates']
        cargo_table_count = parent_vals[0]['cargo_table_count']
        si_template_rec = SiTemplate.sudo().create({
            'name': parent_vals[0]['si_template_name'],
            'transport_document_type_code': parent_vals[0]['transport_document_type_code'],
            'is_shipped_onboard_type': parent_vals[0]['is_shipper_owned'],
            'number_of_originals': parent_vals[0]['number_of_originals'],
            'number_of_copies': parent_vals[0]['number_of_copies'],
            'pre_carriage_under_shippers_responsibility': parent_vals[0]['pre_carriage_under_shippers_responsibility'],
            'is_electronic': parent_vals[0]['is_electronic'],
            'carrier_booking_reference': parent_vals[0]['carrier_booking_reference'],
            'is_charges_displayed': parent_vals[0]['is_charges_displayed'],
            'location_name': parent_vals[0]['inv_payable_location_name'],
            'un_location_code': parent_vals[0]['inv_payable_un_location_code'],
            'city_name': parent_vals[0]['inv_payable_city_name'],
            'state_region': parent_vals[0]['inv_payable_state_region'],
            'country': parent_vals[0]['inv_payable_country'],
            # 'is_shipping_instruction': True,
            'si_user_id': parent_vals[0]['new_si_created_by_user_id'],
            # 'si_inquiry_no': parent_vals[0]['si_create_inquiry_no'],
        })
        if si_template_rec:
            if cargo_table_count > 0:
                for line in cargo_vals:
                    si_template_rec.si_template_cargo_items_line.sudo().create({
                        'si_template_cargo_line_id': si_template_rec.id,
                        'cargo_line_items_id': line['cargo_line_item_id'],
                        'shipping_marks': line['shipping_marks'],
                        'carrier_booking_reference': line['carrier_booking_reference'],
                        'description_of_goods': line['description_of_goods'],
                        'hs_code': line['hs_code'],
                        'number_of_packages': line['no_of_packages'],
                        'weight': line['weight'],
                        'volume': line['volume'],
                        'weight_unit': line['weight_unit'],
                        'volume_unit': line['volume_unit'],
                        'package_code': line['package_code'],
                        'equipment_reference': line['equipment_reference'],
                        'cargo_array_created_by': line['cargo_array_created_by'],
                    })
            tq_table_count = parent_vals[0]['tq_table_count']
            if tq_table_count > 0:
                for tq in tq_vals:
                    si_template_rec.si_template_transport_equipment_line.sudo().create({
                        'si_template_transport_equipment_line_id': si_template_rec.id,
                        'equipment_reference_id': tq['equipment_reference'],
                        'weight_unit': tq['weight_unit_tq'],
                        'cargo_gross_weight': tq['cargo_gross_weight'],
                        'container_tare_weight': tq['container_tare_weight'],
                        'iso_equipment_code': tq['iso_equipment_code'],
                        'is_shipper_owned': tq['is_shipper_owned'],
                        'temperature_min': tq['temperature_min'],
                        'temperature_max': tq['temperature_max'],
                        'temperature_unit': tq['temperature_unit'],
                        'humidity_min': tq['humidity_min'],
                        'humidity_max': tq['humidity_max'],
                        'ventilation_min': tq['ventilation_min'],
                        'ventilation_max': tq['ventilation_max'],
                        'seal_number': tq['seal_number'],
                        'seal_source': tq['seal_source'],
                        'seal_type': tq['seal_type'],
                        'transport_equipment_array_created_by': tq['tq_array_created_by'],
                    })
            dp_table_count = parent_vals[0]['dp_table_count']
            if dp_table_count > 0:
                for dp in dp_vals:
                    si_template_rec.si_template_document_parties_line.sudo().create({
                        'si_template_document_parties_line_id': si_template_rec.id,
                        'party_name_id': dp['party_name'],
                        'tax_reference_1': dp['tax_reference_1_dp'],
                        'public_key': dp['public_key'],
                        'street': dp['street'],
                        'street_number': dp['street_number'],
                        'floor': dp['floor'],
                        'post_code': dp['post_code'],
                        'city': dp['city'],
                        'state_region': dp['state_region'],
                        'country': dp['country'],
                        'tax_reference_2': dp['tax_reference_2'],
                        'nmfta_code': dp['nmfta_code'],
                        'party_function': dp['party_function'],
                        'address_line': dp['address_line'],
                        'name': dp['name'],
                        'email': dp['email'],
                        'phone': dp['phone'],
                        'is_to_be_notified': dp['is_to_be_notified'],
                        'document_parties_array_created_by': dp['dp_array_created_by'],
                    })
            sl_table_count = parent_vals[0]['sl_table_count']
            if sl_table_count > 0:
                for sl in sl_vals:
                    location_type_rec = request.env['location.type'].sudo().search([('name', '=', sl['location_type'])])
                    si_template_rec.si_template_shipment_location_line.sudo().create({
                        'si_template_shipment_location_line_id': si_template_rec.id,
                        'location_type': location_type_rec.id,
                        'displayed_name': sl['displayed_name'],
                        'location_name': sl['location_name'],
                        'latitude': sl['latitude'],
                        'longitude': sl['longitude'],
                        'un_location_code': sl['un_location_code'],
                        'street_name': sl['street_name'],
                        'street_number': sl['street_number'],
                        'floor': sl['floor'],
                        'post_code': sl['post_code'],
                        'city_name': sl['city_name'],
                        'state_region': sl['state_region'],
                        'country': sl['country'],
                        'shipment_location_array_created_by': sl['sl_array_created_by'],
                    })
            rc_table_count = parent_vals[0]['rc_table_count']
            if rc_table_count > 0:
                for rc in rc_vals:
                    si_template_rec.si_template_references_line.sudo().create({
                        'si_template_references_line_id': si_template_rec.id,
                        'reference_type': rc['reference_type'],
                        'reference_value': rc['reference_value'],
                        'references_array_created_by': rc['ref_array_created_by'],
                    })
            return True
        else:
            return False

class InheritInvController(PortalAccount):	
    @http.route(['/my/invoices', '/my/invoices/page/<int:page>'], type='http', auth="user", website=True)	
    def portal_my_invoices(self, page=1, date_begin=None, date_end=None, sortby=None, filterby=None,ship_info=False, **kw):	
        values = self._prepare_my_invoices_values(page, date_begin, date_end, sortby, filterby)	
        # pager	
        pager = portal_pager(**values['pager'])	
        # content according to pager and archive selected	
        invoices = values['invoices'](pager['offset'])	
        request.session['my_invoices_history'] = invoices.ids[:100]	
        values.update({	
            'invoices': invoices,	
            'pager': pager,	
        })	
        if ship_info:	
            inv_rec = request.env['account.move'].sudo().search([('id', 'in',eval(ship_info))])	
            values['invoices'] = inv_rec	
                    
        return request.render("account.portal_my_invoices", values)	
        # res = super(InheritInvController,self).portal_my_invoices(self)	
        # print("----------------------------res",res)	
        # return res