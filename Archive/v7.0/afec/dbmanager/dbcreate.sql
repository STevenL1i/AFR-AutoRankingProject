create table driverList
(
    driverName    varchar(30) not null,
    team          varchar(30) not null,
    driverGroup   varchar(7)  not null,
    driverStatus  varchar(15) not null,
    joinTime      date        not null,
    transferToken tinyint(1)  not null,
    primary key (driverName, team, driverGroup)
);




create table teamList
(
    teamName      varchar(30) not null
        primary key,
    teamColor     varchar(30) not null,
    teamNameAbbr  varchar(8)  not null,
    driver_1      varchar(30) null,
    driver_2      varchar(30) null,
    driver_3      varchar(30) null,
    driver_4      varchar(30) null,
    transferToken tinyint(1)  not null,
    constraint teamList_fk1
        foreign key (driver_1) references driverList (driverName)
            on update cascade on delete cascade,
    constraint teamList_fk2
        foreign key (driver_2) references driverList (driverName)
            on update cascade on delete cascade,
    constraint teamList_fk3
        foreign key (driver_3) references driverList (driverName)
            on update cascade on delete cascade,
    constraint teamList_fk4
        foreign key (driver_4) references driverList (driverName)
            on update cascade on delete cascade
);


create table raceCalendar
(
    Round      tinyint     not null,
    raceDate   date        not null,
    GP_CHN     varchar(5)  not null,
    GP_ENG     varchar(20) not null,
    raceLength varchar(5)  not null,
    raceStatus varchar(15) not null,
    primary key (Round, raceDate)
);

create index CK1
    on raceCalendar (GP_ENG, raceLength);



create table driverLeaderBoard
(
    driverName  varchar(30) not null,
    team        varchar(30) not null,
    driverGroup varchar(7)  not null,
    totalPoints smallint    null,
    primary key (driverName, team, driverGroup),
    constraint leaderBoard_FK1
        foreign key (driverName, team, driverGroup) references driverList (driverName, team, driverGroup)
            on update cascade on delete cascade
);



create table constructorsLeaderBoard
(
    team        varchar(30) not null,
    driverGroup varchar(7)  not null,
    totalPoints float       null,
    primary key (team, driverGroup)
);



create table licensePoint
(
    driverName        varchar(30)   not null,
    driverGroup       varchar(7)    not null,
    warning           decimal(3, 1) null,
    totalLicensePoint tinyint       null,
    raceBan           tinyint       null,
    qualiBan          tinyint       null,
    primary key (driverName, driverGroup),
    constraint licensePoint_FK
        foreign key (driverName) references driverList (driverName)
            on update cascade on delete cascade
);

create index licensePoint_FK_idx
    on licensePoint (driverName, driverGroup);



create table qualiResult
(
    driverGroup  varchar(7)  not null,
    GP           varchar(15) not null,
    position     tinyint     not null,
    driverName   varchar(30) not null,
    team         varchar(30) not null,
    fastestLap   varchar(8)  null,
    tyre         varchar(1)  null,
    driverStatus varchar(10) not null,
    primary key (driverGroup, GP, position),
    constraint qualiResult_FK1
        foreign key (driverName) references driverList (driverName)
            on update cascade on delete cascade
);

create index qualiResult_idx
    on qualiResult (driverName);



create table raceResult
(
    driverGroup    varchar(7)  not null,
    GP             varchar(15) not null,
    finishPosition tinyint     not null,
    driverName     varchar(30) not null,
    team           varchar(30) not null,
    startPosition  tinyint     not null,
    gap            varchar(15) null,
    driverStatus   varchar(10) not null,
    primary key (driverGroup, GP, finishPosition),
    constraint raceResult_FK1
        foreign key (driverName) references driverList (driverName)
            on update cascade on delete cascade
);

create index raceResult_FK1_idx
    on raceResult (driverName);



create table raceDirector
(
    CaseNumber         varchar(4)   not null,
    CaseDate           date         not null,
    driverName         varchar(30)  not null,
    driverGroup        varchar(7)   not null,
    GP                 varchar(15)  not null,
    penalty            varchar(40)  not null,
    penaltyLP          tinyint      not null,
    penaltyWarning     float        null,
    qualiBan           tinyint      null,
    raceBan            tinyint      null,
    PenaltyDescription varchar(500) null,
    primary key (CaseNumber, CaseDate),
    constraint raceDirector_FK
        foreign key (driverName) references driverList (driverName)
            on update cascade on delete cascade,
    constraint raceDirector_FK2
        foreign key (GP) references raceCalendar (GP_ENG)
            on update cascade on delete cascade
);

create index raceDirector_FK_idx
    on raceDirector (driverName);



create table driverTransfer
(
    driverName    varchar(30) not null,
    team1         varchar(30) not null,
    driverGroup1  varchar(4)  not null,
    team2         varchar(30) not null,
    driverGroup2  varchar(4)  not null,
    description   varchar(45) null,
    transferTime  date        not null,
    tokenUsed     tinyint(1)  not null,
    teamtokenUsed tinyint(1)  not null,
    primary key (driverName, team1, driverGroup1, team2, driverGroup2, transferTime),
    constraint driverTransfer_FK
        foreign key (driverName) references driverList (driverName)
            on update cascade on delete cascade
);