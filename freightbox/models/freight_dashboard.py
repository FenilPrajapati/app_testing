# Copyright 2021 PowerpBox IT Solutions Pvt Ltd.

from odoo import models


class FreightDashboard(models.Model):
    _name = 'freight.dashboard'
    _description = "Freight Dashboard"

    def get_freight_dashboard_data(self):
        purchase_order = self.env['purchase.order']
        sale_order = self.env['sale.order']
        job = self.env['job']
        shipping_instructions = self.env['shipping.instruction']
        bol = self.env['bill.of.lading']

        crm_count = self.env['crm.lead'].sudo().search([('company_id', '=', self.env.company.id), ('is_freight_box_crm', '=', True)])
        rc_count = self.env['request.for.quote'].sudo().search([('company_id', '=', self.env.company.id)])
        draft_po_count = purchase_order.sudo().search([('company_id', '=', self.env.company.id), ('is_freight_box_po', '=', True), ('state', '=', 'draft')])
        sq_count = self.env['shipment.quote'].sudo().search([('company_id', '=', self.env.company.id)])
        draft_so_count = sale_order.sudo().search([('company_id', '=', self.env.company.id), ('is_freight_box_so', '=', True), ('state', '=', 'draft')])
        po_count = purchase_order.sudo().search([('company_id', '=', self.env.company.id), ('is_freight_box_po', '=', True), ('state', '!=', 'draft')])
        so_count = sale_order.sudo().search([('company_id', '=', self.env.company.id), ('is_freight_box_so', '=', True), ('state', '!=', 'draft')])
        job_count = job.sudo().search([])
        transport_count = self.env['transport'].sudo().search([])
        open_si_count = shipping_instructions.sudo().search([('state', '=', 'open')])
        draft_si_count = shipping_instructions.sudo().search([('state', '=', 'draft')])
        update_si_count = shipping_instructions.sudo().search([('state', '=', 'updated')])
        approve_si_count = shipping_instructions.sudo().search([('state', '=', 'accepted')])
        draft_bol_count = bol.sudo().search([('state', '=', 'draft')])
        update_bol_count = bol.sudo().search([('state', '=', 'update')])
        hold_bol_count = bol.sudo().search([('state', '=', 'hold')])
        amend_bol_count = bol.sudo().search([('state', '=', 'amend')])
        switch_bol_count = bol.sudo().search([('state', '=', 'switch')])
        issue_bol_count = bol.sudo().search([('state', '=', 'approve')])
        surrender_bol_count = bol.sudo().search([('state', '=', 'done')])
        release_cargo_count = job.sudo().search([('state', '=', 'cargo_released')])
        return {
            "crm_count": len(crm_count),
            "rc_count": len(rc_count),
            "draft_po_count": len(draft_po_count),
            "sq_count": len(sq_count),
            "draft_so_count": len(draft_so_count),
            "po_count": len(po_count),
            "so_count": len(so_count),
            "job_count": len(job_count),
            "transport_count": len(transport_count),
            "open_si_count": len(open_si_count),
            "draft_si_count": len(draft_si_count),
            "update_si_count": len(update_si_count),
            "approve_si_count": len(approve_si_count),
            "draft_bol_count": len(draft_bol_count),
            "update_bol_count": len(update_bol_count),
            "hold_bol_count": len(hold_bol_count),
            "amend_bol_count": len(amend_bol_count),
            "switch_bol_count": len(switch_bol_count),
            "issue_bol_count": len(issue_bol_count),
            "surrender_bol_count": len(surrender_bol_count),
            "release_cargo_count": len(release_cargo_count),
        }
