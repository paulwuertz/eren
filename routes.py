import datetime, flask_login, modeloj, json
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, jsonify, request, abort

from sekreta import *
from helpiloj import *
from app import app

def getCxiujEventojDeTeamo(teamo_nomo):
    teamo_evento = {}
    geventoj = modeloj.GxeneralaEvento.query.filter_by(cxefteamo=teamo_nomo).all()
    for g in geventoj:
        eventoj = modeloj.Evento.query.filter_by(gxeneralaEvento=g.evento_mallongigo).all()
        teamo_evento[g] = [modeloj.TableAsDict(e) for e in eventoj]
    return teamo_evento

@app.route('/uzanto/<string:nomo>')
@flask_login.login_required
def uzanto(nomo):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user, posts=posts)

@app.route('/organizacioj/')
def organizacioj():
    uzantoj = modeloj.Uzanto.query.filter_by(isOrganizacio=1).all();
    return render_template('organizacioj.html', uzantoj=uzantoj);

@app.route('/organizacioj/<string:nomo>')
def organizacio(nomo):
    uzanto = modeloj.Uzanto.query.filter_by(isOrganizacio=1) \
                                 .filter_by(orga_mallongigo=nomo).first()
    #se ne ekzistas UZANTo devas esti teamo
    if not uzanto:
        teamo = modeloj.Teamo.query.filter_by(nomo=nomo).first_or_404()
        membroj = [modeloj.Uzanto.query.filter_by(orga_mallongigo=mem.uzanto_nomo).first_or_404() 
                        for mem in modeloj.TeamMembroj.query.filter_by(teamo_nomo=nomo).all()]
        eventoj = getCxiujEventojDeTeamo(teamo.nomo)
        return render_template('organizacio_teamo.html', teamo=teamo, membroj=membroj, eventoj=eventoj);
    teamoj = modeloj.TeamMembroj.query.filter_by(uzanto_nomo=nomo).all()
    koorps = {t.teamo_nomo:getCxiujEventojDeTeamo(t.teamo_nomo) for t in teamoj}
    return render_template('organizacio.html', uzanto=uzanto, koorps=koorps);

@app.route('/follow/<username>')
@flask_login.login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash('You are following {}!'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@flask_login.login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash('User {} not found.'.format(username))
        return redirect(url_for('index'))
    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash('You are not following {}.'.format(username))
    return redirect(url_for('user', username=username))

@app.route('/<int:jar>/')
def jare(jar):
    return render_template('eventoj.html',jar=jar, GLOBAL=GLOBAL, renoj=readJSON(jar))

#pli detaloj pri gxeneralaj regulaj eventoj
@app.route('/evento/<string:evento_mallongigo>')
def gxeneralaEvento(evento_mallongigo):
    gevento = modeloj.GxeneralaEvento.query.filter_by(evento_mallongigo=evento_mallongigo).first_or_404()
    orga = modeloj.Teamo.query.filter_by(nomo=gevento.cxefteamo).first_or_404()
    eventoj = modeloj.Evento.query.filter_by(gxeneralaEvento=evento_mallongigo)\
                                  .order_by(modeloj.Evento.ektempo.desc()).all()
    eventojDicts = [modeloj.TableAsDict(e) for e in eventoj]
    return render_template('gxeneralaEvento.html', GLOBAL=GLOBAL, gevento=gevento, orga=orga, eventoj=eventojDicts)

#listo de gxeneralaj regulaj eventoj
@app.route('/evento/')
def gxeneralajEventoj():
    eventoj = modeloj.GxeneralaEvento.query.all()
    #orga = Evento.query.filter(Evento.ektempo > ekdato)
    return render_template('gxeneralajEventoj.html', GLOBAL=GLOBAL, gevenetoj=eventoj)

#pli detaloj pri evento proksima
@app.route('/eventoj/<string:nomo>')
def konkretaEvento(nomo):
    evento = modeloj.Evento.query.filter_by(nomo=nomo).first_or_404()
    gevento = modeloj.GxeneralaEvento.query \
                     .filter_by(evento_mallongigo=evento.gxeneralaEvento).first_or_404()
    orga = modeloj.Teamo.query.filter_by(nomo=gevento.cxefteamo).first_or_404()
    return render_template('konkretaEvento.html', GLOBAL=GLOBAL, gevento=gevento, evento=modeloj.TableAsDict(evento), orga=orga)

#listo de eventoj konkretas proksimas
@app.route('/eventoj/')
def konkretajEventoj():
    #ricevi datoj
    hodiaux = datetime.date.today()
    ektempo = request.args.get('ektempo', default=hodiaux, type=toDate)
    fintempo = request.args.get('fintempo', default=hodiaux+datetime.timedelta(weeks=52), type=toDate)
    #filtri la eventoj
    eventoj = modeloj.getEventoj(ekdato=ektempo, findato=fintempo)
    eventojDicts = [modeloj.TableAsDict(e) for e in eventoj]
    #la pagxo
    return render_template('konkretajEventoj.html', GLOBAL=GLOBAL, renoj=eventojDicts)

#listo de eventoj konkretas proksimas
@app.route('/vojagxplani/')
def vojagxPlan():
    #ricevi datoj
    hodiaux = datetime.date.today()
    ektempo = request.args.get('ektempo', default=hodiaux, type=toDate)
    fintempo = request.args.get('fintempo', default=hodiaux+datetime.timedelta(weeks=52), type=toDate)
    #filtri la eventoj
    eventoj = modeloj.getEventoj(ekdato=ektempo, findato=fintempo)
    eventojDicts = [modeloj.TableAsDict(e) for e in eventoj]
    #la pagxo
    return render_template('vojagxplani.html', GLOBAL=GLOBAL, renoj=eventojDicts)

@app.route('/aldoniEventon/', methods=["GET","POST"])
def aldoniEventon():
    if request.method == 'GET':
        return render_template('aldoniEventon.html', GLOBAL=GLOBAL)
    #transformi al sxlosil-valorparoj
    if request.method == 'POST':
        form = request.form.to_dict()
        formulareroj = ('nomo', 'organizanto', 'ekdato', 'lat', 'lng', 'lando', 'urbnomo', 'email', 'priskribo', 'website', 'sekreta') #'grandeco')
        print(form)
        #kontrolu cxu cxiuj endaj kampoj ekzistas kaj ke la kampoj estas plenigita
        #se mankas enda datumero redonu eraron
        if not all(formularero in form and form[formularero] for formularero in formulareroj):
            return jsonify({"succeson":False,"messagxo":"Mankaj kampoj!"})
        #krei eventon se validas
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

@app.route('/geocache', methods=["GET","POST"])
def geocachedebug():
    if not app.debug:
        return abort(404)
    if request.method == 'GET':
        geocache = json.load(open("frozen/geocache.json","r"))
        return render_template('korektiGeolibKordinatoj.html', GLOBAL=GLOBAL, geocache=geocache)
    #transformi al sxlosil-valorparoj
    if request.method == 'POST':
        return

@app.route('/')
def hejme():
    print(GLOBAL)
    return render_template('home.html', GLOBAL=GLOBAL)
