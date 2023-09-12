from odoo import models, fields, api, _


class ChargesLine(models.Model):
    _inherit = 'charges.line'

    purchase_order_id = fields.Many2one('purchase.order', string='Purchase Quote')
    shipment_quote_id = fields.Many2one('shipment.quote', string='Shipment Quote')
    rfq_id = fields.Many2one('request.for.quote', string='Rate Comparison')
    sale_order_id = fields.Many2one('sale.order', string='Sale Quote')

