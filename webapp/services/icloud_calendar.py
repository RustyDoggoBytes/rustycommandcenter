import caldav

# Set up your iCloud username and app-specific password
icloud_username = "ivantakashi@gmail.com"
icloud_app_password = "rpev-ikak-tpdu-snff"

# CalDAV server URL for iCloud
caldav_url = "https://caldav.icloud.com"

# Authenticate and connect to iCloud's CalDAV service
# Create the CalDAV client
client = caldav.DAVClient(
    url=caldav_url, username=icloud_username, password=icloud_app_password
)

# Get the principal (root directory) and list calendars
principal = client.principal()
calendars = principal.calendars()

# Print calendar names
for calendar in calendars:
    print(calendar.name)
