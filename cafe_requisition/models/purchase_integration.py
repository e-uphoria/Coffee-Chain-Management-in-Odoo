from odoo import api, models, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.model
    def create_from_requisition(self, requisition):
        if requisition.state != 'approve':
            raise UserError(_("Only approved requisitions can generate purchase orders."))

        lines = []
        for line in requisition.line_ids:
            if line.requested_qty <= 0:
                continue
            lines.append((0, 0, {
                'product_id': line.product_id.id,
                'name': line.product_id.display_name,
                'product_qty': line.requested_qty,
                'product_uom': line.product_id.uom_id.id,
                'price_unit': line.product_id.standard_price,
            }))

        po_vals = {
            'partner_id': requisition.outlet_location_id.id,  # map to supplier if needed
            'origin': requisition.name,
            'order_line': lines,
        }
        return self.create(po_vals)
