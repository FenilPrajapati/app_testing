from odoo import http
from odoo.http import request


class VesselSchedule(http.Controller):

    @http.route('/vessel_schedule', type='http', auth='public', website=True)
    def vessel_schedule(self, **post):
        port_of_origin_ids = request.env['port'].sudo().search([])
        fpod_ids = request.env['port'].sudo().search([])
        r = request.render('freightbox.vessel_schedule', {
            'port_of_origin_ids': port_of_origin_ids,
            'fpod_ids': fpod_ids,
        })
        return r
