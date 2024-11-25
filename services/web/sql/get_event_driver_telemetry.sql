SELECT 
*
FROM "Telemetry"
WHERE 
"Event" = {EventNumber}
AND "DriverNumber" IN {DriverNumbers}

