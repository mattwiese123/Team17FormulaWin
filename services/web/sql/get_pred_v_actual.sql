SELECT 
	p."FullName"
	, p."TeamName"
	, p."CleanPredictedPosition"/10 as "PredPos"
	, p."ActualPosition"
	, l."Logo"
	, d."HeadshotUrl"
FROM
	"Pred" p
	JOIN "Logo_Link" l
	ON l."TeamName" = p."TeamName"
	JOIN "Driver_Info" d
	ON d."FullName" = p."FullName"
WHERE
	p."RoundNumber" = {EventNumber}
	AND d."Event" = {EventNumber}
  AND CASE 
  WHEN {EventNumber} < 21 THEN p."has_rain_R" IN ('false', 'true')
  ELSE p."has_rain_R" IN ('false')
  END
