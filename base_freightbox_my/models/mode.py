from odoo import models, fields


class Mode(models.Model):
    _name = 'mode'
    inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Mode"

    name = fields.Char("Name")

