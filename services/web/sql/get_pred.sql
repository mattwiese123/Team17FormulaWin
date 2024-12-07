select 
    "FullName"
    , "TeamName"
    ,   "EventFormat"
    ,   "Position_Q" AS "GridPosition"
    ,   ("CleanPredictedPosition" / 10.0)::int8 AS "PredictedPosition"
    ,   "ActualPosition" 
from public."Pred"
where "RoundNumber" = {RoundNumber}
AND "has_rain_R" = 'false'
ORDER BY 
  "ActualPosition", "PredictedPosition"
