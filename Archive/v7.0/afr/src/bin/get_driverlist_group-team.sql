SELECT driverList.driverName, driverList.driverGroup, driverList.team, teamList.teamColor, driverList.driverStatus
FROM driverList LEFT JOIN teamList ON
        driverList.team = teamList.teamName
    AND driverList.driverGroup = teamList.driverGroup
WHERE driverList.driverGroup = "GROUP" AND teamList.teamColor = "THETEAM"
  AND driverList.driverName != "Race Director"
ORDER BY 
/*
    CASE teamList.teamColor
        WHEN "Mercedes AMG" THEN 1
        WHEN "Red Bull Racing" THEN 2
        WHEN "Ferrari" THEN 3
        WHEN "McLaren" THEN 4
        WHEN "Alpine" THEN 5
        WHEN "Alpha Tauri" THEN 6
        WHEN "Aston Martin" THEN 7
        WHEN "Williams" THEN 8
        WHEN "Alfa Romeo" THEN 9
        WHEN "Haas" THEN 10
        ELSE 11
END, teamList.teamColor,

    CASE driverList.driverStatus
        WHEN "1st driver" THEN 1
        WHEN "2ed driver" THEN 2
        WHEN "3rd driver" THEN 3
END, 
*/
driverList.driverStatus ASC, joinTime ASC;