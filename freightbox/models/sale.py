# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.tools.misc import get_lang
from lxml import etree
from datetime import timedelta, datetime,date

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def name_get(self):
        for order in self:
            res = []
            name = order.name
            if order.shipment_quote_id and order.booking_id:
                name += '/' + order.booking_id
            if order._context.get('sale_show_partner_name'):
                if order.partner_id.name:
                    name = '%s - %s' % (name, order.partner_id.name)
            res.append((order.id, name))
            return res
        return super(SaleOrder, self).name_get()

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
    # po_id = fields.Many2one('purchase.order', string='Purchase Order')
    # booking_id = fields.Char(string='Inquiry NO.')
    # is_purchase_confirmed = fields.Boolean(string='Is Purchase Confirmed')
    # expected_date_of_shipment = fields.Date("Expected Date of Shipment")
    # valid_from = fields.Date("Valid From")
    # valid_to = fields.Date("Valid To")
    # remarks = fields.Char("Remarks")
    # shipment_quote_id = fields.Many2one('shipment.quote', string='Shipment Quote', ondelete='cascade')
    # job_id = fields.Many2one('job', "Job")
    # charges_line = fields.One2many('charges.line', 'sale_order_id', string='Charges')
    # total_freight_charge = fields.Float(compute='_get_total', string="Total Freight Charge", digits='Freight')
    # total_destination_charge = fields.Float(compute='_get_total', string="Total Destination Charge", digits='Freight')
    # total_origin_charge = fields.Float(compute='_get_total', string="Total Origin Charge", digits='Freight')
    # total_charge = fields.Float(compute='_get_total', string="Total Charge", digits='Freight')
    # invoice_id = fields.Many2one('account.move', string='Customer Invoice')
    # vendor_bill_id = fields.Many2one('account.move', string='Vendor Bill')
    # total_final_amount_per_unit = fields.Float(compute='_get_final_amount_per_unit',
    #                                            string="Sum of final Amount", digits='Freight')
    # total_prepaid_charges = fields.Float(compute='_get_final_amount_per_unit',
    #                                      string="Sum of Prepaid charges", digits='Freight')
    # total_collect_charges = fields.Float(compute='_get_final_amount_per_unit',
    #                                      string="Sum of Collect charges", digits='Freight')
    # container_type = fields.Many2one('container.iso.code', "Container Type")
    # so_inquiry_status = fields.Selection([
    #     ('po_confirm', 'PO confirmed'), ('under_correction', 'Under Correction'),
    #     ('correction_done', 'Correction Done')], "Inquiry Status")
    correct_reason = fields.Text('Reason For Correction', tracking=True)
    correct_reason_bool = fields.Boolean(string='Correct Bool')
    # volume_uom = fields.Many2one('uom.uom', "Volume Unit")
    # weight_uom = fields.Many2one('uom.uom', "Weight Unit")
    bill_count = fields.Integer(compute="_compute_bills", string='Bill Count')
    job_count = fields.Integer(compute="_get_job_count", string='Job Count')
    bill_ids = fields.Many2many('account.move', compute="_compute_bills", string='Bills')
    so_inquiry_id = fields.Many2one('crm.lead', string='Inquiry ID')
    is_freight_box_so = fields.Boolean('Is FB?')

    # prepaid_total_without_tax = fields.Float(compute='_get_final_amount_per_unit',
    #                                      string="Prepaid Sale", digits='Freight')
    # prepaid_total_tax = fields.Float(compute='_get_final_amount_per_unit',
    #                                      string="Prepaid Tax - tax amt", digits='Freight')
    # collect_total_without_tax = fields.Float(compute='_get_final_amount_per_unit',
    #                                          string="Collect Sale", digits='Freight')
    # collect_total_tax = fields.Float(compute='_get_final_amount_per_unit',
    #                                  string="Collect Tax", digits='Freight')
    # active = fields.Boolean(string='Active', default=True)
    # booking_user_id = fields.Many2one('res.users', string="Shipper/FF")
    delivery_type_id = fields.Many2one('service.type', string="Delivery Type", tracking=True)

    def action_view_vendor_bill(self):
        if self.po_id:
            bills = self.mapped('bill_ids')
            result = self.env['ir.actions.act_window']._for_xml_id('account.action_move_in_invoice_type')
            # choose the view_mode accordingly
            if len(bills) > 1:
                result['domain'] = [('id', 'in', bills.ids)]
            elif len(bills) == 1:
                res = self.env.ref('account.view_move_form', False)
                form_view = [(res and res.id or False, 'form')]
                if 'views' in result:
                    result['views'] = form_view + [(state, view) for state, view in result['views'] if view != 'form']
                else:
                    result['views'] = form_view
                result['res_id'] = bills.id
            else:
                result = {'type': 'ir.actions.act_window_close'}
        return result

    def action_get_job(self):
        itemIds = self.env['job'].search([('id', '=', self.job_id.id)])
        itemIds = itemIds.ids
        return {
            'name': ('Job'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'job',
            'view_id': False,
            'domain': [('id', 'in', itemIds)],
            'target': 'current',
        }

    def _get_job_count(self):
        job_counts = self.env['job'].search_count([('id', '=', self.job_id.id)])
        self.job_count = job_counts

    @api.model
    def action_open_sale_order_tree_view(self):
        view_id = self.env.ref('freightbox.sale_order_tree_inherit').id
        view_form_id = self.env.ref('freightbox.sale_order_form_view_freightbox').id
        action = {
            'name': _('Sale Order'),
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order',
            'view_type': 'list',
            'views': [(view_id, 'list'), (view_form_id, 'form')],
            'view_mode': 'list,form',
        }
        return action

    def action_create_job(self):
        # Create user.
        user_id = False
        partner_id = self.partner_id
        User = self.env['res.users']
        # cargo_plus_obj = self.env["cargo.plus"]
        job_obj = self.env["job"]
        user_rec = User.search([('partner_id', '=', partner_id.id)])
        se_rec = self.env['track.shipment.event'].create({
                'shipment_event': 'Shipment',
                'event_created': date.today(),
                'event_datetime': date.today(),
                'event_classifier_code': 'ACT',
                'shipment_event_type_code': 'RECE',
                'reason':'Job Created',
                'booking_id':self.so_inquiry_id.id
            })
        rfq_ids = self.env['request.for.quote'].search([('booking_id', '=', self.booking_id)])
        if user_rec:
            user_id = user_rec.id
        view_id = self.env.ref('freightbox.job_form_view').id
        shipment_terms_origin = ''
        if self.shipment_terms == 'lcl':
            shipment_terms_origin = 'lcl'
        if self.shipment_terms == 'fcl':
            shipment_terms_origin = 'fcl'
        if self.shipment_terms == 'both':
            shipment_terms_origin = 'both'
        if self.shipment_terms == 'bb':
            shipment_terms_origin = 'bb'

        for cargo_plus_line in self.cargo_plus_ids:
            cargo_plus_line.no_of_confirmed_container = cargo_plus_line.no_of_expected_container

        ctx = dict(
            default_so_id=self.id,
            default_po_id=self.po_id.id,
            default_shipper_id=self.partner_id.id,
            default_booking_id=self.id,
            default_exp_no_of_container=self.po_id.rfq_id.booking_id.no_of_expected_container,
            default_confirmed_no_of_container=self.no_of_expected_container,
            default_requested_equipment_type=self.po_id.rfq_id.booking_id.container_type,
            default_confirmed_equipment_type=self.container_type,
            default_commodity_description=self.cargo_name,
            default_cargo_gross_weight=self.weight,
            default_cargo_uom_id=self.weight_uom.id,
            default_inquiry_id=self.po_id.rfq_id.booking_id.id,
            default_shipment_terms_origin=shipment_terms_origin,
            default_shipment_terms_dest=shipment_terms_origin,
            default_requested_date_time=self.expected_date_of_shipment,
            default_user_id=user_id,
            default_booking_user_id=self.booking_user_id.id,
            default_service_type_origin=self.delivery_type_id.id,
            default_cargo_plus_ids=[(6, 0, self.cargo_plus_ids.ids)]
        )
        for line in rfq_ids:
            if line.is_po_created != True:
                line.write({'state': 'cancelled'})
        return {
            'name': 'Job',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'job',
            'view_id': view_id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'context': ctx,
        }

    def action_create_vendor_bill(self):
        if self.po_id:
            po_order_lines = self.po_id.order_line
            if po_order_lines:
                for o in po_order_lines:
                    o.qty_received = o.product_qty
            se_rec = self.env['track.shipment.event'].create({
                'shipment_event': 'Shipment',
                'event_created': date.today(),
                'event_datetime': date.today(),
                'event_classifier_code': 'ACT',
                'shipment_event_type_code': 'RECE',
                'reason':'Vendor Bill Created',
                'booking_id':self.so_inquiry_id.id
            })
        self.po_id.action_create_invoice()

    def so_tutorial_video_new_tab(self):
        url = self.env['ir.config_parameter'].sudo().get_param('freightbox.complete_tutorial_video_start_to_end',
                                                               "\freightbox\static\src\img\index_file_images\non.png")
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
        if view_id == self.env.ref("freightbox.view_order_form").id:
            url = self.env['ir.config_parameter'].sudo().get_param('freightbox.so_tutorial_video',
                                                                   "/freightbox/static/src/img/index_file_images/not_found.png")
            doc = etree.XML(result['arch'])
            for node in doc.xpath("//iframe[@id='so_tutorial_video']"):
                node.set('src', url)
            result['arch'] = etree.tostring(doc)
        return result


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_charges = fields.Boolean(string='Charges', default=False)

    @api.onchange('product_id')
    def product_id_change(self):
        if not self.product_id:
            return
        valid_values = self.product_id.product_tmpl_id.valid_product_template_attribute_line_ids.product_template_value_ids
        # remove the is_custom values that don't belong to this template
        for pacv in self.product_custom_attribute_value_ids:
            if pacv.custom_product_template_attribute_value_id not in valid_values:
                self.product_custom_attribute_value_ids -= pacv

        # remove the no_variant attributes that don't belong to this template
        for ptav in self.product_no_variant_attribute_value_ids:
            if ptav._origin not in valid_values:
                self.product_no_variant_attribute_value_ids -= ptav

        vals = {}
        if not self.product_uom or (self.product_id.uom_id.id != self.product_uom.id):
            vals['product_uom'] = self.product_id.uom_id
            vals['product_uom_qty'] = self.product_uom_qty or 1.0

        product = self.product_id.with_context(
            lang=get_lang(self.env, self.order_id.partner_id.lang).code,
            partner=self.order_id.partner_id,
            quantity=vals.get('product_uom_qty') or self.product_uom_qty,
            date=self.order_id.date_order,
            pricelist=self.order_id.pricelist_id.id,
            uom=self.product_uom.id
        )

        vals.update(name=self.get_sale_order_line_multiline_description_sale(product))

        if not self.product_id.is_freight_container == True:
            self._compute_tax_id()

        if self.order_id.pricelist_id and self.order_id.partner_id:
            vals['price_unit'] = self.env['account.tax']._fix_tax_included_price_company(
                self._get_display_price(product), product.taxes_id, self.tax_id, self.company_id)
        self.update(vals)

        title = False
        message = False
        result = {}
        warning = {}
        if product.sale_line_warn != 'no-message':
            title = _("Warning for %s", product.name)
            message = product.sale_line_warn_msg
            warning['title'] = title
            warning['message'] = message
            result = {'warning': warning}
            if product.sale_line_warn == 'block':
                self.product_id = False
        return result
