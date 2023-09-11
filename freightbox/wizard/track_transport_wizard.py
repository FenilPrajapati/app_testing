# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class TrackTransportWizard(models.TransientModel):
    _name = 'track.transport.wizard'
    _description = "Track Transport Wizard"

    transport_id = fields.Selection([('cbr','Carrier Booking Reference'),('container_id','Container ID')])

    def action_track(self):
        return True