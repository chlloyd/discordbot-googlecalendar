import datetime
import json
import pickle
import os
from googleapiclient.discovery import build
import pytz
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dateutil.parser import parse as dtparse

CALENDAR = os.getenv("CALENDAR")
CREDENTIALS = os.getenv("CREDENTIALS")
TIMEZONE = pytz.timezone('Europe/London')

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def initiate():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(json.loads(CREDENTIALS), SCOPES)
            creds = flow.run_local_server()
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service


def getrecentevents(results):
    # Call the Calendar API
    now = datetime.datetime.now(tz=TIMEZONE).isoformat()
    events_result = initiate().events().list(calendarId=CALENDAR,
                                             timeMin=now,
                                             maxResults=results, singleEvents=True,
                                             orderBy='startTime').execute()
    events = events_result.get('items', [])
    return oraganisetolist(events)


def gettomorrowevents(results=250):
    tomorrow = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    tomorrowrfc39 = tomorrow.strftime("%Y-%m-%dT00:00:00+01:00")
    dayafter = datetime.datetime.utcnow() + datetime.timedelta(days=2)
    dayafterrfc39 = dayafter.strftime("%Y-%m-%dT00:00:00+01:00")
    events_result = initiate().events().list(calendarId=CALENDAR, maxResults=results, singleEvents=True,
                                             timeMin=tomorrowrfc39, timeMax=dayafterrfc39,
                                             orderBy='startTime').execute()
    events = events_result.get('items', [])
    return oraganisetolist(events)


def oraganisetolist(events):
    if not events:
        return "No Events Found"
    else:
        all_appointments = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))

            start_date = dtparse(start)
            end_date = dtparse(end)

            date = start_date.strftime('%d %B %Y')

            start = start_date.strftime('%H:%M')
            end = end_date.strftime('%H:%M')

            duration = datetime.datetime.strptime(end, "%H:%M") - datetime.datetime.strptime(start, "%H:%M")
            duration = duration.seconds // 3600

            summary = event['summary']
            location = event["location"]

            description = event.get('description', '')

            appointment = [date, start, end, duration, summary, location, description]
            all_appointments.append(appointment)
        return all_appointments


if __name__ == '__main__':
    initiate()
