CREATE TABLE raceCalendar (
    Round           tinyint(2)      NULL,
    raceDate        date            NOT NULL,
    GP_CHN          varchar(5)      NOT NULL,
    GP_ENG          varchar(20)     NOT NULL,
    driverGroup     varchar(4)      NOT NULL,
    PRIMARY KEY (raceDate,driverGroup),
    KEY CK1 (GP_ENG,driverGroup)
);