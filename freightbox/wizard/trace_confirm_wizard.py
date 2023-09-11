# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class TraceConfirmWizard(models.Model):
    _name = 'trace.confirm.wizard'
    _description = "Trace Confirm Wizard"
    _rec_name = "transport_id"

    transport_id = fields.Many2one("transport", "Transport")
    message = fields.Text("Message")
    is_track_used_up = fields.Boolean("Tracks Used Up", default=False)

    def call_trace_api(self):
        return self.transport_id.with_context(confirmed=True).action_request_for_tnt()
