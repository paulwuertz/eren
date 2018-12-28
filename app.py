#! /usr/bin/env python
import json, os, sys, urllib, sqlalchemy, datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import create_engine
from flask_login import LoginManager
from jinja2 import Environment

env = Environment(extensions=['jinja2_time.TimeExtension'])

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
