from odoo import api, fields, models


class HelpCenterArticle(models.Model):
    _name = 'coffee.helpcenter.article'
    _description = 'Help Center Article'
    _order = 'sequence, id'

    name = fields.Char(string='Title', required=True)
    category_id = fields.Many2one(
        'coffee.helpcenter.category', string='Category'
    )
    sequence = fields.Integer(string='Sequence', default=10)
    published = fields.Boolean(string='Published', default=True)
    module_menu_id = fields.Many2one(
        'ir.ui.menu', string='Target Module Menu',
        help="The module this article belongs to"
    )

    about_html = fields.Html(string='About', sanitize=False)
    howto_html = fields.Html(string='How to Use', sanitize=False)
    c4_html = fields.Html(string='C4 Model', sanitize=False)
    faq_html = fields.Html(string='FAQ', sanitize=False)

    has_about = fields.Boolean(compute='_compute_has_flags', store=True)
    has_howto = fields.Boolean(compute='_compute_has_flags', store=True)
    has_c4 = fields.Boolean(compute='_compute_has_flags', store=True)
    has_faq = fields.Boolean(compute='_compute_has_flags', store=True)

    about_attachment_ids = fields.Many2many('ir.attachment', 'help_article_about_rel', 'article_id', 'attachment_id')
    howto_attachment_ids = fields.Many2many('ir.attachment', 'help_article_howto_rel', 'article_id', 'attachment_id')
    c4_attachment_ids = fields.Many2many('ir.attachment', 'help_article_c4_rel', 'article_id', 'attachment_id')
    faq_attachment_ids = fields.Many2many('ir.attachment', 'help_article_faq_rel', 'article_id', 'attachment_id')

    @api.depends('about_html', 'howto_html', 'c4_html', 'faq_html')
    def _compute_has_flags(self):
        for rec in self:
            rec.has_about = bool(rec.about_html and rec.about_html.strip())
            rec.has_howto = bool(rec.howto_html and rec.howto_html.strip())
            rec.has_c4 = bool(rec.c4_html and rec.c4_html.strip())
            rec.has_faq = bool(rec.faq_html and rec.faq_html.strip())

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._ensure_help_menus()
        return records

    def write(self, vals):
        res = super().write(vals)
        self._ensure_help_menus()
        return res

    def unlink(self):
        affected_menus = self.mapped('module_menu_id')
        res = super().unlink()
        for menu in affected_menus:
            self._cleanup_help_menu_if_orphan(menu)
        return res

    def _ensure_help_menus(self):
        menu_obj = self.env['ir.ui.menu'].sudo()
        action_obj = self.env['ir.actions.act_window'].sudo()

        tree_view = self.env.ref('coffee_help_center.view_helpcenter_article_list', False)
        form_view = self.env.ref('coffee_help_center.view_helpcenter_article_form', False)

        tabs = [('About', 'has_about'), ('How to Use', 'has_howto'), ('C4 Model', 'has_c4'), ('FAQ', 'has_faq')]

        for menu in self.mapped('module_menu_id').filtered(lambda m: m):
            articles = self.search([('module_menu_id', '=', menu.id), ('published', '=', True)])
            if not articles:
                self._cleanup_help_menu_if_orphan(menu)
                continue

            help_parent = menu_obj.search([('parent_id', '=', menu.id), ('name', '=', 'Help')], limit=1)
            if not help_parent:
                help_parent = menu_obj.create({'name': 'Help', 'parent_id': menu.id, 'sequence': 99})

            for tab_name, flag in tabs:
                has = any(getattr(a, flag) for a in articles)
                domain = [('module_menu_id', '=', menu.id), (flag, '=', True), ('published', '=', True)]
                action_name = f'{menu.name} - Help: {tab_name}'

                action = action_obj.search([('name', '=', action_name)], limit=1)

                if has and not action:
                    action = action_obj.create({'name': action_name, 'res_model': 'coffee.helpcenter.article',
                                                'view_mode': 'tree,form', 'domain': domain})
                    views = [v.id for v in [tree_view, form_view] if v]
                    if views:
                        action.write({'view_ids': [(6, 0, views)]})

                if action and not has:
                    menu_obj.search([('action', '=', f'ir.actions.act_window,{action.id}')]).unlink()
                    action.unlink()
                    continue

                if has and action:
                    submenu = menu_obj.search([('parent_id', '=', help_parent.id), ('name', '=', tab_name)], limit=1)
                    if not submenu:
                        menu_obj.create({'name': tab_name, 'parent_id': help_parent.id,
                                         'action': f'ir.actions.act_window,{action.id}', 'sequence': 10})

    def _cleanup_help_menu_if_orphan(self, menu):
        menu_obj = self.env['ir.ui.menu'].sudo()
        action_obj = self.env['ir.actions.act_window'].sudo()

        help_parent = menu_obj.search([('parent_id', '=', menu.id), ('name', '=', 'Help')], limit=1)
        if not help_parent:
            return

        pattern = f'{menu.name} - Help:'
        actions = action_obj.search([('name', 'like', pattern)])
        for act in actions:
            menu_obj.search([('action', '=', f'ir.actions.act_window,{act.id}')]).unlink()
            act.unlink()
        help_parent.unlink()


class HelpCenterCategory(models.Model):
    _name = 'coffee.helpcenter.category'
    _description = 'Help Center Category'

    name = fields.Char(string='Category Name', required=True)
    description = fields.Text(string='Description')
    color = fields.Integer(string='Color Index')
