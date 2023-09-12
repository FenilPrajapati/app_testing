from odoo import models, fields


class PortsTemplates(models.Model):
    _name = 'ports.templates'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Ports Template"

    name = fields.Char(string='Name', required=True)
    ports_template_line = fields.One2many('ports.line', 'ports_template_id', string='Ports', tracking=True)


class Port(models.Model):
    _name = 'port'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Port"
    _rec_name = "unloc_code"

    unloc_code = fields.Char(string='UNLOC Code', tracking=True)
    name = fields.Char("Port Name")
    alias_name = fields.Char("Alias Name", tracking=True)
    country_id = fields.Many2one('res.country', string='Country', tracking=True)
    state_id = fields.Many2one('res.country.state', string='Subdivision', tracking=True)
    one = fields.Boolean("Ocean Port", tracking=True)
    two = fields.Boolean("Rail Terminal", tracking=True)
    three = fields.Boolean("Road Terminal", tracking=True)
    four = fields.Boolean("Airport", tracking=True)
    five = fields.Boolean("Postal Exchange", tracking=True)
    six = fields.Boolean("ICDs / CFS/ Multimodal", tracking=True)
    seven = fields.Boolean("Fixed", tracking=True)
    is_b = fields.Boolean("Border Crossing", tracking=True)
    status = fields.Char("Status", tracking=True)
    date = fields.Date("Date", tracking=True)
    iata = fields.Char("IATA", tracking=True)
    latitude = fields.Char("LAT", tracking=True)
    longitude = fields.Char("LONG", tracking=True)
    remarks = fields.Char("Remarks", tracking=True)
    facility_type_id = fields.Many2one('facility.type.code', string='Facility Type', tracking=True)
    facility_id = fields.Many2one('sub.port', string='Facility', tracking=True)
    is_location = fields.Boolean('Location', tracking=True, default=False)
    geo_codes_updated_from_api = fields.Boolean('Geo Locations Updated From API', default=False)

    def name_get(self):
        return [(record.id, "%s - %s" % (record.unloc_code, record.name)) for record in self]


class PortsLine(models.Model):
    _name = 'ports.line'
    _description = "Ports Line"

    ports_template_id = fields.Many2one('ports.templates', string='Template Line')
    port_id = fields.Many2one('port', string='Ports')


class SubPort(models.Model):
    _name = 'sub.port'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Sub Port"

    unloc_code = fields.Many2one('port', string='UNLOC Code', tracking=True)
    terminal_code = fields.Char("Terminal Code", tracking=True)
    facility_name = fields.Char("Facility Name", tracking=True)
    street = fields.Char(string="Street", tracking=True)
    city = fields.Char(string="City", tracking=True)
    post_code = fields.Char(string="Post Code")
    state_id = fields.Many2one('res.country.state', string='State/Region', tracking=True)
    country_id = fields.Many2one('res.country', string='Country', tracking=True)
    latitude = fields.Char("Latitude", tracking=True)
    longitude = fields.Char("Longitude", tracking=True)

    def name_get(self):
        return [(record.id, "%s - %s" % (record.terminal_code, record.facility_name)) for record in self]
