from odoo import http,  _
from odoo.http import request
import logging
import json

from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.website.controllers.form import WebsiteForm
_logger = logging.getLogger(__name__)
GROUP_SYSTEM = 'base.group_system'


class CustomerPortal(CustomerPortal, WebsiteForm):

    @http.route('/booking_form', type='http', auth='public', website=True)
    def booking_form(self, **post):
        _logger.info("Starts New Booking Code")
        user_template_recs = False
        user = False
        partner = False
        state_details = request.env['res.country.state'].sudo().search([])
        country_details = request.env['res.country'].sudo().search([])
        move_type_ids = request.env['move.type'].sudo().search([])
        incoterm_details = request.env['account.incoterms'].sudo().search([])
        # container_type_ids = request.env['container.iso.code'].sudo().search([])
        container_type_ids = request.env['shipping.container'].sudo().search([])
        units_details = request.env['uom.uom'].sudo().search([])
        if request.env.user._is_public():
            result = http.redirect_with_hash('/web/login')
        else:
            user = request.env.user
            partner = user.partner_id
            # user_template_recs = request.env['user.templates'].sudo().search(
            #     ['|', ('is_data_template', '=', True), ('user_template_customer_id', '=', partner.ids)])
            result = request.render('base_freightbox.fb_start_booking_form', {
                'partner': partner,
                'user': user,
                # 'user_template_recs': user_template_recs,
                'move_type_ids': move_type_ids,
                'state_details': state_details,
                'country_details': country_details,
                'incoterm_details': incoterm_details,
                'container_type_ids': container_type_ids,
                'units_details': units_details,
            })
        return result

    @http.route('/booking_confirmation', type='http', auth='public', website=True)
    def booking_confirmation(self, **post):
        crm_lead = request.env['crm.lead']
        container_line = request.env['container.line']
        user = request.env.user
        partner = user.partner_id
        state_id = weight_id = volume_id = False
        parent_id = False
        vals = {}
        cargo = ""
        booking_user = False
        lst_partners = []
        lst_partners.append(partner.id)
        if post:
            if 'state_id' in post:
                state = post['state_id']
                if state:
                    state_id = int(post['state_id'])
            if 'book_for_another_company' in post:
                new_user = request.env['res.users'].sudo().create({
                    'name': post['name'],
                    'login': post['email'],
                    'email': post['email'],
                    'groups_id': [(6, 0, [request.env.ref('base.group_portal').id])],
                    'is_shippers': True
                })
                booking_user = new_user
                if new_user and not new_user.partner_id.parent_id:
                    new_parent_id = request.env['res.partner'].sudo().create({
                        'company_type': 'company',
                        'name': post['company'],
                        'street': str(post['street1']) if post['street1'] else '',
                        'street2': str(post['street2']) if post['street2'] else '',
                        'country_id': int(post['country_id']) if post['country_id'] else False,
                        'state_id': state_id,
                        'zip': str(post['zip']) if post['zip'] else '',
                        'contact_type': 'shippers'
                    })
                    new_user.partner_id.parent_id = new_parent_id
                    new_user.partner_id.contact_type = 'shippers'
                lst_partners.append(new_user.partner_id.id)
                partner = new_user.partner_id

            if 'weight_id' in post:
                weight = post['weight_id']
                if weight:
                    weight_id = int(post['weight_id'])
            if 'volume_id' in post:
                volume = post['volume_id']
                if volume:
                    volume_id = int(post['volume_id'])
            if post['company'] and not partner.parent_id:
                parent_id = request.env['res.partner'].sudo().create({
                    'company_type': 'company',
                    'name': post['company'],
                })
                partner.parent_id = parent_id
            if booking_user:
                shiiper_or_ff = booking_user.id
            else:
                shiiper_or_ff = user.id

            nvocc = request.env['ir.config_parameter'].sudo().get_param('freightbox_nvocc.nvocc') or False

            crm_vals = {
                'name': str(post['company']) + ', ' + str(post['cargo_name']) if post['cargo_name'] else '',
                'partner_id': partner.id,
                'email_from': str(post['email']) if post['email'] else '',
                'country_id': int(post['country_id']) if post['country_id'] else False,
                'state_id': state_id,
                'street': str(post['street1']) if post['street1'] else '',
                'street2': str(post['street2']) if post['street2'] else '',
                'zip': str(post['zip']) if post['zip'] else '',
                'phone': str(post['phone']) if post['phone'] else '',
                'weight': float(post['weight']) if post['weight'] else 0.00,
                'volume': float(post['volume']) if post['volume'] else 0.00,
                'move_type': post['move_type_id'],
                'shipment_terms': post['lcl_fcl_id'],
                'incoterm_id': int(post['incoterm_id']) if post['incoterm_id'] else False,
                'weight_uom': weight_id,
                'volume_uom': volume_id,
                'container_type': int(post['container_type']) if post['container_type'] else False,
                'place_of_origin': str(post['place_of_origin']) if post['place_of_origin'] else False,
                'final_port_of_destination': str(post['final_port_of_destination']) if post[
                    'final_port_of_destination'] else False,
                'point_of_stuffing': str(post['point_of_stuffing']) if post['point_of_stuffing'] else False,
                'point_of_destuffing': str(post['point_of_destuffing']) if post['point_of_destuffing'] else False,
                'no_of_expected_container': float(post['no_of_expected_container']) if post[
                    'no_of_expected_container'] else 0.00,
                'expected_date_of_shipment': post['expected_date_of_shipment'],
                'cargo_name': str(post['cargo_name']) if post['cargo_name'] else '',
                'quantity': float(post['quantity']) if post['quantity'] else 0.00,
                'remarks': str(post['remarks']) if post['remarks'] else '',
                'is_freight_box_crm': True,
                'booking_user_id': shiiper_or_ff,
                'company_id': booking_user.company_id.id if booking_user else user.company_id.id,
                # 'is_nvocc' : nvocc,
            }
            # if nvocc:
            #     crm_vals.update({'is_nvocc': nvocc})

            rec_id = crm_lead.sudo().create(crm_vals)
            rec_id._compute_contact_name()

            container_line.sudo().create({
                'inquiry_id': rec_id.id,
                'no_of_expected_container': int(post['no_of_expected_container']) if post.get(
                    'no_of_expected_container', False) else 0,
                'container_type_id': int(post['container_type']) if post.get('container_type', False) else False,
            })
            try:
                track_count = int(post.get('line_count', 0))
            except:
                track_count = 0
            track_count_range = track_count + 1
            for index in range(track_count_range):
                no_of_containers_key = "no_of_expected_container_%s" % index
                container_type_key = "container_type_%s" % index
                if post.get(no_of_containers_key, False) and post.get(container_type_key, False):
                    container_line.sudo().create({
                        'inquiry_id': rec_id.id,
                        'no_of_expected_container': int(post[no_of_containers_key]),
                        'container_type_id': int(post[container_type_key]),
                    })

            # ir_values = request.env['ir.values']
            # field_value = ir_values.get_default('base.config.settings', 'abcde')
            # res_id = request.env['res.config.settings'].sudo().search([('is_nvocc', '=', True)])
            # if res_id:
            #     crm_lead.is_nvocc = True
            has_group_use_lead = request.env.user.has_group('crm.group_use_lead')
            rec_id.write({
                'type': 'lead' if has_group_use_lead else 'opportunity',
            })
            # if 'create_user_template' in post:
            #     user_template_vals = {
            #         'name': str(post['company']) + ', ' + str(post['cargo_name']) if post['cargo_name'] else '',
            #         'user_template_customer_id': [(6, 0, lst_partners)],
            #         'country': int(post['country_id']) if post['country_id'] else False,
            #         'state_region': state_id,
            #         'address_line1': str(post['street1']) if post['street1'] else '',
            #         'address_line2': str(post['street2']) if post['street2'] else '',
            #         'postcode': str(post['zip']) if post['zip'] else '',
            #         'phone': str(post['phone']) if post['phone'] else '',
            #         'email': str(post['email']) if post['email'] else '',
            #         'weight': float(post['weight']) if post['weight'] else 0.00,
            #         'volume': float(post['volume']) if post['volume'] else 0.00,
            #         'move_type': post['move_type_id'],
            #         'shipment_terms': post['lcl_fcl_id'],
            #         'incoterm_id': int(post['incoterm_id']) if post['incoterm_id'] else False,
            #         'weight_uom': weight_id,
            #         'volume_uom': volume_id,
            #         'container_type': int(post['container_type']) if post['container_type'] else False,
            #         'place_of_origin': str(post['place_of_origin']) if post['place_of_origin'] else False,
            #         'final_port_of_destination': str(post['final_port_of_destination']) if post[
            #             'final_port_of_destination'] else False,
            #         # 'point_of_stuffing': str(post['point_of_stuffing']) if post['point_of_stuffing'] else False,
            #         # 'point_of_destuffing': str(post['point_of_destuffing']) if post['point_of_destuffing'] else False,
            #         'no_of_expected_container': float(post['no_of_expected_container']) if post[
            #             'no_of_expected_container'] else 0.00,
            #         'expected_date_of_shipment': post['expected_date_of_shipment'],
            #         'cargo_name': str(post['cargo_name']) if post['cargo_name'] else '',
            #         'quantity': float(post['quantity']) if post['quantity'] else 0.00,
            #         'remarks': str(post['remarks']) if post['remarks'] else '',
            #         'user_template_user_id': user.id,
            #         'user_name': partner.name,
            #         'company_name': partner.parent_id.name,
            #     }
            #     request.env['user.templates'].sudo().create(user_template_vals)
            vals = {'rec_id': rec_id}

        # if post['contract_ref']:
        #     contract_rec = request.env['contract'].sudo().search(
        #         [('contract_ref', '=', post['contract_ref']), ('shipping_line_name', '=', partner.id)])
        #     print("--------------------- contract_rec", contract_rec)
        #     print("------------------------ print", user.name, partner.id, post['contract_ref'])
        #     if contract_rec:
        #         mrg_line = []
        #         charges_line = []
        #         for rec in contract_rec.mrg_line:
        #             print("testing2")
        #             print("------------------------ container_type", int(post['container_type']))
        #             print("rec.container_type.id", rec.container_type.id)
        #             print("rec.container_type.name", rec.container_type.name)
        #             if rec.port_of_origin_id.name == post[
        #                 'place_of_origin'] and rec.final_port_of_destination_id.name == post[
        #                 'final_port_of_destination']:
        #                 print("origin")
        #                 if rec.container_type.id == int(post[
        #                                                     'container_type']) and rec.from_date <= rec_id.expected_date_of_shipment <= rec.to_date:
        #                     print("post['place_of_origin']", post['place_of_origin'])
        #                     print("post['place_of_origin']", post['final_port_of_destination'])
        #                     mrg_line.append({
        #                         'port_of_origin_id': rec.port_of_origin_id.name,
        #                         'final_port_of_destination_id': rec.final_port_of_destination_id.name,
        #                         'container_type': rec.container_type.name,
        #                         'iso_code_id': rec.iso_code_id.code,
        #                         'mrg_charges': rec.mrg_charges,
        #                         'currency_id': rec.currency_id.name
        #                     })
        #                     # contract_rec = contract_rec
        #         for rec in contract_rec.charges_line:
        #             print("testing4")
        #             print("------------------------ container_type", int(post['container_type']))
        #             print("rec.container_type.id", rec.container_type.id)
        #             if rec.container_type.id == int(post['container_type']):
        #                 print("result")
        #                 charges_line.append({
        #                     'container_type': rec.container_type.name,
        #                     'iso_code_id': rec.container_iso_code.code,
        #                     'charges_id': rec.charges_id.name,
        #                     'charges_type': rec.charges_type,
        #                     'prepaid': rec.prepaid,
        #                     'collect': rec.collect,
        #                     'unit_price': rec.unit_price,
        #                     'currency_id': rec.currency_id.name
        #                 })
        #                 # contract_rec = contract_rec
        #                 print("charges_line", charges_line)
        #                 print("contract_rec", contract_rec)
        #
        #         return request.render('freightbox.quote_form', {"contract_rec": contract_rec, "mrg_line": mrg_line,
        #                                                         "charges_line": charges_line})
        #
        # mrg_rec = request.env['minimum.rate'].sudo().search([('port_of_origin_id.name', '=', post['place_of_origin']),
        #                                                      ('final_port_of_destination_id.name', '=',
        #                                                       post['final_port_of_destination']),
        #                                                      ('container_type.id', '=', int(post['container_type'])),
        #                                                      ('from_date', '<=', rec_id.expected_date_of_shipment),
        #                                                      ('to_date', '>=', rec_id.expected_date_of_shipment)])
        # mrg_line = []
        # charges_line = []
        # if mrg_rec:
        #     for rec in mrg_rec:
        #         if rec.charges_id.type_of_charges == 'freight':
        #             print("testing2")
        #             print("------------------------ container_type", int(post['container_type']))
        #             print("rec.container_type.id", rec.container_type.id)
        #             mrg_line.append({
        #                 # 'port_of_origin_id': rec.port_of_origin_id.name,
        #                 # 'final_port_of_destination_id': rec.final_port_of_destination_id.name,
        #                 'container_type': rec.container_type.name,
        #                 'iso_code_id': rec.iso_code_id.code,
        #                 'charges_id': rec.charges_id.name,
        #                 'prepaid': rec.prepaid,
        #                 'collect': rec.collect,
        #                 'mrg_charges': rec.mrg_charges,
        #                 'currency_id': rec.currency_id.name
        #             })
        #         elif rec.charges_id.type_of_charges != 'freight':
        #             charges_line.append({
        #                 'container_type': rec.container_type.name,
        #                 'iso_code_id': rec.iso_code_id.code,
        #                 'charges_id': rec.charges_id.name,
        #                 # 'charges_type' : rec.charges_type,
        #                 'prepaid': rec.prepaid,
        #                 'collect': rec.collect,
        #                 'unit_price': rec.mrg_charges,
        #                 'currency_id': rec.currency_id.name
        #             })
        #
        #             mrg_rec = mrg_rec
        #     return request.render('freightbox.mrg_form', {"rec_id": rec_id, "mrg_rec": mrg_rec, "mrg_line": mrg_line,
        #                                                   "charges_line": charges_line})
        # else:
        #     return request.render('freightbox.no_mrg_charges', {"mrg_rec": mrg_rec})

            # if mrg_line and contract_rec:
            #     return request.render('freightbox.mrg_contract_form', {"mrg_rec":mrg_rec,"mrg_line":mrg_line,"contract_rec":contract_rec})
            # elif mrg_line:
            #     return request.render('freightbox.mrg_form', {"mrg_rec":mrg_rec,"mrg_line":mrg_line})
            # else:
            #     return request.render('freightbox.no_mrg_charges', {"mrg_rec":mrg_rec})

        # contract_rec = request.env['contract'].sudo().search([('contract_ref', '=', post['contract_ref']), ('shipping_line_name', '=', partner.id)])

        return request.render('base_freightbox.thankyou_page_for_customer', vals)

    @http.route(['/thank-subscribe/<int:rec_id>/<int:partner_id>'], type='http', auth="public", website=True)
    def thanks_subscribe_for_inquiry(self, rec_id, partner_id, access_token=None, **kw):
        partner_rec = request.env['res.partner'].sudo().browse(partner_id)
        partner_rec.user_subscribed = True
        return request.render('base_freightbox.fb_subsciption_accepted')
