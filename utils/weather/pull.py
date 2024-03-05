from location import *
from weatherkit.client import WKClient

#-INFO- ::FUNCTION:: Pulls weather json from api
def pull_weather():
    team_id = "Y9QCH3E9YS"
    service_id = "com.thanksdev.weathersense"
    key_id = "YQLY8XP7XX"
    path_to_key = "weather/secret/AuthKey_YQLY8XP7XX.p8"

    data = get_location()
    client = WKClient(team_id, service_id, key_id, path_to_key)
    res = client.get_weather(data[0], data[1])

    return res