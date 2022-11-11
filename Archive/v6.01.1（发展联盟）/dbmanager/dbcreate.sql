create table driverList
(
    driverName  varchar(30) not null,
    team        varchar(30) not null,
    driverGroup varchar(8)  not null,
    joinTime    date        not null,
    primary key (driverName, team, driverGroup)
);

create table raceCalendar
(
    Round       tinyint     null,
    raceDate    date        not null,
    GP_CHN      varchar(5)  not null,
    GP_ENG      varchar(20) not null,
    driverGroup varchar(8)  not null,
    raceStatus  varchar(15) not null,
    primary key (raceDate, driverGroup)
);

create index CK1
    on raceCalendar (GP_ENG, driverGroup);

create table driverLeaderBoard
(
    driverName  varchar(30) not null,
    team        varchar(30) not null,
    driverGroup varchar(8)  not null,
    totalPoints smallint    null,
    primary key (driverName, team, driverGroup),
    constraint leaderBoard_FK1
        foreign key (driverName, team, driverGroup) references driverList (driverName, team, driverGroup)
            on update cascade on delete cascade
);

create table qualiResult
(
    driverGroup  varchar(8)  not null,
    GP           varchar(15) not null,
    driverName   varchar(30) not null,
    team         varchar(30) not null,
    fastestLap   varchar(8)  null,
    driverStatus varchar(10) not null,
    primary key (driverGroup, GP, driverName),
    constraint qualiResult_FK1
        foreign key (driverName) references driverList (driverName)
            on update cascade on delete cascade
);

create index qualiResult_idx
    on qualiResult (driverName);

create table raceResult
(
    driverGroup   varchar(8)     not null,
    GP            varchar(15)    not null,
    driverName    varchar(30)    not null,
    team          varchar(30)    not null,
    startPosition tinyint        not null,
    fastestLap    varchar(8)     null,
    laps          tinyint        not null,
    totaltime     varchar(10)    not null,
    totaltime_sec decimal(10, 3) not null,
    penalty       tinyint        not null,
    driverStatus  varchar(10)    not null,
    primary key (driverGroup, GP, driverName),
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
    driverGroup        varchar(8)   not null,
    GP                 varchar(15)  not null,
    penalty            varchar(10)  not null,
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
    driverName   varchar(30) not null,
    team1        varchar(30) not null,
    driverGroup1 varchar(8)  not null,
    team2        varchar(30) not null,
    driverGroup2 varchar(8)  not null,
    description  varchar(45) null,
    transferTime date        not null,
    primary key (driverName, team1, driverGroup1, team2, driverGroup2, transferTime),
    constraint driverTransfer_FK
        foreign key (driverName) references driverList (driverName)
            on update cascade on delete cascade
);