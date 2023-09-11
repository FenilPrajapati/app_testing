# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError
from odoo.tools.misc import formatLang, get_lang
from lxml import etree
from datetime import timedelta, datetime,date

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False,submenu=False):
    #     print('-----------***************************------------ view_type ',view_type)
    #     res = super(PurchaseOrder,self).fields_view_get(view_id=view_id, view_type=view_type,
    #                                 toolbar=toolbar, submenu=submenu)
    #     print('----------------------- toolbar',toolbar)
    #     if toolbar:
    #         for action in res['toolbar'].get('action'):
    #             if action.get('xml_id'):
    #                 if action['xml_id'] == 'your xml of action' and self._context.get(
    #                         'default_type') == 'entry':
    #                     res['toolbar']['action'].remove(action)
    #     return res

    @api.depends('name', 'partner_ref', 'rfq_id')
    def name_get(self):
        result = []
        for po in self:
            name = po.name
            if po.partner_ref:
                name += ' (' + po.partner_ref + ')'
            if po.rfq_id and po.booking_id:
                name += '/' + po.booking_id
            if self.env.context.get('show_total_amount') and po.amount_total:
                name += ': ' + formatLang(self.env, po.amount_total, currency_obj=po.currency_id)
            result.append((po.id, name))
        return result

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
    # rfq_id = fields.Many2one('request.for.quote', string='Rate Comparision', ondelete='cascade')
    # po_inquiry_status = fields.Selection([
    #     ('shipment_quote_created', "Shipment Quote Created"),
    #     ('shipment_quote_accepted', "Shipment Quote Accepted"),
    #     ('under_correction', 'Under Correction'),
    #     ('correction_done', 'Correction Done')], "PO Status")
    # party_name_id = fields.Many2one('res.partner', string="Party Name")
    # tax_reference_1 = fields.Text(string="Tax Reference 1")
    # street = fields.Text(string="Street")
    # street_number = fields.Text(string="Street Number")
    # floor = fields.Text(string="Floor")
    # post_code = fields.Text(string="Post Code")
    # city = fields.Text(string="City")
    # state_region = fields.Text(string="State Region")
    # country = fields.Text(string="Country")

    # booking_id = fields.Char(string='Enquiry NO.')
    # expected_date_of_shipment = fields.Date("Expected Date of Shipment")
    # remarks = fields.Char("Remarks")
    # job_id = fields.Many2one('job', "Job")
    # charges_line = fields.One2many('charges.line', 'purchase_order_id', string='Charges')
    # is_rate_camparison = fields.Boolean("Is Rate Camparison")
    # valid_from = fields.Date("Valid From")
    # valid_to = fields.Date("Valid To")
    # total_freight_charge = fields.Float(compute='_get_total', string="Total Freight Charge", digits='Freight')
    # total_destination_charge = fields.Float(compute='_get_total', string="Total Destination Charge", digits='Freight')
    # total_origin_charge = fields.Float(compute='_get_total', string="Total Origin Charge", digits='Freight')
    # total_charge = fields.Float(compute='_get_total', string="Total Charge", digits='Freight')
    # invoice_id = fields.Many2one('account.move', string='Customer Invoice')
    # vendor_bill_id = fields.Many2one('account.move', string='Vendor Bill')
    correct_reason = fields.Text('Reason For Correction', tracking=True)
    correct_reason_bool = fields.Boolean(string='Correct Bool')
    # total_prepaid_charges = fields.Float(compute='_get_final_amount_per_unit',
    #                                      string="Prepaid Amt", digits='Freight')
    # total_collect_charges = fields.Float(compute='_get_final_amount_per_unit',
    #                                      string="Collect Amt", digits='Freight')
    # container_type = fields.Many2one('container.iso.code', "Container Type")
    # volume_uom = fields.Many2one('uom.uom', "Volume Unit")
    # weight_uom = fields.Many2one('uom.uom', "Weight Unit")
    sq_count = fields.Integer(string='SQ Count', compute='_get_sq_count', readonly=True)
    # is_freight_box_po = fields.Boolean('Is FB?')
    # po_inquiry_id = fields.Many2one('crm.lead', string='Inquiry ID')
    # active = fields.Boolean(string='Active', default=True)
    # booking_user_id = fields.Many2one('res.users', string="Shipper/FF")
    # delivery_type_id = fields.Many2one('service.type', string="Delivery Type", tracking=True)
    # cargo_plus_ids = fields.Many2many("cargo.plus", "container_line_purchase_rel", "container_line_id",
    #                                   "purchase_id", string="Cargo Plus")

    def _get_sq_count(self):
        sq_counts = self.env['shipment.quote'].search_count([('po_id', '=', self.id)])
        self.sq_count = sq_counts

    @api.model
    def action_open_po_tree_view(self):
        view_id = self.env.ref('freightbox.purchase_order_tree_view_freightbox').id
        view_form_id = self.env.ref('freightbox.purchase_order_form').id
        action = {
            'name': _('Purchase Order'),
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_type': 'list',
            'views': [(view_id, 'list'), (view_form_id, 'form')],
            'view_mode': 'list,form',
        }
        return action

    def button_confirm(self):
        shipment_quote_obj = self.env['shipment.quote']
        shipment_quote_id = shipment_quote_obj.search(
            [('booking_id', '=', self.rfq_id.booking_id.booking_id), ('state', '!=', 'cancelled')])
        approved_shipment_quote_id = shipment_quote_obj.search(
            [('booking_id', '=', self.rfq_id.booking_id.booking_id), ('state', '=', 'draft')])
        for order in self:
            if self.rfq_id and approved_shipment_quote_id:
                raise UserError(_('Shipment Quote must be approved before confirm'))
            if self.rfq_id and not shipment_quote_id:
                raise UserError(_('Shipment Quote should be created before confirm'))
            if order.po_inquiry_status not in ['shipment_quote_accepted'] and order.state not in ['sent']:
                if self.rfq_id == False:
                    raise UserError(_('First Create the Shipment Quote and then Accept it'))
            # if order.state not in ['shipment_quote_accepted', 'sent'] and self.rfq_id == False:
            #     raise UserError(_('First Create the Shipment Quote and then Accept it'))
            order._add_supplier_to_product()
            # Deal with double validation process
            if order.company_id.po_double_validation == 'one_step' \
                    or (order.company_id.po_double_validation == 'two_step' \
                        and order.amount_total < self.env.company.currency_id._convert(
                        order.company_id.po_double_validation_amount, order.currency_id, order.company_id,
                        order.date_order or fields.Date.today())) \
                    or order.user_has_groups('purchase.group_purchase_manager'):
                order.button_approve()
            else:
                order.write({'state': 'to approve'})
            if order.partner_id not in order.message_partner_ids:
                order.message_subscribe([order.partner_id.id])
            sale_id = self.env['sale.order'].search([('po_id', '=', order.id)])
            if sale_id:
                sale_id.is_purchase_confirmed = True

            self.partner_id.last_transaction_date = date.today()
            self.partner_id.is_manual_active = False
            self.partner_id.is_cust_active = True
        return True

    def action_shipment_quote(self):
        rate_vals = []
        shipment_quote_obj = self.env['shipment.quote']
        shipment_quote_id = shipment_quote_obj.search([
            ('booking_id', '=', self.rfq_id.booking_id.booking_id),
            ('state', '!=', 'cancelled'),
            ('po_id', '=', self.id)
        ])
        if shipment_quote_id:
            raise UserError(
                _('Shipment Quote is already created for this booking %s') % self.rfq_id.booking_id.booking_id)
        shipment_quote_id = shipment_quote_obj.create({
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
            'incoterm_id': self.incoterm_id.id,
            'state': 'draft',
            'po_id': self.id,
            'partner_id': self.rfq_id.booking_id.partner_id.id,
            'booking_id': self.rfq_id.booking_id.booking_id,
            'name': self.rfq_id.booking_id.booking_id,
            'inquiry_id': self.rfq_id.booking_id.id,
            'move_type': self.rfq_id.move_type.id,
            'valid_from': self.rfq_id.valid_from,
            'valid_to': self.rfq_id.valid_to,
            'booking_user_id': self.booking_user_id.id,
            'delivery_type_id':self.delivery_type_id.id,
            'cargo_plus_ids': [(6, 0, self.cargo_plus_ids.ids)]
        })
        if shipment_quote_id:
            shipment_quote_id.inquiry_id.sq_id = shipment_quote_id.id
            for line in self.charges_line:
                rate_vals.append({
                    'charges_id': line.charges_id.id,
                    'container_type': line.container_type.id,
                    'charges_type': line.charges_type,
                    'units': line.units,
                    'unit_price': line.unit_price,
                    'new_unit_price': 0.0,
                    'taxes_id': line.taxes_id.ids,
                    'prepaid': line.prepaid,
                    'collect': line.collect,
                    'comment': line.comment,
                    'shipment_quote_id': shipment_quote_id.id,
                    'is_loaded_for_rfq': True,
                    'currency_id': line.currency_id.id,
                    'to_currency_id': line.to_currency_id.id,
                    'charge_line_insert_update': 'copied',
                })
            shipment_quote_id.charges_line.create(rate_vals)
            if shipment_quote_id.charges_line:
                for qoute in shipment_quote_id.charges_line:
                    qoute._onchange_charges()

        se_rec = self.env['track.shipment.event'].create({
            'shipment_event': 'Shipment',
            'event_created': date.today(),
            'event_datetime': date.today(),
            'event_classifier_code': 'ACT',
            'shipment_event_type_code': 'RECE',
            'reason':'Shipment Quote Received',
            'booking_id':self.rfq_id.id,
        })
        self.po_inquiry_status = 'shipment_quote_created'
        self.rfq_id.is_shipment_quote_created = True
        view_id = self.env.ref('freightbox.shipment_quote_form_view').id
        return {
            'res_id': shipment_quote_id.id,
            'name': 'Request For Quotation',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'shipment.quote',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
        }

    def button_confirm_correction(self):
        for line in self.charges_line:
            line.write({
                'units': self.no_of_expected_container,
                'container_type': self.container_type.id,
            })
            line._onchange_charges()
            if line.unit_price <= 0.00:
                raise UserError(_("Unit Price cannot be less or equal to zero for %s") % line.charges_id.name)
        sq_id = self.env['shipment.quote'].search(
            [('po_id', '=', self.id), ('state', 'not in', ['cancel', 'rejected'])])
        if sq_id:
            so_id = self.env['sale.order'].search([('shipment_quote_id', '=', sq_id.id)])
            sq_id.update({
                'charges_line': self.charges_line.ids,
                'partner_id': self.rfq_id.booking_id.partner_id.id,
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
                'po_id': self.id,
                'booking_id': self.rfq_id.booking_id.booking_id,
                'incoterm_id': self.incoterm_id.id,
                'move_type': self.move_type.id,
                'valid_from': self.valid_from,
                'valid_to': self.valid_to,
            })
            for line in sq_id.charges_line:
                line._onchange_charges()
            sq_id.update_sale_price()
        so_id = self.env['sale.order'].search([('shipment_quote_id', '=', sq_id.id)])
        if so_id:
            so_id.update({
                'charges_line': self.charges_line.ids,
                'partner_id': self.rfq_id.booking_id.partner_id.id,
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
                'shipment_quote_id': sq_id.id,
                'booking_id': self.rfq_id.booking_id.booking_id,
                'incoterm_id': self.incoterm_id.id,
                'move_type': self.move_type.id,
                'valid_from': self.valid_from,
                'valid_to': self.valid_to,
            })
            for line in so_id.charges_line:
                line._onchange_charges()
        self.write({'po_inquiry_status': 'correction_done'})

    def action_get_sq(self):
        itemIds = self.env['shipment.quote'].search([('po_id', '=', self.id)])
        itemIds = itemIds.ids
        return {
            'name': ('Shipment Quote'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'shipment.quote',
            'view_id': False,
            'domain': [('id', 'in', itemIds)],
            'target': 'current',
        }

    def action_create_invoice(self):
        super(PurchaseOrder, self).action_create_invoice()
        for inv in self.invoice_ids:
            if self.charges_line:
                inv.write({
                    'purchase_order_id': self.id,
                    'booking_id': self.booking_id,
                    'place_of_origin': self.place_of_origin,
                    'place_of_destination': self.final_port_of_destination,
                    'amount_tax': self.amount_tax,
                })
                for line in self.charges_line:
                    inv.write({
                        'charges_line': [(0, 0, {
                            'charges_id': line.charges_id.id,
                            'container_type': line.container_type.id,
                            'charges_type': line.charges_type,
                            'units': line.units,
                            'unit_price': line.unit_price,
                            'final_amount': line.final_amount,
                            'sale_final_amount': line.sale_final_amount,
                            'taxes_id': line.taxes_id.ids,
                            'prepaid': line.prepaid,
                            'collect': line.collect,
                            'comment': line.comment,
                            'invoice_order_id': inv.id,
                            'is_loaded_for_rfq': True,
                            'currency_id': line.currency_id.id,
                            'to_currency_id': line.to_currency_id.id,
                        })],
                    })
                for rates in inv.charges_line:
                    rates._onchange_charges()

    @api.onchange('party_name_id')
    def _onchange_party_name_id(self):
        if self.party_name_id:
            self.street = self.party_name_id.street
            self.street_number = self.party_name_id.street2
            self.city = self.party_name_id.city
            self.state_region = self.party_name_id.state_id.name
            self.country = self.party_name_id.country_id.name
            self.post_code = self.party_name_id.zip
            self.tax_reference_1 = self.party_name_id.vat

    def open_po_tutorial_video_new_tab(self):
        url = self.env['ir.config_parameter'].sudo().get_param('freightbox.complete_tutorial_video_start_to_end',  "/freightbox/static/src/img/index_file_images/not_found.png")
        return {
            'type':'ir.actions.act_url',
            'url': url,
            'target': 'new',
        }

    @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    def get_view(self, view_id=None, view_type='form', **options):
        # result = super().fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        result = super().get_view(view_id, view_type, **options)
        if view_id == self.env.ref("freightbox.purchase_order_form").id:
            url = self.env['ir.config_parameter'].sudo().get_param('freightbox.po_tutorial_video',  "/freightbox/static/src/img/index_file_images/not_found.png")
            doc = etree.XML(result['arch'])
            for node in doc.xpath("//iframe[@id='purchase_order_tutorial_video']"):
                node.set('src', url)
            result['arch'] = etree.tostring(doc)
        return result

