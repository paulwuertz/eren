#! /usr/bin/env python
import json, os, sys, urllib, datetime, sqlalchemy
from flask import Flask, render_template, jsonify, request

# from flask_wtf import Form
# from wtforms import StringField, PasswordField
# from wtforms.validators import DataRequired, Email
from flask_wtf.csrf import CSRFProtect

# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import Column, Integer, Date, String, Text, Float, ForeignKey
# from sqlalchemy.dialects.mysql import BIGINT
# from sqlalchemy.dialects.mysql import LONGTEXT
# from sqlalchemy.orm import sessionmaker, relationship, backref

from modeloj import *
from sekreta import *


def readJSON(file):
    with open("renkontoj/"+str(file)+".json","r") as fi:
        data=json.loads(fi.read())
    return data

WWW="http://www.p4w5.eu/eo-renkontoj"
app = Flask(__name__)
csrf = CSRFProtect()
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
	#transformi al sxlosil-valorparoj
	form = request.form.to_dict()
	formulareroj = ('nomo', 'organizanto', 'ekdato', 'lat', 'lng', 'lando', 'urbnomo', 'email', 'priskribo', 'website', 'sekreta') #'grandeco')
	print(form)
	#kontrolu cxu cxiuj endaj kampoj ekzistas kaj ke la kampoj estas plenigita
	#se mankas enda datumero redonu eraron
	print([(formularero, formularero in form and form[formularero]) for formularero in formulareroj])
	if not all(formularero in form and form[formularero] for formularero in formulareroj):
		return jsonify({"succeson":False,"messagxo":"Mankaj kampoj!"})
	#krei eventon kiu se validigas
	nEvo = Evento(nomo=form["nomo"], organizanto=form["organizanto"],
	 		ektiempo=form["ekdato"], lat=form["lat"], lng=form["lng"],
			lando=form["lando"], urbo=form["urbnomo"], retposxto=form["email"],
			priskribo=form["priskribo"], link=form["website"], grandeco=form["grandeco"])
	#aldonu neendaj kampoj
	if "fintempo" in form and form["fintempo"].strip(): nEvo.fintempo = form["findato"]
	if "logo" in form and form["logo"].strip(): nEvo.logo = form["logo"]
	valida = nEvo.valida()
	if valida:
		print("BONEGE!")
		return jsonify({"succeson":True,"messagxo":"BONEGE!"})
	else:
		return jsonify({"succeson":False,"messagxo":valida})

	print(form)
	return mankaj
	# else:
	# 	return jsonify({"succeson":True,"messagxo":"latlng %s nomo %s ektiempo %s fintempo %s retposxto %s priskribo %s link %s loko %s" % [not not o for o in [latlng and nomo and ektiempo and fintempo and retposxto and priskribo and link and loko]]})

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
