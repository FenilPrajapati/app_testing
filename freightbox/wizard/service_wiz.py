# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class ServiceWizard(models.TransientModel):
    _name = 'service.wizard'
    _description = 'Create Vendor Bills'

    vendor_invoice = fields.Selection(
        [('agent', 'Agent'),
         ('consignee', 'Consignee'),
         ('shipper', 'Shipper')],
        required=True,
        default='agent'
    )

    def create_invoices(self):
        services = self.env['service'].browse(self._context.get('active_ids', []))
        print("services", services)
