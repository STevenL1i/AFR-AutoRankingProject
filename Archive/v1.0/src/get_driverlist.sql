SELECT driverName, team, driverGroup, driverStatus
FROM afr_s7.driverList
ORDER BY CASE driverGroup
        WHEN 'A1' THEN 1
        WHEN 'A2' THEN 2
        WHEN 'A3' THEN 3
        ELSE 4
        END, driverGroup,
    CASE team
        WHEN 'Mercedes AMG' THEN 1
        WHEN 'Ferrari' THEN 2
        WHEN 'Red Bull Racing' THEN 3
        WHEN 'McLaren' THEN 4
        WHEN 'Racing Point' THEN 5
        WHEN 'Renault' THEN 6
        WHEN 'Alpha Tauri' THEN 7
        WHEN 'Alfa Romeo' THEN 8
        WHEN 'Williams' THEN 9
        WHEN 'Haas' THEN 10
        ELSE 11
        END, team,
driverStatus ASC;"
