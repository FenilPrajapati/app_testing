# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class BlackListWiz(models.TransientModel):
    _name = 'blacklist.wiz'
    _description = "BlackList Wizard"

    blacklist_reason = fields.Text('Blacklist Reason',required=True)

    def action_blacklist(self):
        partner_rec = self.env['res.partner'].browse(self._context.get('active_ids'))
        if partner_rec:
            partner_rec.is_blacklist = True
            partner_rec.blacklist_ids = [(0,0,{'name':self.blacklist_reason,'block_by_id':self.env.user.id})]

