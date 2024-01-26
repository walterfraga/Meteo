from tkinter import *
from tkinter import ttk
from datetime import datetime
import calendar
from services.GeocodingService import get_location
from services.WeatherService import get_weather


def date_to_day(date):
    datetime_object = datetime.strptime(date, '%Y-%m-%d')
    return calendar.day_name[datetime_object.weekday()]


def initialize_weather_view(weather_view):
    weather_view['columns'] = ('day', 'max', 'min')
    weather_view.column("#0", width=0, stretch=NO)
    weather_view.column("day", anchor=CENTER, width=100)
    weather_view.column("max", anchor=CENTER, width=80)
    weather_view.column("min", anchor=CENTER, width=80)
    weather_view.heading("#0", text="", anchor=CENTER)
    weather_view.heading("day", text="Day", anchor=CENTER)
    weather_view.heading("max", text="Max", anchor=CENTER)
    weather_view.heading("min", text="Min", anchor=CENTER)


def build_weather_table(weather_view, data_dates, data_maximums, data_minimums):
    weather_view.delete(*weather_view.get_children())
    for index in range(7):
        weather_view.insert(parent='', index='end', iid=index, text='',
                            values=(date_to_day(data_dates[index]), data_maximums[index], data_minimums[index]))
    weather_view.grid(column=0, row=2, columnspan=4)

def get_full_location_name(location):
    full_city_name = location['results'][0]['name']
    full_city_name += ', '
    full_city_name += location['results'][0]['country']
    return full_city_name

def submit_clicked(weather_view, full_city_name, city):
    if len(city) > 0:
        location = get_location(city)
        if 'results' not in location.keys():
            print("Unknown city")
            return
        full_city_name.config(text= get_full_location_name(location))
        data = get_weather(str(location['results'][0]['latitude']), str(location['results'][0]['longitude']))
        data_dates = data['daily']['time']
        data_maximums = data['daily']['temperature_2m_max']
        data_minimums = data['daily']['temperature_2m_min']
        build_weather_table(weather_view, data_dates, data_maximums, data_minimums)


def clear_clicked(weather_view, full_city_name, city):
    city.set("")
    full_city_name.config(text="")
    weather_view.delete(*weather_view.get_children())


def main():
    ws = Tk()
    ws.title('Weather')
    ws.geometry('430x225')
    ws['bg'] = '#AC99F2'

    weather_frame = Frame(ws)

    label = ttk.Label(weather_frame, text='Enter city name')
    full_city_name = ttk.Label(weather_frame)

    city = StringVar()
    city_entry = ttk.Entry(weather_frame, textvariable=city)
    city_entry.bind("<Return>", lambda event: submit_clicked(weather_view, full_city_name, city.get()))
    city_entry.focus()

    weather_view = ttk.Treeview(weather_frame)
    submit_button = ttk.Button(weather_frame, text="Submit", command=lambda: submit_clicked(weather_view, full_city_name, city.get()))
    clear_button = ttk.Button(weather_frame, text="Clear", command=lambda: clear_clicked(weather_view, full_city_name, city))

    weather_frame.grid(column=0, row=0)
    label.grid(column=0, row=0)
    city_entry.grid(column=1, row=0)
    submit_button.grid(column=2, row=0)
    clear_button.grid(column=3, row=0)
    full_city_name.grid(column=0, row=1, columnspan=4)

    initialize_weather_view(weather_view)
    ws.bind('<Return>', submit_clicked(weather_view, full_city_name, city.get()))
    ws.mainloop()


if __name__ == "__main__":
    main()
