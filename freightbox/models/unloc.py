from odoo import models, fields, _, api
from odoo.exceptions import UserError
import base64
from io import BytesIO
import xlrd


class ResCountry(models.Model):
    _inherit = 'res.country'

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "{} ({})".format(record.name, record.code)))
        return result


class Unloc(models.Model):
    _name = 'unloc'
    _description = "UNLOC"
    _rec_name = "unloc_code"

    unloc_code = fields.Char("UNLOC Code")
    unloc_name = fields.Char("Name")
    country_id = fields.Many2one('res.country', string='Country')
    unloc_file = fields.Binary('UNLOC Upload')
    unloc_fname = fields.Char('UNLOC', size=64)

    def button_import_unloc(self):
        data_decode = self.unloc_file
        location_obj = self.env['unloc']
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
            unloc_code = ''
            name = ''
            country_id = False
            if sh.row_values(row)[0]:
                country_code = str(sh.row_values(row)[0])
                if country_code:
                    country_id = self.env['res.country'].search([('code', '=', country_code)])
            if not country_id:
                raise UserError(_('The country "%s" not defined in the database!') % (country_code))
            if sh.row_values(row)[1]:
                unloc_code = sh.row_values(row)[1]
            if sh.row_values(row)[2]:
                name = sh.row_values(row)[2]
            if name and unloc_code:
                self._cr.execute(
                    'insert into unloc (unloc_code,name,country_id) values (%s,%s,%s)',
                    (unloc_code, name, country_id.id))
                self._cr.commit()

        return True

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=None):
        recs = self.search([('country_id', operator, name)] + args, limit=limit)
        return recs.name_get()


class Location(models.Model):
    _name = 'location'
    _description = "Location"

    name = fields.Char("Name")
    country_id = fields.Many2one('res.country', string='Country')
    unloc_id = fields.Many2one('unloc', "UNLOC")
    state_id = fields.Many2one('res.country.state', string='Subdivision')
    function = fields.Char("Function")
    status = fields.Char("Status")
    date = fields.Date("Date")
    iata = fields.Char("IATA")
    latitude = fields.Char("LAT")
    longitude = fields.Char("LONG")
    remarks = fields.Char("Remarks")
    location_file = fields.Binary('Location Upload')
    location_fname = fields.Char('Location', size=64)

    def name_get(self):
        result = []
        for record in self:
            result.append((record.id, "{}{}".format(record.country_id.code, record.unloc_id.unloc_code)))
        return result

    @api.onchange('unloc_id')
    def _onchange_unloc_id(self):
        result = {}
        if not self.unloc_id:
            self.name = False
            self.country_id = False
            self.state_id = False
        if self.unloc_id:
            self.name = self.unloc_id.unloc_name
            self.country_id = self.unloc_id.country_id.id

    def import_location(self):
        data_decode = self.location_file
        iso_code_obj = self.env['unloc']
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
