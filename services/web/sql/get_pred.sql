select 
    "FullName" AS "Full Name"
    , "TeamName" AS "Team Name"
    ,   "Position_Q" AS "Grid Position"
    ,   ("CleanPredictedPosition" / 10.0)::int8 AS "Predicted Position"
    ,  "ActualPosition" AS "Actual Position" 
from public."Pred"
where "RoundNumber" = {RoundNumber}
AND CASE 
  WHEN {RoundNumber} < 21 THEN "has_rain_R" IN ('false', 'true')
  ELSE "has_rain_R" IN ('false')
  END
ORDER BY 
  "Actual Position", "Predicted Position"
