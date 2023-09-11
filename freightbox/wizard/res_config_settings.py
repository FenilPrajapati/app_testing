# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    track_count = fields.Integer(
        'Current Tracking API Count',
        config_parameter='odoo_v14_frieght.track_count',
        help="No of API calls you have done."
    )

    allowed_track_api_count = fields.Integer(
        'Allowed Tracking API Count',
        config_parameter='odoo_v14_frieght.allowed_track_count',
        default=10,
        help="Allowed No of API calls."
    )

    shipper_days = fields.Integer('Shippers Inactive Days',
        config_parameter='freightbox.shipper_days',help="Add Shippers Inactive Days")
    consignees_days = fields.Integer('Consignees Inactive Days',
        config_parameter='freightbox.consignees_days',help="Add Consignees Inactive Days")
    freightforwarders_days = fields.Integer('FreightForwarders Inactive Days',
        config_parameter='freightbox.freightforwarders_days',help="Add FreightForwarders Inactive Days")
    nvocc_days = fields.Integer('NVOCC Inactive Days',
        config_parameter='freightbox.nvocc_days',help="Add NVOCC Inactive Days")
    vendors_shipping_lines_days = fields.Integer('Vendors Shipping lines Inactive Days',
        config_parameter='freightbox.vendors_shipping_lines_days',help="Add Vendors Shipping lines Inactive Days")
    agent_days = fields.Integer('agent Inactive Days',
        config_parameter='freightbox.agent_days',help="Add agent Inactive Days")
    send_mail = fields.Boolean('Send Mail',config_parameter='freightbox.send_mail')
