SELECT 
        "Round"
        , "Circuit"
        , "Length"
        , "Total Laps"
        , "Turns"
        , "Type"
        , "Direction"
FROM "Track_Metadata"
WHERE 
  "Round" = {EventNumber}
