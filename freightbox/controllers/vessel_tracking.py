from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
from odoo import _
import requests
import json
import socket
from odoo.osv import expression
from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager, get_records_pager

GROUP_SYSTEM = 'base.group_system'


class VesselTracking(http.Controller):

    @http.route('/vessel_tracking', type='http', auth='public', website=True)
    def vessel_tracking(self, **post):
        job_obj = request.env['job']
        si_obj = request.env['shipping.instruction']
        bol_obj = request.env['bill.of.lading']
        tte_obj = request.env['track.trace.event']
        vessel_track_obj = request.env['vessel.location.track']
        vessel_tracking_data = {}
        user = request.env.user
        user_logged = True
        if user:
            if user.id == request.env.ref('base.public_user').id:
                user_logged = False
            if request.session.uid:
                job_domain = [
                    ('state', 'not in', ['hold', 'inactive', 'done'])
                ]
                if not user.has_group('base.group_system'):
                    job_domain.append(('booking_user_id', '=', user.id))

                jobs = job_obj.sudo().search(job_domain, order="status, id")
                shipping_instructions = si_obj.sudo().search([('job_id', 'in', jobs.ids)])
                master_bols = bol_obj.sudo().search([('job_id', 'in', jobs.ids), ('is_master_bill_of_lading', '=', True)])
                house_bols = bol_obj.sudo().search([('job_id', 'in', jobs.ids), ('is_house_bill_of_lading', '=', True)])
                vessel_track_value_list = []
                js_class_id = 1
                for job in jobs:

                    tnt_recs = tte_obj.search([('carrier_booking', '=', job.carrier_booking)])
                    tnt_rec_with_transport_events = False
                    for tnt_rec in tnt_recs:
                        if len(tnt_rec.transport_event_line.ids) > 0:
                            tnt_rec_with_transport_events = tnt_rec
                            break
                    tnt_data = []
                    if tnt_rec_with_transport_events:
                        for event in tnt_rec_with_transport_events.transport_event_line:
                            msg = ""
                            if event.transport_event_type_code == "DEPA":
                                msg = "Will Leave"
                                if event.location:
                                    msg = "%s from %s" % (msg, event.location)
                                if event.mode_of_transport_code:
                                    msg = "%s by %s " % (msg, event.mode_of_transport_code)
                            if event.transport_event_type_code == "ARRI":
                                msg = "Will arrive"
                                if event.location:
                                    msg = "%s at %s" % (msg, event.location)
                                if event.mode_of_transport_code:
                                    msg = "%s by %s " % (msg, event.mode_of_transport_code)
                            tnt_data.append(
                                (
                                    event.event_datetime,
                                    event.event_type,
                                    event.event_classifier_code,
                                    event.transport_event_type_code,
                                    event.mode_of_transport_code,
                                    msg
                                )
                            )

                    vessel_track_rec = vessel_track_obj.get_latest_vessel_location_rec(job)
                    por_geo_data = self.get_geo_location_from_city(job.port_of_origin_id)
                    pod_geo_data = self.get_geo_location_from_city(job.final_port_of_destination_id)
                    startpoint_unloc = job.port_of_origin_id.unloc_code or False
                    endpoint_unloc = job.final_port_of_destination_id.unloc_code or False
                    startpoint_lon = por_geo_data.get('lon', False)
                    startpoint_lat = por_geo_data.get('lat', False)
                    endpoint_lon = pod_geo_data.get('lon', False)
                    endpoint_lat = pod_geo_data.get('lat', False)
                    job_waypoints = job.route_waypoints and str(job.route_waypoints) or ''
                    prepared_route = ""
                    if job_waypoints.strip() != "" and 'False' not in job_waypoints:
                        prepared_route = job_waypoints
                    if not prepared_route or prepared_route.strip() == "":
                        try:
                            # job.sudo().import_waypoints_from_motherserver()
                            if job_waypoints.strip() != "" and 'False' not in job_waypoints:
                                prepared_route = job.route_waypoints
                        except:
                            prepared_route = ""
                    # response = False
                    # api_rec = request.env['api.integration'].search([('name', '=', 'get_routes_by_loccode')])
                    # if not api_rec:
                    #     raise Warning("API record doesn't exist for 'get_routes_by_loccode' process.")
                    # if startpoint_unloc and endpoint_unloc:
                    #     url = '%s/%s/%s/0/0/0/0' % (api_rec.url,startpoint_unloc, endpoint_unloc)
                    #     response = requests.get(url)
                    # else:
                    #     if startpoint_lon and startpoint_lat and endpoint_lon and endpoint_lat:
                    #         api_rec = request.env['api.integration'].search([('name', '=', 'get_routes_by_geocode')])
                    #         if not api_rec:
                    #             raise Warning("API record doesn't exist for 'get_routes_by_geocode' process.")
                    #         url = '%s/%s/%s/%s/%s/0/0/0/0' % (api_rec.url, startpoint_lon, startpoint_lat, endpoint_lon, endpoint_lat)
                    #         response = requests.get(url)
                    # if response.status_code != 200 and startpoint_lon and startpoint_lat and endpoint_lon and endpoint_lat:
                    #     if startpoint_lon and startpoint_lat and endpoint_lon and endpoint_lat:
                    #         api_rec = request.env['api.integration'].search([('name', '=', 'get_routes_by_geocode')])
                    #         if not api_rec:
                    #             raise Warning("API record doesn't exist for 'get_routes_by_geocode' process.")
                    #     url = '%s/%s/%s/%s/%s/0/0/0/0' % (api_rec.url, startpoint_lon, startpoint_lat, endpoint_lon, endpoint_lat)
                    #     response = requests.get(url)
                    # route_data = {}
                    # try:
                    #     if response and response.status_code == 200:
                    #         route_data = json.loads(response.content)
                    #     else:
                    #         route_data.update({'route': [
                    #                 {
                    #                 'lon': por_geo_data.get('lon', False) if por_geo_data.get('status_code', 0) == 200 else False,
                    #                 'lat': por_geo_data.get('lat', False) if por_geo_data.get('status_code', 0) == 200 else False
                    #                 },
                    #                 {
                    #                     'lon': pod_geo_data.get('lon', False) if pod_geo_data.get('status_code', 0) == 200 else False,
                    #                     'lat': pod_geo_data.get('lat', False) if pod_geo_data.get('status_code', 0) == 200 else False
                    #                 }
                    #             ]
                    #         })
                    # except:
                    #     route_data.update({'route': [
                    #         {
                    #             'lon': por_geo_data.get('lon', False) if por_geo_data.get('status_code',
                    #                                                                       0) == 200 else False,
                    #             'lat': por_geo_data.get('lat', False) if por_geo_data.get('status_code',
                    #                                                                       0) == 200 else False
                    #         },
                    #         {
                    #             'lon': pod_geo_data.get('lon', False) if pod_geo_data.get('status_code',
                    #                                                                       0) == 200 else False,
                    #             'lat': pod_geo_data.get('lat', False) if pod_geo_data.get('status_code',
                    #                                                                       0) == 200 else False
                    #         }
                    #     ]
                    #     })
                    # prepared_route = ""
                    # for route_point in route_data.get('route', []):
                    #     if prepared_route:
                    #         prepared_route = "%s/%s,%s" % (prepared_route,route_point.get('lon'),route_point.get('lat'))
                    #     else:
                    #         prepared_route = "%s,%s" % (route_point.get('lon'), route_point.get('lat'))
                    por_lat = 0
                    por_lon = 0
                    pod_lat = 0
                    pod_lon = 0
                    if prepared_route.strip() != "" and len(prepared_route.split('/')) > 1:
                        por_lat = por_geo_data.get('lat', prepared_route.split('/')[0].split(',')[1])
                        por_lon = por_geo_data.get('lat', prepared_route.split('/')[0].split(',')[0])
                        pod_lat = pod_geo_data.get('lat', prepared_route.split('/')[-1].split(',')[1])
                        pod_lon = pod_geo_data.get('lat', prepared_route.split('/')[-1].split(',')[0])
                    por_text = job.port_of_origin_id.name
                    pod_text = job.final_port_of_destination_id.name
                    if tnt_recs and tnt_recs[0].transport_event_line:
                        por_text = "%s - %s" % (por_text, tnt_recs[0].transport_event_line[0].event_datetime)
                        pod_text = "%s - %s" % (pod_text, tnt_recs[0].transport_event_line[len(tnt_recs[0].transport_event_line) - 1].event_datetime)
                    vessel_track_value = {
                        'booking_ref': job.inquiry_id.booking_id if job.inquiry_id else '',
                        'vessel': job.vessel_name,
                        'carrier_booking': job.carrier_booking,
                        'origin': job.port_of_origin_id.name,
                        'destination': job.final_port_of_destination_id.name,
                        'job_id': job.id,
                        'js_class_id': js_class_id,
                        'por': job.port_of_origin_id.name,
                        'pod': job.final_port_of_destination_id.name,
                        'por_lat': por_geo_data.get('lat', por_lat) if por_geo_data.get('status_code', False) == 200 else por_lat,
                        'por_lon': por_geo_data.get('lon', por_lon) if por_geo_data.get('status_code', False) == 200 else por_lon,
                        'pod_lat': pod_geo_data.get('lat', pod_lat) if pod_geo_data.get('status_code',False) == 200 else pod_lat,
                        'pod_lon': pod_geo_data.get('lon', pod_lon) if pod_geo_data.get('status_code',False) == 200 else pod_lon,
                        'por_text': por_text,
                        'pod_text': pod_text,
                        'cur_lat': vessel_track_rec.latitude if vessel_track_rec else False,
                        'cur_lon': vessel_track_rec.longitude if vessel_track_rec else False,
                        'tnt_data': tnt_data,
                        'status': job.status,
                        'route': prepared_route
                    }
                    js_class_id += 1
                    vessel_track_value_list.append(vessel_track_value)
                    vessel_tracking_data.update({
                        'vessel_track_value': vessel_track_value_list,
                        'si_count': len(shipping_instructions),
                        'mbol_count': len(master_bols),
                        'hmbol_count': len(house_bols),
                    })
        vessel_tracking_data.update({
                        'user_logged': user_logged})

        r = request.render('freightbox.vessel_tracking', vessel_tracking_data)
        return r

    def get_geo_location_from_city(self, port):
        try:
            if port.geo_codes_updated_from_api and port.latitude and port.longitude:
                return {
                    'status_code': 200,
                    'lat': port.latitude,
                    'lon': port.longitude
                }

            api_rec = request.env['api.integration'].search([('name', '=', 'forward_reverse_geo_coding')])[-1]
            if not api_rec:
                raise Warning("API record doesn't exist for 'forward_reverse_geo_coding' process.")

            url = api_rec.url

            querystring = {"format": "json", "city": port.name, "accept-language": "en", "polygon_threshold": "0.0"}

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
                    return data_dict

                else:
                    api_rec = request.env['api.integration'].search([('name', '=', 'get_unloc_code_details')])[-1]
                    if not api_rec:
                        raise Warning("API record doesn't exist for 'get_unloc_code_details' process.")

                    url = api_rec.url

                    querystring = {"unlocode": port.unloc_code}

                    headers = {
                        "X-RapidAPI-Key": api_rec.key,
                        "X-RapidAPI-Host": api_rec.host
                    }

                    response = requests.request("GET", url, headers=headers, params=querystring)

                    return {'status_code': response.status_code}
        except:
            return {}
