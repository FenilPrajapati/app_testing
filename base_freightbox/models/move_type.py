# -*- coding: utf-8 -*-
from odoo import models, fields


class MoveType(models.Model):
    _name = 'move.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Move Type"

    name = fields.Char("Name")
