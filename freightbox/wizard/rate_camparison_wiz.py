# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class MessageWizard(models.TransientModel):
    _name = 'message.wizard'
    _description = "Success or Update Wizard"

    def action_close(self):
        """ close wizard"""
        return {'type': 'ir.actions.act_window_close'}


class RequestForQuote(models.Model):
    _name = 'charges.templates.wiz'
    _description = "Charges Template Wizard"

    name = fields.Char(string='Name', required=True)
    rfq_id = fields.Many2one('request.for.quote', string='Rate Comparison')
    is_created_from_rc = fields.Boolean("Created from RC")

    def update_charge_template(self):
        if self.rfq_id:
            ct_rec = self.env['charges.templates']
            rec = ct_rec.search([('rfq_id', '=', self.rfq_id.id)], limit=1)
            charges = self.rfq_id.charges_line
            if rec:
                rec.write({
                    'name': self.name,
                    'charges_template_line': charges.ids,
                })
        return {
            'name': _('Updated'),
            'type': 'ir.actions.act_window',
            'views': [(self.env.ref('freightbox.message_wizard_form_for_update_msg').id, "form")],
            'view_mode': 'form',
            'res_model': 'message.wizard',
            'target': 'new'
        }

    def create_charge_template(self):
        Rfq = self.env['request.for.quote']
        if self.rfq_id:
            rc_val = self.rfq_id.id
            charges = self.rfq_id.charges_line
        else:
            rfq_rec = Rfq.browse([(self._context['current_id'])])
            rc_val = rfq_rec.id
            charges = rfq_rec.charges_line
        self.env['charges.templates'].create({
            'name': self.name,
            'rfq_id': rc_val,
            'is_created_from_rc': True,
            'charges_template_line': charges.ids,
        })

        return {
            'name': _('Successful'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'views': [(self.env.ref('freightbox.message_wizard_form').id, "form")],
            'res_model': 'message.wizard',
            'target': 'new'
        }


class RcRejectReason(models.TransientModel):
    _name = "rc.reject.reason"
    _description = "Reject Reason"

    reject_reason = fields.Text("Reason For Reject")

    def action_submit(self):
        rc_obj = self.env['request.for.quote']
        rc_id = rc_obj.browse(self._context.get('active_ids'))
        for rec in rc_id:
            rec.write({'reject_reason': self.reject_reason, 'reject_bool': True, 'state': 'rejected'})

class JobHoldReason(models.TransientModel):
    _name = "job.hold.reason"
    _description = "Hold Reason"

    hold_reason = fields.Text("Reason For Hold")

    def action_submit(self):
        job_obj = self.env['job']
        jo_id = job_obj.browse(self._context.get('active_ids'))
        for rec in jo_id:
            rec.job_state_for_hold = rec.state
            rec.write({'hold_reason': self.hold_reason, 'hold_bool': True, 'state': 'hold'})

class BolHoldReason(models.TransientModel):
    _name = "bol.hold.reason"
    _description = "Hold Reason"

    hold_reason = fields.Text("Reason For Hold")

    def action_submit(self):
        bol_obj = self.env['bill.of.lading']
        bl_id = bol_obj.browse(self._context.get('active_ids'))
        for rec in bl_id:
            # rec.job_state_for_hold = rec.state
            rec.write({'hold_reason': self.hold_reason, 'hold_bool': True, 'state': 'hold'})

class SiRejectReason(models.TransientModel):
    _name = "si.reject.reason"
    _description = "Reject Reason"

    reject_reason = fields.Text("Reason For Reject")

    def action_submit(self):
        si_obj = self.env['shipping.instruction']
        si_id = si_obj.browse(self._context.get('active_ids'))
        for rec in si_id:
            rec.write({'reject_reason': self.reject_reason, 'reject_bool': True, 'state': 'rejected'})


class RcCorrectReason(models.TransientModel):
    _name = "rc.correct.reason"
    _description = "Correct Reason"

    correct_reason = fields.Text("Reason For Correction")

    def action_submit(self):
        rc_obj = self.env['request.for.quote']
        rc_id = rc_obj.browse(self._context.get('active_ids'))
        for rec in rc_id:
            if rec.charges_line:
                for line in rec.charges_line:
                    line.write({'charge_line_insert_update': 'copied'})
            rec.write({'correct_reason': self.correct_reason, 'correct_reason_bool': True, 'state': 'under_correction'})


class PoCorrectReason(models.TransientModel):
    _name = "po.correct.reason"
    _description = "Correct Reason"

    correct_reason = fields.Text("Reason For Correction")

    def action_submit_from_po(self):
        po_obj = self.env['purchase.order']
        po_id = po_obj.browse(self._context.get('active_ids'))
        for rec in po_id:
            for line in rec.charges_line:
                line.write({'charge_line_insert_update': 'copied'})
            rec.write({'correct_reason': self.correct_reason, 'correct_reason_bool': True, 'po_inquiry_status': 'under_correction'})


class SqRejectReason(models.TransientModel):
    _name = "sq.reject.reason"
    _description = "Reject Reason"

    reject_reason = fields.Text("Reason For Rejection")

    def action_submit(self):
        sq_obj = self.env['shipment.quote']
        rc_id = sq_obj.browse(self._context.get('active_ids'))
        print("RRRRRRRRRRRRRRRRCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC",rc_id)
        for rec in rc_id:
            rec.write({'reject_reason': self.reject_reason, 'reject_bool': True, 'state': 'rejected'})
            self.env['reject.reason'].create({
                'sq_id': rc_id.id,
                'name': rec.reject_reason,
            
        })


class RcAmendReason(models.TransientModel):
    _name = "rc.amend.reason"
    _description = "Amendment Reason"

    amend_reason = fields.Text("Reason For Amendment")

    def action_submit(self):
        rc_obj = self.env['request.for.quote']
        rc_id = rc_obj.browse(self._context.get('active_ids'))
        for rec in rc_id:
            rec.write({'amend_reason': self.amend_reason, 'amend_bool': True, 'state': 'under_amendment'})
