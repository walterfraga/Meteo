import requests

from model.Location import Location


class GeocodingService:

    def __init__(self):
        pass

    def get_location(self, city):
        result_city = requests.get(url='https://geocoding-api.open-meteo.com/v1/search?name=' + city)
        json_result = result_city.json()
        print(json_result)
        if 'results' not in json_result.keys():
            return None
        latitude = str(json_result['results'][0]['latitude'])
        longitude = str(json_result['results'][0]['longitude'])

        full_city_name = json_result['results'][0]['name']
        full_city_name += ', '
        if 'country' in json_result['results'][0]:
            full_city_name += json_result['results'][0]['country']
        else:
            full_city_name += 'country code:'
            full_city_name += json_result['results'][0]['country_code']

        return Location(latitude, longitude, full_city_name)



