from odoo import models, fields, api


# class MinimumRateGuidelines(models.Model):
#     _name = 'mrg'
#     _inherit = ['mail.thread', 'mail.activity.mixin']
#     _description = "MRG"
#     _rec_name = 'name'

#     @api.depends('port_of_origin_id','final_port_of_destination_id')
#     def _compute_name(self):
#         if self.port_of_origin_id and self.final_port_of_destination_id:
#             self.name = self.port_of_origin_id.name + '-' + self.final_port_of_destination_id.name

#     name = fields.Char("Name", compute=_compute_name, readonly=False, store=True, tracking=True)
#     port_of_origin_id = fields.Many2one('port', string='Port of loading', tracking=True, required=True, domain=[('one', '=', True)])
#     final_port_of_destination_id = fields.Many2one('port', string='Final port of Destination', help="Final Port of Destination", tracking=True, required=True, domain=[('one', '=', True)])
#     min_rates_line = fields.One2many('minimum.rates', 'minimum_rates_id', string='Minimum Rates Lines')
    # from_date = fields.Datetime('Valid from', default=fields.Date.today())
    # to_date = fields.Datetime('Valid to')
    # mrg_charges = fields.Integer('MRG Charges')
    # currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.company.currency_id)
    # container_type = fields.Many2one('shipping.containers', "Container Type", tracking=True)
    # iso_code_id = fields.Many2one('container.iso.code', string="ISO Code")
    # commodity = fields.Char("Commodity", tracking=True)

    # def name_get(self):
    #     res = []
    #     for record in self:
    #         name = str(record.port_of_origin_id.name) + '-' + str(record.final_port_of_destination_id.name)
    #         res.append((record.id, name))
    #     return res

class MinimumRates(models.Model):
    _inherit = 'minimum.rate'
    # _inherit = ['mail.thread', 'mail.activity.mixin']
    # _description = "Minimum Rates"

    # from_date = fields.Datetime('Valid from', default=fields.Date.today(), tracking=True)
    # to_date = fields.Datetime('Valid to', tracking=True)
    # charges_id = fields.Many2one('charges', string='Charges')
    # prepaid = fields.Boolean(string='Prepaid', tracking=True)
    # hs_code_id = fields.Many2one('hs.code', string='HS Code')
    # collect = fields.Boolean(string='Collect', tracking=True)
    # port_of_origin_id = fields.Many2one('port', string='Port of loading', tracking=True, required=True, domain=[('one', '=', True)])
    # final_port_of_destination_id = fields.Many2one('port', string='Final port of Destination', help="Final Port of Destination", tracking=True, required=True, domain=[('one', '=', True)])
    # mrg_charges = fields.Integer('MRG Charges', tracking=True)
    # currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.company.currency_id, tracking=True)
    # container_type = fields.Many2one('shipping.containers', "Container Type", tracking=True)
    # iso_code_id = fields.Many2one('container.iso.code', string="ISO Code", tracking=True)
    # commodity = fields.Char("Commodity description", tracking=True)
    # minimum_rates_id = fields.Many2one('mrg', string='MRG', tracking=True)
    contract_id = fields.Many2one('contract', string="Contract id")
    # party_id = fields.Many2one('res.partner', string="Party Name")

    # def button_create_copy(self):
    #     self.copy()