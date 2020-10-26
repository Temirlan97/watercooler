# Watercooler 2.0

## What is this?
A script to automate watercooler event creation in Google Calendar.

## How to run?
- Make sure to follow steps described [here](https://developers.google.com/calendar/quickstart/python) to be able to use Google Calendar API. I recommend using your personal gmail account for this script.
- Inside `user_groups` directory create yaml file for your team `<team_name>.yaml`. Copy&paste here the content from `user_group_template.txt`. Fill out the fields using the same format.
- IMPORTANT: You need to manually create google meet rooms with corporate account so that other people in that corporation can join the meeting without any approvals.
- Run `python generate_watercoolers.py` to generate watercoolers for all user groups in `user_groups` folder. When running first time, your browser will automatically open authorisation window and promt you to authorise read and write access. 

