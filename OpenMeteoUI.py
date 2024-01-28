from tkinter import *
from tkinter import ttk

from services.GeocodingService import GeocodingService
from services.WeatherService import WeatherService


class OpenMeteoUI:

    def build_weather_table(self, data_dates, data_maximums, data_minimums):
        self.weather_view.delete(*self.weather_view.get_children())
        for index in range(7):
            self.weather_view.insert(parent='', index='end', iid=index, text='',
                                     values=(
                                         data_dates[index], data_maximums[index], data_minimums[index]))
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
        city_entry.bind("<Return>", lambda event: self.submit_clicked())
        city_entry.focus()

        submit_button = ttk.Button(weather_frame, text="Submit",
                                   command=lambda: self.submit_clicked())
        clear_button = ttk.Button(weather_frame, text="Clear",
                                  command=lambda: self.clear_clicked())

        weather_frame.grid(column=0, row=0)
        label.grid(column=0, row=0)
        city_entry.grid(column=1, row=0)
        submit_button.grid(column=2, row=0)
        clear_button.grid(column=3, row=0)
        self.full_city_name.grid(column=0, row=1, columnspan=4)

        self.initialize_weather_view()
        ws.bind('<Return>', self.submit_clicked())
        ws.mainloop()

    def clear_clicked(self):
        self.city.set("")
        self.full_city_name.config(text="")
        self.weather_view.delete(*self.weather_view.get_children())

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

    def submit_clicked(self):
        if len(self.city.get()) > 0:
            geocoding_service = GeocodingService()
            location = geocoding_service.get_location(self.city.get())
            if location is None:
                self.clear_clicked()
                self.full_city_name.config(text="Unknown city")
                return
            self.full_city_name.config(text=location.full_city_name)
            weather_service = WeatherService()
            weather = weather_service.get_weather(location.latitude, location.longitude)
            self.build_weather_table(weather.dates, weather.maximums, weather.minimums)


if __name__ == "__main__":
    openMeteoUI = OpenMeteoUI()
