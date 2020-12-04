"""This module/script contains functions to create gcal auth tokens and events.

See README for usage.
"""
from __future__ import print_function
import argparse
import datetime
import logging
import os.path
import pathlib
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from typing import List


logging.basicConfig(level=logging.INFO)


# If modifying these scopes, delete the file token.pickle.
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def create_service(creds_dir: pathlib.PosixPath):
    return build(
        serviceName="calendar",
        version="v3",
        credentials=load_or_create_creds(creds_dir=creds_dir),
    )


def load_or_create_creds(creds_dir: pathlib.PosixPath, force_create: bool = False):
    """Either loads or creates your google calendar api token.

    :param creds_dir: The directory where the pickle token is to be saved.
    :param force_create: If set a new token will be created and
        saved regardless of if a token already exists.
    """
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    token_fl = creds_dir / "token.pickle"
    if not force_create and os.path.exists(token_fl):
        logging.info("Pickled token file exists and we are loading from it.")
        with open(token_fl, "rb") as token:
            creds = pickle.load(token)
    else:
        creds = None
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        logging.info("Creating a new pickled token file.")
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_dir / "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_fl, "wb") as token:
            logging.info("Writing to the pickled token file.")
            pickle.dump(creds, token)
    return creds


def create_event(
    summary: str,
    start_time: datetime,
    end_time: datetime,
    guest_emails: List[str],
    creds_dir: pathlib.PosixPath,
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
        create_service(creds_dir=creds_dir)
        .events()
        .insert(calendarId="primary", body=event)
        .execute()
    )
    logging.info(f"Event created: {(created_event.get('htmlLink'))}")


########################################################################################
#                                       TESTING
########################################################################################


def test():
    logging.info("Creating test event that starts now...")
    cmd_opts = _parse_args()
    creds_dir = pathlib.Path(__file__).parent.absolute() / "../"
    load_or_create_creds(creds_dir=creds_dir, force_create=cmd_opts.force_create_token)
    now = datetime.datetime.now()
    create_event(
        summary="Test event",
        start_time=now,
        end_time=now + datetime.timedelta(hours=1),
        guest_emails=cmd_opts.email_ids,
        creds_dir=creds_dir,
    )


def _parse_args():
    """Parse command line arguments"""
    cmd_parser = argparse.ArgumentParser(
        description="Script to test event creation.",
    )
    cmd_parser.add_argument(
        "--email-ids",
        dest="email_ids",
        type=str,
        nargs="+",
        help=("List of email ids whom should be included in the event."),
        required=True,
    )
    cmd_parser.add_argument(
        "--force-create-token",
        dest="force_create_token",
        help=(
            "Whether to create and save a new token regardless of if one exists "
            "already.",
        ),
        default=False,
        action="store_true",
    )
    return cmd_parser.parse_args()


if __name__ == "__main__":
    test()
