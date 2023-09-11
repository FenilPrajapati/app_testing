# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
import json
import requests


class FacilityCodeWiz(models.Model):
    _name = 'facility.code.wiz'
    _description = "Facility Code Wiz"

    country_code = fields.Char('Country Code')
    code_provider = fields.Char('Code Provider')

    def import_facility_code(self):
        api_rec = self.env['api.integration'].search([('name', '=', 'get_facility_code')])[-1]
        if not api_rec:
            raise Warning("API record doesn't exist for 'get_facility_code' process.")
        url = api_rec.url
        payload = {"country_code": self.country_code, "code_provider": self.code_provider}
        data = json.dumps(payload)
        headers = {"x-api-key": api_rec.key}
        response = requests.request("GET", url, headers=headers, data=data)
        print("responseeeeeeeeeeeeeeeeee", response)
        result = response.text
        print("resulttttttttttttttttttt", result)
