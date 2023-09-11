from odoo import models, fields, _, api
from odoo.exceptions import UserError
fpod_vals = {'fpod_id': False, 'sequence': 0}


class RouteTemplates(models.Model):
    _name = 'route.templates'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Route Template"

    name = fields.Char(string='Name', required=True)
    route_template_line = fields.One2many('route.line', 'route_template_id', string='Route Line', copy=True, tracking=True)
    point_of_stuffing = fields.Many2one('port', string='Point of Stuffing', tracking=True)
    point_of_destuffing = fields.Many2one('port', string='Point of Destuffing', tracking=True)
    route_id = fields.Many2one('route', string='Route', tracking=True)
    is_created_from_route = fields.Boolean("Created from Route", tracking=True)
    transport_id = fields.Many2one('transport', string='Transport', tracking=True)
    is_created_from_transport = fields.Boolean("Created from Transport", tracking=True)
    is_data_template = fields.Boolean('Is Data Template?', default=False, tracking=True)
    container_route_line = fields.One2many('route.template.container.journey', 'route_temp_id',
                                           string='Container Journey',
                                           copy=True)

    def action_route(self):
        self.ensure_one()
        action = {
            'name': _('Route'),
            'type': 'ir.actions.act_window',
            'views': [(self.env.ref('freightbox.route_tree_view22').id, 'tree'), (False, 'form')],
            'res_model': 'route',
            'target': 'new',
            'context': {'current_id': self.id},
        }
        return action

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        default = dict(default or {}, name=_("%s ( Copy )", self.name))
        return super(RouteTemplates, self).copy(default=default)

    _sql_constraints = [
        ('name_route_uniq', 'unique (name)', "Route Template with same name already exists !"),
    ]


class RouteTemplateContainerJourney(models.Model):
    _name = 'route.template.container.journey'
    _description = "Route Template Container Journey"
    # _order = 'id asc'

    route_temp_id = fields.Many2one('route.templates', string='Route Template')
    end_point = fields.Char(string='End Point')
    # start_point = fields.Char(string='Start Point')
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


class Route(models.Model):
    _name = 'route'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Route"

    @api.depends('route_template_line.service_line')
    def _get_service_count(self):
        service_count = len(self.route_template_line.service_line)
        for line in self:
            line.service_count = service_count
            service_ids = line.route_template_line.service_line.ids
            line.service_ids = service_ids

    def action_view_services(self):
        services = self.mapped('service_ids')
        action = self.env["ir.actions.actions"]._for_xml_id("freightbox.action_service_menu")
        if len(services) >= 1:
            action['domain'] = [('id', 'in', services.ids)]
        context = {
            'default_service_ids': services.ids,
        }
        action['context'] = context
        return action

    port_of_origin_id = fields.Many2one('port', string='Port of Origin', tracking=True)
    fpod_id = fields.Many2one('port', string='FPOD', tracking=True)
    mode_id = fields.Many2one('mode', string='Mode', tracking=True)
    type = fields.Selection([
        ('presales', 'Pre Sales'),
        ('delivery', 'Delivery'),
    ], string='Type', default='delivery', tracking=True)
    estimated_departure_time = fields.Datetime("ETD", tracking=True)
    estimated_arrival_time = fields.Datetime("ETA", tracking=True)
    actual_departure_time = fields.Datetime("ATD", tracking=True)
    actual_arrival_time = fields.Datetime("ATA", tracking=True)
    delay_reason = fields.Char('Reason for Delay', tracking=True)
    route_template_ids = fields.Many2many('route.templates', 'route_templates_rel', 'route_templates_id', 'route_id',
                                            string='Route Templates', tracking=True)
    route_template_id = fields.Many2one('route.templates', string='Route Template', tracking=True)
    route_template_line = fields.One2many('route.line', 'route_id', string='Route', tracking=True)
    service_count = fields.Integer(string='Services Count', compute='_get_service_count', readonly=True, tracking=True)
    service_ids = fields.Many2many("service", string='Invoices', compute="_get_service_count", readonly=True, tracking=True)

    @api.onchange('route_template_id')
    def _onchange_route_template_id(self):
        self.route_template_line = False
        route_list = []
        vals_start ={}
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
            vals_start_tup = (0,0,vals_start)
            vals_end.update({'port_of_origin': route_list[-1][2]['fpod'],
                               'fpod': route_list[-1][2]['point_of_destuffing'],
                               })
            vals_end_tup = (0, 0, vals_end)
            route_list.insert(0, vals_start_tup)
            route_list.append(vals_end_tup)
        self.route_template_line = route_list

    def action_create_route_template(self):
        ctx = {}
        self.ensure_one()
        if not self.route_template_line:
            raise UserError(_("There is no Route to create Route template"))
        routetemplate = self.env['route.templates'].search([('route_id', '=', self.id), ('is_created_from_route', '=', True)],limit=1)
        ctx = dict(
            default_route_id=self.id,
            default_is_created_from_route=True,
            current_id=self.id,
        )
        if routetemplate:
            ctx = dict(
                default_route_id=self.id,
                default_name=routetemplate.name,
                default_is_created_from_route=True,
                current_id=self.id,
            )
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'route.templates.wiz',
            'view_mode': 'form',
            'views': [(self.env.ref('freightbox.route_template_form_wiz').id, "form")],
            'context': ctx,
            'target': 'new',
        }

class RouteLine(models.Model):
    _name = 'route.line'
    _description = "Route Line"
    _order = 'id asc'

    @api.onchange('fpod_id', 'port_of_origin_id')
    def _onchange_fpod_id(self):
        if self.fpod_id:
            fpod_vals.update({'fpod_id': self.fpod_id.id})
            fpod = self.fpod_id.unloc_code + ' ' + self.fpod_id.name
            self.fpod = fpod
        if self.port_of_origin_id:
            port_of_origin = self.port_of_origin_id.unloc_code + ' ' + self.port_of_origin_id.name
            self.port_of_origin = port_of_origin

    def _get_point_of_origin(self):
        print("fpod_vals", fpod_vals)
        port_of_origin_id = fpod_vals['fpod_id']
        return port_of_origin_id

    def _get_sequence(self):
        sequence = fpod_vals['sequence']
        sequence += 1
        fpod_vals['sequence'] = sequence
        return fpod_vals['sequence']

    route_template_id = fields.Many2one('route.templates', string='Route Template')
    transport_id = fields.Many2one('transport', string='Transport')
    route_id = fields.Many2one('route', string='Route')
    port_of_origin_id = fields.Many2one('port', string='Intermediate POL',default=_get_point_of_origin)
    port_of_origin = fields.Char(string='Intermediate Port Of Origin') # this field is not used
    fpod_id = fields.Many2one('port', string='Intermediate POD')
    fpod = fields.Char(string='Intermediate POD -') # this field is not used
    point_of_stuffing = fields.Many2one('port', related='route_template_id.point_of_stuffing',string='Point of Stuffing')
    point_of_destuffing = fields.Many2one('port',related='route_template_id.point_of_destuffing',string='Point of Destuffing')
    mode_id = fields.Many2one('mode', string='Mode')
    estimated_departure_time = fields.Datetime("ETD")
    estimated_arrival_time = fields.Datetime("ETA")
    planned_departure_time = fields.Datetime("PTD")
    planned_arrival_time = fields.Datetime("PTA")
    actual_departure_time = fields.Datetime("ATD")
    actual_arrival_time = fields.Datetime("ATA")
    delay_reason = fields.Char('Reason for Delay')
    change_remark = fields.Text('Change Remark')
    sequence = fields.Integer(string='Sequence', default=_get_sequence)
    service_line = fields.One2many('service', 'route_line_id', string='Service')

    transport_event_id = fields.Char(string='Transport Event ID')
    event_classifier_code = fields.Text("Event Classifier Code",)
    transport_event_type_code = fields.Text("Transport Event Type Code")

    # transport_id = fields.Char(string='Transport ID')
    transport_reference = fields.Text(string='Transport Reference')
    transport_name = fields.Text(string='Transport Name')
    mode_of_transport_code = fields.Text(string='Mode of Transport code')
    load_transport_call_id = fields.Text(string='Load Transport Call ID')
    discharge_transport_call_id = fields.Text(string='Discharge Transport Call ID')
    vessel_imo_number = fields.Text(string='Vessel IMO Number')

    transport_call_id = fields.Char("Transport Call ID")
    carrier_service_code = fields.Char("Carrier Service Code")
    carrier_voyage_number = fields.Text("Carrier Voyage Number")
    un_location_code = fields.Char("UN Location Code")
    facility_code = fields.Char("Facility Code")
    facility_code_list_provider = fields.Char("Facility Code List Provider")
    facility_type_code = fields.Text("Facility Type Code")
    other_facility = fields.Text("Other Facility")
    mode_of_transport = fields.Text("Mode of Transport")
    location = fields.Char("Location")
    vessel_imo_number = fields.Char("Vessel IMO Number")
    vessel_name = fields.Char("Vessel Name")
    vessel_flag = fields.Char("Vessel Flag")
    vessel_call_sign_number = fields.Char("Vessel Call sign Number")
    vessel_operator_carrier_code = fields.Char("Vessel Operator carrier code")
    vessel_operator_carrier_code_list_provider = fields.Char("Vessel Operator Carrier Code List Provider")

    document_reference_line = fields.One2many('document.reference', 'route_line_id', string='Document References')
    reference_line = fields.One2many('reference', 'route_line_id', string='References')


class DocumentReference(models.Model):
    _name = 'document.reference'
    _description = "Document References"

    route_line_id = fields.Many2one('route.line', string='Route Line')
    # route_line_transport_id = fields.Many2one('transport.event', string='Route Line')
    document_reference_type = fields.Char("Document Reference Type")
    document_reference_value = fields.Char("Document Reference Value")


class Reference(models.Model):
    _name = 'reference'
    _description = "References"

    route_line_id = fields.Many2one('route.line', string='Route Line')
    # route_line_transport_id = fields.Many2one('transport.event', string='Route Line')
    reference_type = fields.Char("Reference Type")
    reference_value = fields.Char("Reference Value")
