import csv
import json
import connectserver

db = connectserver.connectserver()
cursor = db.cursor()

def load():
    with open("loadingconfig.json", "r") as config:
        loadingsetup = json.load(config)

    item = loadingsetup.keys()






if __name__ == "__main__":
    load()