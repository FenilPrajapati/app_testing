from odoo import models, fields, _, api, exceptions
from odoo.exceptions import UserError
from lxml import etree
from datetime import timedelta, datetime,date


class ShipmentQuote(models.Model):
    _name = 'shipment.quote'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Shipment Quote"
    _rec_name = 'booking_id'

    @api.depends('charges_line')
    def _get_total(self):
        for rec in self:
            total_freight_charge = 0.0
            total_destination_charge = 0.0
            total_origin_charge = 0.0
            for line in rec.charges_line:
                if line.charges_type == 'freight':
                    total_freight_charge += line.sale_company_currency_tot
                if line.charges_type == 'destination':
                    total_destination_charge += line.sale_company_currency_tot
                if line.charges_type == 'origin':
                    total_origin_charge += line.sale_company_currency_tot
            rec.total_freight_charge = total_freight_charge
            rec.total_destination_charge = total_destination_charge
            rec.total_origin_charge = total_origin_charge
            rec.total_charge = rec.total_freight_charge + rec.total_destination_charge + rec.total_origin_charge

    name = fields.Char("Name")
    cargo_name = fields.Char("Cargo Description")
    quantity = fields.Float("Quantity")
    shipment_terms = fields.Selection([
        ('lcl', 'LCL'),
        ('fcl', 'FCL'),
        ('both', 'LCL and FCL'),
        ('bb', 'BB')], "Shipment Terms")
    weight = fields.Float("Weight")
    volume = fields.Float("Volume")
    move_type = fields.Many2one('move.type', "Move Type")
    incoterm_id = fields.Many2one('account.incoterms', "Incoterms")
    place_of_origin = fields.Char("Point of Origin")
    final_port_of_destination = fields.Char("Point of Destination")
    point_of_stuffing = fields.Many2one('port', string='Point of Stuffing', tracking=True)
    point_of_destuffing = fields.Many2one('port', string='Point of Destuffing', tracking=True)
    no_of_expected_container = fields.Float("No. of Expected Container")
    # rate_file = fields.Binary('Upload Rate File')
    # rate_file_fname = fields.Char('Rate File Name', size=64)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
        ('under_correction', 'Under Correction'),
        ('correction_done', 'Correction Done'),
    ], string='Status', index=True, readonly=True, copy=False, default='draft', tracking=True, )
    charges_line = fields.One2many('charges.line', 'shipment_quote_id', string='Charges')
    volume_uom = fields.Many2one('uom.uom', "Volume Unit")
    weight_uom = fields.Many2one('uom.uom', "Weight Unit")

    po_id = fields.Many2one('purchase.order', string='Purchase Order', ondelete='cascade')
    valid_from = fields.Date("Valid From")
    valid_to = fields.Date("Valid To")
    booking_id = fields.Char(string='Booking NO.')
    inquiry_id = fields.Many2one('crm.lead', "Inquiry")
    partner_id = fields.Many2one('res.partner', "Shipping line")
    expected_date_of_shipment = fields.Date("Expected Date of Shipment")
    remarks = fields.Char("Remarks")
    company_id = fields.Many2one('res.company', 'Company', required=True,
                                 default=lambda self: self.env.company.id)
    currency_id = fields.Many2one('res.currency', 'Currency', readonly=True,
                                  default=lambda self: self.env.company.currency_id)
    job_id = fields.Many2one('job', "Job")
    total_freight_charge = fields.Float(compute='_get_total', string="Total Freight Charge", digits='Freight')
    total_destination_charge = fields.Float(compute='_get_total', string="Total Destination Charge", digits='Freight')
    total_origin_charge = fields.Float(compute='_get_total', string="Total Origin Charge", digits='Freight')
    total_charge = fields.Float(compute='_get_total', string="Total Charge", digits='Freight')
    invoice_id = fields.Many2one('account.move', string='Customer Invoice')
    vendor_bill_id = fields.Many2one('account.move', string='Vendor Bill')
    reject_reason = fields.Text('Reject Reason', tracking=True)
    comment = fields.Text("Comment")
    reject_bool = fields.Boolean(string='Reject Bool')
    container_type = fields.Many2one('container.iso.code', "Container Type")
    total_prepaid_charges = fields.Float(compute='_get_final_amount_per_unit',
                                         string="Prepaid Sale Price", digits='Freight')
    total_collect_charges = fields.Float(compute='_get_final_amount_per_unit',
                                         string="Collect Sale Price", digits='Freight')
    sq_reject_reason = fields.One2many('reject.reason', 'sq_id', string='Reason For Rejection')

    email_sent_bool = fields.Boolean(string='Email Sent Bool')
    active = fields.Boolean(string='Active', default=True)
    booking_user_id = fields.Many2one('res.users', string="Shipper/FF")
    # same_as_cp = fields.Boolean(string='Both Cost and Sale Price are same?')
    allow_shipper_to_approve = fields.Boolean(string='Allow Shipper to View')
    vessel_name = fields.Char("Vessel Name", tracking=True)
    # delivery_type_id = fields.Many2one('service.type', string="Delivery Type", tracking=True)
    cargo_plus_ids = fields.Many2many("cargo.plus", "cargo_plus_sq_rel", "cargo_plus_id", "sq_id",
                                      string="Cargo Plus")


    @api.depends('charges_line')
    def _get_final_amount_per_unit(self):
        total_prepaid_charges = total_collect_charges = 0.0
        for rate in self.charges_line:
            if rate.prepaid:
                total_prepaid_charges_amt = rate.to_currency_id._convert(
                    rate.sale_final_amount, self.currency_id, self.env.company, fields.Date.today(), round=False)
                total_prepaid_charges += total_prepaid_charges_amt
            if rate.collect:
                total_collect_charges_amt = rate.to_currency_id._convert(
                    rate.sale_final_amount, self.currency_id, self.env.company, fields.Date.today(), round=False)
                total_collect_charges += total_collect_charges_amt
        self.total_prepaid_charges = total_prepaid_charges
        self.total_collect_charges = total_collect_charges

    def button_allow_shipper_to_approve(self):
        for line in self.charges_line:
            if line.unit_price > line.new_unit_price:
                raise UserError(
                    _('Sale Price cannot be less than cost price for %s') % line.charges_id.name)
        self.allow_shipper_to_approve = True

    def button_accept(self):
        so_rate_vals = []
        sale_order_obj = self.env['sale.order']
        ProductTemplate = self.env['product.template']
        for line in self.charges_line:
            if line.unit_price > line.new_unit_price:
                raise UserError(
                    _('Sale Price cannot be less than cost price for %s') % line.charges_id.name)
        if self.container_type:
            container_id = self.container_type.id
            container_name = self.container_type.code
            product_found = ProductTemplate.search(
                [('iso_code_id', '=', container_id), ('name', '=', container_name)], limit=1)
            if product_found:
                product_template_id = product_found
            else:
                product_template_id = ProductTemplate.create({
                    'name': container_name,
                    'iso_code_id': container_id,
                    'is_freight_container': True,
                    'type': 'service',
                    'invoice_policy': 'order',
                    'purchase_method': 'receive',
                    'booking_id': self.booking_id,
                    'purchase_ok': True,
                })
        Product = self.env['product.product'].search([('product_tmpl_id', '=', product_template_id.id)])

        purchase_order_id = self.po_id
        purchase_order_id.order_line = False
        
        # se_rec = self.env['track.shipment.event'].create({
        #     'shipment_event': 'Shipment',
        #     'event_created': date.today(),
        #     'event_datetime': date.today(),
        #     'event_classifier_code': 'ACT',
        #     'shipment_event_type_code': 'RECE',
        #     'reason':'Shipment Quote Accept',
        #     'booking_id':self.inquiry_id.id
        # })

        CrmLead = self.env['crm.lead']
        inquiry = CrmLead.search([('booking_id', '=', self.booking_id)])
        so_id = sale_order_obj.create({
            'cargo_name': self.cargo_name or '',
            'quantity': self.quantity,
            'shipment_terms': self.shipment_terms,
            'weight': self.weight,
            'weight_uom': self.weight_uom.id,
            'volume': self.volume,
            'volume_uom': self.volume_uom.id,
            'place_of_origin': self.place_of_origin,
            'final_port_of_destination': self.final_port_of_destination,
            'point_of_stuffing': self.point_of_stuffing.id if self.point_of_stuffing else False,
            'point_of_destuffing': self.point_of_destuffing.id if self.point_of_destuffing else False,
            'no_of_expected_container': self.no_of_expected_container,
            'container_type': self.container_type.id,
            'expected_date_of_shipment': self.expected_date_of_shipment,
            'remarks': self.remarks,
            'state': 'draft',
            'po_id': self.po_id.id,
            'booking_id': self.booking_id,
            'partner_id': self.partner_id.id,
            'incoterm_id': self.incoterm_id.id,
            'shipment_quote_id': self.id,
            'move_type': self.move_type.id,
            'valid_from': self.valid_from,
            'valid_to': self.valid_to,
            'total_freight_charge': self.total_freight_charge,
            'total_destination_charge': self.total_destination_charge,
            'total_origin_charge': self.total_origin_charge,
            'total_charge': self.total_charge,
            'so_inquiry_id': inquiry.id,
            'opportunity_id': inquiry.id,
            'is_freight_box_so': True,
            'booking_user_id': self.booking_user_id.id,
            'delivery_type_id':self.delivery_type_id.id,
            'cargo_plus_ids': [(6, 0, self.cargo_plus_ids.ids)]
        })
        if so_id:
            base_currency = self.env.company.currency_id
            from_today_rate = 0
            for line in purchase_order_id.charges_line:
                if purchase_order_id and line.prepaid:
                    price = line.unit_price
                    if purchase_order_id.currency_id != line.currency_id:
                        cost_price = line.currency_id._convert(
                            price, purchase_order_id.currency_id, self.env.company, fields.Date.today(), round=False)
                    else:
                        cost_price = line.unit_price
                    from_currency = line.currency_id
                    from_today_rate = from_currency._convert(
                        1, base_currency, self.env.company, fields.Date.today(), round=False)
                    today_rate = base_currency._convert(
                        from_today_rate, line.to_currency_id, self.env.company, fields.Date.today(), round=False)
                    exchange_currencies = line.currency_id.name + " to " + line.to_currency_id.name
                    purchase_order_id.order_line.create({
                            'product_id': Product.id,
                            'name': line.charges_id.name,
                            'product_qty': self.no_of_expected_container,
                            'price_unit': cost_price,
                            'order_id': purchase_order_id.id,
                            'taxes_id': line.taxes_id.ids,
                            'today_exchange_rate': today_rate,
                            'exchange_from_to_currency': exchange_currencies,
                            'is_charges': True,
                    })
                line._onchange_charges()
            for so_line in self.charges_line:
                so_rate_vals.append({
                    'charges_id': so_line.charges_id.id,
                    'container_type': so_line.container_type.id,
                    'charges_type': so_line.charges_type,
                    'units': so_line.units,
                    # 'unit_price': line.unit_price,
                    'new_unit_price': so_line.new_unit_price,
                    'taxes_id': so_line.taxes_id.ids,
                    'prepaid': so_line.prepaid,
                    'collect': so_line.collect,
                    'comment': so_line.comment,
                    'sale_order_id': so_id.id,
                    'is_loaded_for_rfq': True,
                    'currency_id': so_line.currency_id.id,
                    'to_currency_id': so_line.to_currency_id.id,
                    'charge_line_insert_update': 'copied',
                })
            so_id.charges_line.create(so_rate_vals)
            for so_line in so_id.charges_line:
                so_line._onchange_charges()
                if so_id and so_line.prepaid:
                    price = so_line.new_unit_price
                    if so_id.currency_id != so_line.currency_id:
                        sale_price = so_line.currency_id._convert(
                            price, so_id.currency_id, self.env.company, fields.Date.today(), round=False)
                    else:
                        sale_price = so_line.new_unit_price
                    from_currency = so_line.currency_id
                    from_today_rate = from_currency._convert(
                        1, base_currency, self.env.company, fields.Date.today(), round=False)
                    so_today_rate = base_currency._convert(
                        from_today_rate, so_line.to_currency_id, self.env.company, fields.Date.today(), round=False)
                    exchange_rate_val = so_line.currency_id.name + " to " + so_line.to_currency_id.name
                    so_id.order_line.create({
                        'product_id': Product.id,
                        'name': so_line.charges_id.name,
                        'product_uom_qty': self.no_of_expected_container,
                        'price_unit': sale_price,
                        'order_id': so_id.id,
                        'tax_id': so_line.taxes_id.ids,
                        'today_exchange_rate': so_today_rate,
                        'exchange_from_to_currency': exchange_rate_val,
                        'is_charges': True,
                    })
        self.write({'state': 'accepted', 'allow_shipper_to_approve': True})
        self.po_id.write({'po_inquiry_status': 'shipment_quote_accepted'})
        stage_id = self.env['crm.stage'].search([('is_won', '=', True)], limit=1)

        if stage_id:
            self.po_id.rfq_id.booking_id.write({'stage_id': stage_id.id})
        view_id = self.env.ref('freightbox_base.view_order_form').id
        ctx = dict(
            default_is_freight_box_so=True,
        )
        return {
            'res_id': so_id.id,
            'name': 'Request For Quotation',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'sale.order',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'ctx': ctx
        }

    def preview_sq(self):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': base_url+'/accept_or_reject_sq/%s?' % self.id,
        }

    def button_set_to_draft(self):
        self.write({'state': 'draft'})

    def button_cancel(self):
        if self.po_id:
            self.po_id.write({'state': 'cancel'})
            self.po_id.rfq_id.write({'state': 'cancelled'})
        self.write({'state': 'cancelled'})

    def action_get_so(self):
        view_id = self.env.ref('freightbox_base.sale_order_tree_inherit').id
        view_form_id = self.env.ref('freightbox_base.view_order_form').id
        itemIds = self.env['sale.order'].search([('shipment_quote_id', '=', self.id)])
        itemIds = itemIds.ids
        return {
            'name': ('Sale Order'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'sale.order',
            'views': [(view_id, 'list'), (view_form_id, 'form')],
            'domain': [('id', 'in', itemIds)],
            'target': 'current',
        }

    def action_sq_send(self):
        """ Open a window to compose an email, with the edi invoice template
            message loaded by default
        """
        outmail_rec = self.env['ir.mail_server'].search([])
        # if not outmail_rec:
        #     raise UserError("Outgoing mail server not set !!!")

        self.ensure_one()
        template = self.env.ref('shipmybox.mail_template_sq', False)
        compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        print("compose_form:", compose_form)
        ctx = dict(
            default_model='shipment.quote',
            default_res_id=self.id,
            default_use_template=bool(template),
            default_template_id=template.id,
            default_composition_mode='comment',
            force_email=True,
        )
        stage_id = self.env['crm.stage'].search([('name', 'ilike', 'Proposition')], limit=1)
        if stage_id:
            self.po_id.po_inquiry_id.write({'stage_id': stage_id.id})
        self.email_sent_bool = True
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

    def action_send_mail_to_shipper(self):
        print("TTTTTTTTTTTTTTTTTTTTTTTTTTTT")
        return True
        # template = self.env.ref('freightbox.mail_template_sq', False)
        # compose_form = self.env.ref('mail.email_compose_message_wizard_form', False)
        # ctx = dict(
        #     default_model='shipment.quote',
        #     default_res_id=self.id,
        #     default_use_template=bool(template),
        #     default_template_id=template.id,
        #     default_composition_mode='comment',
        #     force_email=True,
        # )
        # return {
        #     'name': _('Compose Email'),
        #     'type': 'ir.actions.act_window',
        #     'view_mode': 'form',
        #     'res_model': 'mail.compose.message',
        #     'views': [(compose_form.id, 'form')],
        #     'view_id': compose_form.id,
        #     'target': 'new',
        #     'context': ctx,
        # }

    @api.onchange('po_id')
    def _onchange_po_id(self):
        charge_list = []
        if not self.po_id:
            return
        if self.po_id:
            self.partner_id = self.po_id.partner_id.id or False
            self.cargo_name = self.po_id.cargo_name or ''
            self.quantity = self.po_id.quantity
            self.shipment_terms = self.po_id.shipment_terms
            self.weight = self.po_id.weight
            self.weight_uom = self.po_id.weight_uom
            self.volume = self.po_id.volume
            self.volume_uom = self.po_id.volume_uom
            self.incoterm_id = self.po_id.incoterm_id.id
            self.place_of_origin = self.po_id.place_of_origin
            self.final_port_of_destination = self.po_id.final_port_of_destination
            self.point_of_stuffing = self.po_id.point_of_stuffing.id if self.po_id and self.po_id.point_of_stuffing else False
            self.point_of_destuffing = self.po_id.point_of_destuffing.id if self.po_id and self.po_id.point_of_destuffing else False
            self.no_of_expected_container = self.po_id.no_of_expected_container
            self.container_type = self.po_id.container_type.id
            self.expected_date_of_shipment = self.po_id.expected_date_of_shipment
            self.remarks = self.po_id.remarks
            self.valid_from = self.po_id.valid_from
            self.valid_to = self.po_id.valid_to
            self.booking_id = self.po_id.rfq_id.booking_id.booking_id
            self.inquiry_id = self.po_id.rfq_id.booking_id
            self.move_type = self.po_id.rfq_id.booking_id.move_type.id

            for record in self.po_id.rfq_id.charges_line:
                charge_list.append((0, 0, {'charges_id': record.charges_id.id,
                                           'units': record.units,
                                           'unit_price': record.unit_price,
                                           }))
            self.charges_line = charge_list

    @api.returns('self', lambda value: value.id)
    def copy(self):
        raise exceptions.UserError(_('You cannot duplicate Shipment Quote.'))


class RejectReason(models.Model):
    _name = 'reject.reason'
    _description = "Reject Reason"

    sq_id = fields.Many2one('shipment.quote', string='SQ')
    name = fields.Text("Reason For Rejection")