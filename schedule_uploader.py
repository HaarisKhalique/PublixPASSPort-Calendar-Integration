# Publix Schedule Scraper by Haaris Khalique
'''
This module creates events in Google Calendar
'''
import datetime
import os.path


from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

CREDENTIALS_PATH = 'auth/credentials.json'
TOKEN_PATH = 'auth/token.json'
SCOPES = ["https://www.googleapis.com/auth/calendar.events"] # OAuth 2.0 scope for Google Calendar API v3 (see, edit, share, delete)

def update_calendar(workdays):
    
    if len(workdays) > 0:    

        # The following code was taken from Google's quickstart.py file to authenticate a user
        creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first time.
        if os.path.exists(TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
                creds = flow.run_local_server(port = 0, open_browser=False)
                #Save credentials for next run
                with open(TOKEN_PATH, 'w') as token:
                    token.write(creds.to_json())

        # Create an event in primary
        try:
            service = build('calendar', 'v3', credentials=creds)

            for day in workdays:
                shift = {
                    'summary': 'Work',
                    'start': {
                        'dateTime': day.start,
                        'timeZone': 'America/New_York',
                    },
                    'end':{
                        'dateTime': day.end,
                        'timeZone': 'America/New_York',   
                    }
                }
                shift = service.events().insert(calendarId= 'primary', body = shift).execute()
                
                if(day.meal_start != None):
                    meal = {
                        'summary': 'Break',
                    'start': {
                        'dateTime': day.meal_start,
                        'timeZone': 'America/New_York',
                    },
                    'end':{
                        'dateTime': day.meal_end,
                        'timeZone': 'America/New_York',   
                    }
                    }
                    meal = service.events().insert(calendarId= 'primary', body = meal).execute()
                
        except HttpError as error:
            print(f"An error occurred: {error}")
   
    else:
        print("No schedule data to append to your calendar. Try again when the new schedule releases next Tuesday.")