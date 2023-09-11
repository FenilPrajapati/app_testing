from odoo import http,  _
from odoo.http import request
import logging
import json

from odoo.addons.portal.controllers.portal import CustomerPortal
from odoo.addons.website.controllers.form import WebsiteForm
_logger = logging.getLogger(__name__)
GROUP_SYSTEM = 'base.group_system'
from odoo.exceptions import ValidationError,UserError


class CustomerPortal(CustomerPortal, WebsiteForm):

    @http.route('/dashboard', type='http', auth='public', website=True)
    def freight_dashboard(self, **post):
        purchase_order = request.env['purchase.order']
        sale_order = request.env['sale.order']
        vals = {}
        user = request.env.user
        user_logged = True
        inquiry_count = 0
        rc_count = 0
        po_count = 0
        draft_po_count = 0
        sq_count = 0
        so_count = 0
        draft_so_count = 0
        job_count = 0
        transport_count = 0
        draft_si_count = 0        
        open_si_count = 0
        update_si_count = 0
        approve_si_count = 0
        draft_bol_count = 0
        update_bol_count = 0
        switch_bol_count = 0
        amend_bol_count = 0
        hold_bol_count = 0
        issue_bol_count = 0
        surrender_bol_count = 0
        release_count = 0
        if user.name == 'Public user':
            user_logged = False
        if user.has_group(GROUP_SYSTEM):
            inquiry_rec = request.env['crm.lead'].sudo().search([('is_freight_box_crm', '=', True)])
            inquiry_count = len(inquiry_rec)

            rc_rec = request.env['request.for.quote'].sudo().search([])
            rc_count = len(rc_rec)

            po_rec = purchase_order.sudo().search([('is_freight_box_po', '=', True), ('state', '!=', 'draft')])
            po_count = len(po_rec)

            draft_po_rec = purchase_order.sudo().search([('is_freight_box_po', '=', True), ('state', '=', 'draft')])
            draft_po_count = len(draft_po_rec)

            sq_rec = request.env['shipment.quote'].sudo().search([])
            sq_count = len(sq_rec)

            so_rec = sale_order.sudo().search([('is_freight_box_so', '=', True), ('state', '!=', 'draft')])
            so_count = len(so_rec)

            draft_so_rec = sale_order.sudo().search([('is_freight_box_so', '=', True), ('state', '=', 'draft')])
            draft_so_count = len(draft_so_rec)

            job_rec = request.env['job'].sudo().search([])
            job_count = len(job_rec)

            transport_rec = request.env['transport'].sudo().search([])
            transport_count = len(transport_rec)

            draft_si_rec = request.env['shipping.instruction'].sudo().search([('state', '=', 'draft')])
            draft_si_count = len(draft_si_rec)

            open_si_rec = request.env['shipping.instruction'].sudo().search([('state', '=', 'open')])
            open_si_count = len(open_si_rec)

            update_si_rec = request.env['shipping.instruction'].sudo().search([('state', '=', 'updated')])
            update_si_count = len(update_si_rec)

            approve_si_rec = request.env['shipping.instruction'].sudo().search([('state', '=', 'accepted')])
            approve_si_count = len(approve_si_rec)

            draft_bol_rec = request.env['bill.of.lading'].sudo().search([('state', '=', 'draft')])
            draft_bol_count = len(draft_bol_rec)

            update_bol_rec = request.env['bill.of.lading'].sudo().search([('state', '=', 'update')])
            update_bol_count = len(update_bol_rec)

            switch_bol_rec = request.env['bill.of.lading'].sudo().search([('state', '=', 'switch')])
            switch_bol_count = len(switch_bol_rec)

            amend_bol_rec = request.env['bill.of.lading'].sudo().search([('state', '=', 'amend')])
            amend_bol_count = len(amend_bol_rec)

            hold_bol_rec = request.env['bill.of.lading'].sudo().search([('state', '=', 'hold')])
            hold_bol_count = len(hold_bol_rec)

            issue_bol_rec = request.env['bill.of.lading'].sudo().search([('state', '=', 'approve')])
            issue_bol_count = len(issue_bol_rec)

            surrender_bol_rec = request.env['bill.of.lading'].sudo().search([('state', '=', 'done')])
            surrender_bol_count = len(surrender_bol_rec)

            release_rec = request.env['job'].sudo().search([('state', '=', 'cargo_released')])
            release_count = len(release_rec)
        if user.has_group('base.group_portal'):
            inquiry_rec = request.env['crm.lead'].sudo().search([('is_freight_box_crm', '=', True), ('booking_user_id', '=', user.id)])
            inquiry_count = len(inquiry_rec)

            rc_rec = request.env['request.for.quote'].sudo().search([('booking_user_id', '=', user.id)])
            rc_count = len(rc_rec)

            draft_po_rec = purchase_order.sudo().search([('is_freight_box_po', '=', True), ('state', '=', 'draft'), ('booking_user_id', '=', user.id)])
            draft_po_count = len(draft_po_rec)

            po_rec = purchase_order.sudo().search([('is_freight_box_po', '=', True), ('state', '!=', 'draft'), ('booking_user_id', '=', user.id)])
            po_count = len(po_rec)

            sq_rec = request.env['shipment.quote'].sudo().search([('booking_user_id', '=', user.id)])
            sq_count = len(sq_rec)

            so_rec = sale_order.sudo().search([('is_freight_box_so', '=', True), ('state', '!=', 'draft'), ('booking_user_id', '=', user.id)])
            so_count = len(so_rec)

            draft_so_rec = sale_order.sudo().search([('is_freight_box_so', '=', True), ('state', '=', 'draft'), ('booking_user_id', '=', user.id)])
            draft_so_count = len(draft_so_rec)

            job_rec = request.env['job'].sudo().search([('booking_user_id', '=', user.id)])
            job_count = len(job_rec)

            transport_rec = request.env['transport'].sudo().search([('booking_user_id', '=', user.id)])
            transport_count = len(transport_rec)

            draft_si_rec = request.env['shipping.instruction'].sudo().search([('state', '=', 'draft'), ('booking_user_id', '=', user.id)])
            draft_si_count = len(draft_si_rec)

            open_si_rec = request.env['shipping.instruction'].sudo().search([('state', '=', 'open'), ('booking_user_id', '=', user.id)])
            open_si_count = len(open_si_rec)

            update_si_rec = request.env['shipping.instruction'].sudo().search([('state', '=', 'updated'), ('booking_user_id', '=', user.id)])
            update_si_count = len(update_si_rec)

            approve_si_rec = request.env['shipping.instruction'].sudo().search([('state', '=', 'accepted'), ('booking_user_id', '=', user.id)])
            approve_si_count = len(approve_si_rec)

            draft_bol_rec = request.env['bill.of.lading'].sudo().search([('state', '=', 'draft'), ('booking_user_id', '=', user.id)])
            draft_bol_count = len(draft_bol_rec)

            update_bol_rec = request.env['bill.of.lading'].sudo().search([('state', '=', 'update'), ('booking_user_id', '=', user.id)])
            update_bol_count = len(update_bol_rec)

            switch_bol_rec = request.env['bill.of.lading'].sudo().search([('state', '=', 'switch'), ('booking_user_id', '=', user.id)])
            switch_bol_count = len(switch_bol_rec)

            amend_bol_rec = request.env['bill.of.lading'].sudo().search([('state', '=', 'amend'), ('booking_user_id', '=', user.id)])
            amend_bol_count = len(amend_bol_rec)

            hold_bol_rec = request.env['bill.of.lading'].sudo().search([('state', '=', 'hold'), ('booking_user_id', '=', user.id)])
            hold_bol_count = len(hold_bol_rec)

            issue_bol_rec = request.env['bill.of.lading'].sudo().search([('state', '=', 'approve'), ('booking_user_id', '=', user.id)])
            issue_bol_count = len(issue_bol_rec)

            surrender_bol_rec = request.env['bill.of.lading'].sudo().search([('state', '=', 'done'), ('booking_user_id', '=', user.id)])
            surrender_bol_count = len(surrender_bol_rec)

            release_rec = request.env['job'].sudo().search([('state', '=', 'cargo_released'), ('booking_user_id', '=', user.id)])
            release_count = len(release_rec)
        vals.update({
            'inquiry_count': inquiry_count,
            'rc_count': rc_count,
            'po_count': po_count,
            'draft_po_count': draft_po_count,
            'sq_count': sq_count,
            'so_count': so_count,
            'draft_so_count': draft_so_count,
            'job_count': job_count,
            'transport_count': transport_count,
            'draft_si_count': draft_si_count,
            'open_si_count': open_si_count,
            'update_si_count': update_si_count,
            'approve_si_count': approve_si_count,
            'draft_bol_count': draft_bol_count,
            'switch_bol_count': switch_bol_count,
            'update_bol_count': update_bol_count,
            'amend_bol_count': amend_bol_count,
            'hold_bol_count': hold_bol_count,
            'issue_bol_count': issue_bol_count,
            'surrender_bol_count': surrender_bol_count,
            'release_count': release_count,
            'user_logged': user_logged,

        })
        res = request.render('freightbox.freight_box_dashboard', vals)
        return res

    @http.route(['/user_template_values'], type='json', auth="public", method=['POST'], website=True)
    def user_template_values(self, user_template, **kwargs):
        user_templates = request.env['user.templates']
        user_template_rec = user_templates.sudo().search([('id', '=', user_template)])
        user_template_rec_values = {
            'sb_company_name': user_template_rec.company_name,
            'sb_name': user_template_rec.user_name,
            'sb_street1': user_template_rec.address_line1,
            'sb_street2': user_template_rec.address_line2,
            'country_id': user_template_rec.country.id,
            'sb_state_id': user_template_rec.state_region.id,
            'sb_zip': user_template_rec.postcode,
            'sb_email': user_template_rec.email,
            'sb_phone': user_template_rec.phone,
            'sb_cargo_name': user_template_rec.cargo_name,
            'sb_quantity': user_template_rec.quantity,
            'sb_weight': user_template_rec.weight,
            'sb_volume': user_template_rec.volume,
            'sb_weight_id': user_template_rec.weight_uom.id,
            'sb_volume_id': user_template_rec.volume_uom.id,
            'move_type_id': user_template_rec.move_type.id,
            'incoterm_id': user_template_rec.incoterm_id.id,
            'sb_place_of_origin': user_template_rec.place_of_origin,
            'sb_final_port_of_destination': user_template_rec.final_port_of_destination,
            'sb_point_of_stuffing': user_template_rec.point_of_stuffing.name if user_template_rec.point_of_stuffing else '',
            'sb_point_of_destuffing': user_template_rec.point_of_destuffing.name if user_template_rec.point_of_destuffing else '',
            'sb_no_of_expected_container': user_template_rec.no_of_expected_container,
            'container_type': user_template_rec.container_type.id,
            'sb_expected_date_of_shipment': user_template_rec.expected_date_of_shipment,
            'sb_remarks': user_template_rec.remarks,
        }
        return user_template_rec_values

    @http.route('/start_booking', type='http', auth='public', website=True)
    def start_booking(self, **post):
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
            user_template_recs = request.env['user.templates'].sudo().search(
                ['|', ('is_data_template', '=', True), ('user_template_customer_id', '=', partner.ids)])
            result = request.render('freightbox.start_booking_form', {
                'partner': partner,
                'user': user,
                'user_template_recs': user_template_recs,
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
        cargo_plus_obj = request.env['cargo.plus']
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
                    'is_shippers' : True
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
                        'contact_type' : 'shippers'
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
                'company_id' : booking_user.company_id.id if booking_user else user.company_id.id,
                # 'is_nvocc' : nvocc,
            }
            if nvocc:
                crm_vals.update({'is_nvocc' : nvocc})

            rec_id = crm_lead.sudo().create(crm_vals)
            rec_id._compute_contact_name()

            cargo_plus_obj.sudo().create({
                'inquiry_id': rec_id.id,
                'no_of_expected_container': int(post['no_of_expected_container']) if post.get('no_of_expected_container', False) else 0,
                'container_type_id': int(post['container_type']) if post.get('container_type', False) else False,
                'cargo_description': post['cargo_name'],
                'quantity': float(post['quantity']) if post.get('quantity', False) else 0.0,
                'weight': float(post['weight']) if post.get('weight', False) else 0.0,
                'volume': float(post['volume']) if post.get('volume', False) else 0.0,
                'weight_uom': int(post['weight_id']) if post.get('weight_id', False) else False,
                'volume_uom': int(post['volume_id']) if post.get('volume_id', False) else False,
                'move_type': int(post['move_type_id']) if post.get('move_type_id', False) else False,
                'incoterm_id': int(post['incoterm_id']) if post.get('incoterm_id', False) else False,
            })
            try:
                track_count = int(post.get('line_count', 0))
            except:
                track_count = 0
            track_count_range = track_count + 1
            for index in range(track_count_range):
                no_of_containers_key = "no_of_expected_container_%s" % index
                container_type_key = "container_type_%s" % index
                cargo_description_key = "cargo_description_%s" % index
                quantity_key = "quantity_%s" % index
                weight_key = "weight_%s" % index
                volume_key = "volume_%s" % index
                weight_uom_key = "weight_id_%s" % index
                volume_uom_key = "volume_id_%s" % index
                move_type_key = "move_type_id_%s" % index
                incoterm_key = "incoterm_id_%s" % index
                if post.get(no_of_containers_key, False) and post.get(container_type_key, False):
                    cargo_plus_obj.sudo().create({
                        'inquiry_id': rec_id.id,
                        'no_of_expected_container': int(post[no_of_containers_key]),
                        'container_type_id': int(post[container_type_key]),
                        'cargo_description': post[cargo_description_key],
                        'quantity': float(post[quantity_key]),
                        'weight': float(post[weight_key]),
                        'volume': float(post[volume_key]),
                        'weight_uom': float(post[weight_uom_key]),
                        'volume_uom': float(post[volume_uom_key]),
                        'move_type': float(post[move_type_key]),
                        'incoterm_id': float(post[incoterm_key]),
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
            if 'create_user_template' in post:
                user_template_vals = {
                    'name': str(post['company']) + ', ' + str(post['cargo_name']) if post['cargo_name'] else '',
                    'user_template_customer_id': [(6, 0, lst_partners)],
                    'country': int(post['country_id']) if post['country_id'] else False,
                    'state_region': state_id,
                    'address_line1': str(post['street1']) if post['street1'] else '',
                    'address_line2': str(post['street2']) if post['street2'] else '',
                    'postcode': str(post['zip']) if post['zip'] else '',
                    'phone': str(post['phone']) if post['phone'] else '',
                    'email': str(post['email']) if post['email'] else '',
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
                    # 'point_of_stuffing': str(post['point_of_stuffing']) if post['point_of_stuffing'] else False,
                    # 'point_of_destuffing': str(post['point_of_destuffing']) if post['point_of_destuffing'] else False,
                    'no_of_expected_container': float(post['no_of_expected_container']) if post[
                        'no_of_expected_container'] else 0.00,
                    'expected_date_of_shipment': post['expected_date_of_shipment'],
                    'cargo_name': str(post['cargo_name']) if post['cargo_name'] else '',
                    'quantity': float(post['quantity']) if post['quantity'] else 0.00,
                    'remarks': str(post['remarks']) if post['remarks'] else '',
                    'user_template_user_id': user.id,
                    'user_name': partner.name,
                    'company_name': partner.parent_id.name,
                }
                request.env['user.templates'].sudo().create(user_template_vals)
            vals = {'rec_id': rec_id}

        if post['contract_ref']:
            contract_rec = request.env['contract'].sudo().search([('contract_ref', '=', post['contract_ref']), ('shipping_line_name', '=', partner.id)])
            print("--------------------- contract_rec",contract_rec)
            print("------------------------ print",user.name,partner.id,post['contract_ref'])
            if contract_rec:
                mrg_line = []
                charges_line = []
                for rec in contract_rec.mrg_line:
                    print("testing2")
                    print("------------------------ container_type",int(post['container_type']))
                    print("rec.container_type.id",rec.container_type.id)
                    print("rec.container_type.name",rec.container_type.name)
                    if rec.port_of_origin_id.name == post['place_of_origin'] and rec.final_port_of_destination_id.name == post['final_port_of_destination']:
                        print("origin")
                        if rec.container_type.id == int(post['container_type']) and rec.from_date <= rec_id.expected_date_of_shipment <= rec.to_date:
                            print("post['place_of_origin']",post['place_of_origin'])
                            print("post['place_of_origin']",post['final_port_of_destination'])
                            mrg_line.append({
                                'port_of_origin_id': rec.port_of_origin_id.name,
                                'final_port_of_destination_id': rec.final_port_of_destination_id.name,
                                'container_type': rec.container_type.name,
                                'iso_code_id': rec.iso_code_id.code,
                                'mrg_charges' : rec.mrg_charges,
                                'currency_id':rec.currency_id.name
                            })
                            # contract_rec = contract_rec
                for rec in contract_rec.charges_line:
                    print("testing4")
                    print("------------------------ container_type",int(post['container_type']))
                    print("rec.container_type.id",rec.container_type.id)
                    if rec.container_type.id == int(post['container_type']):
                        print("result")
                        charges_line.append({
                            'container_type': rec.container_type.name,
                            'iso_code_id': rec.container_iso_code.code,
                            'charges_id': rec.charges_id.name,
                            'charges_type' : rec.charges_type,
                            'prepaid' : rec.prepaid,
                            'collect' : rec.collect,
                            'unit_price' : rec.unit_price,
                            'currency_id':rec.currency_id.name
                        })
                        # contract_rec = contract_rec
                        print("charges_line",charges_line)
                        print("contract_rec",contract_rec)

                return request.render('freightbox.quote_form', {"contract_rec":contract_rec,"mrg_line":mrg_line,"charges_line":charges_line})
        
        mrg_rec = request.env['minimum.rate'].sudo().search([('port_of_origin_id.name', '=', post['place_of_origin']), 
        ('final_port_of_destination_id.name', '=', post['final_port_of_destination']), 
        ('container_type.id', '=', int(post['container_type'])), 
        ('from_date', '<=', rec_id.expected_date_of_shipment), 
        ('to_date', '>=', rec_id.expected_date_of_shipment)])
        mrg_line = []
        charges_line = []
        if mrg_rec:
            for rec in mrg_rec:
                if rec.charges_id.type_of_charges == 'freight':
                    print("testing2")
                    print("------------------------ container_type",int(post['container_type']))
                    print("rec.container_type.id",rec.container_type.id)
                    mrg_line.append({
                        # 'port_of_origin_id': rec.port_of_origin_id.name,
                        # 'final_port_of_destination_id': rec.final_port_of_destination_id.name,
                        'container_type': rec.container_type.name,
                        'iso_code_id': rec.iso_code_id.code,
                        'charges_id': rec.charges_id.name,
                        'prepaid' : rec.prepaid,
                        'collect' : rec.collect,
                        'mrg_charges' : rec.mrg_charges,
                        'currency_id':rec.currency_id.name
                    })
                elif rec.charges_id.type_of_charges != 'freight':
                    charges_line.append({
                        'container_type': rec.container_type.name,
                        'iso_code_id': rec.iso_code_id.code,
                        'charges_id': rec.charges_id.name,
                        # 'charges_type' : rec.charges_type,
                        'prepaid' : rec.prepaid,
                        'collect' : rec.collect,
                        'unit_price' : rec.mrg_charges,
                        'currency_id':rec.currency_id.name
                    })

                    mrg_rec = mrg_rec
            mrg_form_req_data = self.get_mrg_form_res_data(rec_id, mrg_rec, mrg_line, charges_line, post)
            return request.render('freightbox.mrg_form', mrg_form_req_data)
        else:
            return self.get_mrg_charges_res_data(mrg_rec, rec_id, post)


            # if mrg_line and contract_rec:
            #     return request.render('freightbox.mrg_contract_form', {"mrg_rec":mrg_rec,"mrg_line":mrg_line,"contract_rec":contract_rec})
            # elif mrg_line:
            #     return request.render('freightbox.mrg_form', {"mrg_rec":mrg_rec,"mrg_line":mrg_line})
            # else:
            #     return request.render('freightbox.no_mrg_charges', {"mrg_rec":mrg_rec})

        # contract_rec = request.env['contract'].sudo().search([('contract_ref', '=', post['contract_ref']), ('shipping_line_name', '=', partner.id)])
       

        return request.render('freightbox.thankyou_page_for_customer', vals)

    def get_mrg_form_res_data(self, rec_id, mrg_rec, mrg_line, charges_line, post):
        return {"rec_id": rec_id, "mrg_rec": mrg_rec, "mrg_line": mrg_line, "charges_line": charges_line}

    def get_mrg_charges_res_data(self, rec_id, mrg_rec, post):
        mrg_charges_data = {"mrg_rec": mrg_rec}
        return request.render('freightbox.no_mrg_charges', mrg_charges_data)

    @http.route(['/inquiry_values'], type='json', auth="public", method=['POST'], website=True)
    def inquiry_values(self, inquiry_company_name, inquiry_company_email, **kwargs):
        is_user_registered = False
        user_partner_rec = request.env['res.users'].sudo().search([
            ('login', '=', inquiry_company_email)])
        if user_partner_rec and user_partner_rec.name != inquiry_company_name:
            is_user_registered = True
        return is_user_registered

    @http.route(['/booking/country_infos/<model("res.country"):country>'], type='json', auth="public", methods=['POST'],
                website=True)
    def country_info(self, country, **kw):
        return dict(state_ids=[(st.id, st.name, st.code) for st in country.state_ids])

    @http.route(['/thank-subscribe/<int:rec_id>/<int:partner_id>'], type='http', auth="public", website=True)
    def thanks_subscribe_for_inquiry(self, rec_id, partner_id, access_token=None, **kw):
        partner_rec = request.env['res.partner'].sudo().browse(partner_id)
        partner_rec.user_subscribed = True
        return request.render('freightbox.subsciption_accepted')


    @http.route(['/thank-accept-mrg/<int:rec_id>'], type='http', auth="public", website=True)
    def thanks_accept_mrg(self, rec_id, access_token=None, **kw):
        # sq_rec_accept = request.env['shipment.quote'].sudo().browse(sq_rec)
        # sq_rec_accept.state = "accepted"
        # sq_rec_accept.button_accept()
        return request.render('freightbox.mrg_accepted')

    @http.route(['/thank-reject-mrg/<int:rec_id>'], type='http', auth="public", website=True)
    def thanks_reject_mrg(self, rec_id, access_token=None, **kw):
        # sq_rec_accept = request.env['shipment.quote'].sudo().browse(sq_rec)
        # sq_rec_accept.state = "accepted"
        # sq_rec_accept.button_accept()
        return request.render('freightbox.mrg_rejected')

    @http.route(['/thank-accept-contract/<int:contract_rec>'], type='http', auth="public", website=True)
    def thanks_accept_contract(self, contract_rec, access_token=None, **kw):
        # sq_rec_accept = request.env['shipment.quote'].sudo().browse(sq_rec)
        # sq_rec_accept.state = "accepted"
        # sq_rec_accept.button_accept()
        return request.render('freightbox.contract_accepted')

    @http.route('/get_model_records', type='json', auth='public')
    def get_model_records(self, model_name):
        records = request.env[model_name].search_read([], ['id', 'name'])
        return json.dumps(records)
