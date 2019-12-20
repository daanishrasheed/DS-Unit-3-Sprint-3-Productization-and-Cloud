"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask, render_template
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

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return '<datetime {}, value {}>'.format(self.datetime, self.value) 

@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    for data in result:
        datetime = data['date']['utc']
        value = data['value']
        final_record = Record(datetime=datetime, value=value)
        DB.session.add(final_record)
    DB.session.commit()
    return 'Data refreshed!'

@APP.route('/fourth')
def fourthpart():
    s = Record.query.filter(Record.value == 10.0 or Record.value > 10.0).all()
    return str(s)