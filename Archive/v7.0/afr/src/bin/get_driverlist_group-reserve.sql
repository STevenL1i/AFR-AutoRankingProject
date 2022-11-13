SELECT driverName, driverGroup, team, driverStatus FROM driverList
WHERE (team = "Reserve" OR team = "Retired")
    AND driverGroup = "GROUP" AND driverName != "Race Director"
ORDER BY CASE team
    WHEN "Reserve" THEN 1
    WHEN "Retired" THEN 2
    ELSE 3
END, team, joinTime ASC;