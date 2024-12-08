select 
    "FullName" AS "Full Name"
    , "TeamName" AS "Team Name"
    ,   "Position_Q" AS "Grid Position"
    ,   ("CleanPredictedPosition" / 10.0)::int8 AS "Predicted Position"
    ,  "ActualPosition" AS "Actual Position" 
from public."Pred"
where "RoundNumber" = {RoundNumber}
AND "has_rain_R" = 'false'
ORDER BY 
  "Actual Position", "Predicted Position"
