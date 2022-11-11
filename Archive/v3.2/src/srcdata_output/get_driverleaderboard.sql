SELECT * FROM afr_s8.driverLeaderBoard
ORDER BY CASE driverGroup
	WHEN 'A1' THEN 1
    WHEN 'A2' THEN 2
    ELSE 3
    END, driverGroup,
totalPoints DESC;