import configparser
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import threading
import requests
import datetime
import pytz
from timezonefinder import TimezoneFinder
class WeatherApp(Tk):
    def __init__(self):
        super().__init__()
        self.title("Weather App")
        self.geometry("800x480")
        self.iconbitmap(r"Images/weather_icon.ico")
        self.resizable(False, False)
        threading.Thread(target=self.build_interface).start()

    def build_interface(self):
        self.border_image = ImageTk.PhotoImage(Image.open(r"Images/black_border.png").resize((275, 35)))
        Label(image=self.border_image).place(x=20, y=20)

        self.search_icon = ImageTk.PhotoImage(Image.open(r"Images/search_btn.png").resize((29, 29)))
        Button(image=self.search_icon, bg="black", command=self.fetch_thread).place(x=297, y=22)
        self.bind("<Return>", self.fetch_thread)

        self.city_name = StringVar()
        Entry(textvariable=self.city_name, font=("Segoe UI", 14, 'bold'), width=24, justify="center", relief="flat").place(x=25, y=25)

        Label(text="Current Weather :", font='Arial 14 bold', fg="red").place(x=590, y=7)

        self.location_icon = ImageTk.PhotoImage(Image.open(r'Images/location.png').resize((20, 20)))
        Label(image=self.location_icon).place(x=595, y=36)
        self.city_display = Label(text='', font='Calibri 15')
        self.city_display.place(x=620, y=34)

        self.city_time = Label(text="", font=("Cambria", 16))
        self.city_time.place(x=590, y=60)

        self.weather_icon = ImageTk.PhotoImage(Image.open(r"Icons/main.png").resize((200, 190)))
        self.weather_image_label = Label(image=self.weather_icon)
        self.weather_image_label.place(x=70, y=110)

        self.temp_label = Label(text="", font=("Cambria", 75, 'bold'))
        self.temp_label.place(x=270, y=140)
        self.temp_unit = Label(text="", font="Cambria 40 bold")
        self.temp_unit.place(x=390, y=135)

        self.feels_like = Label(text="", font=("Nirmala UI", 16, "bold"))
        self.feels_like.place(x=280, y=245)

        self.sunrise_icon = ImageTk.PhotoImage(Image.open(r"Images/sunrise.png").resize((40, 40)))
        Label(image=self.sunrise_icon).place(x=560, y=150)
        self.sunrise_info = Label(text="Sunrise : ", font=("Segoe UI", 14, 'bold'))
        self.sunrise_info.place(x=603, y=155)

        self.sunset_icon = ImageTk.PhotoImage(Image.open(r"Images/sunset.png").resize((40, 30)))
        Label(image=self.sunset_icon).place(x=560, y=215)
        self.sunset_info = Label(text="Sunset : ", font=("Segoe UI", 14, 'bold'))
        self.sunset_info.place(x=603, y=210)

        self.bottom_bar = ImageTk.PhotoImage(Image.open(r'Images/bottom_bar.png').resize((770, 70)))
        Label(image=self.bottom_bar, bg='#00b7ff').place(x=5, y=330)

        Label(text="Humidity", font="Calibri 15 bold", bg='#00b7ff', fg='white').place(x=35, y=335)
        Label(text="Pressure", font="Calibri 15 bold", bg='#00b7ff', fg='white').place(x=210, y=335)
        Label(text="Description", font="Calibri 15 bold", bg='#00b7ff', fg='white').place(x=400, y=335)
        Label(text="Visibility", font="Calibri 15 bold", bg='#00b7ff', fg='white').place(x=600, y=335)

        self.humidity_display = Label(text="", font=("Calibri", 15, 'bold'), bg='#00b7ff', fg='black')
        self.humidity_display.place(x=50, y=361)

        self.pressure_display = Label(text="", font=("Calibri", 15, 'bold'), bg='#00b7ff', fg='black')
        self.pressure_display.place(x=203, y=361)

        self.description_display = Label(text="", font=("Calibri", 15, 'bold'), bg='#00b7ff', fg='black')
        self.description_display.place(x=405, y=361)

        self.visibility_display = Label(text="", font=("Calibri", 15, 'bold'), bg='#00b7ff', fg='black')
        self.visibility_display.place(x=610, y=361)

        Button(text='Exit', font=("Georgia", 16, "bold"), bg='orange', fg='black', width=7, relief='groove', command=self.exit_app).place(x=680, y=420)
        Button(text='Reset', font=("Georgia", 16, "bold"), bg='orange', fg='black', width=7, relief='groove', activebackground="blue", activeforeground='white', command=self.reset_fields).place(x=560, y=420)

    def fetch_weather_data(self):
        try:
            city = self.city_name.get()
            config = configparser.ConfigParser()
            config.read("config.ini")
            api_key = config['Openweather']['api']
            endpoint = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}'
            response = requests.get(endpoint).json()
            self.update_weather(response)

        except requests.exceptions.ConnectionError:
            messagebox.showwarning('Connect', "Connect to The internet")
        except:
            messagebox.showerror('Error', "An Error Occurred. Try again later!")

    def update_weather(self, weather):
        if weather['cod'] == '404':
            messagebox.showerror("Error", "City Not Found")
            self.city_name.set("")
        elif weather['cod'] == '400':
            messagebox.showinfo("Warning", 'Enter a city name')
            self.city_name.set('')
        else:
            longitude = weather['coord']['lon']
            latitude = weather['coord']['lat']
            timezone = TimezoneFinder().timezone_at(lng=longitude, lat=latitude)
            current_time = datetime.datetime.now(pytz.timezone(timezone)).strftime("%d/%m/%y  %I:%M %p")

            self.city_time['text'] = current_time
            self.description_display['text'] = weather['weather'][0]['description']

            temp_c = int(weather['main']['temp'] - 273)
            self.temp_label['text'] = temp_c
            self.temp_unit['text'] = "°C"
            self.update_icon(weather['weather'][0]['main'])

            self.feels_like['text'] = f"Feels Like {int(weather['main']['feels_like'] - 273)}° | {weather['weather'][0]['main']}"
            self.humidity_display['text'] = f"{weather['main']['humidity']} %"
            self.pressure_display['text'] = f"{weather['main']['pressure']} mBar"
            self.city_display.config(text=weather['name'])
            self.visibility_display['text'] = f"{int(weather['visibility'] / 1000)} km"
            self.sunrise_info['text'] = f"Sunrise : \n{datetime.datetime.fromtimestamp(int(weather['sys']['sunrise'])).strftime('%d/%m/%y  %I:%M %p')}"
            self.sunset_info['text'] = f"Sunset : \n{datetime.datetime.fromtimestamp(int(weather['sys']['sunset'])).strftime('%d/%m/%y   %I:%M %p')}"

    def update_icon(self, condition):
        icon_map = {
            "Clear": "clear.png",
            "Clouds": "clouds.png",
            "Rain": "rain.png",
            "Haze": "haze.png"
        }
        filename = icon_map.get(condition, "main.png")
        image = Image.open(f"Icons/{filename}").resize((190, 190))
        self.weather_icon = ImageTk.PhotoImage(image)
        self.weather_image_label.configure(image=self.weather_icon)
        self.weather_image_label.image = self.weather_icon

    def reset_fields(self):
        self.description_display.config(text="")
        self.visibility_display.config(text="")
        self.pressure_display.config(text="")
        self.humidity_display.config(text="")
        self.sunset_info.config(text="Sunset :")
        self.sunrise_info.config(text="Sunrise :")
        self.feels_like.config(text="")
        self.temp_unit.config(text="")
        self.temp_label.config(text="")
        self.city_time.config(text="")
        self.city_display.config(text="")
        self.city_name.set("")
        self.update_icon("main")

    def exit_app(self):
        if messagebox.askyesno('Confirmation', "Are you sure you want to exit?"):
            self.destroy()

    def fetch_thread(self, event=0):
        threading.Thread(target=self.fetch_weather_data).start()

if __name__ == "__main__":
    app = WeatherApp()
    app.mainloop()
