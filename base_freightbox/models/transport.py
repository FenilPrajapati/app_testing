from odoo import models, fields, _, api
from odoo.exceptions import UserError, ValidationError


class Transport(models.Model):
    _name = 'transport'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Transport"
    _rec_name = 'cont_id'

    def action_confirm_transportation(self):
        if self.pickup_loc_id == self.dropoff_loc_id:
            raise UserError(_("Pick up and Drop off locations cannot be same"))
        # If there are container route lines and equipment route lines, create planned track - trace records.
        self.is_transportation_confirmed = True
        self.write({'state': 'confirm'})
        if self.job_id:
            transport_lst = self.job_id.confirmed_transport_ids.ids
            transport_lst.append(self.id)
            self.job_id.confirmed_transport_ids = [(6, 0, transport_lst)]
        return True

    name = fields.Char("Name")
    workorder = fields.Char("Work Order*", tracking=True)
    cont_id = fields.Char("Container ID", tracking=True)
    planned_date = fields.Datetime("Planned Datetime*", tracking=True)
    scheduled_date = fields.Datetime("Estimated Datetime*", tracking=True)
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
    temparature = fields.Char("Temparature", tracking=True)
    ventilation = fields.Char("Ventilation", tracking=True)
    humidity = fields.Char("Humidity", tracking=True)
    is_transportation_confirmed = fields.Boolean('Transportation Confirmed', tracking=True)
    container_route_line = fields.One2many('container.journey', 'transport_id', string='Container Journey', tracking=True)
    equipment_journey_ids = fields.One2many('equipment.journey', 'transport_id', string='Equipment Journey', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Transport Confirmed')
        # ('cancelled', 'Cancelled')
    ], default='draft', tracking=True, string='Status', readonly=True)

    port_of_origin_id = fields.Many2one('port', string='Port of Origin*', tracking=True)
    port_of_origin_facility_id = fields.Many2one('sub.port', string="Port of Origin Facility", tracking=True)

    fpod_id = fields.Many2one('port', string='FPOD*', help="Final Port of Destination", tracking=True)
    fpod_facility_id = fields.Many2one('sub.port', string="FPoD Facility", tracking=True,
                                       help="Final Port of Destination Facility")

    point_of_stuffing = fields.Many2one('port', string='Point of Stuffing', tracking=True)
    point_of_destuffing = fields.Many2one('port', string='Point of Destuffing', tracking=True)
    carrier_booking = fields.Char(string='Carrier Booking*', tracking=True)
    transport_reference = fields.Char(string='Transport Reference*', tracking=True)
    cont_type = fields.Many2one("container.iso.code", string="Container type", tracking=True)
    special_type = fields.Selection(
        [('reefer_active', 'Reefer Active'), ('reefer_inactive', 'Reefer InActive'), ('pl', 'PL'), ('fr', 'FR'),
         ('ot', 'OT')], string="Special", tracking=True)
    job_id = fields.Many2one('job', string='Job*', tracking=True, ondelete='cascade')
    pickup_loc_id = fields.Many2one("port", string="Pick up Location*", tracking=True)
    pickup_loc_facility_id = fields.Many2one('sub.port', string="Pick up Location Facility", tracking=True)
    dropoff_loc_id = fields.Many2one("port", string="Drop Off Location", tracking=True)
    dropoff_loc_facility_id = fields.Many2one('sub.port', string="Drop Off Location Facility", tracking=True)
    shipping_instruction_id = fields.Many2one("shipping.instruction",
                                              string="Shipping Instruction", tracking=True)
    inquiry_id = fields.Many2one('crm.lead', string="Inquiry ID", readonly=True, tracking=True)
    pickup_mode = fields.Many2one('mode', string='Mode of transport from pickup', tracking=True)
    dropoff_mode = fields.Many2one('mode', string='Mode of transport for Dropoff', tracking=True)
    stuffing_mode = fields.Many2one('mode', string='Mode of transport from Stuffing Location', tracking=True)
    destuffing_mode = fields.Many2one('mode', string='Mode of transport for Destuffing Location', tracking=True)
    vessel_mode = fields.Many2one('mode', string='Mode of transport from Port', tracking=True)

    # equipment_event_line_ids = fields.One2many('equipment.event.line', 'equipment_line_id', string='Equipment Event')
    # shipment_event_line = fields.One2many('shipment.event', 'shipment_event_line_id', string='Shipment Event')
    # transport_event_line = fields.One2many('transport.event', 'transport_event_line_id', string='Transport Event')
    create_si_by_shipper = fields.Boolean("Allow Shipper to Create SI", tracking=True)
    # is_multi_modal = fields.Boolean("Is Multi Modal", tracking=True)
    # vessel_name1 = fields.Char("Vessel Name", tracking=True)
    # voyage1 = fields.Char("Voyage", tracking=True)
    # rotation1 = fields.Char("Rotation", tracking=True)
    # imo_no1 = fields.Char("IMO No.", tracking=True)
    # intermediate_pol_id = fields.Many2one("port", string="Intermediate port of loading", tracking=True)
    fb_transport_id = fields.Text("FB Transport ID", default=lambda self: _('New'))
    # no_of_api_calls = fields.Integer(string='Api Calls', readonly=True, tracking=True, default=0)
    # is_track_requested = fields.Boolean("Is track Requested?", tracking=True)
    # second_vessel_mode = fields.Many2one('mode', string='Mode of transport from Port', tracking=True)
    # is_another_ship_needed = fields.Boolean("Is another ship needed?", tracking=True)
    # vessel_name2 = fields.Char("Vessel Name", tracking=True)
    # voyage2 = fields.Char("Voyage", tracking=True)
    # rotation2 = fields.Char("Rotation", tracking=True)
    # imo_no2 = fields.Char("IMO No.", tracking=True)
    # second_intermediate_pol_id = fields.Many2one("port", string="Second Intermediate port of loading", tracking=True)
    # third_vessel_mode = fields.Many2one('mode', string='Mode of transport from Port', tracking=True)
    active = fields.Boolean(string='Active', default=True)
    booking_user_id = fields.Many2one('res.users', string="Shipper/FF")
    si_state = fields.Selection([
        ('yet_to_create', 'Yet To Create'),
        ('si_created', 'SI Created'),
        ('si_accepted', 'SI Accepted'),
    ], default='yet_to_create', tracking=True, string='SI Status', readonly=True)
    # waypoint_coordinates = fields.Text('Waypoint Coordinates')
    # allow_get_waypoints = fields.Boolean("Allow Import Waypoints", compute="onchange_waypoint_coordinates", default=True)
    # cont_jour_count = fields.Integer(string='Contain Jour', compute='_get_container_journy', readonly=True, tracking=True)
    company_id = fields.Many2one('res.company', 'Company', required=True,
                                 default=lambda self: self.env.company.id)


    @api.onchange('cont_type')
    def _onchange_cont_type(self):
        if not self.cont_type:
            self.special_type = False
        if self.cont_type:
            self.special_type = self.cont_type.special_type


class ContainerJourney(models.Model):
    _name = 'container.journey'
    _description = "Container Journey"

    transport_id = fields.Many2one('transport', string='Transport')
    start_point = fields.Many2one('port', string='Start Point')
    end_point = fields.Many2one('port', string='End Point')
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
    speed = fields.Char("Speed", default=30)
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
    co2_emmision = fields.Float("CO2 Emmision", store=True, readonly=True, compute='_calculate_co2_emmision')
    transport_mode = fields.Many2one('mode', string='Mode of Transport')
    gate_in_wait_time = fields.Float("Gate In Waiting Time (hr)", default=24)
    gate_out_wait_time = fields.Float("Gate Out Waiting Time (hr)", default=24)
    travel_time = fields.Float("Time in hr")
    buffer_time = fields.Float("Buffer Time (hr)")
    yard_time = fields.Float("Yard Time (hr)")
    ptd_updated = fields.Boolean("PTD Updated", default=False)
    pta_updated = fields.Boolean("PTA Updated", default=False)
    etd_updated = fields.Boolean("ETD Updated", default=False)
    eta_updated = fields.Boolean("ETA Updated", default=False)
    route_coordinates = fields.Text('Route Coordinates')


class EquipmentJourney(models.Model):
        _name = 'equipment.journey'
        _description = "Equipment Journey"
        _order = 'id'

        transport_id = fields.Many2one('transport', string='Transport')
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
