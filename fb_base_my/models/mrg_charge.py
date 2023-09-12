from odoo import models, fields, api


class MinimumRateGuideline(models.Model):
    _name = 'mrg.charges'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "MRG"
    _rec_name = 'name'

    @api.depends('port_of_origin_id','final_port_of_destination_id')
    def _compute_name(self):
        if self.port_of_origin_id and self.final_port_of_destination_id:
            self.name = self.port_of_origin_id.name + '-' + self.final_port_of_destination_id.name

    name = fields.Char("Name", compute=_compute_name, readonly=False, store=True, tracking=True)
    port_of_origin_id = fields.Many2one('port', string='Port of loading', tracking=True)
    final_port_of_destination_id = fields.Many2one('port', string='Final port of Destination', help="Final Port of Destination", tracking=True)
    min_rates_line = fields.One2many('minimum.rate', 'minimum_rates_id', string='Minimum Rates Lines')
    
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

class MinimumRate(models.Model):
    _name = 'minimum.rate'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Minimum Rates"

    from_date = fields.Date('Valid from', default=fields.Date.today(), tracking=True)
    to_date = fields.Date('Valid to', tracking=True)
    charges_id = fields.Many2one('charges', string='Charges')
    charge_type = fields.Char("Charge Type", tracking=True)
    prepaid = fields.Boolean(string='Prepaid', tracking=True)
    hs_code_id = fields.Many2one('hs.code', string='HS Code')
    collect = fields.Boolean(string='Collect', tracking=True)
    port_of_origin_id = fields.Many2one('port', string='Port of loading', tracking=True)
    final_port_of_destination_id = fields.Many2one('port', string='Final port of Destination', help="Final Port of Destination", tracking=True)
    mrg_charges = fields.Integer('MRG Charges', tracking=True)
    currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.company.currency_id, tracking=True)
    container_type = fields.Many2one('shipping.container', "Container Type", tracking=True)
    iso_code_id = fields.Many2one('container.iso.code', string="ISO Code", tracking=True)
    commodity = fields.Char("Commodity description", tracking=True)
    minimum_rates_id = fields.Many2one('mrg.charges', string='MRG', tracking=True)
    # contract_id = fields.Many2one('contract', string="Contract id")
    party_id = fields.Many2one('res.partner', string="Party Name")
    # mrg_charges_id = fields.Many2one('contract', string="Contract")
    service_id = fields.Many2one('service.for.sl', string="Service name")


    @api.onchange('charges_id')
    def _onchange_charges_id(self):
        if self.charges_id:
            self.charge_type = self.charges_id.type_of_charges

    def button_create_copy(self):
        self.copy()

class HsCodes(models.Model):
    _name = 'hs.code'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "HS Code"

    hs_code_classification = fields.Char("Classification", tracking=True)
    code = fields.Char("Code", tracking=True)
    description = fields.Char("Description", tracking=True)

class DetentionCharges(models.Model):
    _name = 'detention.charges'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Detention Charges"

    # detention_charges_id = fields.Many2one('contract', string="Contract")
    container_type = fields.Many2one('shipping.container', "Container Type", tracking=True)
    iso_code_id = fields.Many2one('container.iso.code', string="ISO Code", tracking=True)
    # location_at = fields.Char("Detention Location", tracking=True)
    detention_at = fields.Selection([
        ('import', 'Import'),
        ('exxport', 'Export'), ], default="import", string="Detention location")
    charges = fields.Float('Rate/container', tracking=True)
    from_days = fields.Integer('From days', tracking=True)
    to_days = fields.Integer('To days', tracking=True)
    quantity = fields.Float('Quantity', tracking=True)
    total_days = fields.Integer('total no of days', tracking=True)
    total_charge = fields.Float('Total rate', tracking=True)
    currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.company.currency_id, tracking=True)
    total_currency_id = fields.Many2one('res.currency', string="Final Currency", default=lambda self: self.env.company.currency_id, tracking=True)
    #  compute="_compute_no_of_days")

    @api.onchange('to_days','total_days','from_days')
    def _onchange_no_of_days(self):
        self.total_days = self.to_days - self.from_days    
    
    @api.onchange('charges','total_days','quantity')
    def _onchange_get_total(self):
        total_charge = 0.0
        for line in self:
            if line.charges or line.total_days or line.quantity:
                total_charge = line.charges * line.total_days * line.quantity
                self.total_charge = total_charge

    @api.onchange('from_days','to_days')
    def _onchange_of_days(self):
        if self.to_days and self.from_days:
            self.total_days = self.to_days - self.from_days

    def button_create_copy(self):
        self.copy()