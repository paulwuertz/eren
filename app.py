import json
import os, sys
from flask import Flask, render_template
import urllib
from flask_frozen import Freezer

DEBUG = True

app = Flask(__name__)
freezer = Freezer(app)
app.config.from_object(__name__)

def readJSON(file):
    with open("renkontoj/"+str(file)+".json","r") as fi:
        data=json.loads(fi.read())
    return data

WWW="http://www.p4w5.eu/eo-renkontoj"
jaroj=range(1996,2018)

@freezer.register_generator
def jare():
    for jar in range(1996,2018):
        yield {'jar': jar}
@app.route('/<jar>/')
def jare(jar):
    return render_template('home.html',jar=jar ,jaroj=jaroj, renoj=readJSON(jar),WWW=WWW)

@app.route('/')
def hejme():
    return render_template('home.html',jaroj=jaroj, hejm=True,WWW=WWW)

if __name__ == '__main__':
    freezer.freeze()
    app.run(port=5000)
