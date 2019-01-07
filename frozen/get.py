import requests, html, regex, json, sys, os, re
from bs4 import BeautifulSoup
from selenium import webdriver

EVENTOJ_URL="http://www.eventoj.hu/{0}.htm"
jaroj=range(1997, 2019)

#kreu subdusierujoj
if not os.path.exists("renkontoj"):
    os.makedirs("renkontoj")
if not os.path.exists("html"):
    os.makedirs("html")

cxiujEventoj = []

"""
Transformas datumo tielmaniere

"26 februaro" aû         -> 2017-02-26
"26 - 27. februaro" aû   -> 2017-02-26 kaj 2017-02-27
"26. februaro - 8. marto"-> 2017-02-26 kaj 2017-03-08"""
def str2strTempo(datString, ren, jaro):
    datString = datString.lower()
    #sen la punkto, legu la numeroj, kiuj versxajne estas la tag(oj)
    tagoj = [int(dato) for dato in re.split("[- .]", datString) if dato.isdigit()]
    #kontrolu, se enhavas unu aux du monatnomoj
    monatoj=[]
    finjaro=jaro
    if "januar"   in datString and not "decembr"  in datString:  monatoj.append("01")
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
        ren["ekdato"]= "%d-%s-%02d" % (jaro, monatoj[0], tagoj[0])
        if len(monatoj)==2:
            ren["findato"]= "%d-%s-%02d" % (finjaro, monatoj[1], tagoj[1])
        elif len(monatoj)==1:
            ren["ekdato"]= "%d-%s-%02d" % (jaro, monatoj[0], tagoj[0])
            ren["findato"]= "%d-%s-%02d" % (jaro, monatoj[0], tagoj[1])
        else: ren["ekdato"] = None
    elif len(tagoj)==1:
        ren["ekdato"] = "%d-%s-%2d" % (jaro, monatoj[0], tagoj[0])
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
    jar_url=EVENTOJ_URL.format(jar)
    print("Skanas jaron", str(jar), "(", jar_url, ") ...")

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
    erenoj, senlokajrenoj = [], []
    cxijarajEventojCnt = 0
    soup = BeautifulSoup(pagxo,"lxml")
    eblajEventoj = soup.find_all('dt')
    for ren in eblajEventoj:
        eren={}
        try:
            tempo = ren.text
            if len(tempo)>6:
                #sekvaj jaroj en la pagxo estas post h1 elementoj
                eren = str2strTempo(tempo, eren, jar +  len(ren.findAllPrevious("h1")))
            else:
                continue
        except Exception as e :
            print("Ne enhavas daton", tempo, "'E", e, "E'\n")
            continue;
        #try:
        dd=ren.find_next("dd")
        if dd and dd.a:
            eren["nomo"]=dd.a.text
            links = dd.find_all("a", href=True)
            #sercxu retposxtadreso kaj ligilo
            for link in links:
                if "mailto:" in link['href']:
                    eren["mail"]=link['href'].replace("mailto:","")
                else: eren["ligilo"] = link['href']
            #"Junulara Esperanta Semajno JES-2016 - en Waldheim am Brahmsee, norda Germanio."
            #ansxtatauxigu helpas kun kelkaj neregulajxoj
            loko = dd.text.replace("–","-").replace(",","-")
            if "- en " in loko and "." in loko:
                eren["loko"]=loko.split("- en ")[1].split(".")[0]
            eren["text"], update = analizuDDTekston(dd.text)
            if update: eren.update(update)
            eren["tutaTeksto"] = dd.text
            #aldonu al listo por json-dosiero
            if eren["ekdato"]:
                cxijarajEventojCnt+=1
                erenoj.append(eren)
                cxiujEventoj.append(eren)

    print("Trovite "+str(len(eblajEventoj)))
    print("Vere enskanita al datumbaza (pro suficxe da datoj): "+str(cxijarajEventojCnt))

    open("renkontoj/"+str(jar)+".json","w").write(
        json.dumps(erenoj,indent=4,ensure_ascii=False))

print("====================",  "\nEne de cxiuj jaroj")
#savu geocache
print("Entute enkontris "+str(len(cxiujEventoj)), "erenkontigxojn kun geokordinatoj kaj", str(len(senlokajrenoj)) ,"sen")

open("eventoj.json","w").write(
    json.dumps(cxiujEventoj,indent=4,ensure_ascii=False))
open("eventoj_senlokaj.json","w").write(
    json.dumps(senlokajrenoj,indent=4,ensure_ascii=False))
