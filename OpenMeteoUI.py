from tkinter import *
from tkinter import ttk

from OpenMeteo import date_to_day
from services.GeocodingService import get_location
from services.WeatherService import get_weather


class OpenMeteoUI:

    def build_weather_table(self, data_dates, data_maximums, data_minimums):
        self.weather_view.delete(*self.weather_view.get_children())
        for index in range(7):
            self.weather_view.insert(parent='', index='end', iid=index, text='',
                                     values=(
                                     date_to_day(data_dates[index]), data_maximums[index], data_minimums[index]))
        self.weather_view.grid(column=0, row=2, columnspan=4)

    def __init__(self):
        ws = Tk()
        ws.title('Weather')
        ws.geometry('430x225')
        ws['bg'] = '#AC99F2'

        weather_frame = Frame(ws)
        self.weather_view = ttk.Treeview(weather_frame)

        label = ttk.Label(weather_frame, text='Enter city name')
        self.full_city_name = ttk.Label(weather_frame)

        self.city = StringVar()
        city_entry = ttk.Entry(weather_frame, textvariable=self.city)
        city_entry.bind("<Return>", lambda event: submit_clicked(self))
        city_entry.focus()

        submit_button = ttk.Button(weather_frame, text="Submit",
                                   command=lambda: submit_clicked(self))
        clear_button = ttk.Button(weather_frame, text="Clear",
                                  command=lambda: clear_clicked(self))

        weather_frame.grid(column=0, row=0)
        label.grid(column=0, row=0)
        city_entry.grid(column=1, row=0)
        submit_button.grid(column=2, row=0)
        clear_button.grid(column=3, row=0)
        self.full_city_name.grid(column=0, row=1, columnspan=4)

        initialize_weather_view(self)
        ws.bind('<Return>', submit_clicked(self))
        ws.mainloop()


def initialize_weather_view(self):
    self.weather_view['columns'] = ('day', 'max', 'min')
    self.weather_view.column("#0", width=0, stretch=NO)
    self.weather_view.column("day", anchor=CENTER, width=100)
    self.weather_view.column("max", anchor=CENTER, width=80)
    self.weather_view.column("min", anchor=CENTER, width=80)
    self.weather_view.heading("#0", text="", anchor=CENTER)
    self.weather_view.heading("day", text="Day", anchor=CENTER)
    self.weather_view.heading("max", text="Max", anchor=CENTER)
    self.weather_view.heading("min", text="Min", anchor=CENTER)




def get_full_location_name(location):
    full_city_name = location['results'][0]['name']
    full_city_name += ', '
    full_city_name += location['results'][0]['country']
    return full_city_name


def submit_clicked(self):
    if len(self.city.get()) > 0:
        location = get_location(self.city.get())
        if 'results' not in location.keys():
            print("Unknown city")
            return
        self.full_city_name.config(text=get_full_location_name(location))
        data = get_weather(str(location['results'][0]['latitude']), str(location['results'][0]['longitude']))
        data_dates = data['daily']['time']
        data_maximums = data['daily']['temperature_2m_max']
        data_minimums = data['daily']['temperature_2m_min']
        self.build_weather_table(data_dates, data_maximums, data_minimums)


def clear_clicked(self):
    self.city.set("")
    self.full_city_name.config(text="")
    self.weather_view.delete(*self.weather_view.get_children())


if __name__ == "__main__":
    openMeteoUI = OpenMeteoUI()
