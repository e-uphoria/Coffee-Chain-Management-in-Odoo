from odoo import models, fields, api, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.model
    def create_from_requisition(self, requisition):
        """
        Creates a Purchase Order from a given cafe.requisition.
        - If a product has a default vendor, it will use that vendor.
        - Otherwise, it uses a default supplier (configured in system parameter).
        """
        self.ensure_one()  # Ensure single record context
        
        if not requisition.line_ids:
            raise UserError(_("Requisition has no lines."))

        # Determine default supplier
        default_partner_id = self.env['ir.config_parameter'].sudo().get_param('cafe.default_supplier_id')
        if not default_partner_id:
            raise UserError(_("Please configure default supplier for Cafe Requisitions"))

        po_vals = {
            'partner_id': int(default_partner_id),
            'origin': requisition.name,
            'date_order': fields.Datetime.now(),
            'order_line': [],
        }

        # Build order lines
        order_lines = []
        for line in requisition.line_ids:
            if line.requested_qty <= 0:
                continue
            # Use default product supplier if exists
            product_supplierinfo = line.product_id.seller_ids[:1]  # first vendor
            supplier_id = product_supplierinfo.name.id if product_supplierinfo else int(default_partner_id)

            order_line_vals = (0, 0, {
                'product_id': line.product_id.id,
                'name': line.product_id.display_name,
                'product_qty': line.requested_qty,
                'product_uom': line.product_id.uom_id.id,
                'price_unit': line.product_id.standard_price or 0.0,
                'date_planned': requisition.schedule_date,
                'partner_id': supplier_id,
            })
            order_lines.append(order_line_vals)

        po_vals['order_line'] = order_lines

        # Create Purchase Order
        po = self.create(po_vals)
        return po
