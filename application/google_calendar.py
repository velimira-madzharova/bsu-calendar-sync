#!/usr/bin/env python3

from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
import googleapiclient
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/calendar']

class Calendar:

    def get_calendar_service(self):
        """Shows basic usage of the Google Calendar API.
        Prints the start and name of the next 10 events on the user's calendar.
        """
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                print('The following authorization of the app can be revoked afterwards through your settings in Google. Credentials will be saved locally where you run the app.')
                creds = flow.run_local_server(port=8000)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return build('calendar', 'v3', credentials=creds)

    def insert_event(self, summary, desc, url, start, end):
        service = self.get_calendar_service()
        start = start.isoformat()
        end = end.isoformat()

        body =  { "summary": summary,
                     "description": desc,
                     "start": {"dateTime": start, "timeZone": 'Europe/Sofia'},
                     "end": {"dateTime": end, "timeZone": 'Europe/Sofia'},
                     "source": {"title" : "BFU", "url": url}}

        try:
            event_result = service.events().insert(calendarId='primary',
                 body=body
              ).execute()
            return event_result['id']
        except googleapiclient.errors.HttpError as e:
            print("Failed to create event")
            print(e)
            return False
    def delete_event(self, event_id):

        service = self.get_calendar_service()
        try:
            service.events().delete(
                calendarId='primary',
                eventId=event_id,
            ).execute()
            return True
        except googleapiclient.errors.HttpError:
            print("Failed to delete event")
            return False