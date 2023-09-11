from odoo import models, fields, _
from odoo.exceptions import UserError
import base64
from io import BytesIO
import xlrd


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
