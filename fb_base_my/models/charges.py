from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class ChargesTemplates(models.Model):
    _name = 'charges.templates'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Charges Template"

    name = fields.Char(string='Name', required=True)
    charges_template_line = fields.One2many('charges.line', 'charges_template_id',
                                            string='Charges', copy=True, tracking=True)
    # rfq_id = fields.Many2one('request.for.quote', string='Rate Comparison', tracking=True)
    # is_created_from_rc = fields.Boolean("Created from RC", tracking=True)
    incoterm_id = fields.Many2one('account.incoterms', string="Incoterm", tracking=True)

    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        default = dict(default or {}, name=_("%s ( Copy )", self.name))
        return super(ChargesTemplates, self).copy(default=default)

    def update_charges_prepaid_collect(self):
        charge_lines = self.charges_template_line
        if charge_lines:
            for charge in charge_lines:
                charge.prepaid = charge.charges_id.prepaid
                charge.collect = charge.charges_id.collect

    def action_charges(self):
        self.ensure_one()
        action = {
            'name': _('Charges'),
            'type': 'ir.actions.act_window',
            'views': [(self.env.ref('freightbox.charges_tree_view2').id, 'tree'), (False, 'form')],
            'res_model': 'charges',
            'target': 'new',
            'context': {'current_id': self.id},
        }
        return action

    _sql_constraints = [
        ('name_uniq', 'unique (name)', "Charges Template name already exists !"),
    ]


class Charges(models.Model):
    _name = 'charges'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Charges"

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code', required=True, tracking=True)
    description = fields.Char(string='Description', tracking=True)
    currency_id = fields.Many2one('res.currency', string="Currency", tracking=True)
    type_of_charges = fields.Selection([
        ('freight', 'Freight'),
        ('origin', 'Origin'),
        ('destination', 'Destination'), ], string="Type of Charges", required=True, tracking=True)
    prepaid = fields.Boolean(string='Prepaid', tracking=True)
    collect = fields.Boolean(string='Collect', tracking=True)
    calculation_basis = fields.Selection([
        ('per_day', 'Per Day'),
        ('per_ton', 'Per Ton'),
        ('per_sq_mt', 'Per Sq. Meter')], string="Calculation Basis", tracking=True)
    # is_nvocc = fields.Boolean('Is NVOCC?')

    def name_get(self):
        res = []
        for record in self:
            name = str(record.code) + '-' + str(record.name)
            res.append((record.id, name))
        return res

    def action_add_charges(self):
        ChargesLine = self.env['charges.line']
        ChargesTemplate = self.env['charges.templates']
        c_obj = ChargesTemplate.browse([(self._context['current_id'])])
        for line in self:
            ChargesLine.create({
                'charges_id': line.id,
                'charges_type': line.type_of_charges,
                'units': 0.0,
                'final_amount': 0.0,
                'tax_amt': 0.0,
                'unit_price': 0.0,
                'charges_template_id': c_obj.id,
                'prepaid': line.prepaid,
                'collect': line.collect,
            })
        return True

    @api.model
    def create(self, vals):
        result = super(Charges, self).create(vals)
        if vals.get('prepaid') or vals.get('collect'):
            if vals.get('prepaid') is True and vals.get('collect') is True:
                raise ValidationError('Both Prepaid and Collect cannot be selected')
            if vals.get('prepaid') is False and vals.get('collect') is False:
                raise ValidationError('Either one of Prepaid or Collect must be selected')
        return result

    def write(self, vals):
        result = super(Charges, self).write(vals)
        if vals.get('prepaid') or vals.get('collect'):
            if self.collect is False and vals.get('prepaid') is False:
                raise ValidationError('Either one of Prepaid or Collect must be selected')
            if self.prepaid is False and vals.get('collect') is False:
                raise ValidationError('Either one of Prepaid or Collect must be selected')

            if vals.get('prepaid') or vals.get('collect'):
                if self.collect is True and vals.get('prepaid') is True:
                    raise ValidationError('Both Prepaid and Collect cannot be selected')
                if self.prepaid is True and vals.get('collect') is True:
                    raise ValidationError('Both Prepaid and Collect cannot be selected')
        return result

    def cancel_charges(self):
        return {'type': 'ir.actions.act_window_close'}

    # def add_charges_rate_comparision(self):
    #     Rfq = self.env['request.for.quote']
    #     c_obj = Rfq.browse([(self._context['current_id'])])
    #     for line in self:
    #         charge_line = c_obj.charges_line.create({
    #             'charges_id': line.id,
    #             'charges_type': line.type_of_charges,
    #             'units': c_obj.no_of_expected_container,
    #             'unit_price': 0.00,
    #             'rfq_id': c_obj.id,
    #             'currency_id': c_obj.currency_id.id,
    #             'to_currency_id': c_obj.currency_id.id,
    #             'container_type': c_obj.container_type.id,
    #             'is_loaded_for_rfq': True,
    #             'prepaid': line.prepaid,
    #             'collect': line.collect,
    #         })
    #     return charge_line


class ChargesLine(models.Model):
    _name = 'charges.line'
    _description = "Charges Line"

    # shipment_quote_id = fields.Many2one('shipment.quote', string='Shipment Quote')
    # purchase_order_id = fields.Many2one('purchase.order', string='Purchase Quote')
    # sale_order_id = fields.Many2one('sale.order', string='Sale Quote')
    # invoice_order_id = fields.Many2one('account.move', string='Invoice ID')

    charges_id = fields.Many2one('charges', string='Charges')
    comment = fields.Char("Comment")
    units = fields.Float(string="Units", readonly=False)
    unit_price = fields.Float("Cost Price")
    new_unit_price = fields.Float("Sale Price")
    currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.company.currency_id)
    final_amount = fields.Float("Cost Final Amount", digits=(12, 3))
    sale_final_amount = fields.Float("Sale Final Amount", digits=(12, 3))
    taxes_id = fields.Many2many('account.tax', 'charges_line_taxes_rel', 'charges_line_id', 'tax_id', string='Taxes')
    tax_amt = fields.Float('Tax Amount')
    sale_tax_amt = fields.Float('Sale Tax Amount')
    # sq_taxes_id = fields.Many2many('account.tax', 'charges_line_sq_taxes_rel', 'charges_line_id', 'sq_tax_id',
    #                                string='Sq Taxes')

    charges_template_id = fields.Many2one('charges.templates', string='Template Line')
    charge_load_bool = fields.Boolean("Charge Load Bool")
    # rfq_id = fields.Many2one('request.for.quote', string='Rate Comparison')
    is_loaded_for_rfq = fields.Boolean('Loaded for RFQ')
    to_currency_id = fields.Many2one('res.currency', string="To Currency",
                                     default=lambda self: self.env.company.currency_id)
    base_currency_id = fields.Many2one('res.currency', string="To Currency",
                                     default=lambda self: self.env.company.currency_id)
    charges_type = fields.Selection([
        ('freight', 'Freight'),
        ('origin', 'Origin'),
        ('destination', 'Destination'), ], string="Charges Type")
    prepaid = fields.Boolean(string='Prepaid')
    collect = fields.Boolean(string='Collect')
    shipping_container_type = fields.Many2one('shipping.container', "Container Type", tracking=True)
    container_type = fields.Many2one('container.iso.code', "ISO code")
    charge_line_insert_update = fields.Selection([
        ('insert', 'Inserted'),
        ('updated', 'Updated'),
        ('copied', 'Copied'),
    ], default="insert", string="Insert/Update")
    today_exchange_rate = fields.Float("Exchange Rate", digits=(12, 5))
    company_currency_total = fields.Float("Company currency total",
                                          digits=(12, 3))
    sale_company_currency_tot = fields.Float("Company currency total",
                                          digits=(12, 3))

    @api.onchange('charges_id')
    def _onchange_charges_id(self):
        if self.charges_id:
            # self.container_type = self.container_type.name
            # self.code = self.charges_id.code
            
            self.currency_id = self.charges_id.currency_id.id
            self.charges_type = self.charges_id.type_of_charges
            self.prepaid = self.charges_id.prepaid
            self.collect = self.charges_id.collect

    def button_create_copy(self):
        self.copy()


    # @api.onchange('charges_id')
    # def _onchange_rfq_id(self):
    #     if self.rfq_id:
    #         self.units = self.rfq_id.no_of_expected_container
    #         self.container_type = self.rfq_id.container_type.id
    #     if self.purchase_order_id:
    #         self.units = self.purchase_order_id.no_of_expected_container
    #         self.container_type = self.purchase_order_id.container_type.id
    #     if self.shipment_quote_id:
    #         self.units = self.shipment_quote_id.no_of_expected_container
    #         self.container_type = self.shipment_quote_id.container_type.id
    #     if self.sale_order_id:
    #         self.units = self.sale_order_id.no_of_expected_container
    #         self.container_type = self.sale_order_id.container_type.id
    #     self.is_loaded_for_rfq = True
    #     self.charges_type = self.charges_id.type_of_charges
    #     self.prepaid = self.charges_id.prepaid
    #     self.collect = self.charges_id.collect
        # self.charge_line_insert_update = 'insert'

    @api.onchange('units', 'unit_price', 'new_unit_price', 'taxes_id', 'currency_id', 'to_currency_id')
    def _onchange_charges(self):
        final_amount = 0.0
        sale_final_amount = 0.0
        tax_amt = price = sale_tax_amt = sale_price = 0.0
        taxes = {}
        sale_taxes = {}
        if self.unit_price > 0.00:
            price = self.unit_price
            final_amount = self.units * price
        if self.new_unit_price > 0.00:
            sale_price = self.new_unit_price
            sale_final_amount = self.units * sale_price
        if self.taxes_id:
            if self.unit_price > 0.00:
                taxes = self.taxes_id.compute_all(self.unit_price, self.currency_id, self.units)
            if self.new_unit_price > 0.00:
                sale_taxes = self.taxes_id.compute_all(self.new_unit_price, self.currency_id, self.units)
        lst = []
        sale_lst = []
        if taxes:
            for val in taxes['taxes']:
                lst.append(val['amount'])
            tax_amt = sum(lst)
        self.tax_amt = tax_amt

        if sale_taxes:
            for sale_val in sale_taxes['taxes']:
                sale_lst.append(sale_val['amount'])
            sale_tax_amt = sum(sale_lst)
        self.sale_tax_amt = sale_tax_amt
        final_amount = final_amount + tax_amt
        sale_final_amount = sale_final_amount + sale_tax_amt

        # Code starts to calculate currency values for final amount
        # if currency then convert final amount to base currency
        # if to_currency selected then calculated from currency to to_currency - final amt
        company = self.env.company
        from_currency = self.currency_id
        to_currency_id = self.to_currency_id
        base_currency = company.currency_id
        from_today_rate = 0

        if from_currency:
            from_currency_value = from_currency._convert(
                final_amount, base_currency, company, fields.Date.today(), round=False)

            sale_from_currency_value = from_currency._convert(
                sale_final_amount, base_currency, company, fields.Date.today(), round=False)
            self.final_amount = from_currency_value
            self.sale_final_amount = sale_from_currency_value
            if self.unit_price:
                self.company_currency_total = from_currency_value
            if self.new_unit_price:
                self.sale_company_currency_tot = sale_from_currency_value
            from_today_rate = from_currency._convert(
                1, base_currency, company, fields.Date.today(), round=False)
        if to_currency_id:
            to_currency_value_2 = base_currency._convert(
                self.final_amount, to_currency_id, company, fields.Date.today(), round=False)
            sale_to_currency_value_2 = base_currency._convert(
                self.sale_final_amount, to_currency_id, company, fields.Date.today(), round=False)
            self.final_amount = to_currency_value_2
            self.sale_final_amount = sale_to_currency_value_2
            today_rate = base_currency._convert(
                from_today_rate, to_currency_id, company, fields.Date.today(), round=False)
            self.today_exchange_rate = today_rate
