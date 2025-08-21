from odoo import api, fields, models, _
from odoo.exceptions import UserError

class CafeRequisition(models.Model):
    _name = "cafe.requisition"
    _description = "Outlet Requisition"
    _rec_name = "name"

    # Fields
    name = fields.Char(string="Requisition Reference", required=True, copy=False, readonly=True, default="New")
    outlet_id = fields.Many2one("coffee.outlet", string="Outlet", required=True)
    schedule_date = fields.Datetime(string="Scheduled Date", default=fields.Datetime.now)
    state = fields.Selection([
        ("draft", "Draft"),
        ("submit", "Submitted"),
        ("approve", "Approved"),
        ("done", "Done"),
        ("cancel", "Cancelled")
    ], string="Status", default="draft")
    note = fields.Text(string="Note", placeholder="Special instructions")
    line_ids = fields.One2many("cafe.requisition.line", "requisition_id", string="Requisition Lines")

    # Auto-generate sequence for name
    @api.model
    def create(self, vals):
        if vals.get("name", "New") == "New":
            vals["name"] = self.env["ir.sequence"].next_by_code("cafe.requisition") or "New"
        return super().create(vals)

    # State transition methods
    def action_submit(self):
        for req in self:
            if req.state != 'draft':
                raise UserError(_("Only draft requisitions can be submitted."))
            req.state = 'submit'

    def action_approve(self):
        for req in self:
            if req.state != 'submit':
                raise UserError(_("Only submitted requisitions can be approved."))
            req.state = 'approve'

    def action_cancel(self):
        for req in self:
            req.state = 'cancel'

     # Stock transfer
    def action_generate_transfer(self):
        StockMove = self.env["stock.move"]
        StockPicking = self.env["stock.picking"]    
        PickingType = self.env["stock.picking.type"]
        Param = self.env["ir.config_parameter"].sudo()

        # Determine HQ Stock location
        hq_location_id = int(Param.get_param("cafe.hq_location_id") or 0)
        if not hq_location_id:
            wh = self.env["stock.warehouse"].search([], limit=1)
            hq_location_id = wh.lot_stock_id.id if wh else 0
        if not hq_location_id:
            raise UserError(_("Configure HQ Stock Location: system parameter 'cafe.hq_location_id'."))

        picking_type = PickingType.search([("code", "=", "internal")], limit=1)
        if not picking_type:
            raise UserError(_("No Internal Transfer picking type found. Install Inventory app."))

        for req in self:
            if req.state != "approve":
                raise UserError(_("Only approved requisitions can generate transfers."))
            if not req.line_ids:
                raise UserError(_("Add lines to the requisition."))

            picking_vals = {
                "picking_type_id": picking_type.id,
                "origin": req.name,
                "location_id": hq_location_id,
                "location_dest_id": req.outlet_location_id.id,
                "scheduled_date": req.schedule_date,
            }
            picking = StockPicking.create(picking_vals)

            for line in req.line_ids:
                if line.requested_qty <= 0:
                    continue
                StockMove.create({
                    "name": f"{req.name}: {line.product_id.display_name}",
                    "product_id": line.product_id.id,
                    "product_uom": line.product_id.uom_id.id,
                    "product_uom_qty": line.requested_qty,
                    "location_id": hq_location_id,
                    "location_dest_id": req.outlet_location_id.id,
                    "picking_id": picking.id,
                })

            picking.action_confirm()
            picking.action_assign()
            req.state = "done"
        return True

    # Purchase integration
    def action_create_purchase_order(self):
        self.ensure_one()
        PurchaseOrder = self.env["purchase.order"]

        # Default Supplier from system parameter
        supplier_id = int(self.env["ir.config_parameter"].sudo().get_param("cafe.default_supplier_id") or 0)
        if not supplier_id:
            raise UserError(_("Configure default supplier: system parameter 'cafe.default_supplier_id'."))

        po_vals = {
            "partner_id": supplier_id,
            "origin": self.name,
            "order_line": [(0, 0, {
                "product_id": line.product_id.id,
                "name": line.product_id.display_name,
                "product_qty": line.requested_qty,
                "product_uom": line.product_id.uom_id.id,
                "price_unit": line.product_id.standard_price,
            }) for line in self.line_ids],
        }
        po = PurchaseOrder.create(po_vals)
        return {
            "type": "ir.actions.act_window",
            "res_model": "purchase.order",
            "view_mode": "form",
            "res_id": po.id,
            "target": "current",
        }
    

class CafeRequisitionLine(models.Model):
    _name = "cafe.requisition.line"
    _description = "Outlet Requisition Line"

    requisition_id = fields.Many2one("cafe.requisition", required=True, ondelete="cascade")
    product_id = fields.Many2one("product.product", required=True)
    requested_qty = fields.Float(required=True, default=1.0)
    uom_id = fields.Many2one("uom.uom", related="product_id.uom_id", store=True, readonly=True)
