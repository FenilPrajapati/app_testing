# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CompanyKYCWiz(models.TransientModel):
    _name = 'company.kyc.wiz'
    _description = "Company KYC Wizard"

    doc_list = fields.Text(string="List Of document")
    line_ids = fields.One2many('company.kyc.line.wiz','mst_id',string="line")
    company_cust_type = fields.Selection([('sole_proprietorship','Sole Proprietorship'),
                    ('partnership','Partnership'),
                    ('limited_liability_partnership','Limited Liability Partnership'),
                    ('private_or_public_limited_company','Private Or Public Limited Company')]
                    ,string="Company Type")
    doc_attachment = fields.Many2many('ir.attachment',string="Upload Documents")
    declaration = fields.Boolean("I hereby declare that the information provided in this form is accurate and complete. I confirm that any information is found incorrect and/or incomplete that leads a violation of regulations may initiate legal actions, and I accept that I am the responsible party for any and all charges, penalties and violations.")
    
    @api.model
    def default_get(self, fields):
        res = super(CompanyKYCWiz, self).default_get(fields)
        active_model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id')
        partner_rec = self.env[active_model].browse(active_id)
        res['company_cust_type'] = partner_rec.company_cust_type
#         if partner_rec.company_cust_type == 'sole_proprietorship':
#             res['doc_list'] = """1) GST registration certificate
# 2) Excise registration certificate
# 3) Value Added Tax (VAT) registration certificate
# 4) Turnover tax registration certificate
# 5) Professional tax registration certificate
# 6) Commercial tax registration certificate
# 7) Importer-Exporter Code Number certificate
# 8) Complete income tax return
# 9) Certificate of registration for small-scale industries or Entrepreneurs Memorandum EM (Part II)
# 10) The municipal authority-issued certificate or registration under the Shops and Establishments Act (Gumastha License) or Municipal Trade/Tax bill
# 11) Utility bills such as water, electricity, and telephone (not older than two months)
# """

#         elif partner_rec.company_cust_type == 'partnership':
#             res['doc_list'] = """1) Registration Certificate for registered partnership firms
# 2) PAN card of the Partnership firm
# 3) Partnership Deed
# 4) Proof of Legal name and telephone number of the firm and its partners
# 5) Power of Attorney granted any one of the partners or employees to transact business on its behalf
# 6) Copies of identity and address proof along with PAN of the partners and officials mentioned in the PoA"""

#         elif partner_rec.company_cust_type == 'limited_liability_partnership':
#             res['doc_list'] = """1) Certificate of Incorporation document (mentioning LLPIN) and DPIN of the
# 2) designated partners
# 3) LLP agreement
# 4) PAN of LLP
# 5) Identity and address proof along with PAN of the designated partners and other people holding the PoA
# 6) Resolution for account opening and a list of authorised persons with specimen signatures to operate the account, duly attested by designated partners."""

#         elif partner_rec.company_cust_type == 'private_or_public_limited_company':
#             res['doc_list'] = """1) Certificate of incorporation (with CIN)
# 2) Memorandum & Articles of Association
# 3) PAN of the Company
# 4) Resolution of the Board of Directors for account opening
# 5) A list containing names of officials authorised to operate the account
# 6) Proof of identity and proof of address along with PAN card of managers, officers, or employees holding Power of Attorney of the company to transact business on its behalf
# 7) Authorised signatories should be identified using pictures and signature cards that the firm has adequately confirmed
# 8) List of directors, DIN, and copy of Form 32 (if directors differ from AOA)
# 9) A valid certified copy of the business commencement certificate (Public Limited Company)
# 10) Proof of the company's name, principal place of business, mailing address, and Telephone/Fax numbers (Telephone bill not older than two months)"""

        return res

    def action_company_kyc(self):
        if not self.declaration:
            raise UserError("Please accept Declaration ")
            
        partner_rec = self.env['res.partner'].browse(self._context.get('active_ids'))
        if partner_rec:
            line_list =[]
            for i in self.line_ids:
                line_list.append((0,0,{
                    'sole_selection' : i.sole_selection,
                    'partnership_selection' : i.partnership_selection,
                    'llp_selection' : i.llp_selection,
                    'plc_selection' : i.plc_selection,
                    'doc_attachment' : i.doc_attachment.ids 
                }))
            partner_rec.company_kyc_line = line_list
            # partner_rec.doc_attachment = self.doc_attachment.ids
            partner_rec.declaration = self.declaration
            partner_rec.state = "kyc"

class CompanyKYCLineWiz(models.TransientModel):
    _name = 'company.kyc.line.wiz'
    _description = "Company KYC Line Wizard"

    mst_id = fields.Many2one('company.kyc.wiz',string="KYC")
  
    sole_selection = fields.Selection(
        [('gst_certificate','GST registration certificate'),
        ('excise_certificate','Excise registration certificate'),
        ('value_tax_certificate','Value Added Tax (VAT) registration certificate'),
        ('turnover_tax_certificate','Turnover tax registration certificate'),
        ('professional_tax_certificate','Professional tax registration certificate'),
        ('commercial_tax_certificate','Commercial tax registration certificate'),
        ('imp_Ex_certificate','Importer-Exporter Code Number certificate'),
        ('income_tax','Complete income tax return'),
        ('certificate_small_scale','Certificate of registration for small-scale industries or Entrepreneurs Memorandum EM (Part II)'),
        ('municipal_authority_issued','The municipal authority-issued certificate or registration under the Shops and Establishments Act (Gumastha License) or Municipal Trade/Tax bill'),
        ('utility_bills','Utility bills such as water, electricity, and telephone (not older than two months)'),
        ],string="Documents")

    partnership_selection = fields.Selection(
        [('registration_certificate','Registration Certificate for registered partnership firms'),
        ('pan_card','PAN card of the Partnership firm'),
        ('partnership_deed','Partnership Deed'),
        ('legal_name_telephone','Proof of Legal name and telephone number of the firm and its partners'),
        ('power_of_attorney','Power of Attorney granted any one of the partners or employees to transact business on its behalf'),
        ('copies_of_identity','Copies of identity and address proof along with PAN of the partners and officials mentioned in the PoA'),
        ],string="Documents")

    llp_selection = fields.Selection(
        [('certificate_of_incorporation','Certificate of Incorporation document (mentioning LLPIN) and DPIN of the'),
        ('designated_partners','Designated Partners'),
        ('llp_agreement','LLP Agreement'),
        ('pan_of_llp','PAN of LLP'),
        ('identity_and_address','Identity and address proof along with PAN of the designated partners and other people holding the PoA'),
        ('account_opening','Resolution for account opening and a list of authorised persons with specimen signatures to operate the account, duly attested by designated partners.'),
        ],string="Documents")

    plc_selection = fields.Selection(
        [('certificate_of_incorporation','Certificate of incorporation (with CIN)'),
        ('articles_of_association','Memorandum & Articles of Association'),
        ('pan_company','PAN of the Company'),
        ('board_of_directors','Resolution of the Board of Directors for account opening'),
        ('officials_authorised','A list containing names of officials authorised to operate the account'),
        ('identity_and_proof_of_address','Proof of identity and proof of address along with PAN card of managers, officers, or employees holding Power of Attorney of the company to transact business on its behalf'),
        ('authorised_signatories','Authorised signatories should be identified using pictures and signature cards that the firm has adequately confirmed'),
        ('list_of_directors','List of directors, DIN, and copy of Form 32 (if directors differ from AOA)'),
        ('business_commencement_certificate','A valid certified copy of the business commencement certificate (Public Limited Company)'),
        ('principal_place_of_business',"Proof of the company's name, principal place of business, mailing address, and Telephone/Fax numbers (Telephone bill not older than two months)"),
        ],string="Documents")

    doc_attachment = fields.Many2many('ir.attachment',string="Documents Attachments")

    
