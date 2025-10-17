from odoo import models, api

class VoipCall(models.Model):
    _inherit = "voip.call"

    @api.model
    def create_call(self, values):
        call = self.create({
            'phone_number': values.get('phone_number'),
            'direction': values.get('direction', 'outgoing'),
        })
        
        return {"status": "success", "call_id": call.id}
