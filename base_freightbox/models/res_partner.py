# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import timedelta, datetime,date
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    user_subscribed = fields.Boolean("User Subscribed?")
    inquery_agent_type_id = fields.Many2one('crm.lead', string="Crm Lead")