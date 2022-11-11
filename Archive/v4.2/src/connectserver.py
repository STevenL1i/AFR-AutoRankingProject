import json
import mysql.connector

def connectserver():
    server_connector = {}

    # old way: using cfg file
    """
    file_path = "server.cfg"
    with open(file_path, "r", newline="") as cfg:
        file_list = cfg.readlines()

    for line in file_list:
        line = line.replace("\r", "").replace("\n", "")
        i = 0
        item = ""
        while i < len(line):
            item += line[i]
            if line[i] == "=":
                item = item [:-2]
                i += 2
                parameter = ''
                while i < len(line):
                    parameter += line[i]
                    if i == len(line)-1:
                        server_connector[item] = parameter
                    i += 1
            i += 1
    """

    # new way: using json file
    with open("server.json") as server:
        server_connector = json.load(server)
    
    
    db = mysql.connector.connect(
    host = server_connector["host"],
    port = server_connector["port"],
    user = server_connector["user"],
    password = server_connector["password"],
    database = server_connector["database"])
    return db