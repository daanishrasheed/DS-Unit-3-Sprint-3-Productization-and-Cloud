"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from openaq import OpenAQ
from flask_sqlalchemy import SQLAlchemy

APP = Flask(__name__)

APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(APP)

api = OpenAQ()

@APP.route('/')
def root():
    """Base view."""
    status, body = api.measurements(city='Los Angeles', parameter='pm25')
    l = []
    for x in body['results']:
        value = x['value']
        utc_datetime = x['date']['utc']
        l.append((utc_datetime, value))
    return str(l)