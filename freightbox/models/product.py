from odoo import models, fields, api, _


# class ShippingContainers(models.Model):
#     _name = 'shipping.containers'
#     _description = "Shipping Containers"
#     _inherit = ['mail.thread', 'mail.activity.mixin']

#     name = fields.Char("Container Name")



class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_freight_container = fields.Boolean(string='Container', default=False)
    container_name = fields.Char(string='Container ID', required=True, copy=False, readonly=True, index=True,
                                 default=lambda self: _('New'))
    iso_code_id = fields.Many2one('container.iso.code', string="ISO Code")
    alias_code = fields.Many2one('shipping.container', string="Alias Code")
    # alias_code = fields.Char("Alias Code")
    description = fields.Char("Description")
    size = fields.Char("Size")
    volume = fields.Char("Volume")
    operator_id = fields.Many2one('res.users', string='Operator')
    soc = fields.Boolean("SOC")
    seal_no = fields.Char("Seal No.")
    container_image = fields.Binary('Conatiner Image')
    special_type = fields.Selection([('reefer', 'Reefer'), ('pl', 'PL'), ('fr', 'FR'), ('ot', 'OT')],
                                    string="Special", )
    live = fields.Boolean("Live")
    inactive = fields.Boolean("Inactive")
    length = fields.Char("Length")
    breadth = fields.Char("Breadth")
    height = fields.Char("Height")
    mode_id = fields.Many2one('mode', string='Mode')
    cargo_line_ids = fields.One2many('cargo.line', 'container_type_id', string='Cargo')
    damage_line_ids = fields.One2many('damage.line', 'container_type_id', string='Damage')
    booking_id = fields.Char(string='Inquiry NO.')
    is_container_damaged = fields.Boolean(string='Is Damaged?', default=False)

    # @api.model
    # def create(self, vals):
    #     if vals.get('container_name', _('New')) == _('New'):
            
    #         vals['container_name'] = self.env.user.company_id.name[:4] + '-' + '####'
    #     result = super(ProductTemplate, self).create(vals)
    #     return result


    @api.model
    def create(self, vals):
        if vals.get('container_name', _('New')) == _('New'):
            vals['container_name'] = self.env['ir.sequence'].next_by_code('container.type.seq') or _('New')
        result = super(ProductTemplate, self).create(vals)
        return result

    @api.onchange('iso_code_id')
    def _onchange_iso_code_id(self):
        if self.iso_code_id:
            self.name = self.iso_code_id.code
