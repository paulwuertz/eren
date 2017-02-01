# ena

Tio estas utilo por skani eventoj.hu kaj aûtomate divenas loko por montri en mapo kaj datumo en kalendaro.

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

Tio estas tre fuŝa servo.
Mi ŝatus:

* ĝin funksciigi per la jaroj antaû 2014 je bazo de datoj de eventoj.hu
* mane korekti lokojn je mapo
* aldoni filtron al mapo, kiu montras la markojn je mapo inter kelkj monatoj