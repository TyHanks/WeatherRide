import json
from datetime import datetime

#********************************************************#
#* CLASS *# Convert metric units 
#********************************************************#
class UnitConversion:

    #-INFO- Convert Celsius to rounded Fahrenheit.
    def celsius_to_fahrenheit(self, celsius):
        fahrenheit = round((1.8 * celsius) + 32)
        return fahrenheit

    #-INFO- Convert meters to rounded miles.
    def meters_to_miles(self, meters):
        miles = round(meters / 1609.344, 1)
        return miles
    
    #-INFO- Convert kilometers to rounded miles.
    def kilometers_to_miles(self, kilometers):
        miles = round(kilometers / 1.609344, 2)
        return miles
    
    #-INFO- Convert millimeters to rounded inches.
    def millimeters_to_inches(self, millimeters):
        inches = round(millimeters / 25.4)
        return inches

    #-INFO- Convert decimal to percentage.
    def decimal_to_percentage(self, decimal):
        percent = decimal * 100
        return percent
    
    #-INFO- Convert millibars to inches.
    def millibars_to_inches(self, millibars):
        inches = round(millibars / 33.86389, 2) 
        return inches

    #-INFO- Convert Wind direction degree to cardinal direction.
    def degree_to_cardinal(self, value):
        directions = [
            (11.25, "NNE"),
            (33.75, "NE"),
            (56.25, "ENE"),
            (78.75, "E"),
            (101.25, "ESE"),
            (123.75, "SE"),
            (146.25, "SSE"),
            (168.75, "S"),
            (191.25, "SSW"),
            (213.75, "SW"),
            (236.25, "WSW"),
            (258.75, "W"),
            (281.25, "WNW"),
            (303.75, "NW"),
            (326.25, "NNW"),
            (348.75, "N")
        ]
        
        for angle, direction in directions:
            if value <= angle:
                return direction
        return "N"

#-INFO- Variables
day = 0
convert = UnitConversion()

#-INFO- ::FUNCTION:: Current day data.
def current_day(convert, current_weather):

    temp_data = current_weather["temperature"]
    temp = convert.celsius_to_fahrenheit(temp_data)
    temp_c = round(temp_data)

    temp_feel_data = current_weather["temperatureApparent"]
    temp_feel = convert.celsius_to_fahrenheit(temp_feel_data)
    temp_feel_c = round(temp_feel_data)

    wind_speed_data = current_weather["windSpeed"]
    wind_speed = int(convert.kilometers_to_miles(wind_speed_data))

    wind_direction_data = current_weather["windDirection"]
    wind_direction = convert.degree_to_cardinal(wind_direction_data)

    condition_code = current_weather["conditionCode"]

    humidity_data = current_weather["humidity"]
    humidity = int(convert.decimal_to_percentage(humidity_data))

    wind_gust_data = current_weather["windGust"]
    wind_gust = int(convert.kilometers_to_miles(wind_gust_data))

    pressure_data = current_weather["pressure"]
    pressure = convert.millibars_to_inches(pressure_data)

    uv_index = current_weather["uvIndex"]

    daylight = current_weather["daylight"]

    visibility_data = current_weather["visibility"]
    visibility = int(convert.meters_to_miles(visibility_data))

    return temp, temp_feel, wind_speed, wind_direction, condition_code, humidity, wind_gust, pressure, uv_index, daylight, visibility, temp_c, temp_feel_c

#-INFO- ::FUNCTION:: Extract daily forecast data.
def extract_forecast_day(timed_data, day_data, convert):
    date = day_data["forecastStart"]
    date_remove_time = date[:-10]
    date_convert = datetime.strptime(date_remove_time, '%Y-%m-%d')
    day_of_week = date_convert.strftime("%A")

    condition_code = day_data["conditionCode"]
    max_uv_index = day_data["maxUvIndex"]
    precipitation_chance = int(convert.decimal_to_percentage(day_data["precipitationChance"]))
    
    temp_max_c = round(day_data["temperatureMax"])
    temp_max_f = convert.celsius_to_fahrenheit(day_data["temperatureMax"])
    
    temp_min_c = round(day_data["temperatureMin"])
    temp_min_f = convert.celsius_to_fahrenheit(day_data["temperatureMin"])

    daytime_forecast = timed_data.get("daytimeForecast")
    night_forecast = timed_data.get("overnightForecast")

    day_condition_code = daytime_forecast["conditionCode"]
    day_humidity = int(convert.decimal_to_percentage(daytime_forecast["humidity"]))
    day_precipitation_chance = int(convert.decimal_to_percentage(daytime_forecast["precipitationChance"]))
    day_wind_direction = convert.degree_to_cardinal(daytime_forecast["windDirection"])
    day_wind_speed = int(convert.kilometers_to_miles(daytime_forecast["windSpeed"]))

    night_condition_code = night_forecast["conditionCode"]
    night_humidity = int(convert.decimal_to_percentage(night_forecast["humidity"]))
    night_precipitation_chance = int(convert.decimal_to_percentage(night_forecast["precipitationChance"]))
    night_wind_direction = convert.degree_to_cardinal(night_forecast["windDirection"])
    night_wind_speed = int(convert.kilometers_to_miles(night_forecast["windSpeed"]))

    return (
        day_of_week, condition_code, max_uv_index, precipitation_chance, 
        temp_max_f, temp_min_f, day_condition_code, day_humidity, 
        day_precipitation_chance, day_wind_direction, day_wind_speed, 
        night_condition_code, night_humidity, night_precipitation_chance, 
        night_wind_direction, night_wind_speed, temp_max_c, temp_min_c,
    )

#-INFO- ::FUNCTION:: Generate forecasts days data
def generate_forecasts(data, convert, day):
    forecast_days = data["forecastDaily"]["days"]
    timed_data = data["forecastDaily"]["days"][day]
    forecasts = []

    for day_data in forecast_days:
        forecast = extract_forecast_day(timed_data, day_data, convert)
        day = day + 1
        forecasts.append(forecast)

    return forecasts

#-INFO- ::FUNCTION:: Load data for forecasts to generate and extract
def forecasts():
    #-DELETE- When ready for api data
    file_path = "utils/weather/test/pull.json"
    with open(file_path) as file:
        data = json.load(file)
    #-DELETE-------------------------
    forecasts = generate_forecasts(data, convert, day)
    current_weather = data["currentWeather"]

    return forecasts, data, current_weather