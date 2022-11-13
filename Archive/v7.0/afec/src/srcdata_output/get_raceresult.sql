SELECT * FROM afr_s*.raceResult
ORDER BY driverGroup ASC, CASE GP
	WHEN 'Australia' THEN 1
    WHEN 'Bahrain' THEN 2
    WHEN 'Vietnam' THEN 3
	WHEN 'China' THEN 4
    WHEN 'Netherlands' THEN 5
    WHEN 'Spain' THEN 6
    WHEN 'Monaco' THEN 7
    WHEN 'Azerbaijan' THEN 8
    WHEN 'Canada' THEN 9
    WHEN 'France' THEN 10
    WHEN 'Austria' THEN 11
    WHEN 'Britain' THEN 12
    WHEN 'Hungary' THEN 13
    WHEN 'Belgium' THEN 14
    WHEN 'Italy' THEN 15
    WHEN 'Singapore' THEN 16
    WHEN 'Russia' THEN 17
    WHEN 'Japan' THEN 18
    WHEN 'USA' THEN 19
    WHEN 'Mexico' THEN 20
    WHEN 'Brazil' THEN 21
    WHEN 'Abu Dahbi' THEN 22
    END, GP,
finishPosition ASC;