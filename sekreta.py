import datetime
from jinja2 import Template

GLOBAL = {
    "DEMANDO":"Kiu kiam?",
    "DEMANDO_KONSILO":"Laux respekto al <a href=\'www.andi.tel\'>Andi</a>:<br> Kiu kaj kiam respondas al kiu kiam elpensis Esperanton.<br> Ekzemple la respondo por kiu kiam al kiu elpenis Volapük estus: \'schleyer1880\'",
    "RESPONDO":"zamenhof1887",
    "WWW":"http://www.p4w5.eu/eo-renkontoj",
    'today': datetime.date.today,
    'strptime': datetime.datetime.strptime
}
SECRET_KEY="geheim;)"
