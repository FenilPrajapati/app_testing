from odoo import models, fields
import requests
import json


class VesselLocationTrack(models.Model):
    _name = 'vessel.location.track'
    _description = "Vessel Location Track"
    _rec_name = 'job_id'
    _order = 'id desc'

    job_id = fields.Many2one('job', 'Job')
    latitude = fields.Char('Latitude')
    longitude = fields.Char('Longitude')
    timestamp = fields.Char('Timestamp')
    draft = fields.Char('Draft')
    cog = fields.Char('Cog')
    heading = fields.Char('Heading')

    def get_latest_vessel_location_rec(self, job):
        latest_rec = self.search([('job_id', '=', job.id)], order='id desc', limit=1)

        # api_rec = self.env['api.integration'].search([('name', '=', 'vessel_location_track')], order='id desc', limit=1)
        #
        # url = "https://api.searoutes.com/vessel/v2/%s/position" % job.imo_no
        #
        # headers = {
        #     "accept": "application/json",
        #     "x-api-key": api_rec.key
        # }
        #
        # response = requests.get(url, headers=headers)
        #
        # response_data = json.loads(response.content)
        # if response.status_code == 200:
        #     new_coords = response_data[0].get('position', {}).get('geometry').get('coordinates', [])
        #     if len(new_coords) > 1:
        #         if latest_rec.longitude != str(new_coords[0]) or latest_rec.latitude != str(new_coords[1]):
        #             latest_rec = self.create({
        #                 'job_id': job.id,
        #                 'longitude': new_coords[0],
        #                 'latitude': new_coords[1]
        #             })

        return latest_rec

    def get_latest_vessel_location(self, job):
        api_rec = self.env['api.integration'].search([('name', '=', 'vessel_location_track')])[-1]

        url = "%s/%s" % (api_rec.url, job.imo_no)

        params = "URL : %s " % url

        headers = {
            "accept": "application/json",
            "x-api-key": api_rec.key
        }
        job.vessel_location_api_parameters = params
        response = requests.get(url, headers=headers)
        job.vessel_location_api_datetime = fields.Datetime.now()
        try:
            response_data = json.loads(response.content)
            job.vessel_location_api_response = response_data
            if response.status_code == 200:
                new_coords = response_data[0].get('position', {}).get('geometry').get('coordinates', [])
                if len(new_coords) > 1:
                    latest_rec = self.get_latest_vessel_location_rec(job)
                    if latest_rec.longitude != str(new_coords[0]) or latest_rec.latitude != str(new_coords[1]):
                        self.create({
                            'job_id': job.id,
                            'longitude': new_coords[0],
                            'latitude': new_coords[1]
                        })
            else:
                job.allow_import_vessel_location = False
        except:
            job.vessel_location_api_response = response.content
        return True
