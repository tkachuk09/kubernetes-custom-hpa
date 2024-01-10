import datetime
import pprint

from datetime import datetime, time, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Set credentials for authorization
class GoogleCalendar:
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    SERVICE_ACCOUNT_FILE = 'path_to_auth.json_file'

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file(
            filename=self.SERVICE_ACCOUNT_FILE, scopes=self.SCOPES
        )
        self.service = build('calendar', 'v3', credentials=credentials)

    def get_calendar_list(self):
        return self.service.calendarList().list().execute()

    def add_calendar(self, calendar_id):
        calendar_list_entry = {
            'id': calendar_id
        }

        return self.service.calendarList().insert(
            body=calendar_list_entry).execute()

auth = GoogleCalendar()
calendar = '' ### Calendar ID

# Define the start and end time for the events you want to fetch
start_time = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
end_time = (datetime.utcnow() + timedelta(days=1)).isoformat() + 'Z' # only for today

# Fetch the events from your calendar
events_result = auth.service.events().list(calendarId=calendar, timeMin=start_time, timeMax=end_time,
                                      maxResults=10, singleEvents=True, orderBy='startTime').execute()
events = events_result.get('items', [])

# Print the events
if not events:
    print('No events found.')
else:
    print('Event found!')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(f'{event["summary"]} ({start})')
