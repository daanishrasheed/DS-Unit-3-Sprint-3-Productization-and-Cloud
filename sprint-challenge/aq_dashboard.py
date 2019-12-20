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

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return return '<datetime: {} --- value: {}>'.format(self.datetime, self.value)


@APP.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    d = root()
    for res in d:
        record = Record(datetime = res[0], value=res[1])
        DB.session.add(record)
    DB.session.commit()
    return 'Data refreshed!'