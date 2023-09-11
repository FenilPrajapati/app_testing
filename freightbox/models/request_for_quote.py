from odoo import models, fields, _, api
from odoo.exceptions import UserError, ValidationError
from lxml import etree
import base64
from datetime import timedelta, datetime,date
import tempfile
import binascii
import re
import csv
import xlrd


class RequestForQuote(models.Model):
    _inherit = 'request.for.quote'
    # _inherit = ['mail.thread', 'mail.activity.mixin']
    # _description = "Request For Quote"
    # _rec_name = 'booking_id'
    # _order = 'total_charge asc'

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        if 'no_of_expected_container' in fields:
            fields.remove('no_of_expected_container')
        return super(RequestForQuote, self).read_group(
            domain, fields, groupby, offset=offset, limit=limit, orderby=orderby, lazy=lazy)

    @api.model
    def action_open_rate_comparison_form_view(self):
        view_id = self.env.ref('freightbox.rfq_tree_view').id
        view_form_id = self.env.ref('freightbox.rfq_form_view').id
        action = {
            'name': _('Rate Comparison'),
            'type': 'ir.actions.act_window',
            'res_model': 'request.for.quote',
            'view_type': 'list',
            'views': [(view_id, 'list'), (view_form_id, 'form')],
            'context': {'search_default_group_booking_id': 1},
            'view_mode': 'list,form',
        }
        return action


    invoice_id = fields.Many2one('account.move', string='Customer Invoice')
    vendor_bill_id = fields.Many2one('account.move', string='Vendor Bill')
    charges_template_ids = fields.Many2many('charges.templates', 'rfq_rel', 'charges_templates_id', 'rfq_id',
                                            string='Charges Template', tracking=True)
    charge_load_bool = fields.Boolean("Charge Load Bool")
    is_loaded_for_rfq = fields.Boolean("Is Loaded for RFQ")
    correct_reason = fields.Text('Reason For Correction', tracking=True)
    correct_reason_bool = fields.Boolean(string='Correction Bool')
    is_po_created = fields.Boolean(string='PO created')
    # amend_reason = fields.Text("Reason For Amendment", tracking=True)
    amend_bool = fields.Boolean(string='Amend Bool')
    # delivery_type_id = fields.Many2one('service.type', string="Delivery Type", tracking=True)
    # cargo_plus_ids = fields.Many2many("cargo.plus", "cargo_plus_rc_rel", "cargo_plus_id", "rc_id",
    #                                   string="Cargo Plus")

    # def action_update_charges_prepaid_collect(self):
    #     charge_lines = self.charges_line
    #     if charge_lines:
    #         for line in charge_lines:
    #             line.prepaid = line.charges_id.prepaid
    #             line.collect = line.charges_id.collect

    @api.model
    def rc_dashboard(self):
        """ This function returns the values to populate the custom dashboard in
            the RC views.
        """
        # self.check_access_rights('read')

        result = {
            'draft': 0,
            'approved': 0,
            'rejected': 0,
            'cancelled': 0,
            'expired': 0,
        }

        result['draft'] = self.search_count([('state', '=', 'draft')])
        result['approved'] = self.search_count([('state', '=', 'approved')])
        result['rejected'] = self.search_count([('state', '=', 'rejected')])
        result['cancelled'] = self.search_count([('state', '=', 'cancelled')])
        result['expired'] = self.search_count([('state', '=', 'expired')])

        return result

    @api.model
    def message_new(self, msg, custom_values=None):
        
        print('----------------------msg-- ',msg)
        defaults = {
            'name': msg.get('subject') or _("No Subject"),
            'valid_from' : date.today(),
            'valid_to' : date.today(),
        }

        code_string = base64.b64encode(msg.get('attachments')[0][1])
        print("------------------------- msg.get('attachments')",msg.get('attachments'))
        print("------------------------- code_string",code_string)

        fp = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
        fp.write(binascii.a2b_base64(code_string))
        fp.seek(0)
        workbook = xlrd.open_workbook(fp.name)
        sheet = workbook.sheet_by_index(0)
        keys = sheet.row_values(0)
        xls_reader = [sheet.row_values(i) for i in range(1, sheet.nrows)]
        data = []
        for row in xls_reader:
            line = dict(zip(keys, row))
            print("-------------------- line",line,row)
            data.append((0,0,{
                'charges_type' : line.get('charge_type'),
                'units' : line.get('unit'),
                'unit_price' : line.get('unit_price'),
                'currency_id' : line.get('currency')
            }))
        # print("------------------------- msg.get('attachments')",msg.get('attachments')[0][1])

        task = super(RequestForQuote, self).message_new(msg, custom_values=defaults)
        print('-----------------------------task',task)
        task.charges_line = data
        return task

    def action_get_po(self):
        view_id = self.env.ref('freightbox.purchase_order_tree_view_freightbox').id
        view_form_id = self.env.ref('freightbox.purchase_order_form').id
        itemIds = self.env['purchase.order'].search([('rfq_id', '=', self.id)])
        itemIds = itemIds.ids
        return {
            'name': "Purchase Order",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order',
            'views': [(view_id, 'list'), (view_form_id, 'form')],
            'domain': [('id', 'in', itemIds)],
            'target': 'current',
        }

    def button_approve(self):
        res = super(RequestForQuote, self).button_approve()
        purchase_id = self.env['purchase.order'].search([
            ('booking_id', '=', self.booking_id.booking_id),
            ('state', 'not in', ['cancel', 'purchase']),
            ('rfq_id', '=', self.id)
        ])
        if purchase_id:
            raise UserError(_('Purchase Order is already created for this booking "%s/%s"') % (
                self.booking_id.booking_id, purchase_id.name))
        else:
            rate_line_vals = []
            purchase_id = self.env['purchase.order'].create({
                'partner_id': self.shipping_name_id.id,
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
                'rfq_id': self.id,
                'booking_id': self.booking_id.booking_id,
                'incoterm_id': self.incoterm_id.id,
                'move_type': self.move_type.id,
                'valid_from': self.valid_from,
                'valid_to': self.valid_to,
                'is_freight_box_po': True,
                'po_inquiry_id': self.booking_id.id,
                'booking_user_id': self.booking_user_id.id,
                'delivery_type_id':self.delivery_type_id.id,
                'cargo_plus_ids': [(6, 0, self.cargo_plus_ids.ids)]
            })
            if purchase_id:
                self.is_po_created = True
                for line in self.charges_line:
                    rate_line_vals.append({
                        'charges_id': line.charges_id.id,
                        'container_type': line.container_type.id,
                        'charges_type': line.charges_type,
                        'units': line.units,
                        'unit_price': line.unit_price,
                        'taxes_id': line.taxes_id.ids,
                        'prepaid': line.prepaid,
                        'collect': line.collect,
                        'comment': line.comment,
                        'purchase_order_id': purchase_id.id,
                        'is_loaded_for_rfq': True,
                        'currency_id': line.currency_id.id,
                        'to_currency_id': line.to_currency_id.id,
                        'charge_line_insert_update': 'copied',
                    })
                    line.charge_line_insert_update = 'copied'
                purchase_id.charges_line.create(rate_line_vals)
                if purchase_id.charges_line:
                    for po_rate in purchase_id.charges_line:
                        po_rate._onchange_charges()
        self.state = 'approved'
        return True

    def button_confirm_correction(self):
        for line in self.charges_line:
            line.write({
                'units': self.no_of_expected_container,
                'container_type': self.container_type.id,
            })
            line._onchange_charges()
            if line.unit_price <= 0.00:
                raise UserError(_("Unit Price cannot be less or equal to zero for %s") % line.charges_id.name)
        sq_id = False
        so_id = False
        po_id = self.env['purchase.order'].search(
            [('rfq_id', '=', self.id), ('state', 'not in', ['cancel'])])
        if po_id:
            sq_id = self.env['shipment.quote'].search(
                [('po_id', '=', po_id.id), ('state', 'not in', ['cancel', 'rejected'])])

            if po_id.state != 'purchase':
                po_id.update({
                    'charges_line': self.charges_line.ids,
                    'partner_id': self.shipping_name_id.id,
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
                    'rfq_id': self.id,
                    'booking_id': self.booking_id.booking_id,
                    'incoterm_id': self.incoterm_id.id,
                    'move_type': self.move_type.id,
                    'valid_from': self.valid_from,
                    'valid_to': self.valid_to,
                    'po_inquiry_id' : self.booking_id.id,
                })
                for line in po_id.charges_line:
                    line._onchange_charges()

        if self.vendor_bill_id and self.vendor_bill_id.state == 'draft':
            self.vendor_bill_id.button_cancel()
            self.vendor_bill_id = False
        elif self.vendor_bill_id and self.vendor_bill_id.state == 'posted':
            raise UserError(
                _('You Cannot Cancel Invoice on %s state, Please first adjust invoice %s .') % (
                    self.vendor_bill_id.state, self.vendor_bill_id.name))
        if sq_id:
            so_id = self.env['sale.order'].search([('shipment_quote_id', '=', sq_id.id)])
            sq_id.update({
                'charges_line': self.charges_line.ids,
                'partner_id': self.booking_id.partner_id.id,
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
                'po_id': po_id.id,
                'booking_id': self.booking_id.booking_id,
                'incoterm_id': self.incoterm_id.id,
                'move_type': self.move_type.id,
                'valid_from': self.valid_from,
                'valid_to': self.valid_to,
            })
            for line in sq_id.charges_line:
                line._onchange_charges()
            sq_id.update_sale_price()

        if so_id:
            so_id.update({
                'charges_line': self.charges_line.ids,
                'partner_id': self.booking_id.partner_id.id,
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
                'booking_id': self.booking_id.booking_id,
                'incoterm_id': self.incoterm_id.id,
                'move_type': self.move_type.id,
                'valid_from': self.valid_from,
                'valid_to': self.valid_to,
            })
            for line in so_id.charges_line:
                line._onchange_charges()
        self.write({'state': 'correction_done'})

    def validity_of_rate(self):
        today = fields.Date.today()
        rfq_id = self.search([('valid_to', '<', today)])
        for rec in rfq_id:
            rec.write({'state': 'expired'})

    def action_load_charges(self):
        charge_list = []
        final_charge_list = []
        # self.delete_charges()
        print("---------------------------- self.charges_template_ids",self.charges_template_ids)
        if self.charges_template_ids or self.incoterm_id:
            for rec in self.incoterm_id.charges_template_ids:
                for line in rec.charges_template_line:
                    if line.charges_id.id not in charge_list:
                        rslt = {
                            'charges_id': line.charges_id.id,
                            'charges_type': line.charges_id.type_of_charges,
                            'unit_price': line.unit_price,
                            'currency_id': line.currency_id.id,
                            'to_currency_id': line.to_currency_id.id,
                            'units': line.units,
                            'taxes_id': line.taxes_id,
                            'prepaid': line.prepaid,
                            'collect': line.collect,
                        }
                        charge_list.append(rslt)

            for rec1 in self.charges_template_ids:
                for line1 in rec1.charges_template_line:
                    if line1.charges_id.id not in charge_list:
                        rslt = {
                            'charges_id': line1.charges_id.id,
                            'charges_type': line1.charges_id.type_of_charges,
                            'unit_price': line1.unit_price,
                            'currency_id': line1.currency_id.id,
                            'to_currency_id': line1.to_currency_id.id,
                            'units': line1.units,
                            'taxes_id': line1.taxes_id,
                            'prepaid': line1.prepaid,
                            'collect': line1.collect,
                        }
                        charge_list.append(rslt)
            for record in charge_list:
                final_charge_list.append((0, 0, {
                    'charges_id': record['charges_id'],
                    'charges_type': record['charges_type'],
                    'units': self.no_of_expected_container,
                    'unit_price': record['unit_price'],
                    'container_type': self.container_type.id,
                    'charge_load_bool': True,
                    'currency_id': record['currency_id'],
                    'to_currency_id': record['to_currency_id'],
                    'taxes_id': record['taxes_id'],
                    'prepaid': record['prepaid'],
                    'collect': record['collect'],
                }))
            self.charges_line = final_charge_list
        for line in self.charges_line:
            line._onchange_charges()
        if final_charge_list == []:
            raise UserError("Please select Charges Template in order to load charges..")

    def delete_charges(self):
        self.charges_line = False
        self.charges_template_ids = False

    def action_charges(self):
        self.ensure_one()
        action = {
            'name': _('Charges'),
            'type': 'ir.actions.act_window',
            'views': [(self.env.ref('freightbox.rate_charges_tree_view').id, 'tree'), (False, 'form')],
            'res_model': 'charges',
            'target': 'new',
            'context': {'current_id': self.id},
        }
        return action

    def action_create_charges_template(self):
        self.ensure_one()
        if not self.charges_line:
            raise UserError(_("There is no charges to create charge template"))
        chargetemplate = self.env['charges.templates'].sudo().search(
            [('rfq_id', '=', self.id), ('is_created_from_rc', '=', True)], limit=1)
        if chargetemplate:
            ctx = dict(
                default_rfq_id=self.id,
                default_name=chargetemplate.name,
                default_is_created_from_rc=chargetemplate.is_created_from_rc,
            )
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'charges.templates.wiz',
                'view_mode': 'form',
                'views': [(self.env.ref('freightbox.charges_template_form_view_wiz').id, "form")],
                'context': ctx,
                'target': 'new',
            }
        else:
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'charges.templates.wiz',
                'view_mode': 'form',
                'views': [(self.env.ref('freightbox.charges_template_form_view_wiz').id, "form")],
                'context': {'current_id': self.id},
                'target': 'new',
            }

    def open_rfq_tutorial_video_new_tab(self):
        url = self.env['ir.config_parameter'].sudo().get_param('freightbox.complete_tutorial_video_start_to_end',  "/freightbox/static/src/img/index_file_images/not_found.png")
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
        if view_id == self.env.ref("freightbox.rfq_form_view").id:
            url = self.env['ir.config_parameter'].sudo().get_param('freightbox.rfq_tutorial_video', "/freightbox/static/src/img/index_file_images/not_found.png")
            doc = etree.XML(result['arch'])
            for node in doc.xpath("//iframe[@id='rfq_tutorial_video']"):
                node.set('src', url)
            result['arch'] = etree.tostring(doc)
        return result
