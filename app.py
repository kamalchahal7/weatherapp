import os

from flask_cors import CORS
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functions import usd

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



@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    """Main Page"""
    if request.method == "GET":
        print("Hello, world.")
        return render_template("query.html")
    else:
        print("Crazy stuff")
        return redirect("/data")
    
@app.route("/data", methods=["GET", "POST"])
def data():
    if request.method == "GET":
        return render_template("data.html")
    else:
        return redirect("/")