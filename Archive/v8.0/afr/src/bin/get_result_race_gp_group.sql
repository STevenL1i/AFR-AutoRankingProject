SELECT driverGroup, GP, finishPosition, driverName, team,
       startPosition, fastestLap, gap, driverStatus
FROM raceResult
WHERE driverGroup = "GROUP" AND GP = "RACE"
ORDER BY finishPosition ASC;