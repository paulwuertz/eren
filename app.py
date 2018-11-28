#! /usr/bin/env python
import json, os, sys, urllib
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import create_engine

from sekreta import *

app = Flask(__name__)
csrf = CSRFProtect()
app.secret_key=SECRET_KEY
csrf.init_app(app)
jaroj=range(1996,2018)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

DEBUG = True

from routes import *
from modeloj import *

if __name__ == '__main__':
    if "genDB" in sys.argv:
           print('running eren ' + sqlalchemy.__version__)
           engine = create_engine(r'sqlite:///eren.db', echo=True) #connect to database
           Base.metadata.create_all(engine) #Lets create the actual sqlite database and schema!
           print('database created: eren.db')
           exit()
    app.run(port=5000, debug=True)
