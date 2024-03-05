from utils.weather.data import forecasts, current_day, convert
from utils.weather.time import *

def passWeatherData():
    
  #-INFO- Data to pass into context_current
  #-DATA- temp, temp_feel, wind_speed, wind_direction, condition_code, humidity, wind_gust, pressure, uv_index, daylight, visibility, temp_c, temp_feel_c
  current_weather = forecasts()
  current_forecasts = forecasts()
  current_forecasts_data = current_forecasts[0]
  current_day_data = current_day(convert, current_weather[2])

  #-DATA- current_time, day_of_week
  current_time_data = pull_time_and_zone(time_zone)

  context_current = {
    'cur_temp': current_day_data[0],
    'cur_tempFeel': current_day_data[1],
    'cur_windSpeed': current_day_data[2],
    'cur_windDirection': current_day_data[3],
    'cur_conditionCode': current_day_data[4],
    'cur_humidity': current_day_data[5],
    'cur_windGust': current_day_data[6],
    'cur_pressure': current_day_data[7],
    'cur_uvIndex': current_day_data[8],
    'cur_daylight': current_day_data[9],
    'cur_visibility': current_day_data[10],
    'cur_tempC': current_day_data[11],
    'cur_tempFeelC': current_day_data[12],
    'cur_time': current_time_data[0],
    'cur_day': current_time_data[1],
  }

  #-INFO- Data to pass into context_daily for loop
  forecast_day_variables = ['dayOfWeek', 'conditionCode', 'maxUvIndex', 'precChance', 'tempMax', 'tempMin',
                          'dConditionCode', 'dHumidity', 'dPrecChance', 'dWindDir', 'dWindSpeed',
                          'nConditionCode', 'nHumidity', 'nPrecChance', 'nWindDir', 'nWindSpeed',
                          'tempMaxC', 'tempMinC']

  forecast_variables = ['day1', 'day2', 'day3', 'day4', 'day5', 'day6', 'day7']

  context_daily = {}

  #-INFO- Creates data for context_daily
  for i, forecast_var in enumerate(forecast_variables):
      day_data = current_forecasts_data[i]
    
      for j, variable in enumerate(forecast_day_variables):
          context_daily[f'{forecast_var}_{variable}'] = day_data[j]

  #-INFO- Combines context_current and context_daily into one dictionary for render
  context = {
        **context_current,
        **context_daily
    }
  
  return context