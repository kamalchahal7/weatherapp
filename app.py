import os

from flask_cors import CORS
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functions import usd, fetch

from datetime import datetime
import pytz
utc_time = datetime.now(pytz.timezone('UTC'))
est_time = utc_time.astimezone(pytz.timezone('US/Eastern'))

app = Flask(__name__)
CORS(app)

app.jinja_env.filters["usd"] = usd

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///query.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    """ Main Page """
    if request.method == "GET":
        print("Hello, world.")
        return render_template("query.html")
    else:
        print("Crazy stuff")
        city = request.form.get("city")
        if not city:
            mssg="No input given please try again :("
            return redirect(url_for('error', error=mssg))
        weather_data = fetch(city)
        
        try:
            name = weather_data['name']
            session["search"] = name
            visibility = weather_data['visibility']
            weather = weather_data['weather']
            coord = weather_data['coord']
            main = weather_data['main']
            wind = weather_data['wind']
            cloudiness = weather_data['clouds']
            cc = weather_data['sys']
            try:
                rain = weather_data['rain']['1h']
            except KeyError:
                rain = 0
            try:
                snow = weather_data['snow']['1h']
            except KeyError:
                snow = 0

            db.execute("""INSERT INTO searches (name, longitude, latitude, weather_id, main_desc, 
                        description, icon, temp, feels_like_temp, temp_min, temp_max, pressure, 
                        humidity, visibility, wind_speed, rain, snow, cloudiness, country_code) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", name,
                        coord['lon'], coord['lat'], weather[0]['id'], weather[0]['main'], weather[0]['description'], 
                        weather[0]['icon'], main['temp'], main['feels_like'], main['temp_min'], main["temp_max"], 
                        main['pressure'], main["humidity"], visibility, wind['speed'], rain, snow, cloudiness['all'],
                        cc['country'])
            return redirect("/data")
        except KeyError:
            if weather_data['message']:
                mssg="Not a valid location :("
                return redirect(url_for('error', error=mssg))
            
@app.route("/data", methods=["GET"])
def data():
    """ Weather Data Page """
    if request.method == "GET":
        data = db.execute("SELECT * FROM searches WHERE name = ? ORDER BY time_of_search DESC LIMIT 1", session["search"])
        return render_template("data.html", name=data[0]['name'], long=data[0]['longitude'], lat=data[0]['latitude'], main_desc=data[0]['main_desc'], description=data[0]['description'],
                               icon=data[0]['icon'], temp=data[0]['temp'], feels_like_temp=data[0]['feels_like_temp'], temp_low=data[0]['temp_min'], temp_high=data[0]['temp_max'],
                               pressure=data[0]['pressure'], humidity=data[0]['humidity'], visibility=data[0]['visibility'], wind_speed=data[0]['wind_speed'],
                               rain=data[0]['rain'], snow=data[0]['snow'], cloudiness=data[0]['cloudiness'], URL="http://openweathermap.org/img/wn/", URL2="@2x.png")
    else:
        return redirect("/")
    
@app.route("/history", methods=["GET"])
def history():
    """ Search History Page"""
    data = db.execute("SELECT name, temp, icon, time_of_search FROM searches ORDER BY time_of_search DESC LIMIT 3")
    return render_template("history.html", data=data, URL="http://openweathermap.org/img/wn/", URL2="@2x.png")
    
@app.route("/error")
def error():
    error = request.args.get('error')
    return render_template("error.html", error=error)