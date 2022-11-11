import mysql.connector
import csv

db = mysql.connector.connect(
    host = "cdb-6iz6vitj.sg.cdb.myqcloud.com",
    port = "3779",
    user = "root",
    password = "ABC19991120ab",
    database = "afr_s7"
)
cursor = db.cursor()



# dbload driverlist
def load_driverlist():
    query = "CREATE TABLE driverList ( \
    driverName      varchar(30)     NOT NULL, \
    team            varchar(30)     NOT NULL, \
    driverGroup     varchar(7)      NOT NULL, \
    driverStatus    varchar(15)     NOT NULL, \
    joinTime        date            NOT NULL, \
    raceBan         tinyint(2)      DEFAULT NULL, \
    qualiBan        tinyint(2)      DEFAULT NULL, \
    transferToken   tinyint(1)      NOT NULL, \
    PRIMARY KEY (driverName, team, driverGroup));"
    cursor.execute(query)

    file_path = "sourcedata\s7_driverlist.csv"
    with open(file_path) as driverlist:
        reader = csv.DictReader(driverlist)

        for row in reader:
            drivername = row.get("driverName")
            team = row.get("team")
            drivergroup = row.get("driverGroup")
            driverstatus = row.get("driverStatus")
            jointime = row.get("joinTime")
            raceban = row.get("raceBan")
            qualiban = row.get("qualiBan")

            query = "INSERT INTO driverList VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
            val = (drivername,team,drivergroup,driverstatus,jointime,raceban,qualiban,1)
            cursor.execute(query, val)

        db.commit()


# dbload race calendar
def load_calendar():
    query = "CREATE TABLE raceCalendar ( \
    Round           tinyint(2)      NOT NULL, \
    raceDate        date            NOT NULL, \
    GP_CHN          varchar(5)      NOT NULL, \
    GP_ENG          varchar(20)     NOT NULL, \
    driverGroup     varchar(2)      NOT NULL, \
    raceStatus      varchar(10)     NOT NULL, \
    PRIMARY KEY (Round, raceDate, driverGroup));"
    cursor.execute(query)

    file_path = "sourcedata\s7_racecalendar.csv"
    with open(file_path) as racecalendar:
        reader = csv.DictReader(racecalendar)

        for row in reader:
            round = row.get("Round")
            racedate = row.get("raceDate")
            gp_chn = row.get("GP_CHN")
            gp_eng = row.get("GP_ENG")
            drivergroup = row.get("driverGroup")
            racestatus = row.get("raceStatus")

            query = "INSERT INTO raceCalendar VALUES (%s, %s, %s, %s, %s, %s);"
            val = (round, racedate, gp_chn, gp_eng, drivergroup, racestatus)
            cursor.execute(query, val)

        db.commit()


# dbload leaderboard
def load_leaderboard():
    # creating the driver table
    query = "CREATE TABLE driverLeaderBoard ( \
    driverName      varchar(30)     NOT NULL, \
    team            varchar(30)     NOT NULL, \
    driverGroup     varchar(7)      NOT NULL, \
    AUS             tinyint(2)      DEFAULT NULL, \
    AUS_pole        tinyint(1)      DEFAULT NULL, \
    AUS_FL          tinyint(1)      DEFAULT NULL, \
    BHR             tinyint(2)      DEFAULT NULL, \
    BHR_pole        tinyint(1)      DEFAULT NULL, \
    BHR_FL          tinyint(1)      DEFAULT NULL, \
    VNM             tinyint(2)      DEFAULT NULL, \
    VNM_pole        tinyint(1)      DEFAULT NULL, \
    VNM_FL          tinyint(1)      DEFAULT NULL, \
    CHN             tinyint(2)      DEFAULT NULL, \
    CHN_pole        tinyint(1)      DEFAULT NULL, \
    CHN_FL          tinyint(1)      DEFAULT NULL, \
    NLD             tinyint(2)      DEFAULT NULL, \
    NLD_pole        tinyint(1)      DEFAULT NULL, \
    NLD_FL          tinyint(1)      DEFAULT NULL, \
    ESP             tinyint(2)      DEFAULT NULL, \
    ESP_pole        tinyint(1)      DEFAULT NULL, \
    ESP_FL          tinyint(1)      DEFAULT NULL, \
    MCO             tinyint(2)      DEFAULT NULL, \
    MCO_pole        tinyint(1)      DEFAULT NULL, \
    MCO_FL          tinyint(1)      DEFAULT NULL, \
    AZE             tinyint(2)      DEFAULT NULL, \
    AZE_pole        tinyint(1)      DEFAULT NULL, \
    AZE_FL          tinyint(1)      DEFAULT NULL, \
    CAN             tinyint(2)      DEFAULT NULL, \
    CAN_pole        tinyint(1)      DEFAULT NULL, \
    CAN_FL          tinyint(1)      DEFAULT NULL, \
    FRA             tinyint(2)      DEFAULT NULL, \
    FRA_pole        tinyint(1)      DEFAULT NULL, \
    FRA_FL          tinyint(1)      DEFAULT NULL, \
    AUT             tinyint(2)      DEFAULT NULL, \
    AUT_pole        tinyint(1)      DEFAULT NULL, \
    AUT_FL          tinyint(1)      DEFAULT NULL, \
    GBR             tinyint(2)      DEFAULT NULL, \
    GBR_pole        tinyint(1)      DEFAULT NULL, \
    GBR_FL          tinyint(1)      DEFAULT NULL, \
    HUN             tinyint(2)      DEFAULT NULL, \
    HUN_pole        tinyint(1)      DEFAULT NULL, \
    HUN_FL          tinyint(1)      DEFAULT NULL, \
    BEL             tinyint(2)      DEFAULT NULL, \
    BEL_pole        tinyint(1)      DEFAULT NULL, \
    BEL_FL          tinyint(1)      DEFAULT NULL, \
    ITA             tinyint(2)      DEFAULT NULL, \
    ITA_pole        tinyint(1)      DEFAULT NULL, \
    ITA_FL          tinyint(1)      DEFAULT NULL, \
    SGP             tinyint(2)      DEFAULT NULL, \
    SGP_pole        tinyint(1)      DEFAULT NULL, \
    SGP_FL          tinyint(1)      DEFAULT NULL, \
    RUS             tinyint(2)      DEFAULT NULL, \
    RUS_pole        tinyint(1)      DEFAULT NULL, \
    RUS_FL          tinyint(1)      DEFAULT NULL, \
    JPN             tinyint(2)      DEFAULT NULL, \
    JPN_pole        tinyint(1)      DEFAULT NULL, \
    JPN_FL          tinyint(1)      DEFAULT NULL, \
    USA             tinyint(2)      DEFAULT NULL, \
    USA_pole        tinyint(1)      DEFAULT NULL, \
    USA_FL          tinyint(1)      DEFAULT NULL, \
    MEX             tinyint(2)      DEFAULT NULL, \
    MEX_pole        tinyint(1)      DEFAULT NULL, \
    MEX_FL          tinyint(1)      DEFAULT NULL, \
    BRA             tinyint(2)      DEFAULT NULL, \
    BRA_pole        tinyint(1)      DEFAULT NULL, \
    BRA_FL          tinyint(1)      DEFAULT NULL, \
    UAE             tinyint(2)      DEFAULT NULL, \
    UAE_pole        tinyint(1)      DEFAULT NULL, \
    UAE_FL          tinyint(1)      DEFAULT NULL, \
    totalPoints     smallint(4)     NOT NULL, \
    PRIMARY KEY (driverName,team,driverGroup), \
    CONSTRAINT leaderBoard_FK1 FOREIGN KEY (driverName, team, driverGroup) \
        REFERENCES driverList (driverName, team, driverGroup) ON DELETE CASCADE ON UPDATE CASCADE);"
    cursor.execute(query)
    
    file_path = "sourcedata\s7_driverleaderboard.csv"
    with open(file_path) as leaderboard:
        reader = csv.DictReader(leaderboard)
        for row in reader:
            drivername = row.get("driverName")
            team = row.get("team")
            drivergroup = row.get("driverGroup")
            totalpoints = row.get("totalPoints")

            query = "INSERT INTO driverLeaderBoard VALUES (%s, %s, %s, null, null, null, \
            null, null, null, null, null, null, null, null, null, null, null, null, \
            null, null, null, null, null, null, null, null, null, null, null, null, \
            null, null, null, null, null, null, null, null, null, null, null, null, \
            null, null, null, null, null, null, null, null, null, null, null, null, \
            null, null, null, null, null, null, null, null, null, null, null, null, \
            null, null, null, %s);"
            val = (drivername, team, drivergroup, totalpoints)
            cursor.execute(query, val)

        db.commit()


    # creating constructors table
    query = "CREATE TABLE constructorsLeaderBoard ( \
    team            varchar(30)     NOT NULL, \
    driverGroup     varchar(7)      NOT NULL, \
    AUS_1           tinyint(1)      DEFAULT NULL, \
    AUS_2           tinyint(1)      DEFAULT NULL, \
    BHR_1           tinyint(1)      DEFAULT NULL, \
    BHR_2           tinyint(1)      DEFAULT NULL, \
    VNM_1           tinyint(1)      DEFAULT NULL, \
    VNM_2           tinyint(1)      DEFAULT NULL, \
    CHN_1           tinyint(1)      DEFAULT NULL, \
    CHN_2           tinyint(1)      DEFAULT NULL, \
    NLD_1           tinyint(1)      DEFAULT NULL, \
    NLD_2           tinyint(1)      DEFAULT NULL, \
    ESP_1           tinyint(1)      DEFAULT NULL, \
    ESP_2           tinyint(1)      DEFAULT NULL, \
    MCO_1           tinyint(1)      DEFAULT NULL, \
    MCO_2           tinyint(1)      DEFAULT NULL, \
    AZE_1           tinyint(1)      DEFAULT NULL, \
    AZE_2           tinyint(1)      DEFAULT NULL, \
    CAN_1           tinyint(1)      DEFAULT NULL, \
    CAN_2           tinyint(1)      DEFAULT NULL, \
    FRA_1           tinyint(1)      DEFAULT NULL, \
    FRA_2           tinyint(1)      DEFAULT NULL, \
    AUT_1           tinyint(1)      DEFAULT NULL, \
    AUT_2           tinyint(1)      DEFAULT NULL, \
    GBR_1           tinyint(1)      DEFAULT NULL, \
    GBR_2           tinyint(1)      DEFAULT NULL, \
    HUN_1           tinyint(1)      DEFAULT NULL, \
    HUN_2           tinyint(1)      DEFAULT NULL, \
    BEL_1           tinyint(1)      DEFAULT NULL, \
    BEL_2           tinyint(1)      DEFAULT NULL, \
    ITA_1           tinyint(1)      DEFAULT NULL, \
    ITA_2           tinyint(1)      DEFAULT NULL, \
    SGP_1           tinyint(1)      DEFAULT NULL, \
    SGP_2           tinyint(1)      DEFAULT NULL, \
    RUS_1           tinyint(1)      DEFAULT NULL, \
    RUS_2           tinyint(1)      DEFAULT NULL, \
    JPN_1           tinyint(1)      DEFAULT NULL, \
    JPN_2           tinyint(1)      DEFAULT NULL, \
    USA_1           tinyint(1)      DEFAULT NULL, \
    USA_2           tinyint(1)      DEFAULT NULL, \
    MEX_1           tinyint(1)      DEFAULT NULL, \
    MEX_2           tinyint(1)      DEFAULT NULL, \
    BRA_1           tinyint(1)      DEFAULT NULL, \
    BRA_2           tinyint(1)      DEFAULT NULL, \
    UAE_1           tinyint(1)      DEFAULT NULL, \
    UAE_2           tinyint(1)      DEFAULT NULL, \
    totalPoints     smallint(4)     NOT NULL, \
    PRIMARY KEY (team,driverGroup));"
    cursor.execute(query)

    file_path = "sourcedata\s7_constructorleaderboard.csv"
    with open(file_path) as leaderboard:
        reader = csv.DictReader(leaderboard)
        for row in reader:
            team = row.get("team")
            drivergroup = row.get("driverGroup")
            totalpoints = row.get("totalPoints")

            query = "INSERT INTO constructorsLeaderBoard VALUES (%s, %s, null, null, null, null, \
            null, null, null, null, null, null, null, null, null, null, null, null, \
            null, null, null, null, null, null, null, null, null, null, null, null, \
            null, null, null, null, null, null, null, null, null, null, null, null, \
            null, null, null, null, %s);"
            val = (team, drivergroup, totalpoints)
            cursor.execute(query, val)

        db.commit()



# dbload license point
def load_licensepoint():
    query = "CREATE TABLE licensePoint ( \
    driverName      varchar(30)     NOT NULL, \
    driverGroup     varchar(7)      NOT NULL, \
    AUS             tinyint(2)      DEFAULT NULL, \
    BHR             tinyint(2)      DEFAULT NULL, \
    VNM             tinyint(2)      DEFAULT NULL, \
    CHN             tinyint(2)      DEFAULT NULL, \
    NLD             tinyint(2)      DEFAULT NULL, \
    ESP             tinyint(2)      DEFAULT NULL, \
    MCO             tinyint(2)      DEFAULT NULL, \
    AZE             tinyint(2)      DEFAULT NULL, \
    CAN             tinyint(2)      DEFAULT NULL, \
    FRA             tinyint(2)      DEFAULT NULL, \
    AUT             tinyint(2)      DEFAULT NULL, \
    GBR             tinyint(2)      DEFAULT NULL, \
    HUN             tinyint(2)      DEFAULT NULL, \
    BEL             tinyint(2)      DEFAULT NULL, \
    ITA             tinyint(2)      DEFAULT NULL, \
    SGP             tinyint(2)      DEFAULT NULL, \
    RUS             tinyint(2)      DEFAULT NULL, \
    JPN             tinyint(2)      DEFAULT NULL, \
    USA             tinyint(2)      DEFAULT NULL, \
    MEX             tinyint(2)      DEFAULT NULL, \
    BRA             tinyint(2)      DEFAULT NULL, \
    UAE             tinyint(2)      DEFAULT NULL, \
    warning         decimal(3,1)    DEFAULT NULL, \
    totalLicensePoint tinyint(2)    NOT NULL, \
    PRIMARY KEY (driverName,driverGroup), \
    KEY licensePoint_FK_idx (driverName,driverGroup), \
    KEY licensePoint_FK_idx1 (driverGroup), \
    CONSTRAINT licensePoint_FK FOREIGN KEY (driverName) \
        REFERENCES driverList (driverName) ON DELETE CASCADE ON UPDATE CASCADE);"
    cursor.execute(query)

    file_path = "sourcedata\s7_licensepoint.csv"
    with open(file_path) as licensepoint:
        reader = csv.DictReader(licensepoint)
        for row in reader:
            drivername = row.get("driverName")
            drivergroup = row.get("driverGroup")
            warning = row.get("warning")
            totalLP = row.get("totalLicensePoint")

            query = "INSERT INTO licensePoint VALUES (%s, %s, null, null, null, null, \
            null, null, null, null, null, null, null, null, null, null, null, null, \
            null, null, null, null, null, null, %s, %s);"
            val = (drivername, drivergroup, warning, totalLP)
            cursor.execute(query, val)

        db.commit()


        


# other tables
def other_tables():
    query = "CREATE TABLE qualiResult ( \
    driverGroup     varchar(7)      NOT NULL, \
    GP              varchar(15)     NOT NULL, \
    position        tinyint(2)      NOT NULL, \
    driverName      varchar(30)     NOT NULL, \
    team            varchar(30)     NOT NULL, \
    fastestLap      varchar(8)      DEFAULT NULL, \
    tyre            varchar(1)      DEFAULT NULL, \
    driverStatus    varchar(10)     NOT NULL, \
    PRIMARY KEY (driverGroup,GP,position), \
    KEY qualiResult_idx (driverName), \
    CONSTRAINT qualiResult_FK1 FOREIGN KEY (driverName) \
    REFERENCES driverList (driverName) ON DELETE NO ACTION ON UPDATE NO ACTION);"
    cursor.execute(query)

    query = "CREATE TABLE raceResult ( \
    driverGroup     varchar(7)      NOT NULL, \
    GP              varchar(15)     NOT NULL, \
    finishPosition  tinyint(2)      NOT NULL, \
    driverName      varchar(30)     NOT NULL, \
    team            varchar(30)     NOT NULL, \
    startPosition   tinyint(2)      NOT NULL, \
    fastestLap      varchar(8)      DEFAULT NULL, \
    driverStatus    varchar(10)     NOT NULL, \
    PRIMARY KEY (driverGroup,GP,finishPosition), \
    KEY raceResult_FK1_idx (driverName), \
    CONSTRAINT raceResult_FK1 FOREIGN KEY (driverName) \
    REFERENCES driverList (driverName) ON DELETE NO ACTION ON UPDATE NO ACTION);"
    cursor.execute(query)

    query = "CREATE TABLE raceDirector ( \
    CaseNumber          varchar(4)      NOT NULL, \
    CaseDate            date            NOT NULL, \
    driverName          varchar(30)     NOT NULL, \
    driverGroup         varchar(7)      NOT NULL, \
    GP                  varchar(15)     NOT NULL, \
    penalty             varchar(40)     NOT NULL, \
    penaltyLP           tinyint(2)      NOT NULL, \
    penaltyWarning      tinyint(1)      DEFAULT NULL, \
    PenaltyDescription  varchar(500)    DEFAULT NULL, \
    PRIMARY KEY (CaseNumber,CaseDate), \
    KEY raceDirector_FK_idx (driverName), \
    CONSTRAINT raceDirector_FK FOREIGN KEY (driverName) \
    REFERENCES driverList (driverName) ON DELETE NO ACTION ON UPDATE NO ACTION);"
    cursor.execute(query)

    query = "CREATE TABLE driverTransfer ( \
    driverName      varchar(30)     NOT NULL, \
    team1           varchar(30)     NOT NULL, \
    driverGroup1    varchar(2)      NOT NULL, \
    team2           varchar(30)     NOT NULL, \
    driverGroup2    varchar(2)      NOT NULL, \
    description     varchar(45)     DEFAULT NULL, \
    transferTime    date            NOT NULL, \
    tokenUsed       tinyint(1)      NOT NULL, \
    PRIMARY KEY (driverName,team1, driverGroup1));"
    cursor.execute(query)

    query = "CREATE TABLE LANusername ( \
    driverName      varchar(30)     NOT NULL, \
    username        varchar(30)     NOT NULL, \
    password        varchar(35)     NOT NULL, \
    accountStatus   varchar(20)     NOT NULL, \
    PRIMARY KEY (driverName,username,password));"
    cursor.execute(query)

    file_path = "sourcedata\s7_lanusername.csv"
    with open(file_path) as username:
        reader = csv.DictReader(username)
        for row in reader:
            drivername = row.get("driverName")
            username = row.get("username")
            password = row.get("password")
            status = row.get("accountStatus")

            query = "INSERT INTO LANusername VALUES (%s, %s, %s, %s);"
            val = (drivername, username, password, status)
            cursor.execute(query, val)
    db.commit()
    

def main():
    #load_driverlist()
    #load_calendar()
    load_leaderboard()
    #load_licensepoint()
    #other_tables()
    pass

main()