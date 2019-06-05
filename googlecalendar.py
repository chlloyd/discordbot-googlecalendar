import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dateutil.parser import parse as dtparse

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
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming %i events' % results)
    events_result = initiate().events().list(calendarId='bolkubtob5hn0q1i9btftud944@group.calendar.google.com',
                                             timeMin=now,
                                             maxResults=results, singleEvents=True,
                                             orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))

        date = datetime.datetime.strftime(dtparse(start), format='%d %B %Y')
        time = datetime.datetime.strftime(dtparse(start), format='%H:%M')

        print(date, time)

        end = event['end'].get('dateTime', event['end'].get('date'))

        # duration

        # 2019-06-01T12:45:00+01:00

        summary = event['summary']
        location = event["location"]

        appointment = []
        print(appointment)
        try:
            description = event["description"]
        except KeyError:
            print("start", event['summary'], event["location"])
        else:
            print("start", event['summary'], event["location"], event["description"])


if __name__ == '__main__':
    initiate()
    getrecentevents(5)
