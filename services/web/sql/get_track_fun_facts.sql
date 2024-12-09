SELECT 
        "Grand Prix"
        , "Fact1"
        , "Fact2"
        , "Fact3"
        , "Fact4"
        , "Fact5"
FROM "Track_Metadata"
WHERE 
  "Round" = {EventNumber}
