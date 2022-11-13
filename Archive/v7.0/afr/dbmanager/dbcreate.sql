CREATE TABLE driverList (
    driverName      varchar(30)     NOT NULL,
    team            varchar(30)     NOT NULL,
    driverGroup     varchar(7)      NOT NULL,
    driverStatus    varchar(15)     NOT NULL,
    joinTime        date            NOT NULL,
    transferToken   tinyint(1)      NOT NULL,
    PRIMARY KEY (driverName)
);

create table teamList (
    teamName      varchar(30) not null,
    teamColor     varchar(30) not null,
    driverGroup  varchar(8)  not null,
    primary key (teamName, driverGroup)
);

CREATE TABLE raceCalendar (
    Round           tinyint(2)      NULL,
    raceDate        date            NOT NULL,
    GP_CHN          varchar(5)      NOT NULL,
    GP_ENG          varchar(20)     NOT NULL,
    driverGroup     varchar(2)      NOT NULL,
    raceStatus      varchar(15)     NOT NULL,
    PRIMARY KEY (raceDate,driverGroup),
    KEY CK1 (GP_ENG,driverGroup)
);

CREATE TABLE driverLeaderBoard (
    driverName      varchar(30)     NOT NULL,
    team            varchar(30)     NOT NULL,
    driverGroup     varchar(7)      NOT NULL,
    totalPoints     smallint(4)     NOT NULL,
    PRIMARY KEY (driverName,driverGroup),
    CONSTRAINT leaderBoard_FK1 
        FOREIGN KEY (driverName) REFERENCES driverList (driverName)
            ON DELETE CASCADE ON UPDATE CASCADE
);


CREATE TABLE constructorsLeaderBoard (
    team            varchar(30)     NOT NULL,
    driverGroup     varchar(7)      NOT NULL,
    totalPoints     smallint(4)     NOT NULL,
    PRIMARY KEY (team,driverGroup)
);



CREATE TABLE licensePoint (
    driverName      varchar(30)     NOT NULL,
    driverGroup     varchar(7)      NOT NULL,
    warning         decimal(3,1)    DEFAULT NULL,
    totalLicensePoint tinyint(2)    NOT NULL,
    raceBan         tinyint(2)      DEFAULT NULL,
    qualiBan        tinyint(2)      DEFAULT NULL,
    PRIMARY KEY (driverName),
    KEY licensePoint_FK_idx (driverName),
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
        REFERENCES driverList (driverName) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE raceResult (
    driverGroup     varchar(7)      NOT NULL,
    GP              varchar(15)     NOT NULL,
    finishPosition  tinyint(2)      NOT NULL,
    driverName      varchar(30)     NOT NULL,
    team            varchar(30)     NOT NULL,
    startPosition   tinyint(2)      NOT NULL,
    fastestLap      varchar(8)      NULL,
    gap            varchar(15)      null,
    driverStatus    varchar(10)     NOT NULL,
    PRIMARY KEY (driverGroup,GP,finishPosition),
    KEY raceResult_FK1_idx (driverName),
    CONSTRAINT raceResult_FK1 FOREIGN KEY (driverName)
        REFERENCES driverList (driverName) ON DELETE CASCADE ON UPDATE CASCADE
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
        REFERENCES raceCalendar (GP_ENG, driverGroup) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE raceDirector (
    CaseNumber          varchar(100)      NOT NULL,
    CaseDate            date            NOT NULL,
    driverName          varchar(30)     NOT NULL,
    driverGroup         varchar(7)      NOT NULL,
    GP                  varchar(15)     NOT NULL,
    penalty             varchar(40)     NOT NULL,
    penaltyLP           tinyint(2)      NOT NULL,
    penaltyWarning      float           DEFAULT NULL,
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

create table driverTransfer (
    driverName          varchar(30) not null,
    team_from           varchar(30) not null,
    driverGroup_from    varchar(2)  not null,
    team_to             varchar(30) not null,
    driverGroup_to      varchar(2)  not null,
    description         varchar(45) null,
    transferTime        date        not null,
    tokenUsed           tinyint(1)  not null,
    primary key (driverName, team_from, driverGroup_from, team_to, driverGroup_to, transferTime),
    constraint driverTransfer_FK
        foreign key (driverName) references driverList (driverName)
            on update cascade on delete cascade
);