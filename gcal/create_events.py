from __future__ import print_function
import datetime
import pickle
import os.path
from datetime import datetime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from typing import List

# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def create_service():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("calendar", "v3", credentials=creds)


def create_event(
    summary: str,
    start_time: datetime,
    end_time: datetime,
    guest_emails: List[str],
    description: str = "Automatically created event",
    google_meet: str = "",
):
    if len(guest_emails) < 2:
        print(
            "WARNING: You're creating an event with < 2 participants. "
            "This event might get automatically declined and deleted."
        )
    event = {
        "summary": summary,
        "location": google_meet,
        "description": description,
        "start": {
            "dateTime": start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "timeZone": "Europe/Berlin",
        },
        "end": {
            "dateTime": end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            "timeZone": "Europe/Berlin",
        },
        "attendees": [{"email": email, "optional": True} for email in guest_emails],
    }
    created_event = (
        create_service().events().insert(calendarId="primary", body=event).execute()
    )
    print(f"Event created: {(created_event.get('htmlLink'))}")


if __name__ == "__main__":
    print("Creating test event that starts now...")
    now = datetime.now()
    from datetime import timedelta

    create_event(
        summary="Test event",
        start_time=now,
        end_time=now + timedelta(hours=1),
        guest_emails=["ulugbekuulutemirlan@gmail.com", "temirlan@yelp.com"],
    )
