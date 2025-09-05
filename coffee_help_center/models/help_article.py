from odoo import models, fields

class HelpCenterArticle(models.Model):
    _name = 'coffee.helpcenter.article'
    _description = 'Help Center Article'
    _order = 'sequence, id'

    name = fields.Char(string='Title', required=True)
    content = fields.Html(string='Content', sanitize=True)
    category_id = fields.Many2one('coffee.helpcenter.category', string='Category')
    sequence = fields.Integer(string='Sequence', default=10)
    published = fields.Boolean(string='Published', default=True)


class HelpCenterCategory(models.Model):
    _name = 'coffee.helpcenter.category'
    _description = 'Help Center Category'

    name = fields.Char(string='Category Name', required=True)
