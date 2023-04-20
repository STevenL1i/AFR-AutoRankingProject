SELECT constructorsLeaderBoard.*, teamList.teamColor
FROM constructorsLeaderBoard LEFT JOIN teamList
  ON constructorsLeaderBoard.team = teamList.teamName
 AND constructorsLeaderBoard.driverGroup = teamList.driverGroup
WHERE constructorsLeaderBoard.driverGroup = "GROUP"
ORDER BY totalPoints DESC;