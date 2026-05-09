import json
import uuid
from datetime import timedelta
import dateparser
from ics import Calendar, Event

# Your JSON string
data_str = r'''
{
    "events": [
        {
            "event": "Infosys internship application deadline",
            "time": "Tomorrow, 8 PM"
        },
        {
            "event": "Infosys internship start date",
            "time": "July 7"
        },
        {
            "event": "Hackathon",
            "time": "May 11"
        },
        {
            "event": "Hackathon",
            "time": "May 12"
        },
        {
            "event": "Hackathon",
            "time": "May 13"
        },
        {
            "event": "Training",
            "time": "Next Friday"
        }
    ]
}
'''

# Parse JSON
data = json.loads(data_str)

# Create calendar
calendar = Calendar()

for item in data["events"]:
    event_name = item["event"]
    time_str = item["time"]

    # Parse date/time
    parsed_date = dateparser.parse(
        time_str,
        settings={
            "PREFER_DATES_FROM": "future",
            "RETURN_AS_TIMEZONE_AWARE": False
        }
    )

    if parsed_date is None:
        print(f"Could not parse date: {time_str}")
        continue

    # Create ICS event
    e = Event()
    e.name = event_name
    e.begin = parsed_date

    # Optional:
    # make all events 1 hour long
    e.end = parsed_date + timedelta(hours=1)

    # Unique ID
    e.uid = str(uuid.uuid4())

    calendar.events.add(e)

# Save to file
with open("events.ics", "w") as f:
    f.writelines(calendar)

print("ICS calendar saved as events.ics")

def view_ics_calendar(file_path):
    with open(file_path, "r") as f:
        calendar = Calendar(f.read())

    print("\n===== CALENDAR EVENTS =====\n")

    # Sort events by start time
    events = sorted(calendar.events, key=lambda e: e.begin)

    for i, event in enumerate(events, start=1):
        print(f"Event {i}")
        print(f"Title : {event.name}")

        # Human readable date/time
        print(f"Start : {event.begin.strftime('%A, %d %B %Y, %I:%M %p')}")

        if event.end:
            print(f"End   : {event.end.strftime('%A, %d %B %Y, %I:%M %p')}")

        print("-" * 40)


# Example usage
view_ics_calendar("events.ics")