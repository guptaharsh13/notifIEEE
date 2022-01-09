from pathlib import Path
import environ
import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import timedelta


path = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(env_file=os.path.join(path, ".env"))


CLIENT_SECRET_FILE = os.path.join(path, "utils/client_secret.json")
API_NAME = "calendar"
API_VERSION = "v3"
SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR_ID = env("CALENDAR_ID")

flow = InstalledAppFlow.from_client_secrets_file(
    CLIENT_SECRET_FILE, scopes=SCOPES)


try:
    credentials = pickle.load(open("token.pkl", "rb"))
except:
    credentials = flow.run_console()
    pickle.dump(credentials, open("token.pkl", "wb"))

service = build("calendar", "v3", credentials=credentials)


def scheduleMeet(meet_name, meet_link, s_datetime, duration, emails):

    end_time = s_datetime + timedelta(hours=duration)
    timezone = "Asia/Kolkata"
    event = {
        # 'location': '',
        'summary': meet_name,
        'description': meet_link,
        'start': {
            'dateTime': s_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': timezone,
        },
        'attendees': emails,
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 10},
                {'method': 'email', 'minutes': 1440},
                {'method': 'popup', 'minutes': 5},
                {'method': 'popup', 'minutes': 1440},
            ],
        },
    }

    return service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
