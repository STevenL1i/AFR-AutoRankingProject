SELECT * FROM afr_s7.licensePoint
ORDER BY CASE driverGroup
    WHEN 'A1' THEN 1
    WHEN 'A2' THEN 2
    WHEN 'A3' THEN 3
    ELSE 4
    END, driverGroup,
driverName ASC;