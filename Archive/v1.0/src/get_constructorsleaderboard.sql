SELECT team, driverGroup, AUS_1, AUS_2, totalPoints FROM afr_s7.constructorsLeaderBoard
ORDER BY CASE driverGroup
	WHEN 'A1' THEN 1
    WHEN 'A2' THEN 2
    ELSE 3
    END, driverGroup,
totalPoints DESC;