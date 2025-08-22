from odoo import models, fields, api
from googleapiclient.discovery import build
from google.oauth2 import service_account
import os

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    cafe_outlet_id = fields.Many2one('res.partner', string='Cafe Outlet')
    shift = fields.Selection([
        ('morning', 'Morning'),
        ('evening', 'Evening'),
        ('night', 'Night')
    ], string='Shift')
    google_event_id = fields.Char(string="Google Calendar Event ID")

    # Path to service account JSON file
    SERVICE_ACCOUNT_FILE = os.path.join(
        os.path.dirname(__file__), '../static/credentials.json'
    )
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    # Calendar ID (replace with the calendar you shared with the service account)
    CALENDAR_ID = '9448746d5d013a49022a574c6e762fec770c7ceb7983754359d530503595d578@group.calendar.google.com'

    def get_google_service(self):
        """Return a Google Calendar service object using service account."""
        if not os.path.exists(self.SERVICE_ACCOUNT_FILE):
            return None
        credentials = service_account.Credentials.from_service_account_file(
            self.SERVICE_ACCOUNT_FILE,
            scopes=self.SCOPES
        )
        service = build('calendar', 'v3', credentials=credentials)
        return service

    def sync_to_google_calendar(self):
        """Create or update Google Calendar events for production orders."""
        service = self.get_google_service()
        if not service:
            return
        for order in self:
            if not order.date_start or not order.date_finished:
                continue  # skip orders without planned dates

            event = {
                'summary': f'Production Order #{order.name}',
                'description': (
                    f'Product: {order.product_id.name}\n'
                    f'Outlet: {order.cafe_outlet_id.name if order.cafe_outlet_id else "N/A"}\n'
                    f'Shift: {order.shift if order.shift else "N/A"}'
                ),
                'start': {'dateTime': order.date_start.isoformat(),
                          'timeZone': 'Asia/Kathmandu'},
                'end': {'dateTime': order.date_finished.isoformat(),
                        'timeZone': 'Asia/Kathmandu'},
            }

            try:
                if order.google_event_id:
                    # Try to update existing event
                    service.events().update(
                        calendarId=self.CALENDAR_ID,
                        eventId=order.google_event_id,
                        body=event
                    ).execute()
                else:
                    # Create new event
                    created_event = service.events().insert(
                        calendarId=self.CALENDAR_ID,
                        body=event
                    ).execute()
                    order.google_event_id = created_event.get('id')
            except Exception:
                # If event deleted externally, create new one
                created_event = service.events().insert(
                    calendarId=self.CALENDAR_ID,
                    body=event
                ).execute()
                order.google_event_id = created_event.get('id')

    def button_confirm_and_sync(self):
        """Confirm the MRP order and sync to Google Calendar."""
        res = self.action_confirm()
        self.sync_to_google_calendar()
        return res
