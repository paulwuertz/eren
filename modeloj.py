from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Date, String, Text, Float, ForeignKey, Boolean, MetaData, Table
from sqlalchemy.orm import sessionmaker, relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

import json, os, sys, urllib, datetime
from datetime import timedelta
from sekreta import *
from app import db

Base = declarative_base()
meta = MetaData()
meta.bind = db

def getEventoj(ekdato=None, findato=None, regionaFiltro=False, tipoj=False):
    if not ekdato: ekdato = datetime.date.today() - datetime.timedelta(days=365*4)
    if not findato: findato = ekdato + datetime.timedelta(days=365*4)
    eventoj = Evento.query.filter(Evento.ektempo > ekdato) \
                          .filter(Evento.ektempo < findato).all()
    return eventoj

def TableAsDict(self):
    return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}

#tio estas aux simpla uzanto aux organizacio, kiu organizas eventoj
class Uzanto(db.Model, UserMixin):
    __tablename__ = 'uzanto'
    nomo = db.Column(db.Text(128), index=True, unique=True, primary_key=True)
    email = db.Column(db.Text(120), index=True, unique=True)
    password_hash = db.Column(db.Text(128))
    logo = Column(Text(255))
    priskribo = Column(Text(255))

    isOrganizacio =  Column(Boolean(), default=True, nullable=True)
    orga_mallongigo = Column(Text(255), unique=True)
    ligilo = Column(Text(255))

    def __init__(self, nomo, ligilo=None, email=None, password_hash=None, logo=None, isOrganizacio=None, priskribo=None, orga_mallongigo=None):
        self.nomo = nomo
        self.email = email
        self.password_hash = password_hash
        self.logo = logo
        self.isOrganizacio = isOrganizacio
        self.priskribo = priskribo
        self.orga_mallongigo = orga_mallongigo

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
        return '<User {}>'.format(self.nomo)

class GxeneralaEvento(db.Model):
    __tablename__ = "gxeneralaEvento"
    nomo = Column(Text(128), unique=True, nullable=False)
    evento_mallongigo = Column(Text(32), primary_key=True, unique=True, nullable=False)
    ligilo = Column(Text(255))
    pri_gxi = Column(Text(255))
    cxefteamo = Column(Text(255), ForeignKey('teamo.nomo'))
    ofteco = Column(Integer)
    grandeco = Column(Integer)
    logo = Column(Text(255))
    ektempo = Column(Date, nullable=False)
    fintempo = Column(Date)

class Teamo(db.Model):
    __tablename__ = "teamo"
    nomo = Column(Text(255), primary_key=True, unique=True, nullable=False)
    priskribo = Column(Text(255))
    ligilo = Column(Text(255))
    priskribo = Column(Text())
    logo = Column(Text(255))

class TeamMembroj(db.Model):
    __tablename__ = 'teammembroj'
    teamo_nomo = Column(Text(), ForeignKey('teamo.nomo'), primary_key=True, nullable=False)
    uzanto_nomo = Column(Text(), ForeignKey('uzanto.orga_mallongigo'), primary_key=True, nullable=False)

#tio estas gxenerala evento, kiu
class Evento(db.Model):
    __tablename__ = "evento"
    nomo = Column(Text(255), nullable=False, primary_key=True)
    ektempo = Column(Date, nullable=False)
    fintempo = Column(Date)
    grandeco = Column(Integer)
    retposxto = Column(Text(255))
    priskribo = Column(Text())
    ligilo = Column(Text(255))#, nullable=False)
    logo = Column(Text(255))

    urbo = Column(Text(255))#, nullable=False)
    lando = Column(Text(255))#, nullable=False)
    regiono = Column(Text(255))#, nullable=False)
    posxtcodo = Column(Text(255))
    lat = Column(Float)#, nullable=False)
    lon = Column(Float)#, nullable=False)
    isLokaEvento = Column(Boolean(), default=True, nullable=True)
    cxijarateamo = Column(Text(255), ForeignKey('teamo.nomo'))
    gxeneralaEvento = Column(Text, ForeignKey('gxeneralaEvento.evento_mallongigo'))

    def __init__(self, nomo, ektempo, gxeneralaEvento=None, ligilo=None, lat=None, lon=None, priskribo=None, grandeco=None, retposxto=None, fintempo=None, logo=None, urbo=None, lando=None, regiono=None, posxtcodo=None):
        self.nomo = nomo.strip()
        self.ektempo = datetime.datetime.strptime(ektempo, "%Y-%m-%d").date()
        if fintempo: self.fintempo = datetime.datetime.strptime(fintempo, "%Y-%m-%d").date()
        if lat:       self.lat = lat
        if lon:       self.lon = lon
        if retposxto: self.retposxto = retposxto.strip()
        if priskribo: self.priskribo = priskribo.strip()
        if ligilo:    self.ligilo = ligilo.strip()
        if grandeco:  self.grandeco = grandeco
        if logo:      self.logo = logo
        if gxeneralaEvento: self.gxeneralaEvento = gxeneralaEvento
        if urbo:      self.urbo = urbo
        if lando:     self.lando = lando
        if regiono:   self.regiono = regiono
        if posxtcodo: self.posxtcodo = posxtcodo

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
        elif grandec==6: return "501-pli"
        else: return None

    def __repr__(self):
        return '<Evento {0} @ {1}>'.format(self.nomo,self.ektempo)


#abono povas esti de evento, organizacio aux regiono
class Abono(db.Model):
    __tablename__ = 'abono'
    abonanto_id = Column(db.Text, ForeignKey('uzanto.nomo'), primary_key=True)
    organiza_id = Column(db.Text, ForeignKey('uzanto.nomo'), nullable=True, primary_key=True)
    evento_id = Column(db.Text, ForeignKey('evento.nomo'), nullable=True, primary_key=True)
    lat = Column(Float, nullable=True, primary_key=True)
    abonoTipo = Column(Text, nullable=False, primary_key=True)
    sendRetPosxto = Column(db.Boolean)
    sendNTagojAntauxe = Column(db.Integer)
    ido = relationship("Evento")
