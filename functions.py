import os
import uuid
from dotenv import load_dotenv
from cs50 import SQL
from datetime import datetime
from time import time
import pytz
import requests

api_key = os.getenv('api_key')

def usd(value):
    return f"${value:,.2f}"

def fetch(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    weather_data = response.json()
    # Sample Data
    # {
    # "coord": { "lon": -0.13, "lat": 51.51 },
    # "weather": [ { "id": 800, "main": "Clear", "description": "clear sky", "icon": "01d" } ],
    # "main": {
    #     "temp": 289.92,
    #     "feels_like": 287.15,
    #     "temp_min": 288.71,
    #     "temp_max": 290.93,
    #     "pressure": 1012,
    #     "humidity": 56
    # },
    # "name": "London"
    # }
    return(weather_data)

    

