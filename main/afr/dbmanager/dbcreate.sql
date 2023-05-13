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
    PRIMARY KEY (team,driverGroup),
    constraint constructorsLeaderBoard_fk
        foreign key (team, driverGroup) 
            references teamList (teamName, driverGroup) ON DELETE CASCADE ON UPDATE CASCADE
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

create table registTable (
    driverName  varchar(30) not null,
    team        varchar(30) not null,
    driverGroup varchar(7)  not null,
    GP          varchar(20) not null,
    raceGroup   varchar(7)  not null,
    registTime  datetime    not null,
    primary key (driverName, GP, raceGroup),
    constraint registTable_fk1
        foreign key (driverName) references driverList (driverName)
            on update cascade on delete cascade,
    constraint registTable_fk2
        foreign key (GP, raceGroup) references raceCalendar (GP_ENG, driverGroup)
            on update cascade on delete cascade
);





create or replace view get_raceResult as
select raceResult.* 
from raceResult join raceCalendar on raceResult.driverGroup = raceCalendar.driverGroup
                                 and raceResult.GP = raceCalendar.GP_ENG
where raceCalendar.raceStatus = "FINISHED"
order by raceCalendar.Round, raceCalendar.driverGroup, raceResult.finishPosition;


create or replace view get_qualiResult as
select qualiResult.*
from qualiResult join raceCalendar on qualiResult.driverGroup = raceCalendar.driverGroup
                                  and qualiResult.GP = raceCalendar.GP_ENG
where raceCalendar.raceStatus = "FINISHED"
order by raceCalendar.Round, raceCalendar.driverGroup, qualiResult.position;


create or replace view get_raceDirector as
select raceDirector.*
from raceDirector join raceCalendar on raceDirector.driverGroup = raceCalendar.driverGroup
                                   and raceDirector.GP = raceCalendar.GP_ENG
where raceCalendar.raceStatus = "FINISHED"
order by raceCalendar.Round, raceDirector.CaseNumber;


create or replace view get_driverList as
select driverList.*, teamList.teamColor 
from driverList left join teamList on driverList.team = teamList.teamName
                                  and driverList.driverGroup = teamList.driverGroup;

create or replace view get_raceCalendar as
select Round, raceDate, GP_CHN, GP_ENG, driverGroup, raceStatus
from raceCalendar
order by raceDate ASC;


create or replace view get_driverleaderboard_short as
select driverLeaderBoard.driverName, driverLeaderBoard.team, teamList.teamColor,
       driverLeaderBoard.driverGroup, driverLeaderBoard.totalPoints, licensePoint.totalLicensePoint,
       licensePoint.warning, licensePoint.qualiBan, licensePoint.raceban
from driverLeaderBoard join licensePoint on driverLeaderBoard.driverName = licensePoint.driverName
                       left join teamList on driverLeaderBoard.team = teamList.teamName
                                         and driverLeaderBoard.driverGroup = teamList.driverGroup
order by totalPoints desc;


create or replace view get_consleaderboard_short as
select constructorsLeaderBoard.team, teamList.teamColor,
       constructorsLeaderBoard.driverGroup, constructorsLeaderBoard.totalPoints
from constructorsLeaderBoard join teamList on constructorsLeaderBoard.team = teamList.teamName
                                          and constructorsLeaderBoard.driverGroup = teamList.driverGroup
order by totalPoints desc;






create or replace view get_raceDone as
select * from raceCalendar
where raceStatus = "FINISHED"
order by raceDate;


create or replace view get_registration as
select registTable.driverName, registTable.driverGroup, registTable.team, teamList.teamColor,
       registTable.registTime, licensePoint.qualiBan, licensePoint.raceBan,
       registTable.raceGroup, registTable.GP
from registTable
    left join licensePoint on registTable.driverName = licensePoint.driverName
    left join teamList on registTable.team = teamList.teamName
                      and registTable.driverGroup = teamList.driverGroup
order by registTable.driverGroup asc,
    CASE registTable.team
        WHEN "Reserve" THEN 2
        ELSE 1
        END,
    registTable.registTime asc;