import ast
import base64
import re

from odoo import _, api, fields, models, tools
from odoo.exceptions import UserError

class InheritEmailTemplate(models.TransientModel):
    _inherit = "mail.compose.message"

    def action_send_mail(self):
        rec = super(InheritEmailTemplate, self).action_send_mail()
        # model = self._context.get('active_model')
        
        if self.model == 'shipping.instruction':
            si_res = self.env[self.model].search([('id','=',self.res_id)])
            if si_res:
                si_res.state = 'si_sent'
        if self.model == 'shipment.quote':
            sq_res = self.env[self.model].search([('id','=',self.res_id)])
            if sq_res:
                stage_id = self.env['crm.stage'].search([('name', 'ilike', 'Proposition')], limit=1)
                if stage_id:
                    sq_res.po_id.po_inquiry_id.write({'stage_id': stage_id.id})
                sq_res.email_sent_bool = True

        return rec