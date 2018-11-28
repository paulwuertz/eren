import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, jsonify, request

from sekreta import *
from helpiloj import *
from modeloj import *
from app import app

@app.route('/<int:jar>/')
def jare(jar):
    return render_template('eventoj.html',jar=jar, GLOBAL=GLOBAL, renoj=readJSON(jar))

@app.route('/eventoj')
def eventoj():
    #ricevi datoj
    hodiaux = datetime.date.today()
    ektempo = request.args.get('ektempo', default = hodiaux, type = toDate)
    fintempo = request.args.get('fintempo', default=hodiaux+datetime.timedelta(weeks=52), type = toDate)
    #filtri la eventoj
    eventoj = getEventoj(ekdato=ektempo, findato=fintempo)
    #la pagxo
    return render_template('eventoj.html',jar=2017, GLOBAL=GLOBAL, renoj=eventoj)

@app.route('/aldoniEventon', methods=["GET","POST"])
def aldoniEventon():
    if request.method == 'GET':
        return render_template('aldoniEventon.html', GLOBAL=GLOBAL, hejm=True)
    #transformi al sxlosil-valorparoj
    if request.method == 'POST':
        form = request.form.to_dict()
        formulareroj = ('nomo', 'organizanto', 'ekdato', 'lat', 'lng', 'lando', 'urbnomo', 'email', 'priskribo', 'website', 'sekreta') #'grandeco')
        print(form)
        #kontrolu cxu cxiuj endaj kampoj ekzistas kaj ke la kampoj estas plenigita
        #se mankas enda datumero redonu eraron
        if not all(formularero in form and form[formularero] for formularero in formulareroj):
            return jsonify({"succeson":False,"messagxo":"Mankaj kampoj!"})
        #krei eventon kiu se validigas
        try:
            nEvo = Evento(nomo=form["nomo"], organizanto=form["organizanto"],
            ektempo=form["ekdato"], lat=form["lat"], lng=form["lng"],
            lando=form["lando"], urbo=form["urbnomo"], retposxto=form["email"],
            priskribo=form["priskribo"], link=form["website"], grandeco=form["grandeco"])
            #aldonu neendaj kampoj
            if "fintempo" in form and form["fintempo"].strip(): nEvo.fintempo = form["findato"]
            if "logo" in form and form["logo"].strip(): nEvo.logo = form["logo"]
            valida = nEvo.valida();
            #se validas aldonu TODO
            if valida==True: return jsonify({"succeson":True,"messagxo":"BONEGE!"})
            #se havas erarmesagxo plendu
            return jsonify({"succeson":False,"messagxo":valida})
        except Exception as e:
            print(e)
            return jsonify({"succeson":False,"messagxo":"Tute fiaskis..."})
        return "Saluton :)"

@app.route('/')
def hejme():
    print(GLOBAL)
    return render_template('home.html', GLOBAL=GLOBAL, hejm=True)
