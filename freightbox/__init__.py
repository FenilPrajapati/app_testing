from . import controllers
from . import models
from . import wizard
from odoo import api, SUPERUSER_ID
from odoo.exceptions import ValidationError
# from odoo.http import request
import requests
import json
import socket


def create_api_integration(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    hostname = socket.gethostname()
    dbuuid = env['ir.config_parameter'].sudo().get_param('database.uuid')
    username = hostname + '_' + dbuuid
    data = {
        "user_name": username,
        "client_db": dbuuid,
        "freightbox_dbname": env.cr.dbname,
        "freightbox_db_username": env.user.name,
        "freightbox_active": True,
        "is_freightbox_user": True
    }
    api_rec = env['api.integration'].search([('name', '=', 'freightbox_installed_user')])[-1]
    if not api_rec:
        raise ValidationError("API Record does not exist for 'freightbox_installed_user'.")
    res = requests.post(api_rec.url,data=json.dumps(data))
    # print("RESSSSSSSSSSSSSSSSSSSSSSS", res)
    # req = requests.delete("http://mother.powerpbox.org:3000/api/v1/users/{}".format(hostname), json=data)
    # response = requests.post("http://mother.powerpbox.org:3000/api/v1/users", json=data)


def uninstall_hook(cr, registry):
    hostname = socket.gethostname()
    env = api.Environment(cr, SUPERUSER_ID, {})
    data = {
        "user_name": hostname,
        "freightbox_dbname": env.cr.dbname,
        "freightbox_db_username": env.user.name,
        "freightbox_active": False,
    }
    api_rec = env['api.integration'].search([('name', '=', 'freightbox_installed_user')])[-1]
    if not api_rec:
        raise ValidationError("API Record does not exist for 'freightbox_installed_user'.")
    res = requests.post(api_rec.url, data=json.dumps(data))
    # print("RESSSSSSSSSSSSSSSSSSSSSSS", res)
    # print("response::", response.text)
    # print("response::", response.status_code)
