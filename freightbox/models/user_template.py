from odoo import models, fields


class NewUserTemplates(models.Model):
    _name = 'user.templates'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "User Template"

    name = fields.Char("User Template Name")
    company_name = fields.Char("Company Name", tracking=True)
    user_name = fields.Char("User Name", tracking=True)
    address_line1 = fields.Char("Address line 1", tracking=True)
    address_line2 = fields.Char("Address line 2", tracking=True)
    postcode = fields.Char("PostCode", tracking=True)
    country = fields.Many2one('res.country', "Country", tracking=True)
    state_region = fields.Many2one('res.country.state', "State", tracking=True)
    email = fields.Char(string="Email", tracking=True)
    phone = fields.Char(string="Phone", tracking=True)
    cargo_name = fields.Char("Cargo Description", tracking=True)
    quantity = fields.Float("Quantity", tracking=True)
    shipment_terms = fields.Selection([
        ('lcl', 'LCL'),
        ('fcl', 'FCL'),
        ('both', 'LCL and FCL'),
        ('bb', 'BB')], "Shipment Terms")
    weight = fields.Float("Weight", tracking=True)
    volume = fields.Float("Volume", tracking=True)
    move_type = fields.Many2one('move.type', "Move Type", tracking=True)
    incoterm_id = fields.Many2one('account.incoterms', "Incoterms", tracking=True)
    place_of_origin = fields.Char("Point of Origin", tracking=True)
    final_port_of_destination = fields.Char("Point of Destination", tracking=True)
    no_of_expected_container = fields.Integer("No. of Expected Container", tracking=True)
    expected_date_of_shipment = fields.Date("Expected Date of Shipment", tracking=True)
    point_of_stuffing = fields.Many2one('port', string='Point of Stuffing', tracking=True)
    point_of_destuffing = fields.Many2one('port', string='Point of Destuffing', tracking=True)
    # container_type = fields.Many2one('container.iso.code', "Container Type", tracking=True)
    container_type = fields.Many2one('shipping.container', "Container Type", tracking=True)
    volume_uom = fields.Many2one('uom.uom', "Volume Unit", tracking=True)
    weight_uom = fields.Many2one('uom.uom', "Weight Unit", tracking=True)
    user_template_user_id = fields.Many2one('res.users', string="Created By")
    remarks = fields.Char("Remarks", tracking=True)
    is_data_template = fields.Boolean('Is Data Template?', default=False, tracking=True)
    user_template_customer_id = fields.Many2many('res.partner', string="Customer")


