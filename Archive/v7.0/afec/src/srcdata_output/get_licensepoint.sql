SELECT * FROM licensePoint JOIN driverList
    ON licensePoint.driverName = driverList.driverName
ORDER BY CASE driverList.driverGroup
    WHEN 'A1' THEN 1
    WHEN 'A2' THEN 2
    WHEN 'A3' THEN 3
    ELSE 4
    END, driverList.driverGroup,
CASE driverList.team
    WHEN 'Mercedes AMG' THEN 1
    WHEN 'Red Bull Racing' THEN 2
    WHEN 'McLaren' THEN 3
    WHEN 'Aston Martin' THEN 4
    WHEN 'Alpine' THEN 5
    WHEN 'Ferrari' THEN 6
    WHEN 'Alpha Tauri' THEN 7
    WHEN 'Alfa Romeo' THEN 8
    WHEN 'Haas' THEN 9
    WHEN 'Williams' THEN 10
    WHEN 'Reserve' THEN 11
    ELSE 12
    END, driverList.team,
CASE driverList.driverStatus
    WHEN '1st driver' THEN 1
    WHEN '2ed driver' THEN 2
    WHEN '3rd driver' THEN 3
    ELSE 4
    END, driverList.driverStatus,
driverList.driverName ASC