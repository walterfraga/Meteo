import requests


def get_location(city):
    result_city = requests.get(url='https://geocoding-api.open-meteo.com/v1/search?name=' + city)
    return result_city.json()
