SELECT driverGroup, GP, position, driverName, team, fastestLap, tyre, driverStatus
FROM qualiResult
WHERE driverGroup = "GROUP" AND GP = "RACE"
ORDER BY position ASC;