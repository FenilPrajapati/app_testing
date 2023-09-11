from odoo import api, fields, models, _
from datetime import timedelta, datetime,date
import hashlib

class BolPrintSignWiz(models.TransientModel):
    _name = 'bol.print.sign.wiz'
    _description = "unBlackList Wizard"

    user_id = fields.Many2one("res.users")
    print_sign = fields.Char('Print Signature')

    @api.model
    def default_get(self, fields):
        res = super(BolPrintSignWiz, self).default_get(fields)
        active_id = self.env.context.get('active_id')
        res['user_id'] = active_id
        return res

    def action_save_sign(self):
        hash_object = hashlib.sha256()
        hash_object.update(self.print_sign.encode())
        encrypted_sign = hash_object.hexdigest()
        self.user_id.print_signature = encrypted_sign