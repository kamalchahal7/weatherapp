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
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    weather_data = response.json(url)
    print(weather_data)
