import sys
from services.WeatherService import get_weather, get_full_location_name
from util.DisplayUtil import date_to_day

from services.GeocodingService import get_location


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
    location = get_location(input_city)

    if 'results' not in location.keys():
        print('Unknown city')
        exit(5)
    else:
        print(get_full_location_name(location))
    data = get_weather(str(location['results'][0]['latitude']), str(location['results'][0]['longitude']))
    data_dates = data['daily']['time']
    data_maximums = data['daily']['temperature_2m_max']
    data_minimums = data['daily']['temperature_2m_min']
    output = ''
    for index in range(7):
        output += build_text(data_dates[index], data_maximums[index], data_minimums[index])
    print(output)


if __name__ == "__main__":
    main()
