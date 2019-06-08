import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dateutil.parser import parse as dtparse

import config

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
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service


def getrecentevents(results):
    # Call the Calendar API
    now = datetime.datetime.astimezone(datetime.datetime.utcnow()).isoformat()
    print(now)
    # print('Getting the upcoming %i events' % results)
    events_result = initiate().events().list(calendarId=config.CALENDAR,
                                             timeMin=now,
                                             maxResults=results, singleEvents=True,
                                             orderBy='startTime').execute()
    events = events_result.get('items', [])
    print(events)
    return oraganisetolist(events)


def gettomorrowevents(results=250):
    tomorrow = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    tomorrowrfc39 = tomorrow.strftime("%Y-%m-%dT00:00:00-01:00")
    dayafter = datetime.datetime.utcnow() + datetime.timedelta(days=2)
    dayafterrfc39 = dayafter.strftime("%Y-%m-%dT00:00:00-01:00")
    print('Getting the upcoming %i events' % results)
    events_result = initiate().events().list(calendarId=config.CALENDAR, maxResults=results, singleEvents=True,
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

            date = datetime.datetime.strftime(dtparse(start), format='%d %B %Y')
            start = datetime.datetime.strftime(dtparse(start), format='%H:%M')
            end = datetime.datetime.strftime(dtparse(event['end'].get('dateTime', event['end'].get('date'))),
                                             format='%H:%M')

            duration = datetime.datetime.strptime(end, "%H:%M") - datetime.datetime.strptime(start, "%H:%M")
            duration = duration.seconds // 3600

            summary = event['summary']
            location = event["location"]

            try:
                description = event["description"]
            except KeyError:
                description = ""

            appointment = [date, start, end, duration, summary, location, description]
            all_appointments.append(appointment)
        return all_appointments


if __name__ == '__main__':
    initiate()
