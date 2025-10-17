from odoo import models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"

    sip_extension = fields.Char("SIP Extension")
