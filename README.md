# Renkontiĝilo

Tio estas utilo por informi pri esperantaj eventoj, kaj emas helpi organizi informaciojn por la partoprenantoj parte :)

Cxio komencis kun la ideo de skani www.eventoj.hu kaj aûtomate divenas loko por montri eventojn en mapo kaj datumo en kalendaro pli belorganizata.

 La uzo de eventoj.hu kaj la geoservilo estas intersavata nun, por eviti trouzu :)
 Speciale la geoservilo, kiu divenas lokoj per openstreetmaps servilo por la eventoj historiaj - blokis vin antauxe, se vi tro ofte uzas la `get.py` skripton. Ankaux korekti la lokoj nun havas perspektivon ^^

## Kiel komenci?

Por servu lokale agu tio:

```bash
#elŝuti nesesaĵoj
pip install -r requirements.txt
#elŝuti renkontaj datumoj
cd frozen && python get.py && cd ..
#konstrui datumbazo
python3 app.py genDB
#plenigu datumbazo
python populate.py
#servu la retpagxaro lokale @ localhost:5000/
python3 app.py
```

## Ideoj

Tio estas tre fuŝa servilo.
Jen sekvaj pasxoj:

* [ ] aldonu funkcionanta datumbazligojn (pagxaro estas sxargxigata de .json datumoj nun)
* [ ] ebligi posti al la datumbazo
* [ ] korekti la divenitaj lokoj de la eventoj estintaj
* [ ] plibelaspektigi la pagxo en mobila versio
* [ ] aldoni filtrojn en la antauxcode (nur montru eventoj laux datoj, regiono, grandeco...)
* [ ] instali abonu funkcion pere de email laux kriterioj
* [ ] programi A* algorithmo de eventkaravano laux plej malgranda tempa- kaj lokadistanco ^^
* [ ] aldoni ludara (kiuj ludoj estas portotaj por kiu renkontiĝoj), gufuja (same kun teo?) kaj karavana organizhelpiloj

## Frostitaj HTML

La frostita versio versxajne ja estas malfunkcianta nun. Historia verzio estas cxi tie:
www.p4w5.eu/eo-renkontoj
