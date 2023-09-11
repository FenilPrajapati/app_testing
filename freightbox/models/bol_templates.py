from odoo import models, fields, _, api
from odoo.exceptions import ValidationError


class BolTemplates(models.Model):
    _name = 'bol.templates'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "BOL Template"

    name = fields.Char("BOL Tempalate")
    transport_document_type_code = fields.Selection([('bol', 'BOL'), ('swb', 'SWB')], default='bol', tracking=True,
                                                    string="Transport Document Type Code",
                                                    help="Specifies the type of transport document (BOL) or a Sea Waybill (SWB)")
    is_shipped_onboard_type = fields.Boolean("Is Shipped Onboard Type", tracking=True,
                                             help="Specifies whether the Transport document is a received for shipment or shipped onboard.")
    number_of_originals = fields.Integer("Number of originals", tracking=True,
                                         help="The requested number of originals of the Transport document to be issued by the carrier. Only applicable for physical documents.")
    number_of_copies = fields.Integer("Number of copies", tracking=True,
                                      help="The requested number of copies of the Transport document to be issued by the carrier.")
    pre_carriage_under_shippers_responsibility = fields.Text("Pre-carriage under shipper’s responsibility",
                                                             tracking=True,
                                                             help="Mode of transportation for precarriage (e.g., truck, barge, rail)")
    is_electronic = fields.Boolean("Is Electronic", default=True, tracking=True, required=True,
                                   help="Indicates whether the transport document should be electronic or not.")
    carrier_booking_reference = fields.Text("Carrier Booking Reference", tracking=True,
                                            help="The associated booking number provided by the carrier.")
    is_charges_displayed = fields.Boolean("Is Charges Displayed", tracking=True, default=True,
                                          help="Indicates whether Charges are displayed.")
    location_name = fields.Text("Location Name", tracking=True, help="Name of the location.")
    un_location_code = fields.Text("UN Location Code", tracking=True,
                                   help="The UN Location code specifying where the place is located.")
    city_name = fields.Text("City Name", tracking=True, help="The city name of the party’s address.")
    state_region = fields.Text("State Region", tracking=True, help="The state/region of the party’s address.")
    country = fields.Text("Country", tracking=True, help="The country of the party’s address.")
    shipping_instruction_ID = fields.Text("Shipping Instruction ID", required=True,
                                          help="The associated Shipping Instruction ID for the reference",
                                          tracking=True)
    transport_document_reference = fields.Text("Transport Document Reference", tracking=True, required=True,
                                               help="A unique reference allocated by the shipping line "
                                                    "to the transport document, and the main number used for the "
                                                    "tracking of the status of the shipment.")
    shipped_onboard_date = fields.Date("Shipped OnBoard Date", tracking=True,
                                       help="Date when the last container that is linked to the transport "
                                            "document will be physically loaded onboard the vessel indicated on the "
                                            "transport document.")
    terms_and_conditions = fields.Text("Terms and Conditions", tracking=True, required=True,
                                       help="Additional carrier terms and conditions aside from the general "
                                            "terms and conditions")
    reciept_or_deliverytype_at_origin = fields.Text("Reciept or Delivery type at Origin", tracking=True, required=True,
                                                    help="Indicates the type of service offered at the place"
                                                         " of receipt.")
    reciept_or_deliverytype_at_dest = fields.Text("Reciept or Delivery type at Destination", tracking=True,
                                                  required=True,
                                                  help="Indicates the type of service offered at the or "
                                                       "place of delivery.")
    cargo_movement_type_at_origin = fields.Text("Cargo movement type at Origin", required=True, tracking=True,
                                                help="Indicates who is responsible for stuffing and stripping the "
                                                     "container at place of receipt.")
    cargo_movement_type_at_dest = fields.Text("Cargo movement type at Destination", required=True, tracking=True,
                                              help="Indicates who is responsible for stuffing and stripping the "
                                                   "container at place of delivery.")
    issue_date = fields.Date("Issue Date", required=True, tracking=True,
                             help=". Date when the Original Bill of Lading will be issued.")
    # PLACE OF ISSUE object
    poi_location_name = fields.Text(string="Location Name", tracking=True, help="Name of the location.")
    poi_un_location_code = fields.Text(string="UN Location Code", tracking=True,
                                       help="The UN Location code specifying where the place is located.")
    poi_street_name = fields.Text(string="Street Name", tracking=True,
                                  help="The name of the street of the party’s address.")
    poi_street_number = fields.Text(string="Street Number", tracking=True,
                                    help="The number of the street of the party’s address.")
    poi_floor = fields.Text(string="Floor", tracking=True, help="The floor of the party’s street number.")
    poi_post_code = fields.Text(string="Post Code", tracking=True, help="The post code of the party’s address.")
    poi_city_name = fields.Text(string="City Name", tracking=True, help="The city name of the party’s address.")
    poi_state_region = fields.Text(string="State Region", tracking=True,
                                   help="The state/region of the party’s address.")
    poi_country = fields.Text(string="Country", tracking=True, help="The country of the party’s address.")

    received_for_shipment_date = fields.Date("Recieved for shipment Date", tracking=True,
                                             help="Date when the carrier has taken possession of the last container "
                                                  "linked to the B/L")
    service_contract_reference = fields.Text("Service Contract Reference", tracking=True,
                                             help="Reference number for agreement between shipper and carrier "
                                                  "through which the shipper commits to provide a certain minimum "
                                                  "quantity of cargo.")

    declared_value = fields.Integer('Declared Value', tracking=True,
                                    help="The value of the cargo that the shipper declares in order to avoid the "
                                         "carrier's limitation of liability and Ad Valorem freight.")
    declared_value_currency = fields.Text('Declared Value Currency', tracking=True,
                                          help="The currency used for the declared value, using the 3-character code "
                                               "defined by ISO 4217.")
    issuer_code = fields.Text('Issuer Code', required=True, tracking=True,
                              help="The SCAC code of the issuing carrier of the Transport Document.")
    issuer_code_list_provider = fields.Text('Issuer Code list provider', tracking=True, required=True,
                                            help="The code list provider for the issuer code. Can be either "
                                                 "NMFTA or SMDG.")

    carrier_clauses_line = fields.One2many('carrier.clauses.line.items', 'carrier_clauses_line_id', copy=True,
                                           string="Carrier Clauses",
                                           help="Additional clauses for a specific shipment added by the carrier to the"
                                                " bill of lading, subject to local rules / guidelines or certain "
                                                "mandatory information required to be shared with the customer.")

    no_of_rider_pages = fields.Integer('Number of rider pages', tracking=True,
                                       help="The number of additional pages required to contain the goods"
                                            " description on a transport document. ")
    binary_copy = fields.Binary('Binary copy', tracking=True,
                                help="Allowed formats: jpg, pdf, png. Maximum allowed size: 4MB.")
    document_hash = fields.Text('Document hash', tracking=True,
                                help="Cryptographic hash of the binary copy using the SHA-256 algorithm, "
                                     "only applicable for electronic documents.")
    planned_arrival_date = fields.Date("Planned Arrival Date", tracking=True, required=True,
                                       help="The date of arrival at place of destination")
    planned_departure_date = fields.Date("Planned Departure Date", tracking=True, required=True,
                                         help=" The date of departure from place of receipt")
    pre_carried_by = fields.Text('Pre-carried by', tracking=True,
                                 help=" Mode of transportation for precarriage (e.g., truck, barge,vessel, rail)")
    # PLACE OF RECIEPT object
    por_location_name = fields.Text(string="Location Name", tracking=True)
    por_un_location_code = fields.Text(string="UN Location Code", tracking=True)
    por_street_name = fields.Text(string="Street Name", tracking=True)
    por_street_number = fields.Text(string="Street Number", tracking=True)
    por_floor = fields.Text(string="Floor", tracking=True)
    por_post_code = fields.Text(string="Post Code", tracking=True)
    por_city_name = fields.Text(string="City Name", tracking=True)
    por_state_region = fields.Text(string="State Region", tracking=True)
    por_country = fields.Text(string="Country", tracking=True)

    # PORT OF LOADING object
    pol_location_name = fields.Text(string="Location Name", required=True, tracking=True)
    pol_un_location_code = fields.Text(string="UN Location Code", required=True, tracking=True)
    pol_city_name = fields.Text(string="City Name", required=True, tracking=True)
    pol_state_region = fields.Text(string="State Region", required=True, tracking=True)
    pol_country = fields.Text(string="Country", required=True, tracking=True)

    # PORT OF DISCHARGE object
    pod_location_name = fields.Text(string="Location Name", required=True, tracking=True)
    pod_un_location_code = fields.Text(string="UN Location Code", required=True, tracking=True)
    pod_city_name = fields.Text(string="City Name", required=True, tracking=True)
    pod_state_region = fields.Text(string="State Region", required=True, tracking=True)
    pod_country = fields.Text(string="Country", required=True, tracking=True)

    # PLACE OF DELIVERY object
    plod_location_name = fields.Text(string="Location Name", tracking=True)
    plod_un_location_code = fields.Text(string="UN Location Code", tracking=True)
    plod_street_name = fields.Text(string="Street Name", tracking=True)
    plod_street_number = fields.Text(string="Street Number", tracking=True)
    plod_floor = fields.Text(string="Floor", tracking=True)
    plod_post_code = fields.Text(string="Post Code", tracking=True)
    plod_city_name = fields.Text(string="City Name", tracking=True)
    plod_state_region = fields.Text(string="State Region", tracking=True)
    plod_country = fields.Text(string="Country", tracking=True)

    # ONWARD INLAND ROUTING object
    oir_location_name = fields.Text(string="Location Name", tracking=True)
    oir_un_location_code = fields.Text(string="UN Location Code", tracking=True)
    oir_street_name = fields.Text(string="Street Name", tracking=True)
    oir_street_number = fields.Text(string="Street Number", tracking=True)
    oir_floor = fields.Text(string="Floor", tracking=True)
    oir_post_code = fields.Text(string="Post Code", tracking=True)
    oir_city_name = fields.Text(string="City Name", tracking=True)
    oir_state_region = fields.Text(string="State Region", tracking=True)
    oir_country = fields.Text(string="Country", tracking=True)

    # PRE-CARRIAGE UNDER SHIPPER'S RESPONSIBILITY object
    pre_location_name = fields.Text(string="Location Name", tracking=True)
    pre_latitude = fields.Text(string="Latitude", tracking=True)
    pre_longitude = fields.Text(string="Longitude", tracking=True)
    pre_un_location_code = fields.Text(string="UN Location Code", tracking=True)
    pre_street_name = fields.Text(string="Street Name", tracking=True)
    pre_street_number = fields.Text(string="Street Number", tracking=True)
    pre_floor = fields.Text(string="Floor", tracking=True)
    pre_post_code = fields.Text(string="Post Code", tracking=True)
    pre_city_name = fields.Text(string="City Name", tracking=True)
    pre_state_region = fields.Text(string="State Region", tracking=True)
    pre_country = fields.Text(string="Country", tracking=True)

    is_data_template = fields.Boolean('Is Data Template?', default=False, tracking=True)

    @api.constrains('planned_departure_date', 'planned_arrival_date')
    def _check_planned_arrival_date(self):
        for rec in self:
            today = fields.Date.today()
            if rec.planned_departure_date > rec.planned_arrival_date:
                raise ValidationError(_("Planned Arrival Date cannot be before Planned Departure Date"))
            if rec.planned_arrival_date<today:
                raise ValidationError(_("Planned Arrival Date, cannot be a Past Date"))

    @api.constrains('carrier_booking_reference')
    def _check_carrier_booking_reference(self):
        if len(self.carrier_booking_reference) > 35:
            raise ValidationError('Carrier Booking Reference (No. of characters must not exceed 35)')

    @api.constrains('location_name')
    def _check_location_name(self):
        if len(self.location_name) > 100:
            raise ValidationError('Location Name (No. of characters must not exceed 100)')

    @api.constrains('un_location_code')
    def _check_un_location_code(self):
        if len(self.un_location_code) > 5:
            raise ValidationError('UNlocation Code (No. of characters must not exceed 5)')

    @api.constrains('city_name')
    def _check_city_name(self):
        if len(self.city_name) > 65:
            raise ValidationError('City Name (No. of characters must not exceed 65)')

    @api.constrains('state_region')
    def _check_state_region(self):
        if len(self.state_region) > 65:
            raise ValidationError('State Region (No. of characters must not exceed 65)')

    @api.constrains('country')
    def _check_country(self):
        if len(self.country) > 75:
            raise ValidationError('Country (No. of characters must not exceed 75)')

    @api.constrains('shipping_instruction_ID')
    def _check_shipping_instruction_id(self):
        if len(self.shipping_instruction_ID) > 100:
            raise ValidationError('Shipping Instruction ID (No. of characters must not exceed 100)')

    @api.constrains('transport_document_reference')
    def _check_transport_document_reference(self):
        if len(self.transport_document_reference) > 20:
            raise ValidationError('Transport Document Reference (No. of characters must not exceed 20)')

    @api.constrains('reciept_or_deliverytype_at_origin')
    def _check_reciept_or_deliverytype_at_origin(self):
        if len(self.reciept_or_deliverytype_at_origin) > 3:
            raise ValidationError('Reciept or Deliverytype at Origin (No. of characters must not exceed 3)')

    @api.constrains('reciept_or_deliverytype_at_dest')
    def _check_reciept_or_deliverytype_at_dest(self):
        if len(self.reciept_or_deliverytype_at_dest) > 3:
            raise ValidationError('Reciept or Deliverytype at Destination (No. of characters must not exceed 3)')

    @api.constrains('cargo_movement_type_at_origin')
    def _check_cargo_movement_type_at_origin(self):
        if len(self.cargo_movement_type_at_origin) > 3:
            raise ValidationError('Cargo movement type at Origin (No. of characters must not exceed 3)')

    @api.constrains('cargo_movement_type_at_dest')
    def _check_cargo_movement_type_at_dest(self):
        if len(self.cargo_movement_type_at_dest) > 3:
            raise ValidationError('Cargo movement type at Destination (No. of characters must not exceed 3)')

    @api.constrains('poi_location_name')
    def _check_poi_location_name(self):
        if self.poi_location_name and len(self.poi_location_name) > 100:
            raise ValidationError('Place of Issue, Location name (No. of characters must not exceed 100)')

    @api.constrains('poi_un_location_code')
    def _check_poi_un_location_code(self):
        if self.poi_un_location_code and len(self.poi_un_location_code) > 5:
            raise ValidationError('Place of Issue, UN Location Code(No. of characters must not exceed 5)')

    @api.constrains('poi_street_name')
    def _check_poi_street_name(self):
        if self.poi_street_name and len(self.poi_street_name) > 100:
            raise ValidationError('Place of Issue, Street Name (No. of characters must not exceed 100)')

    @api.constrains('poi_street_number')
    def _check_poi_street_number(self):
        if self.poi_street_number and len(self.poi_street_number) > 50:
            raise ValidationError('Place of Issue, Street Number(No. of characters must not exceed 50)')

    @api.constrains('poi_floor')
    def _check_poi_floor(self):
        if self.poi_floor and len(self.poi_floor) > 50:
            raise ValidationError('Place of Issue, Floor (No. of characters must not exceed 50)')

    @api.constrains('poi_post_code')
    def _check_poi_post_code(self):
        if self.poi_post_code and len(self.poi_post_code) > 10:
            raise ValidationError('Place of Issue, PostCode (No. of characters must not exceed 10)')

    @api.constrains('poi_city_name')
    def _check_poi_city_name(self):
        if self.poi_city_name and len(self.poi_city_name) > 65:
            raise ValidationError('Place of Issue, City Name (No. of characters must not exceed 65)')

    @api.constrains('poi_state_region')
    def _check_poi_state_region(self):
        if self.poi_state_region and len(self.poi_state_region) > 65:
            raise ValidationError('Place of Issue, State Region (No. of characters must not exceed 65)')

    @api.constrains('poi_country')
    def _check_poi_country(self):
        if self.poi_country and len(self.poi_country) > 75:
            raise ValidationError('Place of Issue, Country (No. of characters must not exceed 75)')

    @api.constrains('service_contract_reference')
    def _check_service_contract_reference(self):
        if self.service_contract_reference and len(self.service_contract_reference) > 30:
            raise ValidationError('Service Contract Reference (No. of characters must not exceed 30)')

    @api.constrains('declared_value_currency')
    def _check_declared_value_currency(self):
        if self.declared_value_currency and len(self.declared_value_currency) > 3:
            raise ValidationError('Declared Value Currency (No. of characters must not exceed 3)')

    @api.constrains('issuer_code')
    def _check_issuer_code(self):
        if len(self.issuer_code) > 4:
            raise ValidationError('Issuer Code (No. of characters must not exceed 4)')

    @api.constrains('issuer_code_list_provider')
    def _check_issuer_code_list_provider(self):
        if len(self.issuer_code_list_provider) > 5:
            raise ValidationError('Issuer Code List Provider (No. of characters must not exceed 5)')

    @api.constrains('por_location_name')
    def _check_por_location_name(self):
        if self.por_location_name and len(self.por_location_name) > 100:
            raise ValidationError('Place of Receipt, Location name (No. of characters must not exceed 100)')

    @api.constrains('por_un_location_code')
    def _check_por_un_location_code(self):
        if self.por_un_location_code and len(self.por_un_location_code) > 5:
            raise ValidationError('Place of Receipt, UN Location Code(No. of characters must not exceed 5)')

    @api.constrains('por_street_name')
    def _check_por_street_name(self):
        if self.por_street_name and len(self.por_street_name) > 100:
            raise ValidationError('Place of Receipt, Street Name (No. of characters must not exceed 100)')

    @api.constrains('por_street_number')
    def _check_por_street_number(self):
        if self.por_street_number and len(self.por_street_number) > 50:
            raise ValidationError('Place of Receipt, Street Number(No. of characters must not exceed 50)')

    @api.constrains('por_floor')
    def _check_por_floor(self):
        if self.por_floor and len(self.por_floor) > 50:
            raise ValidationError('Place of Receipt, Floor (No. of characters must not exceed 50)')

    @api.constrains('por_post_code')
    def _check_por_post_code(self):
        if self.por_post_code and len(self.por_post_code) > 10:
            raise ValidationError('Place of Receipt, PostCode (No. of characters must not exceed 10)')

    @api.constrains('por_city_name')
    def _check_por_city_name(self):
        if self.por_city_name and len(self.por_city_name) > 65:
            raise ValidationError('Place of Receipt, City Name (No. of characters must not exceed 65)')

    @api.constrains('por_state_region')
    def _check_por_state_region(self):
        if self.por_state_region and len(self.por_state_region) > 65:
            raise ValidationError('Place of Receipt, State Region (No. of characters must not exceed 65)')

    @api.constrains('por_country')
    def _check_por_country(self):
        if self.por_country and len(self.por_country) > 75:
            raise ValidationError('Place of Receipt, Country (No. of characters must not exceed 75)')

    @api.constrains('pol_location_name')
    def _check_pol_location_name(self):
        if len(self.pol_location_name) > 100:
            raise ValidationError('Port of Loading, Location name (No. of characters must not exceed 100)')

    @api.constrains('pol_un_location_code')
    def _check_pol_un_location_code(self):
        if len(self.pol_un_location_code) > 5:
            raise ValidationError('Port of Loading, UN Location Code(No. of characters must not exceed 5)')

    @api.constrains('pol_city_name')
    def _check_pol_city_name(self):
        if len(self.pol_city_name) > 65:
            raise ValidationError('Port of Loading, City Name (No. of characters must not exceed 65)')

    @api.constrains('pol_state_region')
    def _check_pol_state_region(self):
        if len(self.pol_state_region) > 65:
            raise ValidationError('Port of Loading, State Region (No. of characters must not exceed 65)')

    @api.constrains('pol_country')
    def _check_pol_country(self):
        if len(self.pol_country) > 75:
            raise ValidationError('Port of Loading, Country (No. of characters must not exceed 75)')

    @api.constrains('pod_location_name')
    def _check_pod_location_name(self):
        if len(self.pod_location_name) > 100:
            raise ValidationError('Port of Discharge, Location name (No. of characters must not exceed 100)')

    @api.constrains('pod_un_location_code')
    def _check_pod_un_location_code(self):
        if len(self.pod_un_location_code) > 5:
            raise ValidationError('Port of Discharge, UN Location Code(No. of characters must not exceed 5)')

    @api.constrains('pod_city_name')
    def _check_pod_city_name(self):
        if len(self.pod_city_name) > 65:
            raise ValidationError('Port of Discharge, City Name (No. of characters must not exceed 65)')

    @api.constrains('pod_state_region')
    def _check_pod_state_region(self):
        if len(self.pod_state_region) > 65:
            raise ValidationError('Port of Discharge, State Region (No. of characters must not exceed 65)')

    @api.constrains('pod_country')
    def _check_pod_country(self):
        if len(self.pod_country) > 75:
            raise ValidationError('Port of Discharge, Country (No. of characters must not exceed 75)')

    @api.constrains('plod_location_name')
    def _check_plod_location_name(self):
        if self.plod_location_name and len(self.plod_location_name) > 100:
            raise ValidationError('Place of Delivery, Location name (No. of characters must not exceed 100)')

    @api.constrains('plod_un_location_code')
    def _check_plod_un_location_code(self):
        if self.plod_un_location_code and len(self.plod_un_location_code) > 5:
            raise ValidationError('Place of Delivery, UN Location Code(No. of characters must not exceed 5)')

    @api.constrains('plod_street_name')
    def _check_plod_street_name(self):
        if self.plod_street_name and len(self.plod_street_name) > 100:
            raise ValidationError('Place of Delivery, Street Name (No. of characters must not exceed 100)')

    @api.constrains('plod_street_number')
    def _check_plod_street_number(self):
        if self.plod_street_number and len(self.plod_street_number) > 50:
            raise ValidationError('Place of Delivery, Street Number(No. of characters must not exceed 50)')

    @api.constrains('plod_floor')
    def _check_plod_floor(self):
        if self.plod_floor and len(self.plod_floor) > 50:
            raise ValidationError('Place of Delivery, Floor (No. of characters must not exceed 50)')

    @api.constrains('plod_post_code')
    def _check_plod_post_code(self):
        if self.plod_post_code and len(self.plod_post_code) > 10:
            raise ValidationError('Place of Delivery, PostCode (No. of characters must not exceed 10)')

    @api.constrains('plod_city_name')
    def _check_plod_city_name(self):
        if self.plod_city_name and len(self.plod_city_name) > 65:
            raise ValidationError('Place of Delivery, City Name (No. of characters must not exceed 65)')

    @api.constrains('plod_state_region')
    def _check_plod_state_region(self):
        if self.plod_state_region and len(self.plod_state_region) > 65:
            raise ValidationError('Place of Delivery, State Region (No. of characters must not exceed 65)')

    @api.constrains('plod_country')
    def _check_plod_country(self):
        if self.plod_country and len(self.plod_country) > 75:
            raise ValidationError('Place of Delivery, Country (No. of characters must not exceed 75)')

    @api.constrains('oir_location_name')
    def _check_oir_location_name(self):
        if self.oir_location_name and len(self.oir_location_name) > 100:
            raise ValidationError('Onward Inland Routing, Location name (No. of characters must not exceed 100)')

    @api.constrains('oir_un_location_code')
    def _check_oir_un_location_code(self):
        if self.oir_un_location_code and len(self.oir_un_location_code) > 5:
            raise ValidationError('Onward Inland Routing, UN Location Code(No. of characters must not exceed 5)')

    @api.constrains('oir_street_name')
    def _check_oir_street_name(self):
        if self.oir_street_name and len(self.oir_street_name) > 100:
            raise ValidationError('Onward Inland Routing, Street Name (No. of characters must not exceed 100)')

    @api.constrains('oir_street_number')
    def _check_oir_street_number(self):
        if self.oir_street_number and len(self.oir_street_number) > 50:
            raise ValidationError('Onward Inland Routing, Street Number(No. of characters must not exceed 50)')

    @api.constrains('oir_floor')
    def _check_oir_floor(self):
        if self.oir_floor and len(self.oir_floor) > 50:
            raise ValidationError('Onward Inland Routing, Floor (No. of characters must not exceed 50)')

    @api.constrains('oir_post_code')
    def _check_oir_post_code(self):
        if self.oir_post_code and len(self.oir_post_code) > 10:
            raise ValidationError('Onward Inland Routing, PostCode (No. of characters must not exceed 10)')

    @api.constrains('oir_city_name')
    def _check_oir_city_name(self):
        if self.oir_city_name and len(self.oir_city_name) > 65:
            raise ValidationError('Onward Inland Routing, City Name (No. of characters must not exceed 65)')

    @api.constrains('oir_state_region')
    def _check_oir_state_region(self):
        if self.oir_state_region and len(self.oir_state_region) > 65:
            raise ValidationError('Onward Inland Routing, State Region (No. of characters must not exceed 65)')

    @api.constrains('oir_country')
    def _check_oir_country(self):
        if self.oir_country and len(self.oir_country) > 75:
            raise ValidationError('Onward Inland Routing, Country (No. of characters must not exceed 75)')

    @api.constrains('pre_location_name')
    def _check_pre_location_name(self):
        if self.pre_location_name and len(self.pre_location_name) > 100:
            raise ValidationError(
                'Pre-Carraige under Shippers Responsibility, Location name (No. of characters must not exceed 100)')

    @api.constrains('pre_latitude')
    def _check_pre_latitude(self):
        if self.pre_latitude and len(self.pre_latitude) > 10:
            raise ValidationError(
                'Pre-Carraige under Shippers Responsibility, Latitude (No. of characters must not exceed 10)')

    @api.constrains('pre_longitude')
    def _check_pre_longitude(self):
        if self.pre_longitude and len(self.pre_longitude) > 11:
            raise ValidationError(
                'Pre-Carraige under Shippers Responsibility, Longitude (No. of characters must not exceed 11)')

    @api.constrains('pre_un_location_code')
    def _check_pre_un_location_code(self):
        if self.pre_un_location_code and len(self.pre_un_location_code) > 5:
            raise ValidationError(
                'Pre-Carraige under Shippers Responsibility, UN Location Code(No. of characters must not exceed 5)')

    @api.constrains('pre_street_name')
    def _check_pre_street_name(self):
        if self.pre_street_name and len(self.pre_street_name) > 100:
            raise ValidationError(
                'Pre-Carraige under Shippers Responsibility, Street Name (No. of characters must not exceed 100)')

    @api.constrains('pre_street_number')
    def _check_pre_street_number(self):
        if self.pre_street_number and len(self.pre_street_number) > 50:
            raise ValidationError(
                'Pre-Carraige under Shippers Responsibility, Street Number(No. of characters must not exceed 50)')

    @api.constrains('pre_floor')
    def _check_pre_floor(self):
        if self.pre_floor and len(self.pre_floor) > 50:
            raise ValidationError(
                'Pre-Carraige under Shippers Responsibility, Floor (No. of characters must not exceed 50)')

    @api.constrains('pre_post_code')
    def _check_pre_post_code(self):
        if self.pre_post_code and len(self.pre_post_code) > 10:
            raise ValidationError(
                'Pre-Carraige under Shippers Responsibility, PostCode (No. of characters must not exceed 10)')

    @api.constrains('pre_city_name')
    def _check_pre_city_name(self):
        if self.pre_city_name and len(self.pre_city_name) > 65:
            raise ValidationError(
                'Pre-Carraige under Shippers Responsibility, City Name (No. of characters must not exceed 65)')

    @api.constrains('pre_state_region')
    def _check_pre_state_region(self):
        if self.pre_state_region and len(self.pre_state_region) > 65:
            raise ValidationError(
                'Pre-Carraige under Shippers Responsibility, State Region (No. of characters must not exceed 65)')

    @api.constrains('pre_country')
    def _check_pre_country(self):
        if self.pre_country and len(self.pre_country) > 75:
            raise ValidationError(
                'Pre-Carraige under Shippers Responsibility, Country (No. of characters must not exceed 75)')

