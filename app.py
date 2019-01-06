#! /usr/bin/env python
import os, sys, urllib, sqlalchemy, datetime
from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import create_engine
from flask_login import LoginManager
from jinja2 import Environment

env = Environment(extensions=['jinja2_time.TimeExtension'])

def json_serial(o):
    if   isinstance(o, datetime.date): return o.__str__()
    elif isinstance(o, datetime.datetime): return o.__str__()
    else: return o

from config import Config
from sekreta import *

app = Flask(__name__)
csrf = CSRFProtect()
app.secret_key=SECRET_KEY
csrf.init_app(app)
jaroj=range(1996,2018)
app.config.from_object(Config)
db = SQLAlchemy(app)
login = LoginManager(app)
login.init_app(app)
migrate = Migrate(app, db)

DEBUG = True

def to_str_encoded_json(value):
    return json.dumps(value, default=json_serial)
app.jinja_env.filters['tojson_str_encoded'] = to_str_encoded_json

import tests.populate
from modeloj import *
from routes import *

if __name__ == '__main__':
    if "genDB" in sys.argv:
       os.remove("eren.db") if os.path.exists("eren.db") else None
       engine = create_engine(r'sqlite:///eren.db', echo=False) #connect to database
       db.metadata.create_all(engine) #Lets create the actual sqlite database and schema!
       print('kreis datumbazo: eren.db')
       tests.populate.plenumiDBkunEkzemploj()
    app.run(port=5000, debug=True)
