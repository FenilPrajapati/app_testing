# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from datetime import timedelta, datetime,date
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = 'res.partner'

    contact_type = fields.Selection([('shippers','Shippers'),
                    ('consignees','Consignees'),
                    ('freightforwarders','FreightForwarders'),
                    ('NVOCC','NVOCC'),
                    ('vendors_shipping_lines','Vendors Shipping lines'),
                    ('creditor','Creditor'),
                    ('debtor','Debtor'),
                    ('agent','Agent')],string="Contact Type")
    # is_cust_active = fields.Boolean('Is Active',default=True)
    # is_blacklist = fields.Boolean('Is Black List')
    # blacklist_ids = fields.One2many('res.blacklist','partner_id',string="BlackList")
    # is_approach_inactive = fields.Boolean('Is Approach Inactive',default=False)
    # is_manual_active = fields.Boolean('Is Manual Active',default=False)
    company_cust_type = fields.Selection([('sole_proprietorship','Sole Proprietorship'),
                    ('partnership','Partnership'),
                    ('limited_liability_partnership','Limited Liability Partnership'),
                    ('private_or_public_limited_company','Private Or Public Limited Company')]
                    ,string="Company Type")
    agent_type_id = fields.Many2one('job', string="Agent type id")
    inquery_agent_type_id = fields.Many2one('crm.lead', string="Crm Lead")
    contract_id = fields.Many2one("contract",string="Contract")
    agent_type = fields.Many2one('agent.type', string="Agent Type")
    # agent_type = fields.Selection([
    #     ('stuffing', 'Stuffing'),
    #     ('destuffing', 'Destuffing'),
    #     ('transhipment', 'Transhipment'),
    #     ('insurance', 'Insurance'),
    #     ('other', 'Other')], "Agent Type", tracking=True)
    # type_of_agent = fields.Text("Type of agent")
    agent_name = fields.Many2one("res.partner", string="Agent", tracking=True)
    charge = fields.Integer(string='Charges', tracking=True)
    agent_loc = fields.Many2one('stock.location', "Location", tracking=True)     
    contract_count = fields.Integer(string='Total contract Count', compute='_get_contract_count', readonly=True, searchable=True)           
    contract_count_store = fields.Integer(string='contract Count',store=True)           


    # # For KYC 
    # state = fields.Selection([('kyc','KYC')],string="State")
    # pan_no = fields.Char(string="Pan No")
    # pan_atta = fields.Binary(string="Pan Attachment",attachment=True,)
    # add_passport = fields.Boolean("Passport")
    # add_dl = fields.Boolean("Driving License")
    # add_sa = fields.Boolean("Registered Lease/Sale Agreement of Residence")
    # add_tele_bill = fields.Boolean("Latest Telephone Bill")
    # add_gas_bill = fields.Boolean("Latest Gas Bill")
    # add_ration_card = fields.Boolean("Ration Card")
    # add_voter_id_card = fields.Boolean("Voter Identity Card")
    # add_bank_detail = fields.Boolean("Latest Bank Account Statement/Passbook")
    # add_electricity_bill = fields.Boolean("Latest Electricity Bill")
    # add_attachment = fields.Many2many('ir.attachment',string="Address Proof")
    # declaration = fields.Boolean("I hereby declare that the information provided in this form is accurate and complete. I confirm that any information is found incorrect and/or incomplete that leads a violation of regulations may initiate legal actions, and I accept that I am the responsible party for any and all charges, penalties and violations.")
    # f_name = fields.Char(string="Frist Name")
    # l_name = fields.Char(string="Last Name")
    # app_sign = fields.Binary(string="Signature",attachment=True,)
    # last_transaction_date = fields.Date(string="Last Transaction Date")
    # doc_attachment = fields.Many2many('ir.attachment','company_kyc',string="Documents")
    # person_kyc_line = fields.One2many('partner.kyc.line','partner_id',string="line")
    # company_kyc_line = fields.One2many('company.kyc.line','partner_id',string="line")
    is_due_days_limit = fields.Boolean("Days Limit")
    due_limit_days = fields.Integer("Days")
    due_days_tolerance = fields.Integer("Tolerance (in Hrs.)")
    is_due_amount_limit = fields.Boolean("Amount Limit")
    due_limit_amount = fields.Float("Amount")
    due_amount_tolerance_percentage = fields.Integer("Tolerance Percentage")
    is_due_exceeded = fields.Boolean("Due Exceeded", compute="get_is_due_exceeded")
    

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        print("--------------------self.env.context. ",self.env.context)

        if self.env.context.get('order_display',False):
            if name:
                records = self.search(args,order="contract_count_store desc")
                return records.name_get()

        return self.search([('name', operator, name)]+args, limit=limit).name_get()

    def _get_contract_count(self):
        for record in self:
            contract_counts = self.env['contract'].search_count([('shipping_line_name', '=', record.id)])
            record.contract_count = contract_counts
            record.contract_count_store = contract_counts

    def action_get_contract(self):
        itemIds = self.env['contract'].search([('shipping_line_name', '=', self.id)])
        itemIds = itemIds.ids
        return {
            'name': "Contract",
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'contract',
            'view_id': False,
            'domain': [('id', 'in', itemIds)],
            'target': 'current',
        }

    @api.constrains('due_amount_tolerance_percentage')
    def _check_due_amount_tolerance_percentage_value(self):
        for record in self:
            if record.due_amount_tolerance_percentage > 100:
                raise ValidationError("The value of Tolerance Percentage cannot be more than 100.")
            if record.due_amount_tolerance_percentage < 0:
                raise ValidationError("The value of Tolerance Percentage cannot be less than 0.")

    def get_is_due_exceeded(self):
        invoice_obj = self.env["account.move"]
        for record in self:
            record.is_due_exceeded = False
            if record.is_due_days_limit or record.is_due_amount_limit:
                all_partners_and_children = {}
                all_partner_ids = []
                for partner in record.filtered('id'):
                    all_partners_and_children[partner] = self.with_context(active_test=False).search(
                        [('id', 'child_of', partner.id)]).ids
                    all_partner_ids += all_partners_and_children[partner]

                if all_partner_ids:
                    invoice_domain = [
                        ('partner_id', 'in', partner.ids),
                        ('move_type', '=', 'out_invoice'),
                        ('payment_state', 'in', ['not_paid', 'in_payment', 'partial'])
                    ]
                    invoices = invoice_obj.search(invoice_domain)
                    total_due_amount = 0
                    for invoice in invoices:
                        if invoice.amount_residual_signed > 0 and record.is_due_amount_limit:
                            tolerance_amount = record.due_limit_amount * record.due_amount_tolerance_percentage / 100
                            credit_amount = record.due_limit_amount + tolerance_amount
                            total_due_amount += invoice.amount_residual_signed
                            if total_due_amount > credit_amount:
                                record.is_due_exceeded = True
                                break

                        if record.is_due_days_limit:
                            due_datetime = invoice.invoice_date_due + timedelta(days=record.due_limit_days) +  timedelta(hours=record.due_days_tolerance)
                            current_datetime = fields.Datetime.now().date()
                            if current_datetime > due_datetime:
                                record.is_due_exceeded = True
                                break

    # Show company name on tree. If contact, show contact name. if company, show company name - by default it shows both
    # using display name compute method - updating new field (customer_contact_name)
    @api.depends('is_company', 'name', 'parent_id.display_name', 'type', 'company_name')
    def _compute_display_name(self):
        diff = dict(show_address=None, show_address_only=None, show_email=None, html_format=None, show_vat=None)
        names = dict(self.with_context(**diff).name_get())
        for partner in self:
            if not partner.parent_name:
                partner.customer_contact_name = partner.name
            if partner.parent_name:
                partner.customer_contact_name = partner.parent_name
            partner.display_name = names.get(partner.id)

    customer_contact_name = fields.Char(string="Customer Company Name")
    user_subscribed = fields.Boolean("User Subscribed?")
    reference_code = fields.Char(string="Reference Code")
    type = fields.Selection(selection_add=[('point_of_stuffing', "Point of Stuffing"),
                                           ('point_of_destuffing', "Point of Destuffing")]
                            )
    # def action_active_partner(self):
    #     if self.is_cust_active:
    #         self.is_cust_active = False
    #     else:
    #         self.is_cust_active = True
    #     self.is_manual_active = True

    def toggal_active(self):
        print(';;;;;;;;;;;;;;;;;;;;;')

    @api.model
    def partner_dashboard(self):
        """ This function returns the values to populate the custom dashboard in
            the RC views.
        """
        # self.check_access_rights('read')

        result = {
            'shippers': 0,
            'consignees': 0,
            'freightforwarders': 0,
            'NVOCC': 0,
            'vendors_shipping_lines': 0,
            'agent': 0,
            'black_list':0,
            'active':0,
            'in_active':0
        }

        result['shippers'] = self.search_count([('contact_type', '=', 'shippers')])
        result['consignees'] = self.search_count([('contact_type', '=', 'consignees')])
        result['freightforwarders'] = self.search_count([('contact_type', '=', 'freightforwarders')])
        result['NVOCC'] = self.search_count([('contact_type', '=', 'NVOCC')])
        result['agent'] = self.search_count([('contact_type', '=', 'agent')])
        # result['black_list'] = self.search_count([('is_blacklist', '=', True)])
        # result['active'] = self.search_count([('is_cust_active', '=', True)])
        # result['in_active'] = self.search_count([('is_cust_active', '!=', True)])

        return result

    # def check_if_active_partner(self,days_diff,check_days):
    #     is_approach_inactive = False
    #     is_cust_active = True
    #     print("---------------- days_diff - check_days",abs(days_diff - check_days))
    #     if abs(days_diff - check_days) < 10:
    #         is_approach_inactive = True
    #     if days_diff > check_days:
    #         is_cust_active = False

    #     return is_approach_inactive,is_cust_active

    # def check_active_partner(self):
    #     partner_rec = self.env['res.partner'].search([])
    #     print('=------------------',partner_rec)

    #     shipper_days = int(self.env['ir.config_parameter'].sudo().get_param('freightbox.shipper_days'))
    #     consignees_days = int(self.env['ir.config_parameter'].sudo().get_param('freightbox.consignees_days'))
    #     freightforwarders_days = int(self.env['ir.config_parameter'].sudo().get_param('freightbox.freightforwarders_days'))
    #     nvocc_days = int(self.env['ir.config_parameter'].sudo().get_param('freightbox.nvocc_days'))
    #     vendors_shipping_lines_days = int(self.env['ir.config_parameter'].sudo().get_param('freightbox.vendors_shipping_lines_days'))
    #     agent_days = int(self.env['ir.config_parameter'].sudo().get_param('freightbox.agent_days'))

    #     for i in partner_rec:
    #         if i.is_manual_active != True:
    #             date1 = date.today()
    #             if i.last_transaction_date:
    #                 date2 = i.last_transaction_date
    #                 days_diff = (date1 - date2).days
    #                 if i.contact_type == 'shippers':
    #                     i.is_approach_inactive,i.is_cust_active = self.check_if_active_partner(days_diff,shipper_days)
                    
    #                 elif i.contact_type == 'consignees':
    #                     i.is_approach_inactive,i.is_cust_active = self.check_if_active_partner(days_diff,consignees_days)

    #                 elif i.contact_type == 'freightforwarders':
    #                     i.is_approach_inactive,i.is_cust_active = self.check_if_active_partner(days_diff,freightforwarders_days)

    #                 elif i.contact_type == 'NVOCC':
    #                     i.is_approach_inactive,i.is_cust_active = self.check_if_active_partner(days_diff,nvocc_days)

    #                 elif i.contact_type == 'vendors_shipping_lines':
    #                     i.is_approach_inactive,i.is_cust_active = self.check_if_active_partner(days_diff,vendors_shipping_lines_days)

    #                 elif i.contact_type == 'agent':
    #                     i.is_approach_inactive,i.is_cust_active = self.check_if_active_partner(days_diff,agent_days)


# class ResBlacklist(models.Model):
#     _name = 'res.blacklist'

#     partner_id = fields.Many2one('res.partner',string="Partner")
#     block_by_id = fields.Many2one('res.users',string="Block By")
#     unblock_by_id = fields.Many2one('res.users',string="Un-Block By")
#     name = fields.Text(string="Reason")
#     unblock_date = fields.Date('Un-Block Date')
#     doc_attachment = fields.Many2many('ir.attachment',string="Documents")


# class PartnerKYCLineWiz(models.Model):
#     _name = 'partner.kyc.line'
#     _description = "Partner KYC Line"

#     partner_id = fields.Many2one('res.partner',string="Partner")
#     doc_selection = fields.Selection(
#         [('pan_card','Pan Card'),
#         ('passport','Passport'),
#         ('driving_license','Driving License'),
#         ('agreement_of_residence','Registered Lease/Sale Agreement of Residence'),
#         ('latest_telephone_bill','Latest Telephone Bill'),
#         ('latest_gas_bill','Latest Gas Bill'),
#         ('ration_card','Ration Card'),
#         ('voter_identity_card','Voter Identity Card'),
#         ('account_statements','Latest Bank Account Statement/Passbook'),
#         ('latest_electricity_bill','Latest Electricity Bill'),
#         ],string="Documents")

#     doc_attachment = fields.Many2many('ir.attachment',string="Documents Attachments")

# class CompanyKYCLine(models.Model):
#     _name = 'company.kyc.line'
#     _description = "Company KYC Line"

#     partner_id = fields.Many2one('res.partner',string="Partner")
  
#     sole_selection = fields.Selection(
#         [('gst_certificate','GST registration certificate'),
#         ('excise_certificate','Excise registration certificate'),
#         ('value_tax_certificate','Value Added Tax (VAT) registration certificate'),
#         ('turnover_tax_certificate','Turnover tax registration certificate'),
#         ('professional_tax_certificate','Professional tax registration certificate'),
#         ('commercial_tax_certificate','Commercial tax registration certificate'),
#         ('imp_Ex_certificate','Importer-Exporter Code Number certificate'),
#         ('income_tax','Complete income tax return'),
#         ('certificate_small_scale','Certificate of registration for small-scale industries or Entrepreneurs Memorandum EM (Part II)'),
#         ('municipal_authority_issued','The municipal authority-issued certificate or registration under the Shops and Establishments Act (Gumastha License) or Municipal Trade/Tax bill'),
#         ('utility_bills','Utility bills such as water, electricity, and telephone (not older than two months)'),
#         ],string="Documents")

#     partnership_selection = fields.Selection(
#         [('registration_certificate','Registration Certificate for registered partnership firms'),
#         ('pan_card','PAN card of the Partnership firm'),
#         ('partnership_deed','Partnership Deed'),
#         ('legal_name_telephone','Proof of Legal name and telephone number of the firm and its partners'),
#         ('power_of_attorney','Power of Attorney granted any one of the partners or employees to transact business on its behalf'),
#         ('copies_of_identity','Copies of identity and address proof along with PAN of the partners and officials mentioned in the PoA'),
#         ],string="Documents")

#     llp_selection = fields.Selection(
#         [('certificate_of_incorporation','Certificate of Incorporation document (mentioning LLPIN) and DPIN of the'),
#         ('designated_partners','Designated Partners'),
#         ('llp_agreement','LLP Agreement'),
#         ('pan_of_llp','PAN of LLP'),
#         ('identity_and_address','Identity and address proof along with PAN of the designated partners and other people holding the PoA'),
#         ('account_opening','Resolution for account opening and a list of authorised persons with specimen signatures to operate the account, duly attested by designated partners.'),
#         ],string="Documents")

#     plc_selection = fields.Selection(
#         [('certificate_of_incorporation','Certificate of incorporation (with CIN)'),
#         ('articles_of_association','Memorandum & Articles of Association'),
#         ('pan_company','PAN of the Company'),
#         ('board_of_directors','Resolution of the Board of Directors for account opening'),
#         ('officials_authorised','A list containing names of officials authorised to operate the account'),
#         ('identity_and_proof_of_address','Proof of identity and proof of address along with PAN card of managers, officers, or employees holding Power of Attorney of the company to transact business on its behalf'),
#         ('authorised_signatories','Authorised signatories should be identified using pictures and signature cards that the firm has adequately confirmed'),
#         ('list_of_directors','List of directors, DIN, and copy of Form 32 (if directors differ from AOA)'),
#         ('business_commencement_certificate','A valid certified copy of the business commencement certificate (Public Limited Company)'),
#         ('principal_place_of_business',"Proof of the company's name, principal place of business, mailing address, and Telephone/Fax numbers (Telephone bill not older than two months)"),
#         ],string="Documents")

#     doc_attachment = fields.Many2many('ir.attachment',string="Documents Attachments")

class AgentType(models.Model):
    _name = 'agent.type'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Agent type"
    _rec_name = 'name'

    name = fields.Char(string="Rate Type")

    
                            