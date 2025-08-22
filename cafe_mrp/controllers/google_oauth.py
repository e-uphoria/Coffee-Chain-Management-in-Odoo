from odoo import http
from odoo.http import request
from google_auth_oauthlib.flow import Flow
import json

class GoogleOAuthController(http.Controller):

    @http.route('/myerp/google_calendar/login', type='http', auth='user')
    def login(self):
        flow = Flow.from_client_secrets_file(
            '/path/to/credentials.json',  # Google Cloud OAuth client
            scopes=['https://www.googleapis.com/auth/calendar'],
            redirect_uri='http://localhost:8069/myerp/google_calendar/callback'
        )
        auth_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        return request.redirect(auth_url)

    @http.route('/myerp/google_calendar/callback', type='http', auth='user')
    def callback(self, **kw):
        flow = Flow.from_client_secrets_file(
            '/path/to/credentials.json',
            scopes=['https://www.googleapis.com/auth/calendar'],
            redirect_uri='http://localhost:8069/myerp/google_calendar/callback'
        )
        flow.fetch_token(code=kw.get('code'))
        credentials = flow.credentials

        # Save credentials in Odoo
        request.env['ir.config_parameter'].sudo().set_param(
            'myerp.google_calendar_credentials', credentials.to_json()
        )
        return "Google Calendar connected successfully!"
