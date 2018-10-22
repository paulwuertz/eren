#! /usr/bin/env python
import json, os, sys, urllib, datetime, sqlalchemy
from flask import Flask, render_template, jsonify

from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email
from flask_wtf.csrf import CSRFProtect

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Date, String, Text, Float, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import sessionmaker, relationship, backref

from sekreta import *

Base = declarative_base()
csrf = CSRFProtect()
class Evento(Base):
	__tablename__ = "Evento"
	id = Column(Integer, primary_key=True, unique=True, nullable=False)
	nomo = Column(Text(255), nullable=False)
	lat = Column(Float, nullable=False)
	lng = Column(Float, nullable=False)
	grandeco = Column(Integer, nullable=False)
	ektiempo = Column(Date, nullable=False)
	fintempo = Column(Date, nullable=False)
	retposxto = Column(Text(255), nullable=False)
	priskribo = Column(Text(), nullable=False)
	link = Column(Text(255), nullable=False)
	loko = Column(Text(255), nullable=False)
	logo = Column(Text(255))

	def __init__(self, nomo=None, ektiempo=None, fintempo=None, latlng=None, retposxto=None, priskribo=None, link=None, loko=None, logo=None):
		self.lat, self.lng = latlng
		self.nomo = nomo
		self.ektiempo = ektiempo
		self.fintempo = fintempo
		self.retposxto = retposxto
		self.priskribo = priskribo
		self.link = link
		self.loko = loko
		if  logo:
			#TODO kontrolu logo kaj savu en datumbazo kiel oktetajxo aux en FS kaj la relativa pos.
			self.logo = logo

	def grandeco2str(self, grandec):
		if grandec==0: return "1-20"
		elif grandec==1: return "20-30"
		elif grandec==2: return "31-50"
		elif grandec==3: return "51-100"
		elif grandec==4: return "101-200"
		elif grandec==5: return "201-500"
		elif grandec==6: return "501-1000"
		elif grandec==7: return "1001-pli"
		else: return None

def readJSON(file):
    with open("renkontoj/"+str(file)+".json","r") as fi:
        data=json.loads(fi.read())
    return data

WWW="http://www.p4w5.eu/eo-renkontoj"
app = Flask(__name__)
jaroj=range(1996,2018)

@app.route('/<jar>/')
def jare(jar):
    return render_template('home.html',jar=jar ,jaroj=jaroj, GLOBAL=GLOBAL, renoj=readJSON(jar),WWW=WWW)

@app.route('/')
def hejme():
	print(GLOBAL)
	return render_template('home.html',jaroj=jaroj, GLOBAL=GLOBAL, hejm=True,WWW=WWW)

@app.route('/aldoniEventon', methods=["POST"])
def aldoniEventon():
	#se mankas enda datumero redonu eraron
	if not (latlng and nomo and ektiempo and fintempo and retposxto and priskribo and link and loko):
		return jsonify({"succeson":False,"messagxo":"latlng %s nomo %s ektiempo %s fintempo %s retposxto %s priskribo %s link %s loko %s" % [not not o for o in [latlng and nomo and ektiempo and fintempo and retposxto and priskribo and link and loko]]})
	else:
		pass
	return render_template('home.html',jaroj=jaroj, hejm=True,WWW=WWW)

DEBUG = True
if __name__ == '__main__':
    if "genDB" in sys.argv:
           print('running eren ' + sqlalchemy.__version__)
           engine = create_engine(r'sqlite:///eren.db', echo=True) #connect to database
           Base.metadata.create_all(engine) #Lets create the actual sqlite database and schema!
           print('database created: eren.db')
           exit()
    app.secret_key=SECRET_KEY
    csrf.init_app(app)
    app.run(port=5000, debug=True)
