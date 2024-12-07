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
  AND p."has_rain_R" = 'false'
