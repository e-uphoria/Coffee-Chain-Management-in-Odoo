from odoo import models, fields, api

class CoffeeSupplier(models.Model):
    _name = 'coffee.supplier'
    _description = 'Coffee Bean Supplier'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    

    name = fields.Char(string='Supplier Name', required=True, tracking=True)
    image_1920 = fields.Image(string="Supplier Image")
    contact_person = fields.Char(string='Contact Person')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    street = fields.Char(string='Street')
    city = fields.Char(string='City')
    state_id = fields.Many2one('res.country.state', string='State')
    country_id = fields.Many2one('res.country', string='Country')
    bean_origin = fields.Char(string='Bean Origin')
    contract_start = fields.Date(string='Contract Start')
    contract_end = fields.Date(string='Contract End')
    active = fields.Boolean(default=True)
    notes = fields.Text(string='Notes')
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company
    )
    price_line_ids = fields.One2many('coffee.supplier.price', 'supplier_id', string='Price List')

    stage_id = fields.Many2one(
        'coffee.supplier.stage',
        string='Stage',
        group_expand='_read_group_stage_ids',
        tracking=True
    )

    contract_duration_days = fields.Integer(
        compute='_compute_contract_duration',
        store=True,
        string='Contract Duration (days)'
    )

    @api.depends('contract_start', 'contract_end')
    def _compute_contract_duration(self):
        for rec in self:
            if rec.contract_start and rec.contract_end:
                rec.contract_duration_days = (rec.contract_end - rec.contract_start).days
            else:
                rec.contract_duration_days = 0

    @api.model
   
    def _read_group_stage_ids(self, stages, domain, order=None, lazy=False):
        return self.env['coffee.supplier.stage'].search([], order=order)


