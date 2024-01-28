from datetime import datetime
import calendar

import requests
from model.Weather import Weather


class WeatherService:

    def __init__(self):
        pass

    def get_weather(self, latitude, longitude):
        result_weather = requests.get(
            url='https://api.open-meteo.com/v1/forecast?latitude=' + latitude + '&longitude=' + longitude + '&hourly=temperature_2m&daily=temperature_2m_max,temperature_2m_min&timezone=auto&forecast_days=16')
        weather_json = result_weather.json()

        dates = []
        for time in weather_json['daily']['time']:
            dates.append(date_to_day(time))
        maximums = weather_json['daily']['temperature_2m_max']
        minimums = weather_json['daily']['temperature_2m_min']
        return Weather(dates, maximums, minimums)


def date_to_day(date):
    datetime_object = datetime.strptime(date, '%Y-%m-%d')
    return calendar.day_name[datetime_object.weekday()]
