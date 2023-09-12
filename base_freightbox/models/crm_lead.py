# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError


class CompanyInherit(models.Model):
    _inherit = 'res.company'

    sale_email = fields.Text("sales email")
    quote_email = fields.Text("Quotes email")


class CrmLead(models.Model):
    _inherit = 'crm.lead'
    _rec_name = 'booking_id'
    _order = 'booking_id desc'

    @api.depends('company_id')
    def _compute_mobile_website(self):
        for record in self:
            if not record.mobile:
                record.mobile = record.company_id.phone
            if not record.website:
                record.website = record.company_id.website

    @api.model
    def create(self, vals):
        if vals.get('booking_id', _('New')) == _('New'):
            vals['booking_id'] = self.env['ir.sequence'].next_by_code('crm.lead.seq') or _('New')
        result = super(CrmLead, self).create(vals)
        return result

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
    booking_id = fields.Char(string='Inquiry NO.', required=True, copy=False, readonly=True, index=True,
                             default=lambda self: _('New'), tracking=True)
    expected_date_of_shipment = fields.Date("Expected Date of Shipment", tracking=True)
    remarks = fields.Char("Remarks", tracking=True)
    job_id = fields.Many2one('job', "Job", copy=False)
    sq_id = fields.Many2one('shipment.quote', "Shipment Quote")
    point_of_stuffing = fields.Char(string='Point of Stuffing', tracking=True)
    point_of_destuffing = fields.Char(string='Point of Destuffing', tracking=True)
    container_type = fields.Many2one('shipping.container', "Container Type", tracking=True)
    volume_uom = fields.Many2one('uom.uom', "Volume Unit", tracking=True)
    weight_uom = fields.Many2one('uom.uom', "Weight Unit", tracking=True)
    rc_count = fields.Integer(string='RC Count', compute='_get_rc_count', readonly=True)
    booking_date = fields.Datetime("Booking Date", tracking=True, default=fields.Datetime.now())
    shipping_line_id = fields.Many2one('res.partner', string="Shipping Line", domain="[('supplier_rank', '>', 0)]")
    mobile = fields.Char('Mobile', compute=_compute_mobile_website, readonly=False, store=True)
    website = fields.Char('Website', index=True, help="Website of the contact", compute=_compute_mobile_website, readonly=False, store=True)
    is_freight_box_crm = fields.Boolean('Is FB?')
    state = fields.Selection([
        ('new', 'New'),
        ('qualified', 'Qualified'),
        ('proposition', 'Proposition'),
        ('won', 'Won'),
    ], string='Status', related='stage_id.state')
    booking_user_id = fields.Many2one('res.users', string="Shipper/FF")
    container_line_ids = fields.One2many("container.line", "inquiry_id", "Container Lines")
    # is_blacklist = fields.Boolean(related='partner_id.is_blacklist')
    agents_line = fields.One2many('res.partner', 'inquery_agent_type_id', string='Agents Lines')
    delivery_type_id = fields.Many2one('service.type', string="Delivery Type", tracking=True)
    cargo_plus_ids = fields.One2many("cargo.plus", "inquiry_id", "Cargo Plus Lines")

    @api.constrains('expected_date_of_shipment')
    def _check_expected_date_of_shipment(self):
        if self.is_freight_box_crm:
            today = fields.Date.today()
            for rec in self:
                if rec.expected_date_of_shipment < today:
                    raise ValidationError(_("EXPECTED DATE OF SHIPMENT cannot be a past date"))

    def action_create_rate_comparision(self):
        view_id = self.env.ref('base_freightbox.rfq_form_view').id
        port_obj = self.env['port']
        rc_obj = self.env['request.for.quote']
        cargo_plus_obj = self.env["cargo.plus"]
        container_type_obj = self.env["container.iso.code"]
        if self.job_id:
            raise UserError("RC cannot be created at this stage,as this booking is already confirmed")
        point_of_stuffing = port_obj.search(['|', '|',
                                                     ('unloc_code', '=', self.point_of_stuffing),
                                                     ('name', '=', self.point_of_stuffing),
                                                     ('alias_name', '=', self.point_of_stuffing)],
                                                    limit=1)

        if not point_of_stuffing:
            point_of_stuffing = port_obj.create({
                'name': self.point_of_stuffing
            })
        point_of_destuffing = port_obj.search(['|', '|',
                                                     ('unloc_code', '=', self.point_of_destuffing),
                                                     ('name', '=', self.point_of_destuffing),
                                                     ('alias_name', '=', self.point_of_destuffing)],
                                                    limit=1
                                                    )
        if not point_of_destuffing:
            point_of_destuffing = port_obj.create({
                'name': self.point_of_destuffing
            })
        ctx = dict(
            default_booking_id=self.id,
            default_shipping_name_id=self.shipping_line_id.id,
            default_booking_user_id=self.booking_user_id.id,
            default_point_of_stuffing=point_of_stuffing.id,
            default_point_of_destuffing= point_of_destuffing.id,
            # default_delivery_type_id= self.delivery_type_id.id,
            default_cargo_plus_ids= [(6, 0, self.cargo_plus_ids.ids)]
        )
        return {
            'name': 'Request for Quotation',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'request.for.quote',
            'view_id': view_id,

            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': ctx,
        }

    def _get_rc_count(self):
        rc_counts = self.env['request.for.quote'].search_count([('booking_id', '=', self.id)])
        self.rc_count = rc_counts

    def action_crm_send(self):
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
            default_model='crm.lead',
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

    def action_crm_send_sl(self):
        """ Open a window to compose an email, with the edi invoice template
            message loaded by default
        """
        outmail_rec = self.env['ir.mail_server'].search([])
        if not outmail_rec:
            raise UserError("Outgoing mail server not set !!!")
        self.ensure_one()
        template = self.env.ref('freightbox.mail_template_crm_sl', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        ctx = dict(
            default_model='crm.lead',
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

    def action_get_rc(self):
        itemIds = self.env['request.for.quote'].search([('booking_id', '=', self.id)])
        itemIds = itemIds.ids
        ctx = dict(
            default_booking_id=self.id,
        )
        return {
            'name': "Rate Comparison",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'request.for.quote',
            'view_id': False,
            'domain': [('id', 'in', itemIds)],
            'target': 'current',
            'context': ctx,
        }


class CargoPlus(models.Model):
    _name = "cargo.plus"
    _description = "Cargo Plus"
    _rec_name = "inquiry_id"

    inquiry_id = fields.Many2one("crm.lead", "Inquiry")
    no_of_expected_container = fields.Integer("No Of Expected Container", required=True)
    no_of_confirmed_container = fields.Integer("No Of Confirmed Container")
    container_type_id = fields.Many2one("shipping.container", "Container Type", required=True)
    cargo_description = fields.Char("Cargo Description")
    quantity = fields.Float("Quantity")
    weight = fields.Float("Weight")
    volume = fields.Float("Volume")
    weight_uom = fields.Many2one('uom.uom', "Weight Unit")
    volume_uom = fields.Many2one('uom.uom', "Volume Unit")
    move_type = fields.Many2one('move.type', "Move Type")
    incoterm_id = fields.Many2one('account.incoterms', "Incoterms")
    shipping_instruction_id = fields.Many2one("shipping.instruction", "SI", help="Related Shipping Instruction.")


class StageInherit(models.Model):
    _inherit = 'crm.stage'

    state = fields.Selection([
        ('new', 'New'),
        ('qualified', 'Qualified'),
        ('proposition', 'Proposition'),
        ('won', 'Won'),
    ], string='Status')


class ContainerLine(models.Model):
    _name = "container.line"
    _description = "Container Line"
    _rec_name = "inquiry_id"

    inquiry_id = fields.Many2one("crm.lead", "Inquiry")
    no_of_expected_container = fields.Integer("No Of Expected Container", required=True)
    container_type_id = fields.Many2one("shipping.container", "Container Type", required=True)

