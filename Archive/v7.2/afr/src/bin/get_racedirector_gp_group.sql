SELECT caseNumber, driverName, driverGroup, GP,
       penaltyLP, penaltyWarning, qualiBan, raceBan
FROM raceDirector
WHERE driverGroup = "GROUP" AND GP = "RACE";