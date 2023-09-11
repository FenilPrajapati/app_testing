# -*- coding: utf-8 -*-
import base64
import os
from odoo.modules.module import get_module_resource
from odoo import models, _
from odoo.tools.mimetypes import guess_mimetype


class ResCompany(models.Model):
    _inherit = "res.company"

    # def write(self, vals):
    #     res = super(ResCompany, self).write(vals)
    #     if vals.get('logo'):
    #         mimetype = guess_mimetype(base64.b64decode(vals['logo']))
    #         file_path = os.path.dirname(__file__)
    #         if mimetype == 'image/png':
    #             file_path += "/../static/src/img/" + str('powerpbox') + ".png"
    #         elif mimetype == 'image/jpeg':
    #             file_path += "/../static/src/img/" + str('powerpbox') + ".jpeg"
    #         if file_path:
    #             with open(file_path, "wb") as imgFile:
    #                 imgFile.write(base64.b64decode(vals['logo']))
    #     return res