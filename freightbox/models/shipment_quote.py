from odoo import models, fields, _, api, exceptions
from odoo.exceptions import UserError
from lxml import etree
from datetime import timedelta, datetime,date


class ShipmentQuote(models.Model):
    _inherit = 'shipment.quote'
    # _inherit = ['mail.thread', 'mail.activity.mixin']
    # _description = "Shipment Quote"
    # _rec_name = 'booking_id'

    # name = fields.Char("Name")
    # cargo_name = fields.Char("Cargo Description")
    # quantity = fields.Float("Quantity")
    # shipment_terms = fields.Selection([
    #     ('lcl', 'LCL'),
    #     ('fcl', 'FCL'),
    #     ('both', 'LCL and FCL'),
    #     ('bb', 'BB')], "Shipment Terms")
    # weight = fields.Float("Weight")
    # volume = fields.Float("Volume")
    # move_type = fields.Many2one('move.type', "Move Type")
    # incoterm_id = fields.Many2one('account.incoterms', "Incoterms")
    # place_of_origin = fields.Char("Point of Origin")
    # final_port_of_destination = fields.Char("Point of Destination")
    # point_of_stuffing = fields.Many2one('port', string='Point of Stuffing', tracking=True)
    # point_of_destuffing = fields.Many2one('port', string='Point of Destuffing', tracking=True)
    # no_of_expected_container = fields.Float("No. of Expected Container")
    rate_file = fields.Binary('Upload Rate File')
    rate_file_fname = fields.Char('Rate File Name', size=64)
    # state = fields.Selection([
    #     ('draft', 'Draft'),
    #     ('accepted', 'Accepted'),
    #     ('rejected', 'Rejected'),
    #     ('cancelled', 'Cancelled'),
    #     ('under_correction', 'Under Correction'),
    #     ('correction_done', 'Correction Done'),
    # ], string='Status', index=True, readonly=True, copy=False, default='draft', tracking=True, )
    # charges_line = fields.One2many('charges.line', 'shipment_quote_id', string='Charges')
    # volume_uom = fields.Many2one('uom.uom', "Volume Unit")
    # weight_uom = fields.Many2one('uom.uom', "Weight Unit")
    #
    # po_id = fields.Many2one('purchase.order', string='Purchase Order', ondelete='cascade')
    # valid_from = fields.Date("Valid From")
    # valid_to = fields.Date("Valid To")
    # booking_id = fields.Char(string='Booking NO.')
    # inquiry_id = fields.Many2one('crm.lead', "Inquiry")
    # partner_id = fields.Many2one('res.partner', "Shipping line")
    # expected_date_of_shipment = fields.Date("Expected Date of Shipment")
    # remarks = fields.Char("Remarks")
    # company_id = fields.Many2one('res.company', 'Company', required=True,
    #                              default=lambda self: self.env.company.id)
    # currency_id = fields.Many2one('res.currency', 'Currency', readonly=True,
    #                               default=lambda self: self.env.company.currency_id)
    # job_id = fields.Many2one('job', "Job")
    # total_freight_charge = fields.Float(compute='_get_total', string="Total Freight Charge", digits='Freight')
    # total_destination_charge = fields.Float(compute='_get_total', string="Total Destination Charge", digits='Freight')
    # total_origin_charge = fields.Float(compute='_get_total', string="Total Origin Charge", digits='Freight')
    # total_charge = fields.Float(compute='_get_total', string="Total Charge", digits='Freight')
    # invoice_id = fields.Many2one('account.move', string='Customer Invoice')
    # vendor_bill_id = fields.Many2one('account.move', string='Vendor Bill')
    reject_reason = fields.Text('Reject Reason', tracking=True)
    # comment = fields.Text("Comment")
    # reject_bool = fields.Boolean(string='Reject Bool')
    correct_reason = fields.Text('Correct Reason', tracking=True)
    correct_reason_bool = fields.Boolean(string='Correct Bool')
    # container_type = fields.Many2one('container.iso.code', "Container Type")
    markup = fields.Float(string="Markup (%)", tracking=True)
    # total_prepaid_charges = fields.Float(compute='_get_final_amount_per_unit',
    #                                      string="Prepaid Sale Price", digits='Freight')
    # total_collect_charges = fields.Float(compute='_get_final_amount_per_unit',
    #                                      string="Collect Sale Price", digits='Freight')
    # sq_reject_reason = fields.One2many('reject.reason', 'sq_id', string='Reason For Rejection')
    #
    # email_sent_bool = fields.Boolean(string='Email Sent Bool')
    # active = fields.Boolean(string='Active', default=True)
    # booking_user_id = fields.Many2one('res.users', string="Shipper/FF")
    same_as_cp = fields.Boolean(string='Both Cost and Sale Price are same?')
    # allow_shipper_to_approve = fields.Boolean(string='Allow Shipper to View')
    # vessel_name = fields.Char("Vessel Name", tracking=True)
    delivery_type_id = fields.Many2one('service.type', string="Delivery Type", tracking=True)
    # cargo_plus_ids = fields.Many2many("cargo.plus", "cargo_plus_sq_rel", "cargo_plus_id", "sq_id",
    #                                   string="Cargo Plus")

    @api.model
    def action_open_shipment_quote_tree_view(self):
        view_id = self.env.ref('freightbox.shipment_quote_tree_view').id
        view_form_id = self.env.ref('freightbox.shipment_quote_form_view').id
        action = {
            'name': _('Shipment Quote'),
            'type': 'ir.actions.act_window',
            'res_model': 'shipment.quote',
            'view_type': 'list',
            'views': [(view_id, 'list'), (view_form_id, 'form')],
            'view_mode': 'list,form',
        }
        return action

    @api.model
    def sq_dashboard(self):
        """ This function returns the values to populate the custom dashboard in
            the RC views.
        """
        # self.check_access_rights('read')

        result = {
            'draft': 0,
            'accepted': 0,
            'rejected': 0,
            'cancelled': 0,
        }

        result['draft'] = self.search_count([('state', '=', 'draft')])
        result['accepted'] = self.search_count([('state', '=', 'accepted')])
        result['rejected'] = self.search_count([('state', '=', 'rejected')])
        result['cancelled'] = self.search_count([('state', '=', 'cancelled')])

        return result

    def update_sale_price(self):
        if self.same_as_cp:
            self.markup = "0"
        elif self.markup < 0:
            raise UserError(_('Please enter a valid Markup value'))
        elif not self.markup:
            raise UserError(_('Please set the Markup (%) to update the Sale Price'))
        for line in self.charges_line:
            sale_price = 0.00
            sale_price = line.unit_price + (self.markup * line.unit_price) / 100
            line.new_unit_price = sale_price
            line._onchange_charges()

    def preview_sq(self):
        self.ensure_one()
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': base_url+'/accept_or_reject_sq/%s?' % self.id,
        }

    def button_allow_shipper_to_approve(self):
        res = super(ShipmentQuote, self).button_allow_shipper_to_approve()
        se_rec = self.env['track.shipment.event'].create({
            'shipment_event': 'Shipment',
            'event_created': date.today(),
            'event_datetime': date.today(),
            'event_classifier_code': 'ACT',
            'shipment_event_type_code': 'RECE',
            'reason':'Shipment Quote Accept/Reject',
            'booking_id':self.inquiry_id.id
        })

    # def button_accept(self):
    #     so_rate_vals = []
    #     sale_order_obj = self.env['sale.order']
    #     ProductTemplate = self.env['product.template']
    #     for line in self.charges_line:
    #         if line.unit_price > line.new_unit_price:
    #             raise UserError(
    #                 _('Sale Price cannot be less than cost price for %s') % line.charges_id.name)
    #     if self.container_type:
    #         container_id = self.container_type.id
    #         container_name = self.container_type.code
    #         product_found = ProductTemplate.search(
    #             [('iso_code_id', '=', container_id), ('name', '=', container_name)], limit=1)
    #         if product_found:
    #             product_template_id = product_found
    #         else:
    #             product_template_id = ProductTemplate.create({
    #                 'name': container_name,
    #                 'iso_code_id': container_id,
    #                 'is_freight_container': True,
    #                 'type': 'service',
    #                 'invoice_policy': 'order',
    #                 'purchase_method': 'receive',
    #                 'booking_id': self.booking_id,
    #                 'purchase_ok': True,
    #             })
    #     Product = self.env['product.product'].search([('product_tmpl_id', '=', product_template_id.id)])
    #
    #     purchase_order_id = self.po_id
    #     purchase_order_id.order_line = False
    #
    #     se_rec = self.env['track.shipment.event'].create({
    #         'shipment_event': 'Shipment',
    #         'event_created': date.today(),
    #         'event_datetime': date.today(),
    #         'event_classifier_code': 'ACT',
    #         'shipment_event_type_code': 'RECE',
    #         'reason':'Shipment Quote Accept',
    #         'booking_id':self.inquiry_id.id
    #     })
    #
    #     CrmLead = self.env['crm.lead']
    #     inquiry = CrmLead.search([('booking_id', '=', self.booking_id)])
    #     so_id = sale_order_obj.create({
    #         'cargo_name': self.cargo_name or '',
    #         'quantity': self.quantity,
    #         'shipment_terms': self.shipment_terms,
    #         'weight': self.weight,
    #         'weight_uom': self.weight_uom.id,
    #         'volume': self.volume,
    #         'volume_uom': self.volume_uom.id,
    #         'place_of_origin': self.place_of_origin,
    #         'final_port_of_destination': self.final_port_of_destination,
    #         'point_of_stuffing': self.point_of_stuffing.id if self.point_of_stuffing else False,
    #         'point_of_destuffing': self.point_of_destuffing.id if self.point_of_destuffing else False,
    #         'no_of_expected_container': self.no_of_expected_container,
    #         'container_type': self.container_type.id,
    #         'expected_date_of_shipment': self.expected_date_of_shipment,
    #         'remarks': self.remarks,
    #         'state': 'draft',
    #         'po_id': self.po_id.id,
    #         'booking_id': self.booking_id,
    #         'partner_id': self.partner_id.id,
    #         'incoterm_id': self.incoterm_id.id,
    #         'shipment_quote_id': self.id,
    #         'move_type': self.move_type.id,
    #         'valid_from': self.valid_from,
    #         'valid_to': self.valid_to,
    #         'total_freight_charge': self.total_freight_charge,
    #         'total_destination_charge': self.total_destination_charge,
    #         'total_origin_charge': self.total_origin_charge,
    #         'total_charge': self.total_charge,
    #         'so_inquiry_id': inquiry.id,
    #         'opportunity_id': inquiry.id,
    #         'is_freight_box_so': True,
    #         'booking_user_id': self.booking_user_id.id,
    #         'delivery_type_id':self.delivery_type_id.id,
    #         'cargo_plus_ids': [(6, 0, self.cargo_plus_ids.ids)]
    #     })
    #     if so_id:
    #         base_currency = self.env.company.currency_id
    #         from_today_rate = 0
    #         for line in purchase_order_id.charges_line:
    #             if purchase_order_id and line.prepaid:
    #                 price = line.unit_price
    #                 if purchase_order_id.currency_id != line.currency_id:
    #                     cost_price = line.currency_id._convert(
    #                         price, purchase_order_id.currency_id, self.env.company, fields.Date.today(), round=False)
    #                 else:
    #                     cost_price = line.unit_price
    #                 from_currency = line.currency_id
    #                 from_today_rate = from_currency._convert(
    #                     1, base_currency, self.env.company, fields.Date.today(), round=False)
    #                 today_rate = base_currency._convert(
    #                     from_today_rate, line.to_currency_id, self.env.company, fields.Date.today(), round=False)
    #                 exchange_currencies = line.currency_id.name + " to " + line.to_currency_id.name
    #                 purchase_order_id.order_line.create({
    #                         'product_id': Product.id,
    #                         'name': line.charges_id.name,
    #                         'product_qty': self.no_of_expected_container,
    #                         'price_unit': cost_price,
    #                         'order_id': purchase_order_id.id,
    #                         'taxes_id': line.taxes_id.ids,
    #                         'today_exchange_rate': today_rate,
    #                         'exchange_from_to_currency': exchange_currencies,
    #                         'is_charges': True,
    #                 })
    #             line._onchange_charges()
    #         for so_line in self.charges_line:
    #             so_rate_vals.append({
    #                 'charges_id': so_line.charges_id.id,
    #                 'container_type': so_line.container_type.id,
    #                 'charges_type': so_line.charges_type,
    #                 'units': so_line.units,
    #                 # 'unit_price': line.unit_price,
    #                 'new_unit_price': so_line.new_unit_price,
    #                 'taxes_id': so_line.taxes_id.ids,
    #                 'prepaid': so_line.prepaid,
    #                 'collect': so_line.collect,
    #                 'comment': so_line.comment,
    #                 'sale_order_id': so_id.id,
    #                 'is_loaded_for_rfq': True,
    #                 'currency_id': so_line.currency_id.id,
    #                 'to_currency_id': so_line.to_currency_id.id,
    #                 'charge_line_insert_update': 'copied',
    #             })
    #         so_id.charges_line.create(so_rate_vals)
    #         for so_line in so_id.charges_line:
    #             so_line._onchange_charges()
    #             if so_id and so_line.prepaid:
    #                 price = so_line.new_unit_price
    #                 if so_id.currency_id != so_line.currency_id:
    #                     sale_price = so_line.currency_id._convert(
    #                         price, so_id.currency_id, self.env.company, fields.Date.today(), round=False)
    #                 else:
    #                     sale_price = so_line.new_unit_price
    #                 from_currency = so_line.currency_id
    #                 from_today_rate = from_currency._convert(
    #                     1, base_currency, self.env.company, fields.Date.today(), round=False)
    #                 so_today_rate = base_currency._convert(
    #                     from_today_rate, so_line.to_currency_id, self.env.company, fields.Date.today(), round=False)
    #                 exchange_rate_val = so_line.currency_id.name + " to " + so_line.to_currency_id.name
    #                 so_id.order_line.create({
    #                     'product_id': Product.id,
    #                     'name': so_line.charges_id.name,
    #                     'product_uom_qty': self.no_of_expected_container,
    #                     'price_unit': sale_price,
    #                     'order_id': so_id.id,
    #                     'tax_id': so_line.taxes_id.ids,
    #                     'today_exchange_rate': so_today_rate,
    #                     'exchange_from_to_currency': exchange_rate_val,
    #                     'is_charges': True,
    #                 })
    #     self.write({'state': 'accepted', 'allow_shipper_to_approve': True})
    #     self.po_id.write({'po_inquiry_status': 'shipment_quote_accepted'})
    #     stage_id = self.env['crm.stage'].search([('is_won', '=', True)], limit=1)
    #
    #     if stage_id:
    #         self.po_id.rfq_id.booking_id.write({'stage_id': stage_id.id})
    #     view_id = self.env.ref('freightbox.view_order_form').id
    #     ctx = dict(
    #         default_is_freight_box_so=True,
    #     )
    #     return {
    #         'res_id': so_id.id,
    #         'name': 'Request For Quotation',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_model': 'sale.order',
    #         'view_id': view_id,
    #         'type': 'ir.actions.act_window',
    #         'ctx': ctx
    #     }

    def button_confirm_correction(self):
        so_id = self.env['sale.order'].search([('booking_id', '=', self.booking_id), ('state', '!=', 'cancel')])
        for line in self.charges_line:
            line.write({
                'units': self.no_of_expected_container,
                'container_type': self.container_type.id,
            })
            line._onchange_charges()
            if line.unit_price > line.new_unit_price:
                raise UserError(
                    _('Sale Price cannot be less than cost price for %s') % line.charges_id.name)
        if so_id:
            if so_id:
                so_id.update({
                    'charges_line': self.charges_line.ids,
                    'partner_id': self.partner_id.id,
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
                    'shipment_quote_id': self.id,
                    'booking_id': self.booking_id,
                    'incoterm_id': self.incoterm_id.id,
                    'move_type': self.move_type.id,
                    'valid_from': self.valid_from,
                    'valid_to': self.valid_to,
                })
                for line in so_id.charges_line:
                    line._onchange_charges()
        self.write({'state': 'correction_done'})

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

    def action_sq_send(self):
        """ Open a window to compose an email, with the edi invoice template
            message loaded by default
        """
        outmail_rec = self.env['ir.mail_server'].search([])
        # if not outmail_rec:
        #     raise UserError("Outgoing mail server not set !!!")
        
        self.ensure_one()
        template = self.env.ref('freightbox.mail_template_sq', False)
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

    def open_shipment_quote_tutorial_video_new_tab(self):
        url = self.env['ir.config_parameter'].sudo().get_param('freightbox.complete_tutorial_video_start_to_end',
                                                               '/freightbox/static/src/img/index_file_images/not_found.png')
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
        if view_id == self.env.ref("freightbox.shipment_quote_form_view").id:
            url = self.env['ir.config_parameter'].sudo().get_param('freightbox.shipment_quote_tutorial_video',
                                                                   '/freightbox/static/src/img/index_file_images/not_found.png')
            doc = etree.XML(result['arch'])
            for node in doc.xpath("//iframe[@id='shipment_quote_tutorial_video']"):
                node.set('src', url)
            result['arch'] = etree.tostring(doc)
        return result


# class RejectReason(models.Model):
#     _name = 'reject.reason'
#     _description = "Reject Reason"
#
#     sq_id = fields.Many2one('shipment.quote', string='SQ')
#     name = fields.Text("Reason For Rejection")
