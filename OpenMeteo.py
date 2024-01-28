import sys
from services.WeatherService import WeatherService
from util.DisplayUtil import date_to_day

from services.GeocodingService import GeocodingService


def build_text(date, maximum, minimum):
    text = date_to_day(date)
    text += " " + str(maximum)
    text += " " + str(minimum)
    text += "\n"
    return text


def main():
    if len(sys.argv) == 1:
        input_city = input('What city would you like to have this weeks forcast?\n')
    else:
        input_city = sys.argv[1]
    geocoding_service = GeocodingService()
    location = geocoding_service.get_location(input_city)

    if location is None:
        print('Unknown city')
        exit(5)
    else:
        print(location.full_city_name)
    weather_service = WeatherService()
    weather = weather_service.get_weather(location.latitude, location.longitude)
    output = ''
    for index in range(7):
        output += build_text(weather.dates[index], weather.maximums[index], weather.minimums[index])
    print(output)


if __name__ == "__main__":
    main()
