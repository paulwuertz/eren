import urllib.request
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
import json, sys, os

EVENTOJ_URL="http://www.eventoj.hu/{0}.htm"
jaroj=range(1996,2018)
geolocator = Nominatim()

if not os.path.exists("renkontoj"):
    os.makedirs("renkontoj")

def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
    formatStr = "{0:." + str(decimals) + "f}"
    percent = formatStr.format(100 * (iteration / float(total)))
    filledLength = int(round(barLength * iteration / float(total)))
    bar = '█' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percent, '%', suffix)),
    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

def int2tagStr(nombr):
	if str(nombr)==1:
		return "0"+str(nombr)
	else:
		return str(nombr)

"""
Transformas datumo kiel

"26 februaro" aû 
"26 - 27. februaro" aû 
"26. februaro - 8. marto"

kaj redonas vin

{"ektago":"26","ekmonato":"02"}
{"ektago":"26","ekmonato":"02","finmonato":"02""fintago":"27"}
{"ektago":"26","ekmonato":"02","finmonato":"03","fintago":"27"}
"""
def str2strTempo(string):
	tagoj = [int(s) for s in string.replace(".","").split() if s.isdigit()]
	monatoj=[]
	if "januar" in eren["tempo"]:
		monatoj.append("01")
	elif "februar" in eren["tempo"]:
		monatoj.append("02")
	elif "mart" in eren["tempo"]:
		monatoj.append("03")
	elif "april" in eren["tempo"]:
		monatoj.append("04")
	elif "maj" in eren["tempo"]:
		monatoj.append("05")
	elif "juni" in eren["tempo"]:
		monatoj.append("06")
	elif "juli" in eren["tempo"]:
		monatoj.append("07")
	elif "gust" in eren["tempo"]:
		monatoj.append("08")
	elif "septembr" in eren["tempo"]:
		monatoj.append("09")
	elif "oktobr" in eren["tempo"]:
		monatoj.append("10")
	elif "novembr" in eren["tempo"]:
		monatoj.append("11")
	elif "dezembr" in eren["tempo"]:
		monatoj.append("12")

	datumo={}

	if len(tagoj)==2:
		datumo["ektago"]=int2tagStr(tagoj[0])
		datumo["fintago"]=int2tagStr(tagoj[1])
	elif len(tagoj)==1:
		datumo["ektago"]=int2tagStr(tagoj[0])


	if len(monatoj)==2:
		datumo["ekmonato"]=monatoj[0]
		datumo["finmonato"]=monatoj[1]
	elif len(monatoj)==1:
		datumo["ekmonato"]=monatoj[0]
		datumo["finmonato"]=monatoj[0]
	return datumo

for jar in jaroj:
	print("Komencas datumi jaro "+str(jar)+" ...")
	jar_url=EVENTOJ_URL.format(jar)
	print(jar_url)
	pagxo = urllib.request.urlopen(jar_url).read()

	if jar>2001:
		renoj=str(pagxo).split("<dt>")
	else:
		renoj=str(pagxo).split("<DT>")

	erenoj=[]
	cnt,loc=0,0

	for ren in renoj:
		eren={}
		soup = BeautifulSoup(ren,"lxml")

		try:
			eren["tempo"]=soup.find_all('strong')[0].text
			eren["periodo"]=str2strTempo(eren["tempo"])
		except Exception :
			continue;

		try:
			dd=soup.find_all('dd')[0]
			eren["nomo"]=dd.a.text
			eren["mail"]=soup.find_all("a")[-1]["href"].replace("mailto:","")
			eren["link"]=dd.a["href"]
			#"Junulara Esperanta Semajno JES-2016 - en Waldheim am Brahmsee, norda Germanio."
			eren["loko"]=dd.text.split(".")[0].split("- en ")[1]
			eren["text"]=".".join(dd.text.split(".")[1:])
			try:
				location = geolocator.geocode(eren["loko"].split(",")[0])	
				eren["lat"]=location.raw["lat"]
				eren["lon"]=location.raw["lon"]
				loc+=1
			except Exception :
				pass
		except Exception :
			continue;

		cnt+=1
		erenoj.append(eren)
		printProgress(cnt, len(renoj), prefix = 'Progreso:', suffix = ' da renkontiĝoj', barLength = 50)
	            
	print()
	print("Trovite "+str(len(renoj)))
	print("Renkontitaj "+str(cnt))
	print("Lokitaj "+str(loc))

	f=open("renkontoj/"+str(jar)+".json","w")
	f.write(json.dumps(erenoj,indent=4))
	f.close()
