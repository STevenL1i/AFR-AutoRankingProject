SELECT registTable.driverName, registTable.driverGroup, registTable.team, teamList.teamColor,
       registTable.registTime, licensePoint.qualiBan, licensePoint.raceBan
FROM registTable
    LEFT JOIN licensePoint on registTable.driverName = licensePoint.driverName
    LEFT JOIN teamList on registTable.team = teamList.teamName
                      and registTable.driverGroup = teamList.driverGroup

WHERE registTable.raceGroup = "GROUP" AND registTable.GP = "RACE"
ORDER BY registTable.driverGroup ASC,
    CASE registTable.team
        WHEN "Reserve" THEN 2
        ELSE 1
        END,
    registTable.registTime ASC;