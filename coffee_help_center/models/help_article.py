from odoo import models, fields

class HelpCenterArticle(models.Model):
    _name = 'coffee.helpcenter.article'
    _description = 'Help Center Article'
    _order = 'sequence, id'

    name = fields.Char(string='Title', required=True)
    category_id = fields.Many2one('coffee.helpcenter.category', string='Category')
    sequence = fields.Integer(string='Sequence', default=10)
    published = fields.Boolean(string='Published', default=True)

    # Rich HTML content per tab
    about_html = fields.Html(string='About the Module', sanitize=False)
    howto_html = fields.Html(string='How to Use', sanitize=False)
    c4_html = fields.Html(string='C4 Model Diagram', sanitize=False)
    faq_html = fields.Html(string='FAQ', sanitize=False)

    # Attachments per tab with explicit relation tables
    about_attachment_ids = fields.Many2many(
        'ir.attachment', 
        'help_article_about_rel', 
        'article_id', 
        'attachment_id', 
        string='About Files'
    )
    howto_attachment_ids = fields.Many2many(
        'ir.attachment', 
        'help_article_howto_rel', 
        'article_id', 
        'attachment_id', 
        string='How-To Files'
    )
    c4_attachment_ids = fields.Many2many(
        'ir.attachment', 
        'help_article_c4_rel', 
        'article_id', 
        'attachment_id', 
        string='C4 Files'
    )
    faq_attachment_ids = fields.Many2many(
        'ir.attachment', 
        'help_article_faq_rel', 
        'article_id', 
        'attachment_id', 
        string='FAQ Files'
    )


class HelpCenterCategory(models.Model):
    _name = 'coffee.helpcenter.category'
    _description = 'Help Center Category'

    name = fields.Char(string='Category Name', required=True)
