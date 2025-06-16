import os
import requests
from dotenv import load_dotenv
import pprint

# Load environment variables from .env file
load_dotenv()
weather_api_key = os.getenv("WEATHER_API_KEY")

class Weather:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def get_weather(self, city):
        params = {
            "q" : city,
            "appid" : self.api_key,
            "units" : "metric"
        }
        response = requests.get(self.base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            weather_desc = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]
            return {
                "city": city,
                "description": weather_desc,
                "temperature_celsius": temp,
                "humidity": humidity,
                "wind_speed_m_s": wind_speed
            }
        else:
            return {"error": f"Coold not retrieve weather data for {city}"}
        

weather = Weather(api_key=weather_api_key)
result = weather.get_weather("Hyderabad")
pprint.pprint(result)