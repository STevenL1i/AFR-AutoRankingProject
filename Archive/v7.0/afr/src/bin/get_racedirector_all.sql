SELECT CaseNumber, CaseDate, driverName, driverGroup, GP,
       penalty, penaltyLP, penaltyWarning, qualiBan, raceBan, PenaltyDescription
FROM raceDirector
ORDER BY CaseDate ASC, CaseNumber ASC;