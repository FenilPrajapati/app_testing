from odoo import models, fields


class FacilityTypeCode(models.Model):
    _name = 'facility.type.code'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Facility Type Code"
    _rec_name = "facility_type_code"

    facility_type_code = fields.Char("Facility Type Code", required="1", tracking=True)
    facility_type_name = fields.Char("Facility Type Name", tracking=True)
    description = fields.Char("Description", tracking=True)

class RepairType(models.Model):
    _name = 'repair.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Repair Type"
    _rec_name = 'name'

    name = fields.Char(string="Repair Type")

class ServiceForSL(models.Model):
    _name = 'service.for.sl'
    # _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Service for SL"
    _rec_name = 'name'

    name = fields.Char(string="Service Name")
    shipping_line_id = fields.Many2one('res.partner', string="Shipping Line", domain="[('supplier_rank', '>', 0)]")

