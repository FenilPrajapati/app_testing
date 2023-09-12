from odoo import models, fields

class AccountIncoterms(models.Model):
    _inherit = 'account.incoterms'

    description = fields.Char('Description')
    charges_template_ids = fields.Many2many('charges.templates', 'incoterm_template_rel', 'charges_templates_id',
                                            'incoterms_id', string='Charges Template')
    prepaid = fields.Boolean(string='Prepaid')
    collect = fields.Boolean(string='Collect')
