# Watercooler 2.0

## What is this?
A script to automate watercooler event creation in Google Calendar.

## How to run?
- Make virtualenv with `make venv && source venv/bin/activate`.
- Generate and save authorisation tokens for Google Calendar API.
  - Make sure to follow steps described [here](https://developers.google.com/calendar/quickstart/python)
  to be able to use Google Calendar API. We recommend using your
  personal gmail account for this script to avoid any unnecessary sharing of corporate
  information.
  - Run the script to create and save your authorsation token in the `token.pickle` file.
  This will automatically open your browser and prompt you to authorise read and write
  access. It will also create a test event for verification.
  ``` bash
  python gcal/create_events.py --email-ids eid1@gmail.com eid2@workemail.com --force-create-token
  ```
- Inside `user_groups` directory create yaml file for your team `<team_name>.yaml`. Copy&paste here the content from `user_group_template.txt`. Fill out the fields using the same format.
- IMPORTANT: You need to manually create google meet rooms with corporate account so that other people in that corporation can join the meeting without any approvals.
- Run `python generate_watercoolers.py` to generate watercoolers for all user groups in
`user_groups` folder. This script will read the cached token from the previous steps
and you would not need a browser.

## Scheduling on cron
The following example schedules the watercoolers every week on Mondays at 5am.
``` bash
$ crontab -e

0 5 * * MON /home/virtualenv/bin/python /home/watercooler/generate_watercoolers.py
```
