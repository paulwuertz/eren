# ena

Tio estas utilo por skani www.eventoj.hu kaj aûtomate divenas loko por montri en mapo kaj datumo en kalendaro.

Ĝi divenas lokoj per openstreetmaps servilo, kiu vin blokas, se vi tro ofte uzas la `get.py` skripton, sed kelkfoje funkscias. Tamen ne trouzu!

### Ekzemplo

www.p4w5.eu/eo-renkontoj

### Kiel uzi?

Estas simplaj frostitaj HTML paĝoj ;)
Kreebla per...

```bash
#elŝuti nesesaĵoj
pip install -r requirements.txt
#elŝuti renkontaj datumoj
python3 get.py
#frosti HTML kaj servu lokale
python3 app.py
```

Do vi ne bezonas specialan retservilo por ĝin servi, estas enua HTML.

### ideoj

Tio estas tre fuŝa servilo.
Jen sekvaj pasxoj:

* [ ] aldonu funkcionanta datumbazligojn (pagxaro estas sxargxigata de .json datumoj nun)
* [ ] ebligi posti al la datumbazo
* [ ] plibelaspektigi la pagxo en mobila versio
* [ ] aldoni filtrojn en la antauxcode (nur montru eventoj laux datoj, regiono, grandeco...)
* [ ] instali abonu funkcion pere de email laux kriterioj
* [ ] programi A* algorithmo de eventkaravano laux plej malgranda tempa- kaj lokadistanco ^^
