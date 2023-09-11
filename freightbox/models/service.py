from odoo import models, fields


class Service(models.Model):
    _name = 'service'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Service"

    name = fields.Char('Service')
    partner_id = fields.Many2one('res.partner', 'Vendor', tracking=True)
    cost_price = fields.Float("Cost Price", tracking=True)
    sale_price = fields.Float("Sale Price", tracking=True)
    route_line_id = fields.Many2one('route.line', string='Route', tracking=True)
    currency_id = fields.Many2one('res.currency', string="Currency", tracking=True)
    description = fields.Char("Description", tracking=True)
    quantity = fields.Float("Quantity", tracking=True)


class ServiceType(models.Model):
    _name = 'service.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "ServiceType"

    name = fields.Char("Name", required=True)
