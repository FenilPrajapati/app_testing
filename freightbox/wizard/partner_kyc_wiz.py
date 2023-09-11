# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class PartnerKYCWiz(models.TransientModel):
    _name = 'partner.kyc.wiz'
    _description = "Partner KYC Wizard"

    pan_no = fields.Char(string="Pan No")
    pan_atta = fields.Binary(string="Pan Attachment",attachment=True,)
    add_passport = fields.Boolean("Passport")
    add_dl = fields.Boolean("Driving License")
    add_sa = fields.Boolean("Registered Lease/Sale Agreement of Residence")
    add_tele_bill = fields.Boolean("Latest Telephone Bill")
    add_gas_bill = fields.Boolean("Latest Gas Bill")
    add_ration_card = fields.Boolean("Ration Card")
    add_voter_id_card = fields.Boolean("Voter Identity Card")
    add_bank_detail = fields.Boolean("Latest Bank Account Statement/Passbook")
    add_electricity_bill = fields.Boolean("Latest Electricity Bill")
    add_attachment = fields.Many2many('ir.attachment',string="Address Proof")
    declaration = fields.Boolean("I hereby declare that the information provided in this form is accurate and complete. I confirm that any information is found incorrect and/or incomplete that leads a violation of regulations may initiate legal actions, and I accept that I am the responsible party for any and all charges, penalties and violations.")
    f_name = fields.Char(string="Frist Name")
    l_name = fields.Char(string="Last Name")
    app_sign = fields.Binary(string="Signature",attachment=True,)
    line_ids = fields.One2many('partner.kyc.line.wiz','mst_id')

    def action_blacklist(self):
        partner_rec = self.env['res.partner'].browse(self._context.get('active_ids'))
        self.check_address()
        if partner_rec:
            # partner_rec.pan_no = self.pan_no
            # partner_rec.pan_atta = self.pan_atta
            # partner_rec.add_passport = self.add_passport
            # partner_rec.add_dl = self.add_dl
            # partner_rec.add_sa = self.add_sa
            # partner_rec.add_tele_bill = self.add_tele_bill
            # partner_rec.add_gas_bill = self.add_gas_bill
            # partner_rec.add_ration_card = self.add_ration_card
            # partner_rec.add_voter_id_card = self.add_voter_id_card
            # partner_rec.add_bank_detail = self.add_bank_detail
            # partner_rec.add_electricity_bill = self.add_electricity_bill
            # partner_rec.add_attachment = self.add_attachment.ids
            line_list =[]
            for i in self.line_ids:
                line_list.append((0,0,{
                    'doc_selection' : i.doc_selection,
                    'doc_attachment' : i.doc_attachment.ids 
                }))
            partner_rec.person_kyc_line = line_list
            partner_rec.declaration = self.declaration
            partner_rec.f_name = self.f_name
            partner_rec.l_name = self.l_name
            partner_rec.app_sign = self.app_sign
            partner_rec.state = "kyc"

    def check_address(self):

        # if not self.pan_no:
        #     raise UserError("Please Enter Pan No")
        # if not self.pan_atta:
        #     raise UserError("Please Attached Pan Card Image ")

        # srl = 0
        # if self.add_passport:
        #     srl += 1
        # if self.add_dl:
        #     srl += 1
        # if self.add_sa:
        #     srl += 1
        # if self.add_tele_bill:
        #     srl += 1
        # if self.add_gas_bill:
        #     srl += 1
        # if self.add_ration_card:
        #     srl += 1
        # if self.add_voter_id_card:
        #     srl += 1
        # if self.add_bank_detail:
        #     srl += 1
        # if self.add_electricity_bill:
        #     srl += 1
        # if srl < 2:
        #     raise UserError("Please Select Atleast Two !!")

        # if len(self.add_attachment) < 2:
        #     raise UserError("Please Attached Atleast Two !!")

        if not self.declaration:
            raise UserError("Please accept Declaration ")

        if not self.app_sign:
            raise UserError("Please Attached Signature ")


class PartnerKYCLineWiz(models.TransientModel):
    _name = 'partner.kyc.line.wiz'
    _description = "Partner KYC Line Wizard"

    mst_id = fields.Many2one('partner.kyc.wiz',string="KYC")
    doc_selection = fields.Selection(
        [('pan_card','Pan Card'),
        ('passport','Passport'),
        ('driving_license','Driving License'),
        ('agreement_of_residence','Registered Lease/Sale Agreement of Residence'),
        ('latest_telephone_bill','Latest Telephone Bill'),
        ('latest_gas_bill','Latest Gas Bill'),
        ('ration_card','Ration Card'),
        ('voter_identity_card','Voter Identity Card'),
        ('account_statements','Latest Bank Account Statement/Passbook'),
        ('latest_electricity_bill','Latest Electricity Bill'),
        ],string="Documents")

    doc_attachment = fields.Many2many('ir.attachment',string="Documents Attachments")
    