SELECT
t."X"
, t."Y"
, t."Sector"
, t."DriverNumber"
FROM "Telemetry" t
WHERE 
"Event" = {EventNumber}
AND "DriverNumber" IN {DriverNumbers}

