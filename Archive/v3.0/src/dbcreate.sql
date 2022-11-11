CREATE TABLE driverList (
    driverName      varchar(30)     NOT NULL,
    team            varchar(30)     NOT NULL,
    driverGroup     varchar(7)      NOT NULL,
    driverStatus    varchar(15)     NOT NULL,
    joinTime        date            NOT NULL,
    transferToken   tinyint(1)      NOT NULL,
    PRIMARY KEY (driverName,team,driverGroup)
);

CREATE TABLE raceCalendar (
    Round           tinyint(2)      NOT NULL,
    raceDate        date            NOT NULL,
    GP_CHN          varchar(5)      NOT NULL,
    GP_ENG          varchar(20)     NOT NULL,
    driverGroup     varchar(2)      NOT NULL,
    raceStatus      varchar(15)     NOT NULL,
    PRIMARY KEY (Round,raceDate,driverGroup),
    KEY CK1 (GP_ENG,driverGroup)
);

CREATE TABLE driverLeaderBoard (
    driverName      varchar(30)     NOT NULL,
    team            varchar(30)     NOT NULL,
    driverGroup     varchar(7)      NOT NULL,
    AUS             tinyint(2)      DEFAULT NULL,
    BHR             tinyint(2)      DEFAULT NULL,
    VNM             tinyint(2)      DEFAULT NULL,
    CHN             tinyint(2)      DEFAULT NULL,
    NLD             tinyint(2)      DEFAULT NULL,
    ESP             tinyint(2)      DEFAULT NULL,
    MCO             tinyint(2)      DEFAULT NULL,
    AZE             tinyint(2)      DEFAULT NULL,
    CAN             tinyint(2)      DEFAULT NULL,
    FRA             tinyint(2)      DEFAULT NULL,
    AUT             tinyint(2)      DEFAULT NULL,
    GBR             tinyint(2)      DEFAULT NULL,
    HUN             tinyint(2)      DEFAULT NULL,
    BEL             tinyint(2)      DEFAULT NULL,
    ITA             tinyint(2)      DEFAULT NULL,
    SGP             tinyint(2)      DEFAULT NULL,
    RUS             tinyint(2)      DEFAULT NULL,
    JPN             tinyint(2)      DEFAULT NULL,
    USA             tinyint(2)      DEFAULT NULL,
    MEX             tinyint(2)      DEFAULT NULL,
    BRA             tinyint(2)      DEFAULT NULL,
    UAE             tinyint(2)      DEFAULT NULL,
    totalPoints     smallint(4)     NOT NULL,
    PRIMARY KEY (driverName,team,driverGroup),
    CONSTRAINT leaderBoard_FK1 FOREIGN KEY (driverName, team, driverGroup) 
            REFERENCES driverList (driverName, team, driverGroup) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE constructorsLeaderBoard (
    team            varchar(30)     NOT NULL,
    driverGroup     varchar(7)      NOT NULL,
    AUS_1           tinyint(1)      DEFAULT NULL,
    AUS_2           tinyint(1)      DEFAULT NULL,
    BHR_1           tinyint(1)      DEFAULT NULL,
    BHR_2           tinyint(1)      DEFAULT NULL,
    VNM_1           tinyint(1)      DEFAULT NULL,
    VNM_2           tinyint(1)      DEFAULT NULL,
    CHN_1           tinyint(1)      DEFAULT NULL,
    CHN_2           tinyint(1)      DEFAULT NULL,
    NLD_1           tinyint(1)      DEFAULT NULL,
    NLD_2           tinyint(1)      DEFAULT NULL,
    ESP_1           tinyint(1)      DEFAULT NULL,
    ESP_2           tinyint(1)      DEFAULT NULL,
    MCO_1           tinyint(1)      DEFAULT NULL,
    MCO_2           tinyint(1)      DEFAULT NULL,
    AZE_1           tinyint(1)      DEFAULT NULL,
    AZE_2           tinyint(1)      DEFAULT NULL,
    CAN_1           tinyint(1)      DEFAULT NULL,
    CAN_2           tinyint(1)      DEFAULT NULL,
    FRA_1           tinyint(1)      DEFAULT NULL,
    FRA_2           tinyint(1)      DEFAULT NULL,
    AUT_1           tinyint(1)      DEFAULT NULL,
    AUT_2           tinyint(1)      DEFAULT NULL,
    GBR_1           tinyint(1)      DEFAULT NULL,
    GBR_2           tinyint(1)      DEFAULT NULL,
    HUN_1           tinyint(1)      DEFAULT NULL,
    HUN_2           tinyint(1)      DEFAULT NULL,
    BEL_1           tinyint(1)      DEFAULT NULL,
    BEL_2           tinyint(1)      DEFAULT NULL,
    ITA_1           tinyint(1)      DEFAULT NULL,
    ITA_2           tinyint(1)      DEFAULT NULL,
    SGP_1           tinyint(1)      DEFAULT NULL,
    SGP_2           tinyint(1)      DEFAULT NULL,
    RUS_1           tinyint(1)      DEFAULT NULL,
    RUS_2           tinyint(1)      DEFAULT NULL,
    JPN_1           tinyint(1)      DEFAULT NULL,
    JPN_2           tinyint(1)      DEFAULT NULL,
    USA_1           tinyint(1)      DEFAULT NULL,
    USA_2           tinyint(1)      DEFAULT NULL,
    MEX_1           tinyint(1)      DEFAULT NULL,
    MEX_2           tinyint(1)      DEFAULT NULL,
    BRA_1           tinyint(1)      DEFAULT NULL,
    BRA_2           tinyint(1)      DEFAULT NULL,
    UAE_1           tinyint(1)      DEFAULT NULL,
    UAE_2           tinyint(1)      DEFAULT NULL,
    totalPoints     smallint(4)     NOT NULL,
    PRIMARY KEY (team,driverGroup)
);



CREATE TABLE licensePoint (
    driverName      varchar(30)     NOT NULL,
    driverGroup     varchar(7)      NOT NULL,
    AUS             tinyint(2)      DEFAULT NULL,
    BHR             tinyint(2)      DEFAULT NULL,
    VNM             tinyint(2)      DEFAULT NULL,
    CHN             tinyint(2)      DEFAULT NULL,
    NLD             tinyint(2)      DEFAULT NULL,
    ESP             tinyint(2)      DEFAULT NULL,
    MCO             tinyint(2)      DEFAULT NULL,
    AZE             tinyint(2)      DEFAULT NULL,
    CAN             tinyint(2)      DEFAULT NULL,
    FRA             tinyint(2)      DEFAULT NULL,
    AUT             tinyint(2)      DEFAULT NULL,
    GBR             tinyint(2)      DEFAULT NULL,
    HUN             tinyint(2)      DEFAULT NULL,
    BEL             tinyint(2)      DEFAULT NULL,
    ITA             tinyint(2)      DEFAULT NULL,
    SGP             tinyint(2)      DEFAULT NULL,
    RUS             tinyint(2)      DEFAULT NULL,
    JPN             tinyint(2)      DEFAULT NULL,
    USA             tinyint(2)      DEFAULT NULL,
    MEX             tinyint(2)      DEFAULT NULL,
    BRA             tinyint(2)      DEFAULT NULL,
    UAE             tinyint(2)      DEFAULT NULL,
    warning         decimal(3,1)    DEFAULT NULL,
    totalLicensePoint tinyint(2)    NOT NULL,
    raceBan         tinyint(2)      DEFAULT NULL,
    qualiBan        tinyint(2)      DEFAULT NULL,
    PRIMARY KEY (driverName,driverGroup),
    KEY licensePoint_FK_idx (driverName,driverGroup),
    CONSTRAINT licensePoint_FK FOREIGN KEY (driverName) 
            REFERENCES driverList (driverName) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE qualiResult (
    driverGroup     varchar(7)      NOT NULL,
    GP              varchar(15)     NOT NULL,
    position        tinyint(2)      NOT NULL,
    driverName      varchar(30)     NOT NULL,
    team            varchar(30)     NOT NULL,
    fastestLap      varchar(8)      DEFAULT NULL,
    tyre            varchar(1)      DEFAULT NULL,
    driverStatus    varchar(10)     NOT NULL,
    PRIMARY KEY (driverGroup,GP,position),
    KEY qualiResult_idx (driverName),
    CONSTRAINT qualiResult_FK1 FOREIGN KEY (driverName)
        REFERENCES driverList (driverName) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE raceResult (
    driverGroup     varchar(7)      NOT NULL,
    GP              varchar(15)     NOT NULL,
    finishPosition  tinyint(2)      NOT NULL,
    driverName      varchar(30)     NOT NULL,
    team            varchar(30)     NOT NULL,
    startPosition   tinyint(2)      NOT NULL,
    fastestLap      varchar(8)      DEFAULT NULL,
    driverStatus    varchar(10)     NOT NULL,
    PRIMARY KEY (driverGroup,GP,finishPosition),
    KEY raceResult_FK1_idx (driverName),
    CONSTRAINT raceResult_FK1 FOREIGN KEY (driverName)
        REFERENCES driverList (driverName) ON DELETE NO ACTION ON UPDATE NO ACTION
);


CREATE TABLE qualiraceFL (
    GP                  varchar(15)     NOT NULL,
    driverGroup         varchar(7)      NOT NULL,
    qualiFLdriver       varchar(30)     DEFAULT NULL,
    qualiFLteam         varchar(30)     DEFAULT NULL,
    raceFLdriver        varchar(30)     DEFAULT NULL,
    raceFLteam          varchar(30)     DEFAULT NULL,
    raceFLvalidation    tinyint         DEFAULT NULL,
    PRIMARY KEY (GP,driverGroup),
    KEY qualiFL_FK_idx (qualiFLdriver,qualiFLteam),
    KEY raceFL_FK_idx (raceFLdriver,raceFLteam),
    CONSTRAINT gp_FK FOREIGN KEY (GP, driverGroup)
        REFERENCES raceCalendar (GP_ENG, driverGroup) ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT qualiFL_FK FOREIGN KEY (qualiFLdriver, qualiFLteam)
        REFERENCES driverlist (driverName, team) ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT raceFL_FK FOREIGN KEY (raceFLdriver, raceFLteam)
        REFERENCES driverlist (driverName, team) ON DELETE NO ACTION ON UPDATE NO ACTION
);

CREATE TABLE raceDirector (
    CaseNumber          varchar(4)      NOT NULL,
    CaseDate            date            NOT NULL,
    driverName          varchar(30)     NOT NULL,
    driverGroup         varchar(7)      NOT NULL,
    GP                  varchar(15)     NOT NULL,
    penalty             varchar(40)     NOT NULL,
    penaltyLP           tinyint(2)      NOT NULL,
    penaltyWarning      tinyint(1)      DEFAULT NULL,
    qualiBan            tinyint         DEFAULT NULL,
    raceBan             tinyint         DEFAULT NULL,
    PenaltyDescription  varchar(500)    DEFAULT NULL,
    PRIMARY KEY (CaseNumber,CaseDate),
    KEY raceDirector_FK_idx (driverName),
    CONSTRAINT raceDirector_FK FOREIGN KEY (driverName)
        REFERENCES driverList (driverName) ON DELETE CASCADE ON UPDATE CASCADE,
    CONSTRAINT raceDirector_FK2 FOREIGN KEY (GP)
        REFERENCES raceCalendar (GP_ENG) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE driverTransfer (
    driverName      varchar(30)     NOT NULL,
    team1           varchar(30)     NOT NULL,
    driverGroup1    varchar(2)      NOT NULL,
    team2           varchar(30)     NOT NULL,
    driverGroup2    varchar(2)      NOT NULL,
    description     varchar(45)     DEFAULT NULL,
    transferTime    date            NOT NULL,
    tokenUsed       tinyint(1)      NOT NULL,
    PRIMARY KEY (driverName,team1,driverGroup1),
    CONSTRAINT driverTransfer_FK FOREIGN KEY (driverName)
        REFERENCES driverList (driverName) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE LANusername (
    driverName      varchar(30)     NOT NULL,
    username        varchar(30)     NOT NULL,
    password        varchar(35)     NOT NULL,
    accountStatus   varchar(20)     NOT NULL,
    PRIMARY KEY (driverName,username,password)
);