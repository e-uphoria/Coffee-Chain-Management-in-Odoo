from odoo import models, fields

class CafeBoMIngredient(models.Model):
    _name = 'cafe.bom.ingredient'
    _description = 'BoM Ingredient Line'

    bom_id = fields.Many2one('cafe.bom', string='BoM', required=True, ondelete='cascade')
    ingredient_id = fields.Many2one('cafe.product', string='Ingredient', required=True)
    quantity = fields.Float(string='Quantity', required=True)

class CafeBoM(models.Model):
    _name = 'cafe.bom'
    _description = 'Recipe BoM'

    name = fields.Char(string='BoM Name', required=True)
    product_id = fields.Many2one('cafe.product', string='Product', required=True)
    ingredient_line_ids = fields.One2many('cafe.bom.ingredient', 'bom_id', string='Ingredients')
    revision = fields.Char(string='Revision', default='v1.0')
    document_id = fields.Many2one('ir.attachment', string='Recipe Document')
    active = fields.Boolean(string='Active', default=True)
    
    def create_new_revision(self, new_document_id=None):
        self.ensure_one()
        revision_number = float(self.revision[1:]) + 0.1
        new_revision = self.copy({
            'revision': f"v{revision_number:.1f}",
            'document_id': new_document_id or self.document_id.id,
            'active': True
        })
        self.active = False
        return new_revision

    def compare_bom(self, other_bom):
        self.ensure_one()
        changes = []
        for line in self.ingredient_line_ids:
            other_line = other_bom.ingredient_line_ids.filtered(lambda l: l.ingredient_id == line.ingredient_id)
            if other_line:
                if line.quantity != other_line.quantity:
                    changes.append(f"{line.ingredient_id.name} quantity changed from {other_line.quantity} to {line.quantity}")
            else:
                changes.append(f"{line.ingredient_id.name} removed in new BOM")
        for line in other_bom.ingredient_line_ids:
            if not self.ingredient_line_ids.filtered(lambda l: l.ingredient_id == line.ingredient_id):
                changes.append(f"{line.ingredient_id.name} added in new BOM")
        return changes