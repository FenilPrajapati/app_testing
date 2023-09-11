# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from datetime import timedelta, datetime,date


class UNBlackListWiz(models.TransientModel):
    _name = 'unblacklist.wiz'
    _description = "unBlackList Wizard"

    blacklist_reason = fields.Text('Blacklist Reason')
    doc_attachment = fields.Many2many('ir.attachment',string="Documents")

    @api.model
    def default_get(self, fields):
        res = super(UNBlackListWiz, self).default_get(fields)
        active_model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id')
        partner_rec = self.env[active_model].browse(active_id)

        for i in partner_rec.blacklist_ids:
            if not i.unblock_date:
                res['blacklist_reason'] = i.name
        
        return res

    def action_unblacklist(self):
        partner_rec = self.env['res.partner'].browse(self._context.get('active_ids'))
        if partner_rec:
            partner_rec.is_blacklist = False
            for i in partner_rec.blacklist_ids:
                if not i.unblock_date:
                    i.unblock_date = date.today()
                    i.doc_attachment = self.doc_attachment.ids
                    i.unblock_by_id = self.env.user.id

