SELECT driverLeaderBoard.driverName, driverLeaderBoard.team, teamList.teamColor, 
       driverLeaderBoard.driverGroup, driverLeaderBoard.totalPoints, licensePoint.totalLicensePoint,
       licensePoint.warning, licensePoint.qualiBan, licensePoint.raceban
FROM driverLeaderBoard JOIN licensePoint
  ON driverLeaderBoard.driverName = licensePoint.driverName
                       LEFT JOIN teamList
  ON driverLeaderBoard.team = teamList.teamName
 AND driverLeaderBoard.driverGroup = teamList.driverGroup
WHERE driverLeaderBoard.driverGroup = "GROUP"
ORDER BY totalPoints DESC; 