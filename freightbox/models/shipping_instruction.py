from odoo import models, fields, _, api
from odoo.exceptions import ValidationError,UserError
from odoo.modules.module import get_module_resource
from lxml import etree


class ShippingInstruction(models.Model):
    _inherit = 'shipping.instruction'
    # _inherit = ['mail.thread', 'mail.activity.mixin']
    # _description = "Shipping Instruction"
    # _rec_name = 'si_sequence_id'

    # name = fields.Char("SI", default=lambda self: _('New'))
    # transport_document_type_code = fields.Selection([('bol', 'BOL'), ('swb', 'SWB')], default='bol', tracking=True,
    #                                                 string="Transport Document Type Code",
    #                                                 help="Specifies the type of transport document (BOL) or a Sea Waybill (SWB)")
    # is_shipped_onboard_type = fields.Boolean("Is Shipped Onboard Type", tracking=True,
    #                                          help="Specifies whether the Transport document is a received for shipment or shipped onboard.")
    # number_of_originals = fields.Integer("Number of originals", tracking=True,
    #                                      help="The requested number of originals of the Transport document to be issued by the carrier. Only applicable for physical documents.")
    # number_of_copies = fields.Integer("Number of copies", tracking=True,
    #                                   help="The requested number of copies of the Transport document to be issued by the carrier.")
    # pre_carriage_under_shippers_responsibility = fields.Text("Pre-carriage under shipper’s responsibility",
    #                                                          tracking=True,
    #                                                          help="Mode of transportation for precarriage (e.g., truck, barge, rail)")
    # is_electronic = fields.Boolean("Is Electronic", default=True, tracking=True, required=True,
    #                                help="Indicates whether the transport document should be electronic or not.")
    # carrier_booking_reference = fields.Text("Carrier Booking Reference", tracking=True,
    #                                         help="The associated booking number provided by the carrier.")
    # is_charges_displayed = fields.Boolean("Is Charges Displayed", tracking=True, default=True,
    #                                       help="Indicates whether Charges are displayed.")
    # location_name = fields.Text("Location Name", tracking=True, help="Name of the location.")
    # un_location_code = fields.Text("UN Location Code", tracking=True,
    #                                help="The UN Location code specifying where the place is located.")
    # city_name = fields.Text("City Name", tracking=True, help="The city name of the party’s address.")
    # state_region = fields.Text("State Region", tracking=True, help="The state/region of the party’s address.")
    # country = fields.Text("Country", tracking=True, help="The country of the party’s address.")
    # si_created_by = fields.Text("Created By", tracking=True, default=lambda self: self.env.user.partner_id.name)
    # si_updated_by = fields.Text("Updated By", tracking=True, default=lambda self: self.env.user.partner_id.name)
    # si_inquiry_no = fields.Many2one('crm.lead', string="Inquiry ID", readonly=True, tracking=True)
    # shipping_instruction_id = fields.Text("Shipping Instruction ID", tracking=True)
    # saved_si_name = fields.Text("Open SI Name", tracking=True)
    # job_id = fields.Many2one("job", string="Job", tracking=True)
    # cont_id = fields.Char("Container ID", tracking=True)
    # state = fields.Selection([
    #     ('open', 'Open'),
    #     ('draft', 'Draft'),
    #     ('si_sent', 'SI Sent'),
    #     ('update in progress', 'Update In Progress'),
    #     ('updated', 'Updated'),
    #     ('accepted', 'Accepted'),
    #     ('rejected', 'Rejected'),
    #     ('cancelled', 'Cancelled'),
    #     # ('amended', 'Amended'),
    # ], string='Status', index=True, readonly=True, copy=False, default='open', tracking=True, )
    # is_shipping_instruction = fields.Boolean(string="Is Shipping Instruction", tracking=True)
    # is_shipping_instruction_ammendment = fields.Boolean(string="Is Shipping Instruction Ammendment")
    # cargo_items_line = fields.One2many('cargo.line.items', 'cargo_line_id', string="Cargo", tracking=True)
    # transport_equipment_line = fields.One2many('transport.equipment', 'transport_equipment_line_id',
    #                                            string="Transport Equipment")
    # document_parties_line = fields.One2many('document.parties', 'document_parties_line_id')
    # shipment_location_line = fields.One2many('shipment.location', 'shipment_location_line_id',
    #                                          string="Shipment Location")
    # references_line = fields.One2many('shipping.references', 'references_line_id', string="References")
    # update_si = fields.Boolean(string="Update Shipping Instruction")
    # shipper_id = fields.Many2one('res.partner', "Shipper", default=lambda self: self.env.user.partner_id)
    # si_uploaded_from_shipper = fields.Binary('SI Uploaded From Shipper', attachment=True)
    # si_upload_shipper = fields.Binary('SI Upload', attachment=True)
    # si_uploaded_from_shipper_fname = fields.Char('File Name')
    # is_saved = fields.Boolean(string="Is Saved")
    # reject_reason = fields.Text('Reject Reason', tracking=True)
    # reject_bool = fields.Boolean(string='Reject Bool')
    # shipment_event_line = fields.One2many('shipment.event', 'shipment_event_line_id', string='Shipment Event')
    si_templates = fields.Many2one('si.templates', string="New SI Template")
    # transport_id = fields.Many2one("transport", string="Transport", ondelete='cascade')
    # bill_of_lading_id = fields.Many2one("bill.of.lading", string="Bill of Lading")
    # transport_container_id = fields.Text('Container ID')
    # si_sequence_id = fields.Text("SI Seq. ID", default=lambda self: _('New'))
    # is_bol_created = fields.Boolean(string="Is BOL created")
    # active = fields.Boolean(string='Active', default=True)
    # booking_user_id = fields.Many2one('res.users', string="Shipper/FF")

    @api.model
    def action_open_draft_si_form_view(self):
        view_id = self.env.ref('freightbox.shipping_instruction_tree_view').id
        view_form_id = self.env.ref('freightbox.shipping_instuction_form_view').id
        action = {
            'name': _('Draft Shipping Instruction'),
            'type': 'ir.actions.act_window',
            'res_model': 'shipping.instruction',
            'view_type': 'list',
            'views': [(view_id, 'list'), (view_form_id, 'form')],
            'view_mode': 'list,form',
        }
        return action

    def action_shiper_send(self):
        """ Open a window to compose an email, with the edi invoice template
            message loaded by default
        """
        outmail_rec = self.env['ir.mail_server'].search([])
        if not outmail_rec:
            raise UserError("Outgoing mail server not set !!!")
            
        self.ensure_one()
        template = self.env.ref('freightbox.mail_template_crm', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='shipping.instruction',
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

    def action_si_send(self):
        """ Open a window to compose an email, with the edi invoice template
            message loaded by default
        """
        outmail_rec = self.env['ir.mail_server'].search([])
        if not outmail_rec:
            raise UserError("Outgoing mail server not set !!!")

        self.ensure_one()
        template = self.env.ref('freightbox.mail_template_si', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='shipping.instruction',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template.id,
            default_composition_mode='comment',
            force_email=True,
        )
        # self.write({'state': 'si_sent'})
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

    def generate_pdf(self):
        file_path = get_module_resource('freightbox', 'report')
        return self.env.ref('freightbox.action_report_shipping_instruction').report_action(self)

    @api.onchange('si_templates')
    def onchange_si_template(self):
        si_template = self.si_templates
        if si_template:
            self.transport_document_type_code = si_template.transport_document_type_code
            self.is_shipped_onboard_type = si_template.is_shipped_onboard_type
            self.number_of_originals = si_template.number_of_originals
            self.number_of_copies = si_template.number_of_copies
            self.pre_carriage_under_shippers_responsibility = si_template.pre_carriage_under_shippers_responsibility
            self.is_charges_displayed = si_template.is_charges_displayed
            self.location_name = si_template.location_name
            self.un_location_code = si_template.un_location_code
            self.city_name = si_template.city_name
            self.state_region = si_template.state_region
            self.country = si_template.country
            # get the list of cargo items from template and create.
            cargo_lines = [(5, 0, 0)]
            container_id = self.transport_id.cont_id
            for cl in si_template.si_template_cargo_items_line:
                cl_vals = {
                    'cargo_line_items_id': cl.cargo_line_items_id,
                    'shipping_marks': cl.shipping_marks,
                    'carrier_booking_reference': self.carrier_booking_reference,
                    'description_of_goods': cl.description_of_goods,
                    'hs_code': cl.hs_code,
                    'number_of_packages': cl.number_of_packages,
                    'weight': cl.weight,
                    'volume': cl.volume,
                    'weight_unit': cl.weight_unit,
                    'volume_unit': cl.volume_unit,
                    'package_code': cl.package_code,
                    'equipment_reference': container_id,
                    'cargo_array_created_by': cl.cargo_array_created_by,
                }
                cargo_lines.append((0, 0, cl_vals))
            self.cargo_items_line = cargo_lines
            # get the list of transport_equipment_line from template and create.
            transport_equipment_lines = [(5, 0, 0)]
            for tq in si_template.si_template_transport_equipment_line:
                trans_eq_vals = {
                    'equipment_reference_id': container_id,
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
                }
                transport_equipment_lines.append((0, 0, trans_eq_vals))
            self.transport_equipment_line = transport_equipment_lines
            # get the list of document_parties_line from template and create.
            document_parties_lines = [(5, 0, 0)]
            for dp in si_template.si_template_document_parties_line:
                dp_vals = {
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
                }
                document_parties_lines.append((0, 0, dp_vals))
            self.document_parties_line = document_parties_lines

            # get the list of shipment_location_lines from template and create.
            shipment_location_lines = [(5, 0, 0)]
            for sl in si_template.si_template_shipment_location_line:
                sl_vals = {
                    'location_type': sl.location_type.id,
                    'displayed_name': sl.displayed_name,
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
                    'shipment_location_array_created_by': sl.shipment_location_array_created_by,
                }
                shipment_location_lines.append((0, 0, sl_vals))
            self.shipment_location_line = shipment_location_lines
            # get the list of shipment_location_lines from template and create.
            references_lines = [(5, 0, 0)]
            for rc in si_template.si_template_references_line:
                rc_vals = {
                    'reference_type': rc.reference_type,
                    'reference_value': rc.reference_value,
                    'references_array_created_by': rc.references_array_created_by,
                }
                references_lines.append((0, 0, rc_vals))
            self.references_line = references_lines
        else:
            self.transport_document_type_code = ""
            self.is_shipped_onboard_type = ""
            self.number_of_originals = ""
            self.number_of_copies = ""
            self.pre_carriage_under_shippers_responsibility = ""
            # self.carrier_booking_reference = ""
            self.is_charges_displayed = ""
            self.location_name = ""
            self.un_location_code = ""
            self.city_name = ""
            self.state_region = ""
            self.country = ""
            self.cargo_items_line = False
            self.transport_equipment_line = False
            self.document_parties_line = False
            self.shipment_location_line = False
            self.references_line = False

    def button_create_si_template(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'si.templates.wiz',
            'view_mode': 'form',
            'views': [(self.env.ref('freightbox.si_template_form_view_wiz').id, "form")],
            'context': {'current_id': self.id},
            'target': 'new',
        }

    def si_tutorial_video_new_tab(self):
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
        if view_id == self.env.ref("freightbox.shipping_instuction_form_view").id:
            url = self.env['ir.config_parameter'].sudo().get_param('freightbox.si_tutorial_video',
                                                                   "/freightbox/static/src/img/index_file_images/not_found.png")
            doc = etree.XML(result['arch'])
            for node in doc.xpath("//iframe[@id='si_tutorial_video']"):
                node.set('src', url)
            result['arch'] = etree.tostring(doc)
        return result


class CargoLineItems(models.Model):
    _inherit = 'cargo.line.items'
    # _description = "Cargo Line Items"


    # cargo_line_id = fields.Many2one('shipping.instruction', string='Cargo Line Item')
    # cargo_line_id_is_to_update = fields.Boolean(string='SI Update In Progress', related='cargo_line_id.update_si')
    # bol_cargo_line_id = fields.Many2one('bill.of.lading', string='BOL Cargo Line Item')
    # cargo_line_items_id = fields.Text('Cargo Line Item ID',track_visibility='onchange',
    #                                   help="Identifies the cargo line item (package) within the cargo.")
    # new_cargo_line_items_id = fields.Text('New Cargo Line Item ID')
    # shipping_marks = fields.Text('Shipping Marks',
    #                              help="The identifying details on a package or the actual markings that appear on the package(s).")
    # new_shipping_marks = fields.Text('New Shipping Marks')
    # carrier_booking_reference = fields.Text('Carrier Booking Reference',
    #                                         help="The associated booking number provided by the carrier for this cargo line item.")
    # new_carrier_booking_reference = fields.Text('New Carrier Booking Reference')
    # description_of_goods = fields.Text('Description of Goods',
    #                                    help="The cargo description are details which accurately and properly describe the cargo being shipped in the container(s).")
    # new_description_of_goods = fields.Text('New Description of Goods')
    # hs_code = fields.Text('HS Code', help="The type of HS code depends on country and customs requirements.")
    # new_hs_code = fields.Text('New HS Code')
    # number_of_packages = fields.Integer('Number of Packages',
    #                                     help="Specifies the number of packages associated with this cargo item.")
    # new_number_of_packages = fields.Integer('New Number of Packages')
    # weight = fields.Float('Weight',
    #                       help="The weight of the cargo item including packaging items being carried in the container(s).")
    # new_weight = fields.Float('New Weight')
    # volume = fields.Float('Volume', help="Calculated by multiplying the width,height, and length of the packed cargo.")
    # new_volume = fields.Float('New Volume')
    # weight_unit = fields.Text('Weight Unit',
    #                           help="The unit of measure, which can be expressed in either imperial or metric terms.")
    # new_weight_unit = fields.Text('New Weight Unit')
    # volume_unit = fields.Text('Volume Unit',
    #                           help="The unit of measure which can be expressed in either MTQ or FTQ, as provided by the shipper.")
    # new_volume_unit = fields.Text('New Volume Unit')
    # package_code = fields.Text('Package Code', help="A code identifying the outer package.")
    # new_package_code = fields.Text('New Package Code')
    # equipment_reference = fields.Text('Container ID',
    #                                   help="The unique identifier for the equipment, which should follow the BIC ISO Container Identification Number where possible.")  # equipment_reference is container id
    # new_equipment_reference = fields.Text('New Container ID')
    # cargo_array_created_by = fields.Text('Created By')
    si_template_cargo_line_id = fields.Many2one('si.templates', string='SI Cargo Line Item')
    # update_si_cargo = fields.Boolean('Update Shipping instruction')
    # cargo_line_items_row_id = fields.Text('Cargo line items row ID')
    # cli_modified_by = fields.Text('Cargo Line Item ID Modified By')
    # cli_is_approved = fields.Boolean('Cargo Line Item ID Approve')
    # sm_modified_by = fields.Text('shipping Marks Modified By')
    # sm_is_approved = fields.Boolean('shipping Marks Approve')
    # cbr_modified_by = fields.Text('Carrier Booking Ref Modified By')
    # cbr_is_approved = fields.Boolean('Carrier Booking Ref Approved')
    # dsg_modified_by = fields.Text('Description of Goods Modified By')
    # dsg_is_approved = fields.Boolean('Description of Goods Approved')
    # hc_modified_by = fields.Text('HS Code Modified By')
    # hc_is_approved = fields.Boolean('HS Code Approved')
    # nop_modified_by = fields.Text('No. of Packages Modified By')
    # nop_is_approved = fields.Boolean('No. of Packages Approved')
    # wgt_modified_by = fields.Text('Weight Modified By')
    # wgt_is_approved = fields.Boolean('Weight Approved')
    # vol_modified_by = fields.Text('Volume Modified By')
    # vol_is_approved = fields.Boolean('Volume Approved')
    # wu_modified_by = fields.Text('Weight Unit Modified By')
    # wu_is_approved = fields.Boolean('Weight Unit Approved')
    # vu_modified_by = fields.Text('Volume Unit Modified By')
    # vu_is_approved = fields.Boolean('Volume Unit Approved')
    # pc_modified_by = fields.Text('Package Code Modified By')
    # pc_is_approved = fields.Boolean('Package Code Approved')
    # eq_modified_by = fields.Text('Container ID Modified By')
    # eq_is_approved = fields.Boolean('Container ID Approved')
    # si_name = fields.Text('Shipping ID')


class TransportEquipment(models.Model):
    _inherit = 'transport.equipment'
#     _description = "Transport Equipment"
#
#     @api.constrains('equipment_reference_id')
#     def _check_equipment_reference_id(self):
#         for line in self:
#             if line.equipment_reference_id and len(line.equipment_reference_id) > 15:
#                 raise ValidationError(
#                     'Container ID in Transport Equipment(No. of characters must not exceed 15)')
#
#     @api.constrains('weight_unit')
#     def _check_weight_unit(self):
#         for line in self:
#             if line.weight_unit and len(line.weight_unit) > 3:
#                 raise ValidationError('Weight Unit in Transport Equipment (No. of characters must not exceed 3)')
#
#     @api.constrains('iso_equipment_code')
#     def _check_iso_equipment_code(self):
#         for line in self:
#             if line.iso_equipment_code and len(line.iso_equipment_code) > 4:
#                 raise ValidationError('ISO Equipment Code in Transport Equipment (No. of characters must not exceed 4)')
#
#     @api.constrains('temperature_unit')
#     def _check_temperature_unit(self):
#         for line in self:
#             if line.temperature_unit and len(line.temperature_unit) > 3:
#                 raise ValidationError('Temperature Unit in Transport Equipment (No. of characters must not exceed 3)')
#             print("line.temperature_unit", line.temperature_unit)
#             if line.temperature_unit not in ['CEL', 'FAH']:
#                 raise ValidationError('Temperature Unit in Transport Equipment can either be CEL or FAH')
#
#     @api.constrains('seal_number')
#     def _check_seal_number(self):
#         for line in self:
#             if line.seal_number and len(line.seal_number) > 15:
#                 raise ValidationError('Seal Number in Transport Equipment (No. of characters must not exceed 15)')
#
#     @api.constrains('seal_source')
#     def _check_seal_source(self):
#         for line in self:
#             if line.seal_source and len(line.seal_source) > 5:
#                 raise ValidationError('Seal Source in Transport Equipment (No. of characters must not exceed 5)')
#
#     @api.constrains('seal_type')
#     def _check_seal_type(self):
#         for line in self:
#             if line.seal_type and len(line.seal_type) > 5:
#                 raise ValidationError('Seal Type in Transport Equipment (No. of characters must not exceed 5)')
#
#     transport_equipment_line_id = fields.Many2one('shipping.instruction', string='Transport Equipment')
#     bol_tq_line_id = fields.Many2one('bill.of.lading', string='BOL Transport Equipment')
#     transport_equipment_row_id = fields.Text('Transport Equipment row ID')
#     equipment_reference_id = fields.Text(string='Container ID',
#                                          help="The unique identifier for the equipment, which should follow the BIC ISO Container Identification Number where possible.")
#     new_equipment_reference_id = fields.Text(string='New Container ID')
#     eqr_modified_by = fields.Text('Container ID Modified By')
#     eqr_is_approved = fields.Boolean('Container ID Approved')
#     weight_unit = fields.Text(string='Weight Unit',
#                               help="The unit of measure, which can be expressed in either imperial or metric terms.")
#     new_weight_unit = fields.Text(string='New Weight Unit')
#     wtu_modified_by = fields.Text('Weight Unit Modified By')
#     wtu_is_approved = fields.Boolean('Weight Unit Approved')
#     cargo_gross_weight = fields.Float(string="Cargo Gross Weight",
#                                       help="The grand total weight of the cargo and weight per container(s) including packaging items being carried,which can be expressed in imperial or metric terms.")
#     new_cargo_gross_weight = fields.Float(string="New Cargo Gross Weight")
#     cgw_modified_by = fields.Text('Cargo Gross Weight Modified By')
#     cgw_is_approved = fields.Boolean('Cargo Gross Weight Approved')
#     container_tare_weight = fields.Float(string="Container Tare Weight",
#                                          help="Tare weight of the container as registered on the CSC plate of the physical container unit.")
#     new_container_tare_weight = fields.Float(string="New Container Tare Weight")
#     ctw_modified_by = fields.Text('Container Tare Weight Modified By')
#     ctw_is_approved = fields.Boolean('Container Tare Weight Approved')
#     iso_equipment_code = fields.Text(string="ISO Equipment Code",
#                                      help="Unique code for the different equipment size/type used for transporting commodities")
#     new_iso_equipment_code = fields.Text(string="New ISO Equipment Code")
#     iso_ec_modified_by = fields.Text('ISO Equipment Code Modified By')
#     iso_ec_is_approved = fields.Boolean('ISO Equipment Code Approved')
#     is_shipper_owned = fields.Boolean(string="Is Shipper Owned",
#                                       help="Indicates whether the container is shipper owned (SOC)")
#     new_is_shipper_owned = fields.Boolean(string="New Is Shipper Owned")
#     is_so_modified_by = fields.Text('Is Shipper Owned Modified By')
#     is_so_is_approved = fields.Boolean('Is Shipper Owned Approved')
#     temperature_min = fields.Float(string="Temperature Min",
#                                    help="Indicates the minimum temperature setting on the container")
#     new_temperature_min = fields.Float(string="New Temperature Min")
#     tm_modified_by = fields.Text('Temperature Min Modified By')
#     tm_is_approved = fields.Boolean('Temperature Min Approved')
#     temperature_max = fields.Float(string="Temperature Max",
#                                    help="Indicates the maximum temperature setting on the container")
#     new_temperature_max = fields.Float(string="New Temperature Max")
#     tma_modified_by = fields.Text('Temperature Max Modified By')
#     tma_is_approved = fields.Boolean('Temperature Max Approved')
#     temperature_unit = fields.Text(string="Temperature Unit", help="Celsius (CEL) or Fahrenheit (FAH)")
#     new_temperature_unit = fields.Text(string="New Temperature Unit")
#     tu_modified_by = fields.Text('Temperature Unit Modified By')
#     tu_is_approved = fields.Boolean('Temperature Unit Approved')
#     humidity_min = fields.Float(string="Humidity Min",
#                                 help="Indicates the minimum humidity setting on the container in percent")
#     new_humidity_min = fields.Float(string="New Humidity Min")
#     hm_modified_by = fields.Text('Humidity Min Modified By')
#     hm_is_approved = fields.Boolean('Humidity Min Approved')
#     humidity_max = fields.Float(string="Humidity Max",
#                                 help="Indicates the maximum humidity setting on the container in percent.")
#     new_humidity_max = fields.Float(string="New Humidity Max")
#     hma_modified_by = fields.Text('Humidity Max Modified By')
#     hma_is_approved = fields.Boolean('Humidity Max Approved')
#     ventilation_min = fields.Float(string="Ventilation Min",
#                                    help="Indicates the minimum ventilation setting on the container CBM/Hr")
#     new_ventilation_min = fields.Float(string="New Ventilation Min")
#     vm_modified_by = fields.Text('Ventilation Min Modified By')
#     vm_is_approved = fields.Boolean('Ventilation Min Approved')
#     ventilation_max = fields.Float(string="Ventilation Max",
#                                    help="Indicates the maximum ventilation setting on the container CBM/Hr")
#     new_ventilation_max = fields.Float(string="New Ventilation Max")
#     vma_modified_by = fields.Text('Ventilation Max Modified By')
#     vma_is_approved = fields.Boolean('Ventilation Max Approved')
#     seal_number = fields.Text(string="Seal Number", help=" Indicates the number or reference listed on the Seal")
#     new_seal_number = fields.Text(string="New Seal Number")
#     sn_modified_by = fields.Text('Seal Number Modified By')
#     sn_is_approved = fields.Boolean('Seal Number Approved')
#     seal_source = fields.Text(string="Seal Source", help="The source of seal, namely who has affixed the seal.")
#     new_seal_source = fields.Text(string="New Seal Source")
#     ss_modified_by = fields.Text('Seal Source Modified By')
#     ss_is_approved = fields.Boolean('Seal Source Approved')
#     seal_type = fields.Text(string="Seal Type", help=" Addresses the type of seal")
#     new_seal_type = fields.Text(string="New Seal Type")
#     st_modified_by = fields.Text('Seal Type Modified By')
#     st_is_approved = fields.Boolean('Seal Type Approved')
#     transport_equipment_array_created_by = fields.Text('Created By')
    si_template_transport_equipment_line_id = fields.Many2one('si.templates', string='SI Transport Equipment')
#     tq_is_to_update = fields.Boolean(string='SI Update In Progress', related='transport_equipment_line_id.update_si')
#     si_name = fields.Text('Shipping ID')
#
#     def button_open_update_tq(self):
#         return {
#             'type': 'ir.actions.act_window',
#             'res_model': 'transport.equipment',
#             'view_mode': 'form',
#             'views': [(self.env.ref('freightbox.update_edit_tq_form_view').id, "form")],
#             'res_id': self.id,
#             'target': 'new',
#         }
#
#     def button_approve(self):
#         if self.equipment_reference_id:
#             self.equipment_reference_id = self.new_equipment_reference_id
#         else:
#             self.equipment_reference_id = self.equipment_reference_id
#         if self.weight_unit:
#             self.weight_unit = self.new_weight_unit
#         else:
#             self.weight_unit = self.weight_unit
#         if self.cargo_gross_weight:
#             self.cargo_gross_weight = self.new_cargo_gross_weight
#         else:
#             self.cargo_gross_weight = self.cargo_gross_weight
#         if self.container_tare_weight:
#             self.container_tare_weight = self.new_container_tare_weight
#         else:
#             self.container_tare_weight = self.container_tare_weight
#         if self.iso_equipment_code:
#             self.iso_equipment_code = self.new_iso_equipment_code
#         else:
#             self.iso_equipment_code = self.iso_equipment_code
#         if self.is_shipper_owned:
#             self.is_shipper_owned = self.new_is_shipper_owned
#         else:
#             self.is_shipper_owned = self.is_shipper_owned
#         if self.temperature_min:
#             self.temperature_min = self.new_temperature_min
#         else:
#             self.temperature_min = self.temperature_min
#         if self.temperature_max:
#             self.temperature_max = self.new_temperature_max
#         else:
#             self.temperature_max = self.temperature_max
#         if self.temperature_unit:
#             self.temperature_unit = self.new_temperature_max
#         else:
#             self.temperature_unit = self.temperature_unit
#         if self.humidity_min:
#             self.humidity_min = self.new_humidity_min
#         else:
#             self.humidity_min = self.humidity_min
#         if self.humidity_max:
#             self.humidity_max = self.new_humidity_max
#         else:
#             self.humidity_max = self.humidity_max
#         if self.ventilation_min:
#             self.ventilation_min = self.new_ventilation_min
#         else:
#             self.ventilation_min = self.ventilation_min
#         if self.ventilation_max:
#             self.ventilation_max = self.new_ventilation_max
#         else:
#             self.ventilation_max = self.ventilation_max
#         if self.seal_number:
#             self.seal_number = self.new_seal_number
#         else:
#             self.seal_number = self.seal_number
#         if self.seal_source:
#             self.seal_source = self.new_seal_source
#         else:
#             self.seal_source = self.seal_source
#         if self.seal_type:
#             self.seal_type = self.new_seal_type
#         else:
#             self.seal_type = self.seal_type
#         return True
#
#
class DocumentParties(models.Model):
    _inherit = 'document.parties'
#     _description = "Document Parties"
#
#     @api.constrains('party_name_id')
#     def _check_party_name_id(self):
#         for line in self:
#             if line.party_name_id and len(line.party_name_id) > 100:
#                 raise ValidationError('Party Name Id in Document Parties (No. of characters must not exceed 100)')
#
#     @api.constrains('tax_reference_1')
#     def _check_tax_reference_1(self):
#         for line in self:
#             if line.tax_reference_1 and len(line.tax_reference_1) > 20:
#                 raise ValidationError('Tax Reference 1 in Document Parties (No. of characters must not exceed 20)')
#
#     @api.constrains('public_key')
#     def _check_public_key(self):
#         for line in self:
#             if line.public_key and len(line.public_key) > 500:
#                 raise ValidationError('Public Key in Document Parties (No. of characters must not exceed 500)')
#
#     @api.constrains('street')
#     def _check_street(self):
#         for line in self:
#             if line.street and len(line.street) > 100:
#                 raise ValidationError('Street in Document Parties (No. of characters must not exceed 100)')
#
#     @api.constrains('street_number')
#     def _check_street_number(self):
#         for line in self:
#             if line.street_number and len(line.street_number) > 50:
#                 raise ValidationError('Street Number in Document Parties (No. of characters must not exceed 50)')
#
#     @api.constrains('floor')
#     def _check_floor(self):
#         for line in self:
#             if line.floor and len(line.floor) > 50:
#                 raise ValidationError('Floor in Document Parties (No. of characters must not exceed 50)')
#
#     @api.constrains('post_code')
#     def _check_post_code(self):
#         for line in self:
#             if line.post_code and len(line.post_code) > 10:
#                 raise ValidationError('Post Code in Document Parties (No. of characters must not exceed 10)')
#
#     @api.constrains('city')
#     def _check_city(self):
#         for line in self:
#             if line.city and len(line.city) > 65:
#                 raise ValidationError('City in Document Parties (No. of characters must not exceed 65)')
#
#     @api.constrains('state_region')
#     def _check_state_region(self):
#         for line in self:
#             if line.state_region and len(line.state_region) > 65:
#                 raise ValidationError('State Region in Document Parties (No. of characters must not exceed 65)')
#
#     @api.constrains('country')
#     def _check_country(self):
#         for line in self:
#             if line.country and len(line.country) > 75:
#                 raise ValidationError('Country in Document Parties (No. of characters must not exceed 75)')
#
#     @api.constrains('tax_reference_2')
#     def _check_tax_reference_2(self):
#         for line in self:
#             if line.tax_reference_2 and len(line.tax_reference_2) > 20:
#                 raise ValidationError('Tax Reference 2 in Document Parties (No. of characters must not exceed 20)')
#
#     @api.constrains('nmfta_code')
#     def _check_nmfta_code(self):
#         for line in self:
#             if line.nmfta_code and len(line.nmfta_code) > 4:
#                 raise ValidationError('NMFTA Code in Document Parties (No. of characters must not exceed 4)')
#
#     @api.constrains('party_function')
#     def _check_party_function(self):
#         for line in self:
#             if len(line.party_function) > 3:
#                 raise ValidationError('Party Function in Document Parties (No. of characters must not exceed 3)')
#
#     @api.constrains('address_line')
#     def _check_address_line(self):
#         for line in self:
#             if line.address_line and len(line.address_line) > 250:
#                 raise ValidationError('Address Line in Document Parties (No. of characters must not exceed 250)')
#
#     @api.constrains('name')
#     def _check_name(self):
#         for line in self:
#             if len(line.name) > 100:
#                 raise ValidationError('Name in Document Parties (No. of characters must not exceed 100)')
#
#     @api.constrains('email')
#     def _check_email(self):
#         for line in self:
#             if len(line.email) > 100:
#                 raise ValidationError('Email in Document Parties (No. of characters must not exceed 100)')
#
#     @api.constrains('phone')
#     def _check_phone(self):
#         for line in self:
#             if len(line.phone) > 30:
#                 raise ValidationError('Phone in Document Parties (No. of characters must not exceed 30)')
#
#     document_parties_line_id = fields.Many2one('shipping.instruction', string="Document Parties Line")
#     dp_line_id_is_to_update = fields.Boolean(string='Document Parties Update In Progress',
#                                              related='document_parties_line_id.update_si')
#     bol_dp_line_id = fields.Many2one('bill.of.lading', string="BOL Document Parties Line")
#     document_parties_row_id = fields.Text('Document parties row ID')
#     new_document_parties_row_id = fields.Text('New Document parties row ID')
#     dp_modified_by = fields.Text('Document parties Modified By')
#     dp_is_approved = fields.Boolean('Document parties Approved')
#     party_name_id = fields.Text(string="Party Name", help="Name of the party")
#     new_party_name_id = fields.Text(string="New Party Name")
#     pn_modified_by = fields.Text('Party Name Modified By')
#     pn_is_approved = fields.Boolean('Party Name Approved')
#     tax_reference_1 = fields.Text(string="Tax Reference 1",
#                                   help="The identifying number of the consignee or shipper (Individual or entity) used for tax purposes")
#     new_tax_reference_1 = fields.Text(string="New Tax Reference 1")
#     tax1_modified_by = fields.Text('Tax Reference 1 Modified By')
#     tax1_is_approved = fields.Boolean('Tax Reference 1 Approved')
#     public_key = fields.Text(string="Public Key", help="The public key used for a digital signature")
#     new_public_key = fields.Text(string="New Public Key")
#     pk_modified_by = fields.Text('Public Key Modified By')
#     pk_is_approved = fields.Boolean('Public Key Approved')
#     street = fields.Text(string="Street", help="The name of the street of the party’s address")
#     new_street = fields.Text(string="New Street")
#     strt_modified_by = fields.Text('Street Modified By')
#     strt_is_approved = fields.Boolean('Street Approved')
#     street_number = fields.Text(string="Street Number", help="The number of the street of the party’s address")
#     new_street_number = fields.Text(string="New Street Number")
#     stno_modified_by = fields.Text('Street Number Modified By')
#     stno_is_approved = fields.Boolean('Street Number Approved')
#     floor = fields.Text(string="Floor", help="The floor of the party’s street number")
#     new_floor = fields.Text(string="New Floor")
#     flr_modified_by = fields.Text('Floor Modified By')
#     flr_is_approved = fields.Boolean('Floor Approved')
#     post_code = fields.Text(string="Post Code", help="The post code of the party’s address")
#     new_post_code = fields.Text(string="New Post Code")
#     pc_modified_by = fields.Text('Post Code Modified By')
#     pc_is_approved = fields.Boolean('Post Code Approved')
#     city = fields.Text(string="City", help="The city name of the party’s address")
#     new_city = fields.Text(string="New City")
#     cty_modified_by = fields.Text('City Modified By')
#     cty_is_approved = fields.Boolean('City Approved')
#     state_region = fields.Text(string="State Region", help="The state/region of the party’s address")
#     new_state_region = fields.Text(string="New State Region")
#     str_modified_by = fields.Text('State Region Modified By')
#     str_is_approved = fields.Boolean('State Approved')
#     country = fields.Text(string="Country", help="The country of the party’s address")
#     new_country = fields.Text(string="New Country")
#     cntry_modified_by = fields.Text('Country Modified By')
#     cntry_is_approved = fields.Boolean('Country Approved')
#     tax_reference_2 = fields.Text(string="Tax Reference 2",
#                                   help="The 2nd identifying number of the consignee or shipper (Individual or entity) used for tax purposes")
#     new_tax_reference_2 = fields.Text(string="New Tax Reference 2")
#     tax2_modified_by = fields.Text('Tax Reference 2 Modified By')
#     tax2_is_approved = fields.Boolean('Tax Reference 2 Approved')
#     nmfta_code = fields.Text(string="NMFTA Code", help="The applicable SCAC code for a party.")
#     new_nmfta_code = fields.Text(string="New NMFTA Code")
#     nmfta_modified_by = fields.Text('NMFTA Code Modified By')
#     nmfta_is_approved = fields.Boolean('NMFTA Code Approved')
#     party_function = fields.Text(string="Party Function",
#                                  help="The name of the specific role, which can be one of the following values: OS,CN,COW,COX,N1,N2,NI,DDR,DDS,MS.")
#     new_party_function = fields.Text(string="New Party Function")
#     pf_modified_by = fields.Text('Party Function Modified By')
#     pf_is_approved = fields.Boolean('Party Function Approved')
#     address_line = fields.Text(string="Address Line", help="Address of the party")
#     new_address_line = fields.Text(string="New Address Line")
#     al_modified_by = fields.Text('Address Line Modified By')
#     al_is_approved = fields.Boolean('Address Line Approved')
#     name = fields.Text(string="Name", help="Name of the contact")
#     new_name = fields.Text(string="New Name")
#     nm_modified_by = fields.Text('Name Modified By')
#     nm_is_approved = fields.Boolean('Name Approved')
#     email = fields.Text(string="Email", help="Email of the contact")
#     new_email = fields.Text(string="New Email")
#     email_modified_by = fields.Text('Email Modified By')
#     email_is_approved = fields.Boolean('Email Approved')
#     phone = fields.Text(string="Phone", help="Phone number of the contact")
#     new_phone = fields.Text(string="New Phone")
#     ph_modified_by = fields.Text('Phone Modified By')
#     ph_is_approved = fields.Boolean('Phone Approved')
#     is_to_be_notified = fields.Boolean(string="Is To Be Notified",
#                                        help="Used to decide whether the party will be notified of the arrival of the cargo.")
#     new_is_to_be_notified = fields.Boolean(string="Is To Be Notified - New")
#     itbn_modified_by = fields.Text('Is To Be Notified Modified By')
#     itbn_is_approved = fields.Boolean('Is To Be Notified Approved')
#     document_parties_array_created_by = fields.Text('Created By')
#     # si_document_parties_line_id = fields.Many2one('si.template', string="Document Parties Line")
    si_template_document_parties_line_id = fields.Many2one('si.templates', string="SI Document Parties Line")
#     update_si_document = fields.Boolean('Update Shipping Instruction')
#     si_name = fields.Text('Shipping ID')
#
#     def button_approve(self):
#         if self.dp_is_approved:
#             self.document_parties_row_id = self.new_document_parties_row_id
#         else:
#             self.document_parties_row_id = self.document_parties_row_id
#
#         if self.pn_is_approved:
#             self.party_name_id = self.new_party_name_id
#         else:
#             self.party_name_id = self.party_name_id
#
#         if self.tax1_is_approved:
#             self.tax_reference_1 = self.new_tax_reference_1
#         else:
#             self.tax_reference_1 = self.tax_reference_1
#
#         if self.pk_is_approved:
#             self.public_key = self.new_public_key
#         else:
#             self.public_key = self.public_key
#
#         if self.strt_is_approved:
#             self.street = self.new_street
#         else:
#             self.street = self.street
#
#         if self.stno_is_approved:
#             self.street_number = self.new_street_number
#         else:
#             self.street_number = self.street_number
#
#         if self.flr_is_approved:
#             self.floor = self.new_floor
#         else:
#             self.floor = self.floor
#
#         if self.pc_is_approved:
#             self.post_code = self.new_post_code
#         else:
#             self.post_code = self.post_code
#
#         if self.cty_is_approved:
#             self.city = self.new_city
#         else:
#             self.city = self.city
#
#         if self.str_is_approved:
#             self.state_region = self.new_state_region
#         else:
#             self.state_region = self.state_region
#
#         if self.cntry_is_approved:
#             self.country = self.new_country
#         else:
#             self.country = self.country
#
#         if self.tax2_is_approved:
#             self.tax_reference_2 = self.new_tax_reference_2
#         else:
#             self.tax_reference_2 = self.tax_reference_2
#
#         if self.nmfta_is_approved:
#             self.nmfta_code = self.new_nmfta_code
#         else:
#             self.nmfta_code = self.nmfta_code
#
#         if self.pf_is_approved:
#             self.party_function = self.new_party_function
#         else:
#             self.party_function = self.party_function
#
#         if self.al_is_approved:
#             self.address_line = self.new_address_line
#         else:
#             self.address_line = self.address_line
#
#         if self.nm_is_approved:
#             self.name = self.new_name
#         else:
#             self.name = self.name
#
#         if self.email_is_approved:
#             self.email = self.new_email
#         else:
#             self.email = self.email
#
#         if self.ph_is_approved:
#             self.phone = self.new_phone
#         else:
#             self.phone = self.phone
#
#         if self.itbn_is_approved:
#             self.is_to_be_notified = self.new_is_to_be_notified
#         else:
#             self.is_to_be_notified = self.is_to_be_notified
#         return True
#
#     def button_open_update_document_parties(self):
#         return {
#             'type': 'ir.actions.act_window',
#             'res_model': 'document.parties',
#             'view_mode': 'form',
#             'views': [(self.env.ref('freightbox.update_dp_template_form_view_wiz').id, "form")],
#             'res_id': self.id,
#             'target': 'new',
#         }
#

class ShipmentLocation(models.Model):
    _inherit = 'shipment.location'
#     _description = "Shipment Location"
#
#     @api.constrains('location_type')
#     def _check_location_type(self):
#         for line in self:
#             if len(line.location_type) > 100:
#                 raise ValidationError('Location Type in Shipment Location(No. of characters must not exceed 100)')
#
#     @api.constrains('location_name')
#     def _check_location_name(self):
#         for line in self:
#             if line.location_name and len(line.location_name) > 100:
#                 raise ValidationError('Location name in Shipment Location (No. of characters must not exceed 100)')
#
#     @api.constrains('latitude')
#     def _check_latitude(self):
#         for line in self:
#             if line.latitude and len(line.latitude) > 10:
#                 raise ValidationError('Latitude in Shipment Location (No. of characters must not exceed 10)')
#
#     @api.constrains('longitude')
#     def _check_longitude(self):
#         for line in self:
#             if line.longitude and len(line.longitude) > 11:
#                 raise ValidationError('Longitude in Shipment Location (No. of characters must not exceed 11)')
#
#     @api.constrains('un_location_code')
#     def _check_un_location_code(self):
#         for line in self:
#             if line.un_location_code and len(line.un_location_code) > 5:
#                 raise ValidationError('UN Location Code in Shipment Location (No. of characters must not exceed 5)')
#
#     @api.constrains('street_name')
#     def _check_street_name(self):
#         for line in self:
#             if line.street_name and len(line.street_name) > 100:
#                 raise ValidationError('Street Name in Shipment Location (No. of characters must not exceed 100)')
#
#     @api.constrains('street_number')
#     def _check_street_number(self):
#         for line in self:
#             if line.street_number and len(line.street_number) > 50:
#                 raise ValidationError('Street Number in Shipment Location (No. of characters must not exceed 50)')
#
#     @api.constrains('floor')
#     def _check_floor(self):
#         for line in self:
#             if line.floor and len(line.floor) > 50:
#                 raise ValidationError('Floor in Shipment Location (No. of characters must not exceed 50)')
#
#     @api.constrains('post_code')
#     def _check_post_code(self):
#         for line in self:
#             if line.post_code and len(line.post_code) > 10:
#                 raise ValidationError('PostCode in Shipment Location (No. of characters must not exceed 10)')
#
#     @api.constrains('city_name')
#     def _check_city_name(self):
#         for line in self:
#             if line.state_region and len(line.state_region) > 65:
#                 raise ValidationError('City Name in Shipment Location (No. of characters must not exceed 65)')
#
#     @api.constrains('state_region')
#     def _check_state_region(self):
#         for line in self:
#             if line.state_region and len(line.state_region) > 65:
#                 raise ValidationError('State Region in Shipment Location (No. of characters must not exceed 65)')
#
#     @api.constrains('country')
#     def _check_country(self):
#         for line in self:
#             if line.country and len(line.country) > 75:
#                 raise ValidationError('Country in Shipment Location (No. of characters must not exceed 75)')
#
#     shipment_location_line_id = fields.Many2one('shipping.instruction', string="Shipment Location Line")
#     sl_line_id_is_to_update = fields.Boolean(string='Shipment Location Update In Progress',
#                                              related='shipment_location_line_id.update_si')
#     bol_sl_line_id = fields.Many2one('bill.of.lading', string="BOL Shipment Location Line")
#     shipment_location_row_id = fields.Text('Shipment location row ID')
#     new_shipment_location_row_id = fields.Text('New Shipment location row ID')
#     sl_modified_by = fields.Text('Shipment Location Modified By')
#     sl_is_approved = fields.Boolean('Shipment Location Approved')
#     location_type = fields.Many2one('location.type', string="Location Type",
#                                     help="DCSA-defined code for shipment locations.")
#     loc_type_val = fields.Boolean('Location Type Value')
#     new_location_type = fields.Many2one('location.type', string="New Location Type")
#     lt_modified_by = fields.Text('Location Type Modified By')
#     lt_is_approved = fields.Boolean('Location Type Approved')
#     location_name = fields.Text(string="Location Name", help="Name of the location.")
#     new_location_name = fields.Text(string="New Location Name")
#     ln_modified_by = fields.Text('Location Name Modified By')
#     ln_is_approved = fields.Boolean('Location Name Approved')
#     latitude = fields.Text(string="Latitude",
#                            help="Geographic coordinate that specifies the north–south position of a point on the Earth's surface.")
#     new_latitude = fields.Text(string="New Latitude")
#     lat_modified_by = fields.Text('Latitude Modified By')
#     lat_is_approved = fields.Boolean('Latitude Approved')
#     longitude = fields.Text(string="Longitude",
#                             help="Geographic coordinate that specifies the east–west position of a point on the Earth's surface.")
#     new_longitude = fields.Text(string="New Longitude")
#     lg_modified_by = fields.Text('Longitude Modified By')
#     lg_is_approved = fields.Boolean('Longitude Approved')
#     un_location_code = fields.Text(string="UN Location Code",
#                                    help="The UN Location code specifying where the place is located.")
#     new_un_location_code = fields.Text(string="New UN Location Code")
#     unlc_modified_by = fields.Text('UN Location Code Modified By')
#     unlc_is_approved = fields.Boolean('UN Location Code Approved')
#     street_name = fields.Text(string="Street Name", help="The name of the street of the party’s address")
#     new_street_name = fields.Text(string="New Street Name")
#     st_nm_modified_by = fields.Text('Street Name Modified By')
#     st_nm_is_approved = fields.Boolean('Street Name Approved')
#     street_number = fields.Text(string="Street Number", help="The number of the street of the party’s address")
#     new_street_number = fields.Text(string="New Street Number")
#     st_no_modified_by = fields.Text('Street Number Modified By')
#     st_no_is_approved = fields.Boolean('Street Number Approved')
#     floor = fields.Text(string="Floor", help="The floor of the party’s street number")
#     new_floor = fields.Text(string="New Floor")
#     flo_modified_by = fields.Text('Floor Modified By')
#     flo_is_approved = fields.Boolean('Floor Approved')
#     post_code = fields.Text(string="Post Code", help="The post code of the party’s address")
#     new_post_code = fields.Text(string="New Post Code")
#     pc_modified_by = fields.Text('Post Code Modified By')
#     pc_is_approved = fields.Boolean('Post Code Approved')
#     city_name = fields.Text(string="City Name", help="The city name of the party’s address")
#     new_city_name = fields.Text(string="New City Name")
#     ctnm_modified_by = fields.Text('City Name Modified By')
#     ctnm_is_approved = fields.Boolean('City Name Approved')
#     state_region = fields.Text(string="State Region", help="The state/region of the party’s address")
#     new_state_region = fields.Text(string="New State Region")
#     strg_modified_by = fields.Text('State Region Modified By')
#     strg_is_approved = fields.Boolean('State Region Approved')
#     country = fields.Text(string="Country", help="The country of the party’s address")
#     new_country = fields.Text(string="New Country")
#     cntry_modified_by = fields.Text('Country Modified By')
#     cntry_is_approved = fields.Boolean('Country Approved')
#     displayed_name = fields.Text(string="Displayed Name",
#                                  help="The location to be displayed on the transport document.")
#     new_displayed_name = fields.Text(string="New Displayed Name")
#     dn_modified_by = fields.Text('Displayed Name Modified By')
#     dn_is_approved = fields.Boolean('Displayed Name Approved')
#     shipment_location_array_created_by = fields.Text('Created By')
    si_template_shipment_location_line_id = fields.Many2one('si.templates', string="SI Shipment Location Line")
#     update_si_shipment = fields.Boolean('Update Shipping Instruction')
#     si_name = fields.Text('Shipping ID')
#
#     @api.onchange('location_type')
#     def onchange_location_type(self):
#         if self.location_type:
#             if self.location_type.name == "POD":
#                 self.loc_type_val = True
#             elif self.location_type.name == "POL":
#                 self.loc_type_val = True
#             else:
#                 self.loc_type_val = False
#
#     def button_approve(self):
#         if self.sl_is_approved:
#             self.shipment_location_row_id = self.new_shipment_location_row_id
#         else:
#             self.shipment_location_row_id = self.shipment_location_row_id
#
#         if self.lt_is_approved:
#             self.location_type = self.new_location_type
#         else:
#             self.location_type = self.location_type
#
#         if self.ln_is_approved:
#             self.location_name = self.new_location_name
#         else:
#             self.location_name = self.location_name
#
#         if self.lat_is_approved:
#             self.latitude = self.new_latitude
#         else:
#             self.latitude = self.latitude
#
#         if self.lg_is_approved:
#             self.longitude = self.new_longitude
#         else:
#             self.longitude = self.longitude
#
#         if self.unlc_is_approved:
#             self.un_location_code = self.new_un_location_code
#         else:
#             self.un_location_code = self.un_location_code
#
#         if self.st_nm_is_approved:
#             self.street_name = self.new_street_name
#         else:
#             self.street_name = self.street_name
#
#         if self.st_no_is_approved:
#             self.street_number = self.new_street_number
#         else:
#             self.street_number = self.street_number
#
#         if self.flo_is_approved:
#             self.floor = self.new_floor
#         else:
#             self.floor = self.floor
#
#         if self.pc_is_approved:
#             self.post_code = self.new_post_code
#         else:
#             self.post_code = self.post_code
#
#         if self.ctnm_is_approved:
#             self.city_name = self.new_city_name
#         else:
#             self.city_name = self.city_name
#
#         if self.strg_is_approved:
#             self.state_region = self.new_state_region
#         else:
#             self.state_region = self.state_region
#
#         if self.cntry_is_approved:
#             self.country = self.new_country
#         else:
#             self.country = self.country
#
#         if self.dn_is_approved:
#             self.displayed_name = self.new_displayed_name
#         else:
#             self.displayed_name = self.displayed_name
#
#         return True
#
#     def button_open_update_shipment_location(self):
#         return {
#             'type': 'ir.actions.act_window',
#             'res_model': 'shipment.location',
#             'view_mode': 'form',
#             'views': [(self.env.ref('freightbox.update_sl_template_form_view_wiz').id, "form")],
#             'res_id': self.id,
#             'target': 'new',
#         }
#
#
class ShippingReferences(models.Model):
    _inherit = 'shipping.references'
#     _description = "Shipping References"
#
#     @api.constrains('reference_type')
#     def _check_reference_type(self):
#         for line in self:
#             if len(line.reference_type) > 3:
#                 raise ValidationError('Reference Type in References (No. of characters must not exceed 3)')
#
#     @api.constrains('reference_value')
#     def _check_reference_value(self):
#         for line in self:
#             if len(line.reference_value) > 100:
#                 raise ValidationError('Reference Value in References (No. of characters must not exceed 100)')
#
#     references_line_id = fields.Many2one('shipping.instruction', string="Reference Location Line")
#     sr_line_id_is_to_update = fields.Boolean(string='Shipping References Update In Progress',
#                                              related='references_line_id.update_si')
#     bol_ref_line_id = fields.Many2one('bill.of.lading', string="BOL Reference Location Line")
#     shipping_references_row_id = fields.Text('Shipping references row ID')
#     new_shipping_references_row_id = fields.Text('New shipping references row ID')
#     sr_modified_by = fields.Text('Shipping References Modified By')
#     sr_is_approved = fields.Boolean('Shipping References Approved')
#     reference_type = fields.Text(string="Reference Type",
#                                  help="The reference type codes defined by DCSA, which can be one of the following values: FF, SI, PO, CR, AAO.")
#     new_reference_type = fields.Text(string="New Reference Type")
#     rt_modified_by = fields.Text('Reference Type Modified By')
#     rt_is_approved = fields.Boolean('Reference Type Approved')
#     reference_value = fields.Text(string="Reference Value", help="The actual value of the reference.")
#     new_reference_value = fields.Text(string="New Reference Value")
#     rv_modified_by = fields.Text('Reference Value Modified By')
#     rv_is_approved = fields.Boolean('Reference Value Approved')
#     references_array_created_by = fields.Text('Created By')
    si_template_references_line_id = fields.Many2one('si.templates', string="SI Reference Location Line")
#     update_si_shipping = fields.Boolean('Update Shipping Instruction')
#     si_name = fields.Text('Shipping ID')
#
#     def button_approve(self):
#         if self.sr_is_approved:
#             self.shipping_references_row_id = self.new_shipping_references_row_id
#         else:
#             self.shipping_references_row_id = self.shipping_references_row_id
#
#         if self.rt_is_approved:
#             self.reference_type = self.new_reference_type
#         else:
#             self.reference_type = self.reference_type
#
#         if self.rv_is_approved:
#             self.reference_value = self.new_reference_value
#         else:
#             self.reference_value = self.reference_value
#
#         return True
#
#     def button_open_update_shipping_references(self):
#         return {
#             'type': 'ir.actions.act_window',
#             'res_model': 'shipping.references',
#             'view_mode': 'form',
#             'views': [(self.env.ref('freightbox.update_sr_template_form_view_wiz').id, "form")],
#             'res_id': self.id,
#             'target': 'new',
#         }


# class HsCode(models.Model):
#     _name = 'hs.code'
#     _inherit = ['mail.thread', 'mail.activity.mixin']
#     _description = "HS Code"

#     hs_code_classification = fields.Char("Classification", tracking=True)
#     code = fields.Char("Code", tracking=True)
#     description = fields.Char("Description", tracking=True)


# class LocationType(models.Model):
#     _name = 'location.type'
#     _inherit = ['mail.thread', 'mail.activity.mixin']
#     _description = "Location Type"
#
#     name = fields.Char("Name", required=True, tracking=True)
#
