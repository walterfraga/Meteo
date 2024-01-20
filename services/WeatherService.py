import requests


def get_weather(latitude, longitude):
    result_weather = requests.get(
        url='https://api.open-meteo.com/v1/forecast?latitude=' + latitude + '&longitude=' + longitude + '&hourly=temperature_2m&daily=temperature_2m_max,temperature_2m_min&timezone=auto&forecast_days=16')
    return result_weather.json()
