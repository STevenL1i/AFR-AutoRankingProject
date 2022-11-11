SELECT driverLeaderBoard.*, teamList.teamColor
FROM driverLeaderBoard LEFT JOIN teamList
  ON driverLeaderBoard.team = teamList.teamName
 AND driverLeaderBoard.driverGroup = teamList.driverGroup
WHERE driverLeaderBoard.driverGroup = "GROUP"
ORDER BY totalPoints DESC;