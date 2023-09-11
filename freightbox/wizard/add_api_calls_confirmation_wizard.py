# -*- coding: utf-8 -*-
from odoo import fields, models, _
from odoo.exceptions import ValidationError
import requests
import json
import socket


class AddApiCallsConfirmationWizard(models.TransientModel):
    _name = 'add.api.calls.confirmation.wizard'
    _description = "Add Api Calls Confirmation Wizard"

    no_of_api_calls_to_add = fields.Integer('No Of Api Calls to Add', default=10)

    def action_add_api_calls(self):
        hostname = socket.gethostname()
        dbuuid = self.env['ir.config_parameter'].sudo().get_param('database.uuid')
        username = hostname + '_' + dbuuid
        add_allowed_api_call_vals = {
            'username': username,
            'add_allowed_api_calls': 10
        }
        api_rec = self.env['api.integration'].search([('name', '=', 'add_allowed_api_calls')])[-1]
        if not api_rec:
            raise ValidationError("API Record does not exist for 'add_allowed_api_calls'.")
        requests.post(api_rec.url, data=json.dumps(add_allowed_api_call_vals))

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'add.api.calls.confirmation.wizard',
            'view_mode': 'form',
            'views': [(self.env.ref('freightbox.add_api_calls_notification_wizard_form').id, "form")],
            'target': 'new',
        }

    def action_okay(self):
        return True

