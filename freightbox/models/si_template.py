from odoo import models, fields, api, _


class NewSiTemplates(models.Model):
    _name = 'si.templates'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Shipping Instruction Template"

    name = fields.Char("SI Template Name")
    transport_document_type_code = fields.Selection([('bol','BOL'),('swb','SWB')],
                                          default='bol', string= "Transport Document Type Code", tracking=True)
    is_shipped_onboard_type = fields.Boolean("Is Shipped Onboard Type", tracking=True)
    number_of_originals = fields.Integer("Number of originals", tracking=True)
    number_of_copies = fields.Integer("Number of copies", tracking=True)
    pre_carriage_under_shippers_responsibility = fields.Text("Pre-carriage under shipper’s responsibility",
                                                             tracking=True)
    is_electronic = fields.Boolean("Is Electronic", default=True, required=True, tracking=True)
    carrier_booking_reference = fields.Text("Carrier Booking Reference", tracking=True)
    is_charges_displayed = fields.Boolean("Is Charges Displayed", default=True, tracking=True)
    location_name = fields.Text("Location Name", tracking=True)
    un_location_code = fields.Text("UN Location Code", tracking=True)
    city_name = fields.Text("City Name", tracking=True)
    state_region = fields.Text("State Region", tracking=True)
    country = fields.Text("Country", tracking=True)
    si_user_id = fields.Many2one('res.users', string="Created By", tracking=True)
    is_data_template = fields.Boolean('Is Data Template?', default=False, tracking=True)
    si_template_cargo_items_line = fields.One2many('cargo.line.items', 'si_template_cargo_line_id', string="Cargo",
                                                   copy=True)
    si_template_transport_equipment_line = fields.One2many('transport.equipment', 'si_template_transport_equipment_line_id',
                                                  string="Transport", copy=True)
    si_template_document_parties_line = fields.One2many('document.parties', 'si_template_document_parties_line_id',
                                                        copy=True)
    si_template_shipment_location_line = fields.One2many('shipment.location', 'si_template_shipment_location_line_id',
                                                  string="Shipment Location", copy=True)
    si_template_references_line = fields.One2many('shipping.references', 'si_template_references_line_id',
                                                  string="References", copy=True)

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        default = dict(default or {}, name=_("%s ( Copy )", self.name))
        return super(NewSiTemplates, self).copy(default=default)

