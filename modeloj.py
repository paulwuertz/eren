from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Date, String, Text, Float, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import sessionmaker, relationship, backref

import json, os, sys, urllib, datetime
from datetime import timedelta
from sekreta import *
from app import db

Base = declarative_base()

def getEventoj(ekdato=None, findato=None, regionaFiltro=False, tipoj=False):
    if not ekdato: ekdato = datetime.date.today() - datetime.timedelta(days=365*4)
    if not findato: findato = ekdato + datetime.timedelta(days=365*4)
    eventoj = Evento.query.filter(Evento.ektempo > ekdato) \
                          .filter(Evento.fintempo < findato).all()
    return eventoj

class Evento(db.Model):
    __tablename__ = "Evento"
    id = Column(Integer, primary_key=True, unique=True, nullable=False)
    nomo = Column(Text(255), nullable=False)
    organizanto = Column(Text(255), nullable=False)
    lando = Column(Text(255), nullable=False)
    urbo = Column(Text(255), nullable=False)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    grandeco = Column(Integer, nullable=False)
    ektempo = Column(Date, nullable=False)
    fintempo = Column(Date)
    retposxto = Column(Text(255), nullable=False)
    priskribo = Column(Text(), nullable=False)
    link = Column(Text(255), nullable=False)
    logo = Column(Text(255))

    def __init__(self, nomo, organizanto, ektempo, lat, lng, lando, urbo, retposxto, priskribo, link, grandeco, fintempo=None, logo=None):
        print(nomo, organizanto, ektempo, lat, lng, lando, urbo, retposxto, priskribo, link, grandeco, fintempo, logo, end="\n\n")
        self.lat = float(lat)
        self.lng = float(lng)
        self.nomo = nomo.strip()
        self.organizanto = organizanto.strip()
        self.ektempo = datetime.datetime.strptime(ektempo, "%Y-%m-%d").date()
        if fintempo: self.fintempo = datetime.datetime.strptime(fintempo, "%Y-%m-%d").date()
        self.lando = lando.strip()
        self.urbo = urbo.strip()
        self.retposxto = retposxto.strip()
        self.priskribo = priskribo.strip()
        self.link = link.strip()
        self.grandeco = grandeco
        if logo:
            #TODO kontrolu logo kaj savu en datumbazo kiel oktetajxo aux en FS kaj la relativa pos.
            self.logo = logo

    def valida(self):
        problemoj=""
        try:
            if not all([self.nomo, self.organizanto, self.urbo, self.priskribo]): problemoj+= "Bonvole plenigu cxiujn kampojn!</br>"
            #TODO if lando:
            #TODO if retposxto:
            #TODO if link:
            #TODO if grandeco:
            if self.ektempo < datetime.date.today(): problemoj+= "Bonvole elektu validan daton, no en la pasinteco!</br>"
            if self.fintempo and self.ektempo > self.fintempo: problemoj+= "Bonvole elektu validan findaton, post la ekdato!</br>"
            if self.lat > 90 or self.lat < -90 : problemoj+= "Ne validaj latitudaj datoj</br>"
            if self.lng > 180 or self.lng < -180 : problemoj+= "Ne validaj longitudaj datoj</br>"
        except Exception as e:
            print(e)
            return "Tute fiaskis :_("
        if problemoj: return problemoj
        return True

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

    def __repr__(self):
        return '<Evento {0} @ {1}>'.format(self.nomo,self.ektempo)
