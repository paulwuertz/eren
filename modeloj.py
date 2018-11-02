from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Date, String, Text, Float, ForeignKey
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import sessionmaker, relationship, backref

from sekreta import *

Base = declarative_base()
class Evento(Base):
	__tablename__ = "Evento"
	id = Column(Integer, primary_key=True, unique=True, nullable=False)
	nomo = Column(Text(255), nullable=False)
	organizanto = Column(Text(255), nullable=False)
	lando = Column(Text(255), nullable=False)
	urbo = Column(Text(255), nullable=False)
	lat = Column(Float, nullable=False)
	lng = Column(Float, nullable=False)
	grandeco = Column(Integer, nullable=False)
	ektiempo = Column(Date, nullable=False)
	fintempo = Column(Date, nullable=False)
	retposxto = Column(Text(255), nullable=False)
	priskribo = Column(Text(), nullable=False)
	link = Column(Text(255), nullable=False)
	logo = Column(Text(255))

	def __init__(self, nomo, organizanto, ektiempo, lat, lng, lando, urbo, retposxto, priskribo, link, grandeco, fintempo=None, logo=None):
		self.lat = lat
		self.lng = lng
		self.nomo = nomo
		self.organizanto = organizanto
		self.ektiempo = ektiempo
		self.fintempo = fintempo
		self.lando = lando
		self.urbo = urbo
		self.retposxto = retposxto
		self.priskribo = priskribo
		self.link = link
		self.grandeco = grandeco
		if logo:
			#TODO kontrolu logo kaj savu en datumbazo kiel oktetajxo aux en FS kaj la relativa pos.
			self.logo = logo

	#devas esti vlida dato kaj post hodiaux
	def validaDato(self, str):
		try:
			ek=d.datetime.strptime(str,"%d-%m-%Y").date();
			print("pasis", ek>datetime.date.today())
			if ek>datetime.date.today(): return True
		except Exception as e: return False
		return False

	def valida(self):
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
