import csv, datetime, requests, sys, json, os, re
from sqlalchemy import update
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
sys.path.append("../..")
from modeloj import Teamo, TeamMembroj, GxeneralaEvento, Evento, Uzanto
from app import db

def orga2img(orga, url): return "static/img/organizajBildoj/"+orga+"."+url.split(".")[-1]
def event2img(event, url): return "static/img/eventajBildoj/"+event+"."+url.split(".")[-1]

def savuBildoSeNeEstas(url, path):
    if url!="" and not os.path.isfile(path):
        response = requests.get(url)
        if response.status_code == 200:
            open(path, 'w+b').write(response.content)

stelo="http://podkasto.net/esperanto_pl/wp-content/uploads/2017/11/stelo.jpg"
savuBildoSeNeEstas(stelo, "static/img/stelo.jpg")

def orgaByName(name):
    return session.query(Uzanto).filter_by(uzantnomo=name).all()[0]

def addUzantojKajTeamoj():
    for e in csv.reader(open('tests/csv/uzantoj_orgas.csv'), delimiter=',', skipinitialspace=True):
        #elsxuti eventbildo se ankoraux ne ekzistas
        savuBildoSeNeEstas(e[2], orga2img(e[1], e[2]))
        logo = orga2img(e[1], e[2]).replace("static/","") if e[2]!="" else ""
        db.session.add(Uzanto(e[0], ligilo=e[3], logo=logo, orga_mallongigo=e[1], isOrganizacio=True))
        #aldoni un teamo nur por la orga
        db.session.add(Teamo(nomo=e[1],logo=logo))
        db.session.add(TeamMembroj(teamo_nomo=e[1],uzanto_nomo=e[1]))
    #teamoj de pli ol 2 membroj
    for e in csv.reader(open('tests/csv/orga_teamoj.csv'), delimiter=',', skipinitialspace=True):
        db.session.add(Teamo(nomo=e[1],logo=e[2]))
        GxeneralaEvento.query.filter_by(cxefteamo=e[0]).update({"cxefteamo":e[1]})
        for mem in e[0].split("."):
            db.session.add(TeamMembroj(teamo_nomo=e[1],uzanto_nomo=mem))
    db.session.commit()

def addGeneralajEventoj():
    dummy = "Tio estas evento. Vizitu gxin, gxi estas bona. La homoj gxuas la tempo cxi-tie. Ne povas fari io pli bone ol ir al tio evento!!!"
    for e in csv.reader(open('tests/csv/gxeneralajEventoj.csv'), delimiter=',', skipinitialspace=True):
        teamo = e[2]
        #elsxuti eventbildo se ankoraux ne ekzistas
        savuBildoSeNeEstas(e[6], event2img(e[1], e[6]))
        logo = event2img(e[1], e[6]).replace("static/","") if e[6]!="" else ""
        d = datetime.datetime.strptime(e[3], "%Y-%m-%d").date()
        if e[4]:
            fd = datetime.datetime.strptime(e[3], "%Y-%m-%d").date()
            db.session.add(GxeneralaEvento(nomo=e[0],ligilo=e[5],pri_gxi=dummy,cxefteamo=teamo,ofteco=365,logo=logo,ektempo=d,fintempo=fd, evento_mallongigo=e[1]))
        else:
            db.session.add(GxeneralaEvento(nomo=e[0],ligilo=e[5],pri_gxi=dummy,cxefteamo=teamo,ofteco=365,logo=logo,ektempo=d, evento_mallongigo=e[1]))
    db.session.commit()

def addEventoj():
    sercxoj = [["Printempa Semajno Internacia", "PSI"],["Universala Kongreso de Esperanto", "UK"],["Germana Esperanto-Kongreso", "GEK"],["PRINTEMPaS", "PRINTEMPaS"],["Roskilde", "Roskilde"],["Esperanta Printempo","ŜEP"],["JER"],["IJK"],["SAT"],["IJS"],["KAEST"],["KEKSO"],["ILEI"],["ARKONES"],["BIERo"],["BAVELO"],["NR"],["KoKoLoRES"],["Israela Kongreso", "IKE2"],["Brazila Kongreso de Esperanto", "BKE"],["Skota Kongreso", "SKE"],["Japana Esperanto-Kongreso", "JEK"],["PEKO"],["Centrejo"],["Beneluksa Kongreso", "BEKO"],["Brita", "BK"],["baltia", "BET"],["Sud-Azia", "SAS"],["Internacia Esperanto-Semajno", "IES"],["Mediteranea Esperanto","MES"],["a Mezorienta","MK"],["IREK"],["MeKaRo"],["a Itala Kongreso","IKE"],["BARO"],["Renkontiĝo de Amikoj","RA"],["a ABELO","ABELO"],["Milan Zvara","MZP"],["Blindaj","IKBE"],["IEK"],["Hispana Kongreso","HEK"],["Ŝĉecina Esperanta Printempo","ŜEP"],["somerkursaro","AKE"],["Poludnica"],["Meksika","MEK"],["Rata Rendevuo","RR"],["a Azia","AK"],["AŬTUNE"],["a JES", "JES"],["Junulara Esperanta Semajno","JES"], ["Internacia Junulara Festivalo", "IJF"],["Somera Esperanto-Studado","SES"], ["a Internacia Seminario","IS"],["Ago-Semajno","AS"],["Brita Kongreso de Esperanto","BK"]]
    eventoj = json.load(open("frozen/eventoj.json"))
    ev=None
    for sercxo in sercxoj:
        geStr = sercxo[0] if len(sercxo)==1 else sercxo[1]
        ge = GxeneralaEvento.query.filter(GxeneralaEvento.evento_mallongigo == geStr)[0]
        nedublaj = set()
        for e in eventoj:
            if geStr in e["nomo"] and not (e["ekdato"], ge.nomo + " - " + e["ekdato"][:4], geStr) in nedublaj:
                fin = None if not "findato" in e else e["findato"]
                nomo = ge.nomo + " - " + e["ekdato"][:4]
                priskribo = e["text"] if "text" in e else None
                loko = e["loko"] if "loko" in e else None
                if "posxtcodo" in e:
                    posxtcodo, urbo = re.split("[\- .]", e["posxtcodo"].strip("- \t"), 1)
                else:
                    posxtcodo, urbo = None, None
                lando = e["lando"] if "lando" in e else None
                mail = e["mail"] if "mail" in e else None
                link = e["ligilo"] if "ligilo" in e else None
                lat, lon = (e["lat"], e["lon"]) if "lat" in e else (None, None)
                ev=Evento(nomo=nomo, ektempo=e["ekdato"], fintempo=fin, lat=lat, lon=lon, priskribo=priskribo, gxeneralaEvento=geStr, retposxto=mail, urbo=urbo, lando=lando, regiono=loko, ligilo=link, posxtcodo=posxtcodo)
                db.session.add(ev)
                eventoj.remove(e)
                nedublaj.add((str(ev.ektempo), nomo, ev.gxeneralaEvento))
    db.session.commit()
    print("aldonis %d Eventoj al la testdatumbazo. restas %d eventoj neenigxataj" % (len(db.session.query(Evento).all()), len(eventoj)))
    #skribu restantaj eventoj en datumo
    open("neUzataj.json", "w").write(json.dumps(eventoj, ensure_ascii=False, indent=4))

def plenumiDBkunEkzemploj():
    addGeneralajEventoj()
    print("aldonis Generalaj Eventoj")
    addUzantojKajTeamoj()
    print("aldonis Uzantoj Kaj Teamoj")
    print("aldonas Eventoj")
    addEventoj()

#TODO elsuxtu informoj de asocioj, ligiloj, blabla
def ueaOrgas():
    ueas = ["af","al","dz","ad","ao","ag","ar","am","aw","ai","au","at","az","bs","bd","bb","bh","be","bz","by","bj","bm","mm","bw","bo","ba","br","gb","bn","bg","bf","bi","bt","cf","td","cz","cl","cn","dk","do","dm","ci","eg","ec","gq","ee","er","et","ph","fi","fj","fr","pf","ga","gm","gh","de","gr","gd","gl","gp","gt","gy","gn","gw","gi","dj","ht","in","es","hn","hu","hk","id","iq","ir","ie","is","il","it","jm","jp","ye","jo","cv","cm","kh","ky","ca","ge","qa","kz","ke","kg","ki","cy","co","km","cd","cg","kr","kp","cr","hr","cu","ck","cw","kw","la","lv","ls","lb","lr","ly","li","lt","lu","mg","mo","mk","my","mw","mv","ml","mt","mh","ma","mq","mu","mr","mx","fm","md","mc","ms","mn","me","mz","na","nr","nl","np","ng","ne","ni","no","nc","nz","tl","om","pk","pw","ps","pa","pg","py","pe","pl","pr","pt","re","rw","ro","ru","sv","sb","ws","kn","lc","vc","sm","st","sa","sc","rs","sn","sl","sg","sy","sk","si","so","lk","za","sd","ss","sr","sz","se","ch","tj","th","tw","tz","tg","to","tt","tn","tr","tc","tm","tv","ug","ua","ae","uy","us","uz","vu","va","ve","vn","zm", "zw"]
    ueaLink = "https://uea.org/landoj?korektu={0}"
    for ueaOrga in ueas:
        response = requests.get(url)
if __name__ == '__main__':
    ueaOrgas()

#Evento(nomo, organizanto, ektempo, retposxto, priskribo, link, fintempo=None, logo=None):
#Pola Esperanto 2
#TORPEDo  5x
#SALO 4
#Roma Festivaleto 5
#SEFT 5 -- 140
#POLUDNICA 4
#"KEF", "", "1986-01-01", retposxto, priskribo, link, "img/eventajBildoj/kef.jpg"
