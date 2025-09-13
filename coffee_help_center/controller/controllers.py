from odoo import http
from odoo.http import request

class HelpCenterWebsite(http.Controller):

    @http.route(['/helpcenter'], type='http', auth='public', website=True)
    def helpcenter_index(self, **kwargs):
        """
        Show module/menu grid (3x3). Only modules with published help articles are shown.
        """
        # Fetch all top-level modules/menus (you can filter as needed)
        module_menu_ids = request.env['ir.ui.menu'].sudo().search([
            ('parent_id', '=', False)
        ])
        categories = module_menu_ids
        return request.render('coffee_help_center.website_helpcenter_page', {
            'categories': categories,
        })

    @http.route(['/helpcenter/category/<int:menu_id>'], type='http', auth='public', website=True)
    def helpcenter_category(self, menu_id, **kwargs):
        """
        Display all published articles for a module/menu.
        """
        menu = request.env['ir.ui.menu'].sudo().browse(menu_id)
        articles = request.env['coffee.helpcenter.article'].sudo().search([
            ('module_menu_id', '=', menu.id),
            ('published', '=', True)
        ], order='sequence, id')
        return request.render('coffee_help_center.website_helpcenter_category', {
            'menu': menu,
            'articles': articles,
        })

    @http.route(['/helpcenter/article/<int:article_id>'], type='http', auth='public', website=True)
    @http.route(['/helpcenter/article/<int:article_id>/<string:active_tab>'], type='http', auth='public', website=True)
    def helpcenter_article(self, article_id, active_tab='about', **kwargs):
        """
        Show single article with tabs (About, How-to, C4, FAQ).
        """
        article = request.env['coffee.helpcenter.article'].sudo().browse(article_id)
        # Validate tab
        if active_tab not in ['about', 'howto', 'c4', 'faq']:
            active_tab = 'about'
        return request.render('coffee_help_center.website_helpcenter_article_page', {
            'article': article,
            'active_tab': active_tab,
        })
