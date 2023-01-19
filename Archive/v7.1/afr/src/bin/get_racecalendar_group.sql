SELECT Round, raceDate, GP_CHN, GP_ENG, driverGroup, raceStatus
FROM raceCalendar
WHERE driverGroup = "GROUP"
ORDER BY raceDate ASC;