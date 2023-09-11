from odoo import fields, models, api, _
import hashlib


class InheritResUsers(models.Model):
    _inherit = 'res.users'

    is_shippers = fields.Boolean(string="Is Shippers")
    is_consignees = fields.Boolean(string="Is Consignees")
    sales_rights_str = fields.Char("Sales Right", compute="get_sales_rights")
    invoicing_rights_str = fields.Char("Invoicing Right", compute="get_invoicing_rights")
    inventory_rights_str = fields.Char("Inventory Right", compute="get_inventory_rights")
    purchase_rights_str = fields.Char("Purchase Right", compute="get_purchase_rights")
    website_rights_str = fields.Char("Website Right", compute="get_website_rights")
    administration_rights_str = fields.Char("Administration Right", compute="get_administration_rights")
    ship_my_box_rights_str = fields.Char("ShipMyBox Right", compute="get_ship_my_box_rights")
    print_signature = fields.Char( string="Print Singnature",
                                   copy=False,
                                   help="This signature will be required for Shipment Information Documents.")
    allow_print_without_signature = fields.Boolean("Allow Print Without Signature", default=False)

    def check_signature(self, signature):
        sign_match = False
        try:
            hash_object = hashlib.sha256()
            hash_object.update(signature.encode())
            encrypted_sign = hash_object.hexdigest()
            print("---------------------encrypted_sign",encrypted_sign)
            if encrypted_sign == self.print_signature:
                sign_match = True

        except Exception:
            return False

        return sign_match

    def open_record_from_kanban(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'res.users',
            'res_id': self.id,
            'view_mode': 'form',
            'view_id': self.env.ref('base.view_users_form').id,
            'target': 'current',
        }

    def get_ship_my_box_rights(self):
        for record in self:
            if record.has_group('freightbox.group_shipmybox_manager'):
                record.ship_my_box_rights_str = "Administrator"
            elif record.has_group('freightbox.group_shipmybox_user'):
                record.ship_my_box_rights_str = "User - All Documents"
            else:
                record.ship_my_box_rights_str = "N/A"

    def get_sales_rights(self):
        for record in self:
            if record.has_group('sales_team.group_sale_manager'):
                record.sales_rights_str = "Administrator"
            elif record.has_group('sales_team.group_sale_salesman_all_leads'):
                record.sales_rights_str = "User - All Documents"
            elif record.has_group('sales_team.group_sale_salesman'):
                record.sales_rights_str = "User - Own Documents Only"
            else:
                record.sales_rights_str = "N/A"

    def get_invoicing_rights(self):
        for record in self:
            if record.has_group('account.group_account_manager'):
                record.invoicing_rights_str = "Billing Administrator"
            elif record.has_group('account.group_account_invoice'):
                record.invoicing_rights_str = "Billing"
            else:
                record.invoicing_rights_str = "N/A"

    def get_inventory_rights(self):
        for record in self:
            if record.has_group('stock.group_stock_manager'):
                record.inventory_rights_str = "Administrator"
            elif record.has_group('stock.group_stock_user'):
                record.inventory_rights_str = "User"
            else:
                record.inventory_rights_str = "N/A"

    def get_purchase_rights(self):
        for record in self:
            if record.has_group('purchase.group_purchase_manager'):
                record.purchase_rights_str = "Administrator"
            elif record.has_group('purchase.group_purchase_user'):
                record.purchase_rights_str = "User"
            else:
                record.purchase_rights_str = "N/A"

    def get_website_rights(self):
        for record in self:
            if record.has_group('website.group_website_designer'):
                record.website_rights_str = "Editor and Designer"
            elif record.has_group('website.group_website_publisher'):
                record.website_rights_str = "Restricted Editor"
            else:
                record.website_rights_str = "None"

    def get_administration_rights(self):
        for record in self:
            if record.has_group('base.group_system'):
                record.administration_rights_str = "Settings"
            elif record.has_group('base.group_erp_manager'):
                record.administration_rights_str = "Access Rights"
            else:
                record.administration_rights_str = "N/A"
    