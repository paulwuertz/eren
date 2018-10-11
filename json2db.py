# -*- coding: utf-8 -*-
# Tio dosiero estas un skripto, ke transformas la kde4 tradukajn dosierojo al un .sqlite dosiero...
import os, json, sqlalchemy
from datetime import datetime
from sqlite3 import *
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from app import Evento
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///eren.db')
Session = sessionmaker()
session = Session.configure(bind=engine)
session = Session()
# Construct a sessionmaker object

#faras espereble la skripto kurebla de skript- kaj cxefdosierujo
eren_jsons = ["renkontoj/"+f for f in os.listdir("renkontoj") if ".json" in f]

# Insert a row of data
for jaro in eren_jsons:
    jjaro = json.load(open(jaro))
    for evento in jjaro:
        nomo, ektiempo, fintempo, latlng, retposxto, priskribo, link, loko, logo = [None for i in range(9)]
        if "periodo" in evento and "ektago" in evento["periodo"] and "ekmonato" in evento["periodo"]:
            ektiempo=datetime.datetime.strptime(jaro[-9:-5]+"-"+evento["periodo"]["ekmonato"]+"-"+evento["periodo"]["ektago"], "%Y-%m-%d")
            if "fintago" in evento["periodo"] and "finmonato" in evento["periodo"]:
                fintempo=datetime.datetime.strptime(jaro[-9:-5]+"-"+evento["periodo"]["finmonato"]+"-"+evento["periodo"]["fintago"], "%Y-%m-%d")
            if "fintago" in evento["periodo"]:
                fintempo=datetime.datetime.strptime(jaro[-9:-5]+"-"+evento["periodo"]["ekmonato"]+"-"+evento["periodo"]["fintago"], "%Y-%m-%d")
        if "lat" in evento and  "lon" in evento:  latlng = (evento["lat"],evento["lon"])
        if "mail" in evento: retposxto=evento["mail"]
        if "text" in evento: priskribo=evento["text"]
        if "link" in evento: link=evento["link"]
        if "loko" in evento: loko=evento["loko"]
        if "logo" in evento: logo=evento["logo"]
        if "nomo" in evento: nomo=evento["nomo"]
        ev=Evento(nomo=nomo, ektiempo=ektiempo, fintempo=fintempo, latlng=latlng, retposxto=retposxto, priskribo=priskribo, link=link, loko=loko, logo=logo)
        session.add(ev)
session.commit()
        #print(evento)
        ##etikedo_str = [etikedo_,sekcio_]+[trd_json[sekcio_][etikedo_][lang] if lang in trd_json[sekcio_][etikedo_] else "" for lang in langs]
        #c.execute("INSERT INTO trd VALUES (%s)" % ",".join(["?"]*len(cols)), etikedo_str)

# Save (commit) the changes
#conn.commit()
#conn.close()
