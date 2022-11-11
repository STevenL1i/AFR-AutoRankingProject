SELECT driverName, team, driverGroup, AUS, BHR, VNM, CHN, NLD, ESP, MCO, AZE, CAN, FRA, AUT, GBR,
HUN, BEL, ITA, SGP, RUS, JPN, USA, MEX, BRA, UAE, totalPoints
FROM afr_s7.driverLeaderBoard
ORDER BY CASE driverGroup
	WHEN 'A1' THEN 1
    WHEN 'A2' THEN 2
    ELSE 3
    END, driverGroup,
totalPoints DESC;