from odoo import models, fields, _, api
from odoo.exceptions import UserError

transport_fpod_vals = {'fpod_id': False, 'sequence': 0}


class TransportTemplate(models.Model):
    _name = 'transport.template'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Transport Template"

    name = fields.Char("Name")
    workorder = fields.Char("Work Order*", tracking=True)
    cont_id = fields.Char("Container ID", tracking=True)
    planned_date = fields.Datetime("Planned Datetime*", tracking=True)
    actual_date = fields.Datetime("Actual Datetime", tracking=True)
    delay_reason = fields.Char("Delay Reason", tracking=True)
    remarks = fields.Char("Remarks", tracking=True)
    carrier_handover = fields.Many2one('port', string="Carrier Handover", tracking=True)
    vessel_name = fields.Char("Vessel Name*", tracking=True)
    imo_no = fields.Char("IMO No.", tracking=True)
    voyage = fields.Char("Voyage", tracking=True)
    rotation = fields.Char("Rotation", tracking=True)
    proforma_schedule = fields.Binary("Proforma Schedule", tracking=True)
    proforma_schedule_fname = fields.Char("Proforma Schedule Filename", tracking=True)
    gate_cutoff = fields.Datetime("Gate Cut Off", tracking=True)
    # facility = fields.Many2one('port', string="Facility")
    temparature = fields.Char("Temparature", tracking=True)
    ventilation = fields.Char("Ventilation", tracking=True)
    humidity = fields.Char("Humidity", tracking=True)
    is_transportation_confirmed = fields.Boolean('Transportation Confirmed', tracking=True)
    route_template_id = fields.Many2one('route.templates', string='Route Template', tracking=True)
    transport_template_route_line = fields.One2many('transport.template.route.line', 'transport_template_id', string='Route', tracking=True)

    port_of_origin_id = fields.Many2one('port', string='Port of Origin*', tracking=True)
    port_of_origin_facility_id = fields.Many2one('sub.port', string="Port of Origin Facility", tracking=True)

    fpod_id = fields.Many2one('port', string='FPOD*', help="Final Port of Destination", tracking=True)
    fpod_facility_id = fields.Many2one('sub.port', string="FPoD Facility", tracking=True,
                                       help="Final Port of Destination Facility")

    point_of_stuffing = fields.Many2one('port', string='Point of Stuffing', tracking=True)
    point_of_destuffing = fields.Many2one('port', string='Point of Destuffing', tracking=True)
    carrier_booking = fields.Char(string='Carrier Booking*', tracking=True)
    transport_reference = fields.Char(string='Transport Reference*', tracking=True)
    is_created_from_transport = fields.Boolean(string='Is created from Transport', tracking=True)
    transport_id = fields.Many2one('transport', string='Transport', tracking=True)
    cont_type = fields.Many2one("container.type", string="Container type", tracking=True)
    special_type = fields.Selection(
        [('reefer_active', 'Reefer Active'), ('reefer_inactive', 'Reefer InActive'), ('pl', 'PL'), ('fr', 'FR'),
         ('ot', 'OT')], string="Special", tracking=True)
    pickup_loc_id = fields.Many2one("port", string="Pick up Location*", tracking=True)
    pickup_loc_facility_id = fields.Many2one('sub.port', string="Pick up Location Facility", tracking=True)
    dropoff_loc_id = fields.Many2one("port", string="Drop Off Location", tracking=True)
    dropoff_loc_facility_id = fields.Many2one('sub.port', string="Drop Off Location Facility", tracking=True)

    pickup_mode = fields.Many2one('mode', string='Mode of transport from pickup', tracking=True)
    dropoff_mode = fields.Many2one('mode', string='Mode of transport for Dropoff', tracking=True)
    stuffing_mode = fields.Many2one('mode', string='Mode of transport from Stuffing Location', tracking=True)
    destuffing_mode = fields.Many2one('mode', string='Mode of transport for Destuffing Location', tracking=True)
    vessel_mode = fields.Many2one('mode', string='Mode of transport from Port', tracking=True)

    is_multi_modal = fields.Boolean("Is Multi Modal", tracking=True)
    vessel_name1 = fields.Char("Vessel Name", tracking=True)
    voyage1 = fields.Char("Voyage", tracking=True)
    rotation1 = fields.Char("Rotation", tracking=True)
    imo_no1 = fields.Char("IMO No.", tracking=True)
    is_data_template = fields.Boolean('Is Data Template?', default=False, tracking=True)
    intermediate_pol_id = fields.Many2one("port", string="Intermediate port of loading", tracking=True)

    container_route_line = fields.One2many('trans.temp.container.journey', 'transport_template_id', string='Container Journey',
                                           copy=True)

    equipment_route_line = fields.One2many('trans.temp.equipment.journey', 'transport_template_id', string='Equipment Journey',
                                           tracking=True)

    def action_load_route_template(self):
        self.transport_template_route_line = False
        route_list = []
        vals_start = {}
        vals_end = {}
        vals_start_tup = ()
        vals_end_tup = ()
        for line in self.route_template_id.route_template_line:
            route_list.append((0, 0, {'port_of_origin_id': line.port_of_origin_id.id,
                                      'fpod_id': line.fpod_id.id,
                                      'port_of_origin': line.port_of_origin,
                                      'fpod': line.fpod,
                                      'point_of_stuffing': line.point_of_stuffing.id if line.point_of_stuffing else False,
                                      'point_of_destuffing': line.point_of_destuffing.id if line.point_of_destuffing else False,
                                      'mode_id': line.mode_id.id,
                                      'estimated_departure_time': line.estimated_departure_time,
                                      'estimated_arrival_time': line.estimated_arrival_time,
                                      'actual_departure_time': line.actual_departure_time,
                                      'actual_arrival_time': line.actual_arrival_time,
                                      'delay_reason': line.delay_reason,
                                      }))
        if route_list != []:
            vals_start.update({'port_of_origin': route_list[0][2]['point_of_stuffing'],
                               'fpod': route_list[0][2]['port_of_origin'],
                               })
            vals_start_tup = (0, 0, vals_start)
            vals_end.update({'port_of_origin': route_list[-1][2]['fpod'],
                             'fpod': route_list[-1][2]['point_of_destuffing'],
                             })
            vals_end_tup = (0, 0, vals_end)
            route_list.insert(0, vals_start_tup)
            route_list.append(vals_end_tup)
        self.transport_template_route_line = route_list

    def action_delete_route_template(self):
        self.transport_template_route_line = False

    def action_create_route_template(self):
        ctx = {}
        self.ensure_one()
        if not self.transport_template_route_line:
            raise UserError(_("There is no Route to create Route template"))
        routetemplate = self.env['route.templates'].search([('transport_id', '=', self.id)])
        if routetemplate:
            ctx = dict(
                default_transport_id=self.id,
                default_name=routetemplate.name,
                default_is_created_from_transport=routetemplate.is_created_from_transport,
                current_id=self.id,
            )
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'route.templates',
            'view_mode': 'form',
            'views': [(self.env.ref('freightbox.route_template_form_wiz').id, "form")],
            'context': ctx,
            'target': 'new',
        }


class TransportTemplateRouteLine(models.Model):
    _name = 'transport.template.route.line'
    _description = "Transport Template Route Line"
    _order = 'id asc'

    @api.onchange('fpod_id', 'port_of_origin_id')
    def _onchange_fpod_id(self):
        if self.fpod_id:
            transport_fpod_vals.update({'fpod_id': self.fpod_id.id})
            fpod = self.fpod_id.unloc_code + ' ' + self.fpod_id.name
            self.fpod = fpod
        if self.port_of_origin_id:
            port_of_origin = self.port_of_origin_id.unloc_code + ' ' + self.port_of_origin_id.name
            self.port_of_origin = port_of_origin

    def _get_point_of_origin(self):
        port_of_origin_id = transport_fpod_vals['fpod_id']
        return port_of_origin_id

    transport_template_id = fields.Many2one('transport.template', string='Transport Template')
    port_of_origin_id = fields.Many2one('port', string='Intermediate POL',default = _get_point_of_origin)
    port_of_origin = fields.Char(string='Intermediate POL')
    fpod_id = fields.Many2one('port', string='Intermediate POD')
    fpod = fields.Char(string='Intermediate POD')
    point_of_stuffing = fields.Many2one('port', related='transport_template_id.point_of_stuffing',string='Point of Stuffing')
    point_of_destuffing = fields.Many2one('port', related='transport_template_id.point_of_destuffing',string='Point of Destuffing')
    mode_id = fields.Many2one('mode', string='Mode')
    estimated_departure_time = fields.Datetime("ETD")
    estimated_arrival_time = fields.Datetime("ETA")
    planned_departure_time = fields.Datetime("PTD")
    planned_arrival_time = fields.Datetime("PTA")
    actual_departure_time = fields.Datetime("ATD")
    actual_arrival_time = fields.Datetime("ATA")
    delay_reason = fields.Char('Reason for Delay')
    change_remark = fields.Text('Change Remark')


class TransportTemplateContainerJourney(models.Model):
    _name = 'trans.temp.container.journey'
    _description = "Transport Template Container Journey"
    # _order = 'id asc'

    transport_template_id = fields.Many2one('transport.template', string='Transport Tempalte')
    end_point = fields.Many2one('port', string='End Point')
    start_point = fields.Many2one('port', string='Start Point')
    # transport_mode = fields.Char(string='Mode of Transport')
    transport_mode = fields.Many2one('mode', string='Mode of Transport')
    estimated_departure_time = fields.Datetime("ETD")
    estimated_arrival_time = fields.Datetime("ETA")
    planned_departure_time = fields.Datetime("PTD")
    planned_arrival_time = fields.Datetime("PTA")
    actual_departure_time = fields.Datetime("ATD")
    actual_arrival_time = fields.Datetime("ATA")
    delay_reason = fields.Char('Reason for Delay')
    change_remark = fields.Text('Change Remark')
    # Temporary fields to show in template
    distance = fields.Char("Distance (KM)")
    speed = fields.Char("Speed")
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
    gate_in_wait_time = fields.Float("Gate In Waiting Time (hr)")
    gate_out_wait_time = fields.Float("Gate Out Waiting Time (hr)")
    travel_time = fields.Float("Time in hr")
    buffer_time = fields.Float("Buffer Time (hr)")
    yard_time = fields.Float("Yard Time (hr)")

class TransportTemplateEquipmentJourney(models.Model):
    _name = 'trans.temp.equipment.journey'
    _description = "Transport Template Equipment Journey"
    # _order = 'id asc'

    transport_template_id = fields.Many2one('transport.template', string='Transport Tempalte')
    track_trace_event_id = fields.Many2one('track.trace.event', string='Track Trace Event')
    equip_event_id = fields.Char("Equipment Event ID", help="Unique identifier for the equipment event captured.")
    event_created_datetime = fields.Datetime("Event Created DateTime",
                                             help="The date and time when the event entry was created.")
    estimated_event_time = fields.Datetime("ETA", help="Estimated Time of Action")
    event_classifier_code = fields.Text("Event Classifier Code",
                                        help="The code for the event classifier, e.g.,Actual.")
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
