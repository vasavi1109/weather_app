# 🌦 Weather App

A real-time weather forecasting desktop application built with **Python**, **Tkinter**, and the **OpenWeatherMap API**. The app fetches current weather data for any city entered by the user and displays it in an intuitive GUI with dynamic icons, temperature, humidity, pressure, visibility, and local time.

## 🚀 Features

- 🌍 Search for weather by city name worldwide
- ⏰ Displays local time using timezone conversion
- 🌡 Shows temperature, humidity, pressure, and visibility
- 🌄 Sunrise and sunset times
- 🌤 Dynamic weather icons based on current conditions
- ⚡ Responsive and multi-threaded for smooth performance

## 🛠 Technologies Used

- Python
- Tkinter (GUI)
- OpenWeatherMap API
- PIL (Pillow)
- timezonefinder
- pytz
- threading

## 🔧 Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/vasavi1109/weather_app.git
   cd weather_app


2. Install the required packages:
   ```bash
   pip install -r requirements.txt
4. Create a config.ini file in the root directory with the following content:
   [Openweather]
api = your_openweathermap_api_key_here
Replace your_openweathermap_api_key_here with your OpenWeatherMap API key.

5. Run the app:
   python weather_app.py
