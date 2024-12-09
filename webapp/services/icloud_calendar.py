import json
from datetime import datetime, timedelta

import caldav

# Set up your iCloud username and app-specific password
icloud_username = "ivantakashi@gmail.com"
icloud_app_password = "rpev-ikak-tpdu-snff"

# CalDAV server URL for iCloud
caldav_url = "https://caldav.icloud.com"

# Authenticate and connect to iCloud's CalDAV service
# Create the CalDAV client
# client = caldav.DAVClient(
#     url=caldav_url, username=icloud_username, password=icloud_app_password
# )
#
# # Get the principal (root directory) and list calendars
# principal = client.principal()
# # Fetch the calendar (you can list all calendars, or use the first one)
# print(principal.calendars())
# calendar = next((c for c in principal.calendars() if c.name == "Home"), None)
#
#
# for calendar in principal.calendars():
#     print(calendar.name)
#
# # Get events within a certain time range
start_date = datetime.now()
end_date = start_date + timedelta(weeks=1)
#
# # Fetch events within the given time range
# events = calendar.date_search(start=start_date, end=end_date)


def fetch_and_print():
    with caldav.DAVClient(
        url=caldav_url,
        username=icloud_username,
        password=icloud_app_password,
    ) as client:
        print_calendars_demo(client.principal().calendars())


def print_calendars_demo(calendars):
    if not calendars:
        return
    events = []
    for calendar in calendars:
        if calendar.name != "Home":
            continue
        for event in calendar.date_search(start=start_date, end=end_date):
            for component in event.icalendar_instance.walk():
                if component.name != "VEVENT":
                    continue
                events.append(fill_event(component, calendar))
    print(json.dumps(events, indent=2, ensure_ascii=False))


def fill_event(component, calendar) -> dict[str, str]:
    cur = {}
    cur["calendar"] = f"{calendar}"
    cur["summary"] = component.get("summary")
    cur["description"] = component.get("description")
    cur["start"] = component.get("dtstart").dt.strftime("%m/%d/%Y %H:%M")
    endDate = component.get("dtend")
    if endDate and endDate.dt:
        cur["end"] = endDate.dt.strftime("%m/%d/%Y %H:%M")
    cur["datestamp"] = component.get("dtstamp").dt.strftime("%m/%d/%Y %H:%M")
    return cur


if __name__ == "__main__":
    fetch_and_print()
