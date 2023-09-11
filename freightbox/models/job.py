from odoo import models, fields, _, api
from odoo.exceptions import ValidationError, UserError
from lxml import etree
from datetime import timedelta, datetime,date
import requests
import json


class Job(models.Model):
    _inherit = 'job'

    def _compute_transport(self):
        for rec in self:
            transport_ids = rec.env['transport'].search([('carrier_booking', '=', rec.carrier_booking)])
            transport_ids = transport_ids.ids
            rec.write({'transport_ids': [(6, 0, transport_ids)]})
            rec.transport_count = len(transport_ids)
            max_transport_limit = rec.confirmed_no_of_container
            if rec.cargo_plus_ids:
                max_transport_limit = int(sum(rec.cargo_plus_ids.mapped('no_of_confirmed_container')))
            if rec.transport_count >= max_transport_limit:
                rec.stop_transport_creation = True
            else:
                rec.stop_transport_creation = False

    def _get_si_count(self):
        for record in self:
            si_counts = self.env['shipping.instruction'].search_count([('job_id', '=', record.id)])
            record.si_count = si_counts

    def _get_trans_count(self):
        for record in self:
            transport_counts = self.env['transport'].search_count([('job_id', '=', record.id)])
            record.trans_count = transport_counts

    def _get_mbol_count(self):
        for record in self:
            mbol_counts = self.env['bill.of.lading'].search_count([('job_id', '=', record.id), ('is_master_bill_of_lading', '=', True)])
            record.mbol_count = mbol_counts
    
    def _get_hbol_count(self):
        for record in self:
            hbol_counts = self.env['bill.of.lading'].search_count([('job_id', '=', self.id),('is_house_bill_of_lading', '=', True)])
            self.hbol_count = hbol_counts

    def _get_job_invoice_count(self):
        for record in self:
            invoice_counts = self.env['account.move'].search_count([('job_id', '=', record.id), ('is_job_invoice', '=', True)])
            record.invoice_count = invoice_counts

    def _get_mbl_invoice_count(self):
        for record in self:
            invoice_rec = self.env['account.move'].sudo().search([('job_id', '=', record.id), ('is_bol_invoice', '=', True),('is_master_bill_of_lading', '=', True)])
            record.mb_invoice_count = len(invoice_rec)
        # if self.bol_id:
            # invoice_counts = self.env['account.move'].search_count([('bol_id', '=', self.id)])
            # self.mb_invoice_count = invoice_counts

    def _get_hbl_invoice_count(self):
        for record in self:
            invoice_rec = self.env['account.move'].sudo().search([('job_id', '=', record.id),('is_bol_invoice', '=', True), ('is_house_bill_of_lading', '=', True)])
            record.hb_invoice_count = len(invoice_rec)

    def _get_tnt_count(self):
        for record in self:
            tnt_counts = self.env['track.trace.event'].search_count([('carrier_booking', '=', record.carrier_booking)])
            record.tnt_count = tnt_counts

    def _get_vessel_location_track_count(self):
        for record in self:
            vessel_track_counts = self.env['vessel.location.track'].search_count([('job_id', '=', record.id)])
            record.vessel_location_track_count = vessel_track_counts

    def action_get_tnt(self):
        itemids = self.env['track.trace.event'].search([('carrier_booking', '=', self.carrier_booking)])
        # itemids = self.env['track.trace.event'].search([('carrier_booking', '=', self.carrier_booking)])
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

    def action_get_vessel_location_track(self):
        records = self.env['vessel.location.track'].search([('job_id', '=', self.id)])
        return {
            'name': "Vessel Tracking",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'vessel.location.track',
            'view_id': False,
            'domain': [('id', 'in', records.ids)],
            'target': 'current',
        }

    # booking_id = fields.Many2one('sale.order', string="Enquiry No", tracking=True)
    # job_no = fields.Char("Job No.", required=True, copy=False, tracking=True, readonly=True, index=True,
    #                      default=lambda self: _('New'))
    # job_date = fields.Date("Job Date", required=True, readonly="1", tracking=True, default=fields.Date.today())
    # job_state_for_hold = fields.Selection([
    #     ('draft', 'Draft'),
    #     ('si_created', 'SI Created'),
    #     ('si_accepted', 'All SI accepted'),
    #     ('draft_bol', 'Draft M BoL created'),
    #     ('update_bol', 'Update on M BoL'),
    #     ('bol_received', 'M BoL Issued'),
    #     ('hold', 'On hold'),
    #     ('cargo_released', 'Cargo Released'),
    #     ('container', 'Container Returned'),
    #     ('inactive', 'Inactive'),
        ('invoiced', 'Invoiced'),
        # ('done', 'Done')
    # ], string='Job Status', default='draft')
    # state = fields.Selection([
    #     ('draft', 'Draft'),
    #     ('si_created', 'SI Created'),
    #     ('si_accepted', 'All SI accepted'),
    #     ('draft_bol', 'Draft M BoL created'),
    #     ('update_bol', 'Update on M BoL'),
    #     ('bol_received', 'M BoL Issued'),
    #     ('hold', 'On hold'),
    #     ('cargo_released', 'Cargo Released'),
    #     ('container', 'Container Returned'),
    #     ('inactive', 'Inactive'),
    #     # ('invoiced', 'Invoiced'),
    #     ('done', 'Done')
    # ], string='Status', index=True, readonly=True, copy=False, default='draft', tracking=True)
    # carrier_booking = fields.Char("Carrier Booking", tracking=True)
    # carrrier_date = fields.Date("Carrier Date", tracking=True)
    # carrrier_id = fields.Char("Carrier Id", tracking=True)
    svc_cont = fields.Char("Service Contract", tracking=True)
    service_type_origin = fields.Many2one('service.type', string="Service Type Origin", tracking=True)
    service_type_dest = fields.Many2one('service.type', string="Service Type Destination", tracking=True)
    # shipment_terms_origin = fields.Selection([
    #     ('lcl', 'LCL'),
    #     ('fcl', 'FCL'),
    #     ('both', 'LCL and FCL'),
    #     ('bb', 'BB')], "Shipment Terms Origin", tracking=True)
    # shipment_terms_dest = fields.Selection([
    #     ('lcl', 'LCL'),
    #     ('fcl', 'FCL'),
    #     ('both', 'LCL and FCL'),
    #     ('bb', 'BB')], "Shipment Terms Destination", tracking=True)
    # commodity_hs_code = fields.Char("Commodity HS Code")
    # commodity_description = fields.Char("Commodity Description", tracking=True)
    # cargo_gross_weight = fields.Float("Cargo Gross Weight", tracking=True)
    # cargo_uom_id = fields.Many2one('uom.uom', "Gross Unit", tracking=True)
    # shipment_id = fields.Char("Shipment Id", tracking=True)
    # requested_equipment_type = fields.Many2one("container.iso.code", "Requested Container Type", tracking=True)
    # requested_equip_unit_id = fields.Many2one('uom.uom', "Requested Equipment Unit", tracking=True)
    # confirmed_equipment_type = fields.Many2one("container.iso.code", "Confirmed Container Type", tracking=True)
    # confirmed_equip_unit_id = fields.Many2one('uom.uom', "Confirmed Equipment Unit")
    # requested_date_time = fields.Datetime("Requested Date Time", tracking=True)
    # actual_date_time = fields.Datetime("Actual Date Time", tracking=True)
    # reference_id = fields.Char("Reference Id", tracking=True)
    # reference_type = fields.Char("Reference Type", tracking=True)
    # place_of_origin = fields.Char("Point of Origin", tracking=True)
    # final_port_of_destination = fields.Char("Point of Destination", tracking=True)
    # reference_name = fields.Char("Reference Name")
    # reference_description = fields.Char("Reference Description")
    # shipping_instruction = fields.Text("Shipping Instruction",tracking=True)
    # shipping_description = fields.Text("Shipping Description", tracking=True)
    # so_id = fields.Many2one("sale.order", string="Sale order", tracking=True, ondelete='cascade')
    # po_id = fields.Many2one("purchase.order", string="Purchase order", tracking=True)
    # shipper_id = fields.Many2one("res.partner", string="Shipper", tracking=True)
    # shipping_instruction_ids = fields.Many2many('shipping.instruction', string="Shipping Instruction", tracking=True)
    # transport_ids = fields.Many2many('transport', string="Transport", tracking=True)
    # confirmed_transport_ids = fields.Many2many('transport', 'job_rel', 'job_id', 'transport_id',
    #                                            string="Confirmed Transport", tracking=True)
    transport_count = fields.Integer(compute='_compute_transport', string="Transport Count")
    stop_transport_creation = fields.Boolean(compute='_compute_transport',
                                             string="Stop Transport Creation", tracking=True)
    # exp_no_of_container = fields.Float('Expected No of Container', tracking=True)
    # confirmed_no_of_container = fields.Float('Confirmed No of Container', tracking=True)
    # inquiry_id = fields.Many2one('crm.lead', string="Inquiry ID", readonly=True, tracking=True)
    # vessel_name = fields.Char("Vessel Name", tracking=True)
    # voyage = fields.Char("Voyage", tracking=True)
    # rotation = fields.Char("Rotation", tracking=True)
    # imo_no = fields.Char("IMO No.", tracking=True)
    # user_id = fields.Many2one("res.users", string="User", tracking=True)
    # invoice_ids = fields.Many2many("account.move", string='Invoices', tracking=True)
    si_count = fields.Integer(string='SI Count', compute='_get_si_count', readonly=True)
    trans_count = fields.Integer(string='Total Transport Count', compute='_get_trans_count', readonly=True)
    mbol_count = fields.Integer(string='Master BOL Count', compute='_get_mbol_count', readonly=True)
    hbol_count = fields.Integer(string='House BOL Count', compute='_get_hbol_count', readonly=True)
    invoice_count = fields.Integer(string='Job Invoice Count', compute='_get_job_invoice_count', readonly=True)
    mb_invoice_count = fields.Integer(string='Master B/L Invoice Count', compute='_get_mbl_invoice_count', readonly=True)
    hb_invoice_count = fields.Integer(string='House B/L Invoice Count', compute='_get_hbl_invoice_count', readonly=True)
    charge_line = fields.One2many('charges.line.items', 'charge_job_line_id', string="Charges", tracking=True)
    total_charge = fields.Float(compute='_compute_total_charge', string="Total Charge", tracking=True)
    tnt_count = fields.Integer(string='TNT Count', compute='_get_tnt_count', readonly=True, tracking=True)
    # is_cont_released = fields.Boolean("Is Container Released", tracking=True)
    is_multi_modal = fields.Boolean("Is Transhipment?", tracking=True)
    vessel_name1 = fields.Char("Vessel Name", tracking=True)
    voyage1 = fields.Char("Voyage", tracking=True)
    rotation1 = fields.Char("Rotation", tracking=True)
    imo_no1 = fields.Char("IMO No.", tracking=True)
    intermediate_pol_id = fields.Many2one("port", string="Intermediate port of loading", tracking=True)
    second_vessel_mode = fields.Many2one('mode', string='Mode of transport from Port', tracking=True)
    is_another_ship_needed = fields.Boolean("Is another ship needed?", tracking=True)
    vessel_name2 = fields.Char("Vessel Name", tracking=True)
    voyage2 = fields.Char("Voyage", tracking=True)
    rotation2 = fields.Char("Rotation", tracking=True)
    imo_no2 = fields.Char("IMO No.", tracking=True)
    second_intermediate_pol_id = fields.Many2one("port", string="Second Intermediate port of loading", tracking=True)
    third_vessel_mode = fields.Many2one('mode', string='Mode of transport from Port', tracking=True)
    # is_house_bol_needed = fields.Boolean(string="Is House BOL needed")
    # active = fields.Boolean(string='Active', default=True)
    # booking_user_id = fields.Many2one('res.users', string="Shipper/FF")
    # hold_reason = fields.Text('Hold Reason', tracking=True)
    # hold_bool = fields.Boolean(string='Hold Bool')
    load_free_days = fields.Integer(string='Loading Free days', tracking=True)
    discharge_free_days = fields.Integer(string='Discharge Free days', tracking=True)
    detention = fields.Integer(string='Detention during load & discharge', tracking=True)
    lay_time = fields.Integer(string='Lay Time', tracking=True)
    # port_of_origin_id = fields.Many2one('port', string='Port of Origin', tracking=True, required=True, domain=[('one', '=', True)])
    # final_port_of_destination_id = fields.Many2one('port', string='Final Point of Destination', help="Final Port of Destination", tracking=True, required=True, domain=[('one', '=', True)])
    vessel_location_track_count = fields.Integer(string='Vessel Location Track Count', compute='_get_vessel_location_track_count', readonly=True, tracking=True)
    status = fields.Selection([('on_time', 'On Time'),
                               ('late', 'Late')],
                              'Status', default='on_time', required=1,
                              compute='_get_job_status')
    allow_import_way_points = fields.Boolean("Allow Import Waypoints", default=True)
    allow_import_vessel_location = fields.Boolean("Allow Import Waypoints", default=False)
    route_waypoints = fields.Text('Waypoints')
    vessel_location_api_datetime = fields.Datetime('Last API Called At')
    vessel_location_api_parameters = fields.Text('API Parameters')
    vessel_location_api_response = fields.Text('API Response')
    is_send_mail = fields.Boolean(string="Send Mail")
    is_cargo_send_mail = fields.Boolean(string="Send Mail")
    agents_line = fields.One2many('res.partner', 'agent_type_id', string='Agents Lines')
    po_charges = fields.Integer(string='PO Invoices', tracking=True, default=0) # compute="_compute_po_charges")
    so_charges = fields.Integer(string='SO Invoices', tracking=True, default=0) #compute="_compute_so_charges")
    additional_bills = fields.Integer(string='Additional charges paid', tracking=True,default=0)
    additional_invoices = fields.Integer(string='Additional Charges recieved', default=0, tracking=True)
    currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.company.currency_id)
    currency_id1 = fields.Many2one('res.currency', string="Currency") # compute="_compute_po_charges")
    currency_id2 = fields.Many2one('res.currency', string="Currency") # compute="_compute_so_charges")
    profit_charges = fields.Integer(string='Profit', tracking=True, default=0)
    loss_charges = fields.Integer(string='Loss', tracking=True, default=0)
    add_attachment = fields.Many2many('ir.attachment', string="Additional invoices/bills")


    # def _compute_so_charges(self):
    #     if self.so_id:
    #         print("so_id::::::::::",self.so_id)
    #         self.so_charges = self.so_id.total_charge
    #         print("so_charges::::::::::",self.so_charges)
    #         self.currency_id2 = self.so_id.currency_id

    # def _compute_po_charges(self):
    #     if self.po_id:
    #         self.po_charges = 0.0 #self.po_id.total_charge
    #         self.currency_id1 = self.po_id.currency_id

    @api.onchange('po_charges', 'so_charges', 'additional_bills', 'additional_invoices', 'profit_charges', 'loss_charges')
    def _onchange_charges(self):
        total_expenses = self.additional_bills+self.po_charges
        total_income = self.so_charges+self.additional_invoices
        if total_income > total_expenses:
            total_charges = total_income - total_expenses
            print("total_chargestotal_chargestotal_chargestotal_charges",total_charges)
            self.profit_charges = total_charges
            print("profitprofitprofitprofitprofitprofitprofitprofit",self.profit_charges)
        if total_expenses > total_income:
            total_charges = total_expenses - total_income
            print("losslosslosslosslosslosslosslosslossloss",total_charges)
            self.loss_charges = total_charges
            print("profitprofitprofitprofitprofitprofitprofitprofit",self.loss_charges)

    # def _compute_profit_or_loss(self):
    #     # total_expenses = 0
    #     # total_income = 0
    #     # total_charges = 0
    #     # if self.po_charges or self.so_charges or self.additional_bills or self.additional_invoices :
    #     for i in self:
    #         total_expenses = i.additional_bills+i.po_charges
    #         total_income = i.so_charges+i.additional_invoices
    #         i.profit_charges = 0
    #         i.loss_charges = 0
    #         print("total_chargestotal_chargestotal_chargestotal_charges",total_expenses)
    #         print("total_chargestotal_chargestotal_chargestotal_charges",total_income)
    #         if total_income > total_expenses:
    #             total_charges = total_income - total_expenses
    #             print("total_chargestotal_chargestotal_chargestotal_charges",total_charges)
    #             i.profit_charges = total_charges
    #             print("profitprofitprofitprofitprofitprofitprofitprofit",i.profit_charges)
    #         if total_expenses > total_income:
    #             total_charges = total_expenses - total_income
    #             print("losslosslosslosslosslosslosslosslossloss",total_charges)
    #             i.loss_charges = total_charges
    #             print("profitprofitprofitprofitprofitprofitprofitprofit",i.loss_charges)
            # if total_charges<0:
            #     self.loss_charges == total_charges


    def send_job_auto_mail_cron(self):
        job_rec = self.env['job'].search([('state','=','draft_bol')])
        for i in job_rec:
            if not i.is_send_mail:
                template_id = self.env.ref('freightbox.mail_template_job_auto_send')
                template_id.send_mail(i.id, force_send=True)
                i.is_send_mail = True

    def send_job_auto_mail_cron_cargo_release(self):
        print("000000000000000000000")
        job_rec = self.env['job'].search([('state','=','cargo_released')])
        for i in job_rec:
            print("------------is_cargo_send_mail",i.is_cargo_send_mail)
            if not i.is_cargo_send_mail:
                template_id = self.env.ref('freightbox.mail_template_job_cargo_released')
                template_id.send_mail(i.id, force_send=True)
                i.is_cargo_send_mail = True


    def import_waypoints_from_motherserver(self):

        for record in self:
            por_geo_data = self.get_geo_location_from_port(record.port_of_origin_id)
            pod_geo_data = self.get_geo_location_from_port(record.final_port_of_destination_id)
            startpoint_unloc = record.port_of_origin_id.unloc_code or False
            endpoint_unloc = record.final_port_of_destination_id.unloc_code or False
            startpoint_lon = por_geo_data.get('lon', False)
            startpoint_lat = por_geo_data.get('lat', False)
            endpoint_lon = pod_geo_data.get('lon', False)
            endpoint_lat = pod_geo_data.get('lat', False)
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
                url = '%s/%s/%s/%s/%s/0/0/0/0' % (api_rec.url, startpoint_lon, startpoint_lat, endpoint_lon, endpoint_lat)
                response = requests.get(url)
            route_data = {}
            try:
                if response and response.status_code == 200:
                    route_data = json.loads(response.content)
                else:
                    if por_geo_data.get('status_code', 0) == 200 and pod_geo_data.get('status_code', 0) == 200:
                        route_data.update({'route': [
                            {
                                'lon': por_geo_data.get('lon', False) if por_geo_data.get('status_code', 0) == 200 else False,
                                'lat': por_geo_data.get('lat', False) if por_geo_data.get('status_code', 0) == 200 else False
                            },
                            {
                                'lon': pod_geo_data.get('lon', False) if pod_geo_data.get('status_code', 0) == 200 else False,
                                'lat': pod_geo_data.get('lat', False) if pod_geo_data.get('status_code', 0) == 200 else False
                            }
                        ]
                        })
            except:
                if por_geo_data.get('status_code', 0) == 200 and pod_geo_data.get('status_code', 0) == 200:
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
            prepared_route = ""
            for route_point in route_data.get('route', []):
                if route_point.get('lat', False) != False and route_point.get('lon', False) != False:
                    if prepared_route:
                        prepared_route = "%s/%s,%s" % (prepared_route, route_point.get('lon'), route_point.get('lat'))
                    else:
                        prepared_route = "%s,%s" % (route_point.get('lon'), route_point.get('lat'))

            if prepared_route and prepared_route.strip() != "":
                record.route_waypoints = prepared_route
                record.allow_import_way_points = False
        return True

    def import_waypoints_cron(self):
        jobs_to_process = self.sudo().search([
            ('state', 'not in', ['hold', 'inactive', 'done']),
            ('allow_import_way_points', '=', True)
        ])
        if jobs_to_process:
            jobs_to_process.import_waypoints_from_motherserver()
        return True

    def import_vessel_location_cron(self):
        jobs_to_process = self.sudo().search([
            ('state', 'not in', ['hold', 'inactive', 'done']),
            ('allow_import_vessel_location', '=', True)
        ])
        if jobs_to_process:
            jobs_to_process.import_vessel_location()
        return True

    def import_vessel_location(self):
        vessel_location_track_obj = self.env['vessel.location.track']
        for record in self:
            vessel_location_track_obj.get_latest_vessel_location(record)
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

    def _get_job_status(self):
        for record in self:
            record.status = 'on_time'
            track_records = tnt_counts = self.env['track.trace.event'].search([('carrier_booking', '=', record.carrier_booking)])
            hold_jobs = track_records.mapped('transport_event_line').filtered(lambda transport_event_line: transport_event_line.delay_reason and len(transport_event_line.delay_reason.strip()) > 0)
            if hold_jobs:
                record.status = 'late'

    @api.onchange('load_free_days', 'discharge_free_days')
    def _onchange_load_discharge_free_days(self):
        if self.load_free_days or self.discharge_free_days:
            self.lay_time = self.load_free_days + self.discharge_free_days
        else:
            self.lay_time = 0

    invoice_status = fields.Selection([
        ('paid', 'Fully Invoiced (paid)'),
        ('partial', 'Partially Invoiced'),
        ('to invoice', 'To Invoice'),
        ('no', 'Nothing to Invoice')
    ], string='Invoice Status', default='no')

    @api.model
    def job_dashboard(self):
        """ This function returns the values to populate the custom dashboard in
            the Job views.
        """
        # self.check_access_rights('read')

        result = {
            'draft': 0,
            'si_accepted': 0,
            'draft_bol': 0,
            'hold': 0,
            'cargo_released': 0,
            'done': 0,
        }

        result['draft'] = self.search_count([('state', '=', 'draft')])
        result['si_accepted'] = self.search_count([('state', '=', 'si_accepted')])
        result['draft_bol'] = self.search_count([('state', '=', 'draft_bol')])
        result['hold'] = self.search_count([('state', '=', 'hold')])
        result['cargo_released'] = self.search_count([('state', '=', 'cargo_released')])
        result['done'] = self.search_count([('state', '=', 'done')])

        return result

    def check_validity_on_hold(self):
        hold_rec = self.search([('state','=','hold')])
        
        if hold_rec:
            for i in hold_rec:
                body = """
                        Dear Sir/Madam,
                        <br/>
                        <b><p> Your Job Is On Hold For %s Reason. </p></b>
                        <p><b>  </b> </p> 
                        
                        """%str(i.hold_reason)
               
                to_email = ""
                if i.shipper_id.email:
                    to_email = i.shipper_id.email


                self.env['mail.mail'].sudo().create({
                    'email_from': "fenil.prajapati@powerpbox.org",
                    'author_id': self.env.user.partner_id.id,
                    'body_html': body,
                    'subject': 'Your Job %s '%str(i.job_no),
                    'email_to': to_email,
                }).send()

    def button_container(self):
        transport_ids = self.transport_ids
        no_of_cont = self.confirmed_no_of_container
        cont_returned = 0
        # if self.is_nvocc==True:
        #     for order in self.so_id.order_line:
        #         order.product_id.is_alloted = False
        #         order.product_id.is_reserved = False

        # for t in transport_ids:
        #     cont_id = t.cont_id
        #     track_eq_event_obj = self.env['track.equipment.event']
        #
        #     eq_event = track_eq_event_obj.sudo().search([
        #         ('equip_reference', '=', cont_id),
        #         ('empty_indicator_code', '=', "EMPTY"),
        #         ('equip_event_type_code', '=', "GTIN")])
        #     print("sdf", eq_event)
        #     if eq_event:
        #         print("sdf", eq_event)
        #         cont_returned += 1
        # print("cont_returned::::", cont_returned)
        # if cont_returned == no_of_cont:
        self.write({'state': 'container'})
        # else:
        #     raise ValidationError('Container is not yet returned')

    def button_invoice(self):
        account_move = self.env['account.move']
        if not self.charge_line:
            raise UserError(_('Charge Line is empty, Please Add Some Charge.'))
        if self.total_charge <= 0:
            raise ValidationError('Total Charges should be a greater than 0')
        else:
            inv = account_move.create({
                'ref': self.carrier_booking,
                'move_type': 'out_invoice',
                'invoice_origin': self.carrier_booking,
                'partner_id': self.user_id.partner_id.id,
                # 'partner_shipping_id': self.job_id.so_id.partner_shipping_id.id,
                'currency_id': self.env.company.currency_id,
                'payment_reference': self.carrier_booking,
                'invoice_payment_term_id': self.booking_id.po_id.payment_term_id.id,
                'job_id': self.id,
                'booking_id': self.so_id.booking_id,
                'place_of_origin': self.so_id.place_of_origin,
                'place_of_destination': self.so_id.final_port_of_destination,
                'vessel_name': self.vessel_name,
                'voyage': self.voyage,
                'rotation': self.rotation,
                'imo_no': self.imo_no,
                'is_job_invoice': True,
            })
        if inv:
            for line in self.charge_line:
                rec = inv.job_charge_line.create({
                    'charge_type': line.charge_type,
                    'calculation_basis': line.calculation_basis,
                    'currency_code': line.currency_code,
                    'payment_term': line.payment_term,
                    'unit_price': line.unit_price,
                    'quantity': line.quantity,
                    'currency_amount': line.quantity * line.unit_price,
                    # 'final_amount': line.final_amount,
                    'job_account_charge_line_id': inv.id,
                })
        product_template = self.env['product.template']
        container_id = self.so_id.container_type.id
        container_name = self.so_id.container_type.code
        product_template_id = product_template.search(
            [('iso_code_id', '=', container_id), ('name', '=', container_name)], limit=1)
        product = self.env['product.product'].search([('product_tmpl_id', '=', product_template_id.id)], limit=1)
        account = inv.journal_id.default_account_id
        inv_lines = {
            'name': product.name,
            'move_id': inv.id,
            'product_id': product.id,
            'product_uom_id': product.uom_id.id,
            'quantity': inv.job_id.confirmed_no_of_container,  #len(inv.job_charge_line),
            'price_unit': inv.job_total_charge / inv.job_id.confirmed_no_of_container, #len(inv.job_charge_line),
            'account_id': account.id,
            # 'exclude_from_invoice_tab': False,
        }
        inv.invoice_line_ids.with_context(check_move_validity=False).create(inv_lines)
        inv.write({'job_id': self.id})
        job_inv_ids = self.env['account.move'].sudo().search([('job_id', '=', self.id), ('is_job_invoice', '=', True)])
        self.invoice_ids = [(6, 0, job_inv_ids.ids)]
        self.invoice_status = "partial"

    def button_create_bol(self):
        view_id = self.env.ref('freightbox.bill_of_lading_tree_view').id
        view_form_id = self.env.ref('freightbox.bill_of_lading_form_view').id
        bol_rec = self.env['bill.of.lading'].search([('job_id', '=', self.id),('is_master_bill_of_lading', '=', True)])
        if bol_rec:
            action = {
                'name': "Master Bill of Lading",
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'bill.of.lading',
                'view_id': False,
                'domain': [('id', '=', bol_rec.id)],
                'target': 'current',
            }
            return action
        else:
            ctx = dict(
                # default_model='job',
                default_si_ids=self.shipping_instruction_ids.ids,
                default_job_id=self.id,
                default_carrier_booking_reference=self.carrier_booking,
                default_is_master_bill_of_lading=True,
                default_inquiry_id=self.inquiry_id.id,
                default_booking_user_id=self.booking_user_id.id,
                default_cargo_plus_ids=[(6, 0, self.cargo_plus_ids.ids)]
                # default_use_template=bool(template.id),
                # default_template_id=template.id,
                # default_composition_mode='comment',
                # force_email=True,
            )
            action = {
                'name': _('BOL'),
                'type': 'ir.actions.act_window',
                'res_model': 'bill.of.lading',
                'view_type': 'form',
                'views': [(view_form_id, 'form')],
                'view_mode': 'form',
                'context': ctx
            }
            return action

    @api.model
    def action_open_job_form_view(self):
        view_id = self.env.ref('freightbox.job_tree_view').id
        view_form_id = self.env.ref('freightbox.job_form_view').id
        action = {
            'name': _('Job'),
            'type': 'ir.actions.act_window',
            'res_model': 'job',
            'view_type': 'list',
            'views': [(view_id, 'list'), (view_form_id, 'form')],
            'view_mode': 'list,form',
        }
        return action

    def action_job_send(self):
        """ Open a window to compose an email, with the edi invoice template
            message loaded by default
        """
        outmail_rec = self.env['ir.mail_server'].search([])
        if not outmail_rec:
            raise UserError("Outgoing mail server not set !!!")
            
        # self.user_id.sudo().action_reset_password()
        self.ensure_one()
        template = self.env.ref('freightbox.mail_template_job', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        # self.user_id.with_context(active_test=True)._send_email()
        # self.user_id.refresh()

        ctx = dict(
            default_model='job',
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

    def action_send_link_consignee(self):
        user_obj = self.env['res.users']
        consignee = self.po_id.party_name_id
        if consignee:
            consignee_found = user_obj.sudo().search([('login', '=', consignee.email)])
            if not consignee_found:
                consignee_user = user_obj.sudo().create({
                    'name': consignee.name,
                    'login': consignee.email,
                    'email': consignee.email,
                    'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])],
                })
                consignee_user.with_context(create_user=True).action_reset_password()
            consignee_found.action_reset_password()

    def action_get_si(self):
        itemIds = self.env['shipping.instruction'].search([('job_id', '=', self.id)])
        itemIds = itemIds.ids
        return {
            'name': "Shipping Instruction",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'shipping.instruction',
            'view_id': False,
            'domain': [('id', 'in', itemIds)],
            'target': 'current',
        }

    def action_get_transport(self):
        itemIds = self.env['transport'].search([('job_id', '=', self.id)])
        itemIds = itemIds.ids
        return {
            'name': "Transport",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'transport',
            'view_id': False,
            'domain': [('id', 'in', itemIds)],
            'target': 'current',
        }

    def action_get_mbol(self):
        itemIds = self.env['bill.of.lading'].search([('job_id', '=', self.id), ('is_master_bill_of_lading', '=', True)])
        itemIds = itemIds.ids
        return {
            'name': "Master Bill of Lading",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'bill.of.lading',
            'view_id': False,
            'domain': [('id', 'in', itemIds)],
            'target': 'current',
        }

    def action_get_hbol(self):
        itemIds = self.env['bill.of.lading'].search([('job_id', '=', self.id), ('is_house_bill_of_lading', '=', True)])
        itemIds = itemIds.ids
        return {
            'name': "House Bill of Lading",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'bill.of.lading',
            'view_id': False,
            'domain': [('id', 'in', itemIds)],
            'target': 'current',
        }

    def action_get_invoice(self):
        itemIds = self.env['account.move'].search([('job_id', '=', self.id), ('is_job_invoice', '=', True)])
        itemIds = itemIds.ids
        return {
            'name': "Job Invoice",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'view_id': False,
            'domain': [('id', 'in', itemIds)],
            'target': 'current',
        }

    def action_get_mbl_invoice(self):
        # invoice_rec = request.env['account.move'].sudo().search([('is_bol_invoice', '=', True)])
        item_ids = self.env['account.move'].sudo().search([('job_id', '=', self.id), ('is_bol_invoice', '=', True),('is_master_bill_of_lading', '=', True)])
        item_ids = item_ids.ids
        return {
            'name': "Master B/L Invoice",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'view_id': False,
            'domain': [('id', 'in', item_ids)],
            'target': 'current',
        }

    def action_get_hbl_invoice(self):
        # invoice_rec = request.env['account.move'].sudo().search([('is_bol_invoice', '=', True)])
        item_ids = self.env['account.move'].sudo().search([('job_id', '=', self.id), ('is_bol_invoice', '=', True), ('is_house_bill_of_lading', '=', True)])
        item_ids = item_ids.ids
        return {
            'name': "House B/L Invoice",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.move',
            'view_id': False,
            'domain': [('id', 'in', item_ids)],
            'target': 'current',
        }

    def action_create_transport(self):
        view_id = self.env.ref('freightbox.transport_form_view').id
        se_rec = self.env['track.shipment.event'].create({
                'shipment_event': 'Shipment',
                'event_created': date.today(),
                'event_datetime': date.today(),
                'event_classifier_code': 'ACT',
                'shipment_event_type_code': 'RECE',
                'reason':'Transport Created',
                'booking_id':self.inquiry_id.id
            })
        ctx = dict(
            default_job_id=self.id,
            default_carrier_booking=self.carrier_booking,
            default_vessel_name=self.vessel_name,
            default_voyage=self.voyage,
            default_rotation=self.rotation,
            default_imo_no=self.imo_no,
            default_is_multi_modal=self.is_multi_modal,
            default_vessel_name1=self.vessel_name1,
            default_voyage1=self.voyage1,
            default_rotation1=self.rotation1,
            default_imo_no1=self.imo_no1,
            default_intermediate_pol_id=self.intermediate_pol_id.id,
            default_second_vessel_mode=self.second_vessel_mode.id,
            default_is_another_ship_needed=self.is_another_ship_needed,
            default_vessel_name2=self.vessel_name2,
            default_voyage2=self.voyage2,
            default_rotation2=self.rotation2,
            default_imo_no2=self.imo_no2,
            default_second_intermediate_pol_id=self.second_intermediate_pol_id.id,
            default_third_vessel_mode=self.third_vessel_mode.id,
            default_inquiry_id=self.inquiry_id.id,
            default_booking_user_id=self.booking_user_id.id,
        )

        if self.booking_id.po_id.rfq_id.booking_id.point_of_stuffing:
            dict.update({
                'default_point_of_stuffing' : self.booking_id.po_id.point_of_stuffing.id,
            })
        if self.booking_id.po_id.rfq_id.booking_id.point_of_destuffing:
            dict.update({
                'default_point_of_destuffing' : self.booking_id.po_id.point_of_destuffing.id,
            })
        return {
            'name': 'Transport',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'transport',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': ctx,
        }

    def action_create_house_bol(self):
        view_id = self.env.ref('freightbox.bill_of_lading_tree_view').id
        view_form_id = self.env.ref('freightbox.bill_of_lading_form_view').id
        ctx = dict(
            # default_model='job',
            default_si_ids=self.shipping_instruction_ids.ids,
            default_job_id=self.id,
            default_carrier_booking_reference=self.carrier_booking,
            default_is_house_bill_of_lading=True,
            default_inquiry_id=self.inquiry_id.id,
            default_booking_user_id=self.booking_user_id.id,
            # default_use_template=bool(template.id),
            # default_template_id=template.id,
            # default_composition_mode='comment',
            # force_email=True,
        )
        action = {
            'name': "House Bill of Lading",
            'type': 'ir.actions.act_window',
            'res_model': 'bill.of.lading',
            'view_type': 'form',
            'views': [(view_id, 'False'), (view_form_id, 'form')],
            'view_mode': 'form',
            # 'target': 'new',
            'context': ctx
        }
        return action
        # return False

    def job_tutorial_video_new_tab(self):
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
        if view_id == self.env.ref("freightbox.job_form_view").id:
            url = self.env['ir.config_parameter'].sudo().get_param('freightbox.job_tutorial_video',
                                                                   "/freightbox/static/src/img/index_file_images/not_found.png")
            doc = etree.XML(result['arch'])
            for node in doc.xpath("//iframe[@id='job_tutorial_video']"):
                node.set('src', url)
            result['arch'] = etree.tostring(doc)
        return result