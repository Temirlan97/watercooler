# Watercooler 2.0

## What is this?
A script to automate watercooler event creation in Google Calendar.

## How to run?
- Make sure to follow steps described [here](https://developers.google.com/calendar/quickstart/python) to be able to use Google Calendar API.
- Create team folder that contains "users.txt"(participants' email addresses) and "google_meets.txt"(pre-created google meet links). You need to create google meet rooms with corporate account so that other people in that corporation can join the meeting without any approvals.
- Run `python watercooler.py [team_name] [number_of_rooms]`. When running first time, your browser will automatically open authorisation window and promt you to authorise read and write access. I recommend using your personal email for this script. 

