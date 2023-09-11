from odoo import api, fields, models, _


class SqCorrectReason(models.TransientModel):
    _name = "sq.correct.reason"
    _description = "Correct Reason"

    correct_reason = fields.Text("Correct Reason")

    def action_submit(self):
        sq_obj = self.env['shipment.quote']
        sq_id = sq_obj.browse(self._context.get('active_ids'))
        for rec in sq_id:
            for line in rec.charges_line:
                line.write({'charge_line_insert_update': 'copied'})
            rec.write({'correct_reason': self.correct_reason, 'correct_reason_bool': True, 'state': 'under_correction'})


class SoCorrectReason(models.TransientModel):
    _name = "so.correct.reason"
    _description = "Correct Reason"

    correct_reason = fields.Text("Correct Reason")

    def action_submit(self):
        so_obj = self.env['sale.order']
        so_id = so_obj.browse(self._context.get('active_ids'))
        for rec in so_id:
            for line in rec.charges_line:
                line.write({'charge_line_insert_update': 'copied'})
            rec.write({'correct_reason': self.correct_reason, 'correct_reason_bool': True, 'so_inquiry_status': 'under_correction'})
