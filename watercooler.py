import argparse
import math
import numpy as np
import random
from datetime import date
from datetime import datetime
from datetime import timedelta
from termcolor import colored
from typing import Tuple

from gcal.create_events import create_event

parser = argparse.ArgumentParser()

WEEKDAYS = [1, 3]  # 0 - Monday, 1 - Tuesday...
START_DELTA = timedelta(hours=14, minutes=30)
DURATION = timedelta(minutes=30)

parser.add_argument(
    "team",
    nargs="?",
    type=str,
    help="Which team are you generating watercooler for (e.g. uli, mlocrep)",
    default="uli",
)

parser.add_argument(
    "num_watercoolers",
    nargs="?",
    type=int,
    help="Number of watercoolers that you want to have",
    default=3,
)
TEAM = parser.parse_args().team
NUM_GROUPS = parser.parse_args().num_watercoolers


with open(f"{TEAM}/users.txt", "r") as users_file:
    all_users = list(map(str.strip, users_file.readlines()))
    active_users = list(filter(lambda x: not x.startswith("#"), all_users))

with open(f"{TEAM}/google_meets.txt", "r") as google_meets:
    gmeets = list(map(str.strip, google_meets.readlines()))
    if len(gmeets) < NUM_GROUPS:
        raise ValueError(
            f"Not enough google meets rooms in {TEAM}/google_meets.txt\n"
            f"Required {NUM_GROUPS}, found {len(gmeets)}"
        )


with open("topics.txt", "r") as topics_file:
    all_topics = list(
        map(str.strip, filter(lambda x: x, topics_file.read().split("TOPIC_BEGIN")))
    )


def generate_event_times() -> Tuple[datetime, datetime]:
    today = date.today()
    week_start = today - timedelta(today.weekday())
    for weekday in WEEKDAYS:
        start_time = (
            datetime(week_start.year, week_start.month, week_start.day)
            + timedelta(days=weekday)
            + START_DELTA
        )
        if start_time < datetime.now():
            start_time += timedelta(weeks=1)
        yield start_time, start_time + DURATION


for start_time, end_time in generate_event_times():
    random.shuffle(active_users)
    users_chunks = np.array_split(active_users, NUM_GROUPS)
    chosen_topics = random.sample(all_topics, NUM_GROUPS)
    i = 0

    for i in range(NUM_GROUPS):
        event_name = f"Watercooler #{i+1}"
        print(colored(f"<======= Creating {event_name}: =======>", "blue"))
        print(f"Event time: {start_time}")
        users_in_watercooler = users_chunks[i].tolist()
        print(colored("Participants: " + ",".join(users_in_watercooler), "green"))
        print(colored("Watercooler topic: ", "magenta"))
        print(chosen_topics[i])
        print(gmeets[i])
        create_event(
            summary=event_name,
            start_time=start_time,
            end_time=end_time,
            guest_emails=users_in_watercooler,
            description=(f"Watercooler topic:\n{chosen_topics[i]}"),
            google_meet=gmeets[i],
        )
