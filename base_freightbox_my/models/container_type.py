from odoo import models, fields, _


class ContainerType(models.Model):
    _name = 'container.type'
    _description = "Container Type"

    name = fields.Char(string='Container ID', required=True, copy=False, readonly=True, index=True,
                       default=lambda self: _('New'))
    iso_code_id = fields.Many2one('container.iso.code', string="ISO Code")
    alias_code = fields.Char("Alias Code")
    description = fields.Char("Description")
    size = fields.Char("Size")
    volume = fields.Char("Volume")
    operator_id = fields.Many2one('res.users', string='Operator')
    soc = fields.Boolean("SOC")
    seal_no = fields.Char("Seal No.")
    container_image = fields.Binary('Conatiner Image')
    special_type = fields.Selection(
        [('reefer_active', 'Reefer Active'), ('reefer_inactive', 'Reefer InActive'), ('pl', 'PL'), ('fr', 'FR'),
         ('ot', 'OT')], string="Special", )
    length = fields.Char("Length")
    breadth = fields.Char("Breadth")
    height = fields.Char("Height")
    mode_id = fields.Many2one('mode', string='Mode')
    cargo_line_ids = fields.One2many('cargo.line', 'container_type_id', string='Cargo')
    damage_line_ids = fields.One2many('damage.line', 'container_type_id', string='Damage')

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "{} ({})".format(record.name, record.special_type)))
        return result


class CargoLine(models.Model):
    _name = 'cargo.line'
    _description = "Cargo Details"

    container_type_id = fields.Many2one('container.type', string='Container Type')
    name = fields.Char("Cargo Name")
    description = fields.Char("Description")
    shipper_name = fields.Char("Shipper")
    cosignee_name = fields.Char("Cosignee")


class DamageLine(models.Model):
    _name = 'damage.line'
    _description = "Damage Details"

    container_type_id = fields.Many2one('container.type', string='Container Type')
    damage_image = fields.Binary('Damage Image')
    damage_fname = fields.Char('Damage File Name', size=64)
    description = fields.Char("Description")
