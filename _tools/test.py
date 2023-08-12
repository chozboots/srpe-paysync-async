from datetime import datetime
import pytz

# Define the CST and CDT timezones using pytz
cst_tz = pytz.timezone('America/Chicago')

# Get the current time in the Central Time Zone
current_time = datetime.now(cst_tz)

print("Current Central Time:", current_time)
