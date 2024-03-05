from datetime import datetime
from timezonefinder import TimezoneFinder
from utils.weather.location import *
import pytz

#-INFO- Display current time and day of week
location_pull = get_location()
country = location_pull[2]
day_of_week = ''
lon = location_pull[0]
lat = location_pull[1]
tz = TimezoneFinder()
time_zone = tz.timezone_at(lng=lat, lat=lon)

#-INFO- ::FUNCTION:: Pulls time and timezone with day of the week
#-TODO- Have to fix the if/else issue (as on main branch) for non us users
def pull_time_and_zone(time_zone):
    time = datetime.now(pytz.timezone(time_zone))
    current_time = time.strftime("%I:%M %p")
    day_of_week = time.strftime("%A")
    return current_time, day_of_week

current_time, day_of_week = pull_time_and_zone(time_zone)