# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class MailWiz(models.TransientModel):
    _name = "mail.wiz"
    _description = "Mail Wizard"

    name = fields.Char('Subject', default='Shipment Quote')

    partner_ids = fields.Many2many('res.partner', string='Recipients', )

    body = fields.Html('Contents', default='')
    attachment_ids = fields.Many2many(
        'ir.attachment', 'mail_wiz_attachments_rel',
        'mail_wiz_id', 'attachment_id', 'Attachments')

    def send_mail(self):
        ir_mail_server = self.env['ir.mail_server']
        mail_mail = self.env['mail.mail']
        mail_server_ids = ir_mail_server.sudo().search([], order='sequence', limit=1)
        attachment_list = []
        text = self.body
        # Mail send for user
        email_from = self.env.user.email
        if not self.partner_ids:
            raise UserError(_("Please select at least one Shipment Line."))
        for partner in self.partner_ids:
            if mail_server_ids and mail_server_ids.smtp_user:
                text = self.body
                vals = {
                    'email_from': email_from,
                    'email_to': partner.email,
                    'body': text,
                    'body_html': text,
                    'parent_id': None,
                    'auto_delete': True,
                    'attachment_ids': [(6, 0, self.attachment_ids.ids)]
                }
                mail = mail_mail.create(vals)
                mail.send()
