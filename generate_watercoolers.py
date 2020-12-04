import math
import numpy as np
import os
import pathlib
import random
import yaml
import sys
from datetime import date
from datetime import datetime
from datetime import timedelta
from termcolor import colored
from typing import Dict
from typing import List
from typing import Tuple

from gcal.create_events import create_event


def generate_watercoolers():
    script_dir = pathlib.Path(__file__).parent.absolute()
    # Load user_groups and generate watercoolers
    user_groups_directory = script_dir / "user_groups"
    all_files = [
        os.path.join(user_groups_directory, f)
        for f in os.listdir(user_groups_directory)
    ]
    yaml_files = [f for f in all_files if os.path.isfile(f) and f.endswith(".yaml")]
    for yaml_file in yaml_files:
        print(colored(f"Reading file {yaml_file}...", "magenta"))
        generate_watercoolers_for_user_group(
            user_group_file_name=yaml_file, script_dir=script_dir,
        )


def generate_watercoolers_for_user_group(
    user_group_file_name: str, script_dir: pathlib.PosixPath,
):
    # Load topics
    with open(script_dir / "topics.txt", "r") as topics_file:
        all_topics = list(
            map(str.strip, filter(lambda x: x, topics_file.read().split("TOPIC_BEGIN")))
        )

    with open(user_group_file_name, "r") as file:
        user_group = yaml.full_load(file)
    print(
        colored(
            f"Generating watercoolers for {user_group['user_group_name']}", "magenta"
        )
    )
    google_events = []
    for start_time, end_time in generate_event_times(user_group["slots"]):
        random.shuffle(user_group["user_emails"])
        number_of_rooms = user_group["number_of_rooms"]
        if number_of_rooms < 1:
            error(f"Number of rooms must be positive, given {number_of_rooms}")
        gmeets = user_group["google_meet_links"]
        if len(gmeets) < number_of_rooms:
            error(
                f"{len(gmeets)} google meet links provided, >= {number_of_rooms} required"
            )
        users_chunks = np.array_split(user_group["user_emails"], number_of_rooms)
        chosen_topics = random.sample(all_topics, number_of_rooms)
        for i in range(number_of_rooms):
            event_name = f"{user_group['user_group_name']} Watercooler #{i+1}"
            print(colored(f"<======= Creating {event_name}: =======>", "blue"))
            print(f"Event time: {start_time} - {end_time}")
            users_in_watercooler = users_chunks[i].tolist()
            print(colored("Participants: " + ",".join(users_in_watercooler), "green"))
            print("Watercooler topic: ")
            print(chosen_topics[i])
            print(gmeets[i])
            google_events.append(
                {
                    "summary": event_name,
                    "start_time": start_time,
                    "end_time": end_time,
                    "guest_emails": users_in_watercooler,
                    "description": f"Watercooler topic:\n{chosen_topics[i]}",
                    "google_meet": gmeets[i],
                    "creds_dir": script_dir,
                }
            )

    for event in google_events:
        create_event(**event)


def generate_event_times(slots: List[Dict[str, str]]) -> Tuple[datetime, datetime]:
    today = date.today()
    week_start = today - timedelta(today.weekday())
    weekday_to_int = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
        "Saturday": 5,
        "Sunday": 6,
    }
    for slot in slots:
        if slot["day"] not in weekday_to_int:
            error(f"Slot day must be one of {weekday_to_int.keys()}")
        weekday = weekday_to_int[slot["day"]]
        start_time = (
            datetime(week_start.year, week_start.month, week_start.day)
            + timedelta(days=weekday)
            + timedelta(minutes=slot["start_time"])
        )
        end_time = (
            datetime(week_start.year, week_start.month, week_start.day)
            + timedelta(days=weekday)
            + timedelta(minutes=slot["end_time"])
        )
        if start_time >= end_time:
            error(
                f"End time for events must be after start time, given {start_time} - {end_time}"
            )
        # schedule for next week if time has already passed
        if start_time < datetime.now():
            start_time += timedelta(weeks=1)
            end_time += timedelta(weeks=1)
        yield start_time, end_time


def error(message: str):
    print(colored("ERROR: " + message, "red"))
    print(colored("No events were generated. Exiting the program...", "red"))
    sys.exit()


if __name__ == "__main__":
    generate_watercoolers()
