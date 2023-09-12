from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
from io import BytesIO
import xlrd
import random



class ProductTemplate(models.Model):
    _inherit = "product.template"
    _order = 'id desc'

    parent_container = fields.Many2one('shipping.container', string="Parent Container")
    is_alias_product = fields.Boolean(string="Is Alias Product")


class ContainerIsoCode(models.Model):
    _name = 'container.iso.code'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Container Iso Code"
    _rec_name = "code"

    code = fields.Char("Code", tracking=True)
    description = fields.Char("Description", tracking=True)
    alias_code = fields.Char("Alias Code", tracking=True)
    container_type_id = fields.Many2one('shipping.container', string="Container Type") # use alias_code
    iso_code_file = fields.Binary('ISO Code Upload', tracking=True)
    iso_code_fname = fields.Char('ISO Code', size=64, tracking=True)

    def import_iso_code(self):
        data_decode = self.iso_code_file
        iso_code_obj = self.env['container.iso.code']
        if not data_decode:
            raise UserError(_('Please Choose The File!'))
        val = base64.decodestring(data_decode)
        fp = BytesIO()
        fp.write(val)
        wb = xlrd.open_workbook(file_contents=fp.getvalue())
        wb.sheet_names()
        sheet_name = wb.sheet_names()
        sh = wb.sheet_by_name(sheet_name[0])
        n_rows = sh.nrows
        for row in range(1, n_rows):
            country_code = ''
            iso_code = ''
            description = ''
            if sh.row_values(row)[0]:
                iso_code = sh.row_values(row)[0]
            if sh.row_values(row)[1]:
                description = sh.row_values(row)[1]
            if iso_code and description:
                iso_code_id = iso_code_obj.sudo().create({
                    'code': iso_code or '',
                    'description': description,
                })
        return True

class ShippingContainers(models.Model):
    _name = 'shipping.container'
    _description = "Shipping Containers"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char("Container Name")
    description = fields.Char("Description")
    # default_location_id = fields.Many2one('stock.location', string='Default Location')

    @api.model
    def create(self, vals):
        result = super(ShippingContainers, self).create(vals)
        if result:
            # create a 10 default sample containers for each shipping containers
            for i in range(0, 10):
                # ===================================================================
                owner_code = "BHAU"
                # Generate a random serial number
                serial_number = ''.join(random.choices('0123456789', k=6))

                # Calculate the check digit
                digits = owner_code + serial_number
                weight_factors = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
                weighted_sum = sum(int(digit, 36) * weight for digit, weight in zip(digits, weight_factors))
                check_digit = (11 - (weighted_sum % 11)) % 11
                # Construct the container number with check digit
                container_number = owner_code + serial_number + str(check_digit)
                # use generate_container_id() to get cont id.
                # ======================================================================
                vals['default_code'] = container_number
                sample_shipping_containers = self.env['product.template'].create({
                    'name': result.name,
                    'default_code': container_number,
                    'type': 'product',
                    'parent_container': result.id,
                    # 'cont_onhand_qty': 1,
                    # 'depot_loc': 5,
                    # 'gate_in': fields.Datetime.now(),
                    # 'is_nvocc_product': True,
                    # 'is_freight_container': True,
                })
                print("sample_shipping_containers", sample_shipping_containers)

            # create a new record in product.template for alias product
            product_id = self.env['product.template'].search(
                [('type', '=', 'service'), ('parent_container', '=', self.id), ('name', '=', result.name)])
            if not product_id:
                # create a new record in product.template table
                alias_product = self.env['product.template'].create({
                    'name': result.name,
                    'type': 'service',
                    'parent_container': result.id,
                    'is_alias_product': True,
                    # 'is_freight_container': True,
                    # 'is_nvocc_product': True
                })
                alias_product.write({'parent_container': result.id})
        return result
