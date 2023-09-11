# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from lxml import etree


class CrmLead(models.Model):
    _inherit = 'crm.lead'
    _rec_name = 'booking_id'
    _order = 'booking_id desc'

    # is_blacklist = fields.Boolean(related='partner_id.is_blacklist')

    def action_view_sale_quotation(self):
        action = self.env["ir.actions.actions"]._for_xml_id("sale.action_quotations_with_onboarding")
        action['context'] = {
            'search_default_draft': 1,
            'search_default_partner_id': self.partner_id.id,
            'default_partner_id': self.partner_id.id,
            'default_opportunity_id': self.id
        }
        action['domain'] = [('opportunity_id', '=', self.id), ('state', 'in', ['draft', 'sent'])]
        quotations = self.mapped('order_ids').filtered(lambda l: l.state in ('draft', 'sent'))
        if len(quotations) == 1:
            if self.is_freight_box_crm:
                action['views'] = [(self.env.ref('freightbox.view_order_form').id, 'form')]
            else:
                action['views'] = [(self.env.ref('sale.view_order_form').id, 'form')]
            action['res_id'] = quotations.id
        return action

    @api.model
    def action_get_crm_freightbox_views(self):
        view_id = self.env.ref('freightbox.freight_box_crm_tree').id
        view_form_id = self.env.ref('freightbox.crm_lead_view_form').id
        rfq_tree_id = self.env.ref('base_freightbox.rfq_tree_view').id
        rfq_form_id = self.env.ref('freightbox.rfq_form_view').id
        po_tree_id = self.env.ref('base_freightbox.purchase_order_tree_view_freightbox').id
        po_form_id = self.env.ref('freightbox.purchase_order_form').id
        sq_tree_id = self.env.ref('base_freightbox.shipment_quote_tree_view').id
        sq_form_id = self.env.ref('freightbox.shipment_quote_form_view').id
        so_tree_id = self.env.ref('base_freightbox.sale_order_tree_inherit').id
        so_form_id = self.env.ref('freightbox.view_order_form').id
        action = {
            'crm_form_id': view_form_id,
            'crm_tree_id': view_id,
            'po_form_id': po_form_id,
            'po_tree_id': po_tree_id,
            'so_form_id': so_form_id,
            'so_tree_id': so_tree_id,
            'rfq_form_id': rfq_form_id,
            'rfq_tree_id': rfq_tree_id,
            'sq_tree_id': sq_tree_id,
            'sq_form_id': sq_form_id,
        }
        return action

    @api.model
    def action_open_enquiry_form_view(self):
        view_id = self.env.ref('freightbox.crm_lead_tree_opportunity_inherited').id
        view_form_id = self.env.ref('freightbox.crm_lead_view_form').id
        action = {
            'name': _('Inquiry'),
            'type': 'ir.actions.act_window',
            'res_model': 'crm.lead',
            'view_type': 'list',
            'views': [(view_id, 'list'), (view_form_id, 'form')],
            'view_mode': 'list,form',
        }
        return action

    def open_inquiry_tutorial_video_new_tab(self):
        url = self.env['ir.config_parameter'].sudo().get_param('freightbox.complete_tutorial_video_start_to_end', '/freightbox/static/src/img/index_file_images/not_found.png')
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
        if view_id == self.env.ref("freightbox.crm_lead_view_form").id:
            url = self.env['ir.config_parameter'].sudo().get_param('freightbox.inquiry_tutorial_video', "/freightbox/static/src/img/index_file_images/not_found.png")
            doc = etree.XML(result['arch'])
            for node in doc.xpath("//iframe[@id='inquiry_tutorial_video']"):
                node.set('src', url)
            result['arch'] = etree.tostring(doc)
        return result

    
    @api.model
    def fbcrm_dashboard(self):
        """ This function returns the values to populate the custom dashboard in
            the Job views.
        """
        result = {'freight_box': 0}
        result['freight_box'] = self.search_count([('is_freight_box_crm','=',True)])
        print("-----------------------result",result)
        return result


class InheritLeadPartner(models.TransientModel):
    _inherit = "crm.lead2opportunity.partner"

    def action_apply(self):
        res = super(InheritLeadPartner,self).action_apply()
        active_ids = self.env.context.get('active_ids')
        inquiry = self.env['crm.lead'].browse(active_ids)

        se_rec = self.env['track.shipment.event'].create({
            'shipment_event': 'Shipment',
            'event_created': inquiry.create_date,
            'event_datetime': inquiry.create_date,
            'event_classifier_code': 'ACT',
            'shipment_event_type_code': 'RECE',
            'reason':'Booking Received',
            'booking_id':inquiry.id

        })

        return res