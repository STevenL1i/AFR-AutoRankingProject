SELECT Round, GP_CHN, GP_ENG, driverGroup, raceStatus
FROM raceCalendar
WHERE driverGroup = "GROUP" AND raceStatus = "STATUS" AND Round is not null
ORDER BY Round ASC;