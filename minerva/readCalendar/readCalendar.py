from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import datetime 

creds = None
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

class ReadCalendar:
    def readStudioCalendar():
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'readCalendar/credentials-calendar.json', SCOPES)
                creds = flow.run_local_server(port=0)

            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('calendar', 'v3', credentials=creds)

        today = datetime.datetime.now(datetime.UTC) 
        start = today.isoformat()  
        end = (today + datetime.timedelta(days=5)).isoformat()

        events_results = service.events().list(
            calendarId='c7e5737297d1974b2bf92d840321eaee2cc39732173cba161d98b1834e079669@group.calendar.google.com',
            timeMin=start,
            timeMax=end,
            singleEvents=True,
            orderBy='startTime'
        ).execute()

        events = events_results.get('items', [])

        if not events:
            print('No upcoming events found.')
        else:
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                return event.get('summary', 'No Title')