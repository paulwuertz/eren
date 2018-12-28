import requests, html, regex, json, sys, os
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from selenium import webdriver

EVENTOJ_URL="http://www.eventoj.hu/{0}.htm"
jaroj=range(1997,2019)
geolocator = Nominatim()

if not os.path.exists("renkontoj"):
    os.makedirs("renkontoj")
if not os.path.exists("html"):
    os.makedirs("html")
geocache = {} if not os.path.isfile("geocache.json") else json.load(open("geocache.json","r"))
geoc = 0
geol = 0
cxiujEventoj = []

#Uzu la geopy lib por elsxuti divenata koordinatoj
def getGeoCoords(string):
    global geoc, geol
    if string in geocache:
        geoc+=1
        return geocache[string]
    else:
        geol+=1
        try:
            location = geolocator.geocode(string)
            geocache[string] = location.raw["lat"], location.raw["lon"]
            open("geocache.json","w").write(json.dumps(geocache,indent=4))
            return location.raw["lat"], location.raw["lon"]
        except Exception as e:
            geocache[string] = None, None
            open("geocache.json","w").write(json.dumps(geocache,indent=4,ensure_ascii=False))
            return None, None

"""
Transformas datumo tielmaniere

"26 februaro" aû         -> 2017-02-26
"26 - 27. februaro" aû   -> 2017-02-26 kaj 2017-02-27
"26. februaro - 8. marto"-> 2017-02-26 kaj 2017-03-08"""
def str2strTempo(datString, ren, jaro):
    datString = datString.lower()
    #sen la punkto, legu la numeroj, kiuj versxajne estas la tag(oj)
    tagoj = [s for s in datString.replace("."," ").split() if s.isdigit()]
    #kontrolu, se enhavas unu aux du monatnomoj
    monatoj=[]
    finjaro=jaro
    if "januar"   in datString and not "dezembr"  in datString:  monatoj.append("01")
    if "februar"  in datString:  monatoj.append("02")
    if "mart"     in datString:  monatoj.append("03")
    if "april"    in datString:  monatoj.append("04")
    if "maj"      in datString:  monatoj.append("05")
    if "juni"     in datString:  monatoj.append("06")
    if "juli"     in datString:  monatoj.append("07")
    if "gust"     in datString:  monatoj.append("08")
    if "septembr" in datString:  monatoj.append("09")
    if "oktobr"   in datString:  monatoj.append("10")
    if "novembr"  in datString:  monatoj.append("11")
    if "decembr"  in datString:
        monatoj.append("12")
        if "januar"   in datString:
            monatoj.append("01")
            finjaro=jaro+1

    datumo={}
    #print(datString, jaro,finjaro, monatoj, tagoj)

    if len(tagoj)==2:
        ren["ekdato"]= "%d-%s-%s" % (jaro, monatoj[0], tagoj[0])
        if len(monatoj)==2:
            ren["findato"]= "%d-%s-%s" % (finjaro, monatoj[1], tagoj[1])
        elif len(monatoj)==1:
            ren["ekdato"]= "%d-%s-%s" % (jaro, monatoj[0], tagoj[0])
            ren["findato"]= "%d-%s-%s" % (jaro, monatoj[0], tagoj[1])
        else: ren["ekdato"] = None
    elif len(tagoj)==1:
        ren["ekdato"] = "%d-%s-%s" % (jaro, monatoj[0], tagoj[0])
    else: ren["ekdato"] = None
    return ren

def analizuDDTekston(dd):
    #inf regex - kaj
    spl = regex.split("[\ +]?((Inf)|(Org))[\.]?[\:]?", dd)
    tel = "[\(\)\-\+0-9]{7,}"
    posxtcodo_lando = "[A-Z]{2}[\ -]*[0-9\-]{4,}[\ ]*[\p{L}-\ ]+,\ +[\p{L}-\ ]+"
    text = ".".join(spl[0].split(".")[1:])
    if len(spl)<2: return text, None
    infoj = spl[-1].replace("\n"," ").strip()
    if len(infoj)<=2: return text, None
    #print(infoj)
    trovita = {}
    if regex.search(tel, infoj):
        trovita["tel"] = regex.findall(tel, infoj)[0]
    if regex.search(posxtcodo_lando, infoj):
        trovita["posxtcodo"],trovita["lando"] = regex.findall(posxtcodo_lando, infoj)[0].split(",")
        trovita["posxtcodo"] = trovita["posxtcodo"][3:].strip()
    #print("\t=>",trovita)
    return text, trovita

###############
#######SKRIPTO
###############
for jar in jaroj:
    print("Komencas datumi jaro "+str(jar)+" ...")
    jar_url=EVENTOJ_URL.format(jar)
    print(jar_url)

    #Sxargxu vere aux servo de cache
    if os.path.isfile("html/"+str(jar)+".html"):
        print("Caching","html/"+str(jar)+".html")
        pagxo = open("html/"+str(jar)+".html","r").read()
    else:
        driver = webdriver.Chrome()
        print("Loading","html/"+str(jar)+".html kaj savu por la cache...")
        pagxo = driver.get(jar_url)
        open("html/"+str(jar)+".html","w").write(driver.page_source)
        driver.close()
    erenoj=[]
    cnt,loc=0,0
    soup = BeautifulSoup(pagxo,"lxml")
    eblajEventoj = soup.find_all('dt')
    for ren in eblajEventoj:
        eren={}
        #print(ren,ren.find_all('strong')[0].text,"\n--PPP--\n")
        try:
            tempo = ren.find_all('strong')[0].text
            #sekvaj jaroj en la pagxo estas post h1 elementoj
            eren = str2strTempo(tempo, eren, jar +  len(ren.findAllPrevious("h1")))
        except Exception as e :
            print("ERROR",ren, "'E", e, "E'\n")
            continue;
        #try:
        dd=ren.find_next("dd")
        if dd and dd.a:
            eren["nomo"]=dd.a.text
            links = dd.find_all("a")
            #sercxu retposxtadreso kaj ligilo
            for link in links:
                if link.href:
                    if "mailto:" in link.href:
                        eren["mail"]=link.href.replace("mailto:","")
                    else: eren["link"] = links[0].href
            #"Junulara Esperanta Semajno JES-2016 - en Waldheim am Brahmsee, norda Germanio."
            #ansxtatauxigu helpas kun kelkaj neregulajxoj
            loko = dd.text.replace("–","-").replace(",","-")
            if "- en " in loko and "." in loko:
                eren["loko"]=loko.split("- en ")[1].split(".")[0]
            eren["text"], update = analizuDDTekston(dd.text)
            if update: eren.update(update)
            geoString = ""
            if "lando" in eren and "posxtcodo" in eren:
                geoString = eren["posxtcodo"].split(" ",1)[-1] + " - " + eren["posxtcodo"].split(" ")[0] + eren["lando"]
            elif "loko" in eren: geoString = eren["loko"]
            if geoString: eren["lat"], eren["lon"] = getGeoCoords(geoString)
            loc+=1
        #se havas minimume 4 informacioj uzu kiel evento
        if len(list(eren.values()))-list(eren.values()).count(None)>3 and eren["ekdato"] and eren["text"]:
            cnt+=1
            erenoj.append(eren)
            cxiujEventoj.append(eren)

    print("\nTrovite "+str(len(eblajEventoj)))
    print("Renkontitaj "+str(cnt))
    print("Lokitaj "+str(loc))

    open("renkontoj/"+str(jar)+".json","w").write(
        json.dumps(erenoj,indent=4,ensure_ascii=False)
    )

#savu geocache
print("geosuchen",geoc,"/",geoc+geol)
print("Total renoj "+str(len(cxiujEventoj)))

f=open("eventoj.json","w")
f.write(json.dumps(cxiujEventoj,indent=4,ensure_ascii=False))
f.close()
