SELECT 
"X"
, "Y"
, "RPM"
, "Speed"
, "nGear"
, "Throttle"
, "Brake"
, "Sector"
, "Event"
, "DriverNumber"
FROM "Telemetry"
WHERE 
"Event" = {EventNumber}
AND "DriverNumber" IN {DriverNumbers}

