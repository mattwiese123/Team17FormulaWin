SELECT
t."X"
, t."Y"
, t."RPM"
, t."Speed"
, t."nGear"
, t."Throttle"
, t."Brake"
, t."Sector"
, t."Event"
, t."DriverNumber"
, d."FullName" AS "Driver"
FROM "Telemetry" t
JOIN "Driver_Info" d
ON t."DriverNumber" = d."DriverNumber"
WHERE 
t."Event" = {EventNumber}
AND t."DriverNumber" IN {DriverNumbers}

