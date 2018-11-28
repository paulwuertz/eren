import datetime, json

def toDate(ektempo):
    return datetime.datetime.strptime(ektempo, "%Y-%m-%d").date()

def readJSON(file):
    with open("renkontoj/"+str(file)+".json","r") as fi:
        data=json.loads(fi.read())
    return data
