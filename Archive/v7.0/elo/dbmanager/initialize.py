

import connectserver

db = connectserver.connectserver("43.128.56.235", 3306, "StevenLi", "ABC@1120ab")
cursor = db.cursor()

# get season information
seasoninfo = {}
query = f'SELECT * FROM afr_elo.info'
cursor.execute(query)
result = cursor.fetchall()
for record in result:
    seasoninfo[record[0]] = record[1]
afrdb = seasoninfo["afr_db"]
afecdb = seasoninfo["afec_db"]
elodb = seasoninfo["elo_db"]


def cleardb():
    query = f'DELETE FROM {elodb}.elo'
    cursor.execute(query)
    db.commit()


def initialize_elo():
    if True:
        cleardb()

    
    # copy driverlist from afr database
    query = f'SELECT driverName, driverGroup from {afrdb}.driverList \
              WHERE team != "Team AFR2" AND team != "Team AFR3" \
                AND driverName != "Race Director";'
    cursor.execute(query)
    result = cursor.fetchall()

    for driver in result:
        query = f'INSERT INTO {elodb}.elo VALUES \
                (%s, %s, %s, %s)'
        if driver[1] == "A1":
            val = (driver[0], 750, 750, "Unranked")
        if driver[1] == "A2":
            val = (driver[0], 600, 600, "Unranked")
        if driver[1] == "A3":
            val = (driver[0], 450, 450, "Unranked")
        cursor.execute(query, val)

    db.commit()


def initialize_calander():
    query = f'SELECT * FROM {elodb}.raceCalendar'
    cursor.execute(query)
    result = cursor.fetchall()
    if len(result) != 0:
        return None

    
    # copy race calander from afr and afec database
    query = f'SELECT * FROM {afrdb}.raceCalendar \
             WHERE Round is not null \
             ORDER BY raceDate;'
    cursor.execute(query)
    result_afr = cursor.fetchall()
    query = f'SELECT * FROM {afecdb}.raceCalendar \
             WHERE Round is not null \
             ORDER BY raceDate;'
    cursor.execute(query)
    result_afec = cursor.fetchall()
    
    for race in result_afr:
        query = f'INSERT INTO {elodb}.raceCalendar VALUES \
                  (%s, %s, %s, %s, %s);'
        val = (race[0], race[1], race[2], race[3], race[4])
        cursor.execute(query, val)
    
    for race in result_afec:
        query = f'INSERT INTO {elodb}.raceCalendar VALUES \
                  (%s, %s, %s, %s, %s);'
        val = (race[0], race[1], race[2], race[3], "AFEC")
        cursor.execute(query, val)

    db.commit()

    


def main():
    initialize_elo()
    initialize_calander()


if __name__ == "__main__":
    main()