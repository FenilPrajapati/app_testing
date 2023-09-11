from odoo import http
from odoo.http import request
from werkzeug.utils import redirect
from io import BytesIO
from odoo.addons.web.controllers.main import ReportController
import base64

class BolDownloadController(http.Controller):
    @http.route('/pdf/<int:bol_id>', type='http', auth='user')
    def download_report(self, bol_id, **kwargs):
        # Retrieve the record containing the binary field
        record = request.env['bill.of.lading'].browse(bol_id)
        iso_pdf = request.env['ir.actions.report'].with_context(force_report_rendering=True)._render_qweb_pdf('freightbox.action_report_prepare_bill_of_lading_document', res_ids=record.id)
        data = base64.b64encode(iso_pdf[0])
        bol_pdf_data = base64.b64decode(data)

        buffer = BytesIO(bol_pdf_data)

        http_response = request.make_response(buffer.getvalue(),
                                              headers=[('Content-Type', 'application/pdf')])
        file_name = "bol_%s.pdf" % bol_id

        http_response.headers.add('Content-Disposition', 'attachment', filename=file_name)

        return http_response