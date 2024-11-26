WITH table_1 AS (SELECT 
	ev."Year"
	, ev."Event"
	, ev."Location"
	, ev."EventName"
	, ev."EventDate"
	, rr."Abbreviation"
	, rr."FullName"
	, rr."Position"
	, rr."GridPosition"
	, rr."Status"
FROM
"Events" ev JOIN "Race_Results" rr
ON ev."Year" = rr."Year"
AND ev."Event" = rr."Event"),
df8 AS (
SELECT DISTINCT ON ("Year", "Event", "Driver")
	"Year"
	, "Event"
	, "Driver"
	, "Compound"
	, "TyreLife"
	, LPAD(FLOOR(EXTRACT(EPOCH FROM ("LapTime")) / 60)::TEXT, 2, '0') || ':' ||
    LPAD(FLOOR(EXTRACT(EPOCH FROM ("LapTime")) %% 60)::TEXT, 2, '0') || ':' ||
    LPAD(FLOOR(EXTRACT(MILLISECOND FROM "LapTime"))::TEXT, 3, '0') AS "LapTime"
FROM 
	"Race_Laps"
WHERE "LapTime_sec" IS NOT NULL
ORDER BY 
	"Year", "Event", "Driver", "LapTime" ASC
),
table_2 AS (
SELECT 
	table_1."Year"
	, table_1."Event"
	, table_1."Location"
	, table_1."EventName"
	, table_1."EventDate"
	, table_1."Abbreviation"
	, table_1."FullName"
	, table_1."Position"
	, table_1."GridPosition"
	, table_1."Status"
	--, df8."Driver" 
	, df8."Compound"
	, df8."TyreLife"
	, df8."LapTime"
FROM 
table_1 JOIN df8
ON table_1."Year" = df8."Year"
AND table_1."Event" = df8."Event"
AND table_1."Abbreviation" = df8."Driver"
),
table_3 AS (
SELECT 
	"Year"
	, "Event"
	, "Driver"
	, "LapTime"
	, "LapTime_sec"
	, "TrackStatus"
	, "PitOutTime_sec"
	, "PitInTime_sec"
FROM "Race_Laps"
WHERE 
	"TrackStatus" = 1
	AND "LapTime_sec" IS NOT NULL
	AND "PitOutTime_sec" IS NULL
	AND "PitInTime_sec" IS NULL
),
table_4 AS (
	SELECT 
		"Year"
		, "Event"
		, "Driver"
		, AVG("LapTime") "LapTime"
	FROM table_3
	GROUP BY "Year", "Event", "Driver"
),
table_5 AS (
	SELECT 
	"Year"
	, "Event"
	, "Driver"
	, LPAD(FLOOR(EXTRACT(EPOCH FROM ("LapTime")) / 60)::TEXT, 2, '0') || ':' ||
    LPAD(FLOOR(EXTRACT(EPOCH FROM ("LapTime")) %% 60)::TEXT, 2, '0') || ':' ||
    LPAD(FLOOR(EXTRACT(MILLISECOND FROM "LapTime"))::TEXT, 3, '0') AS "LapTime"
FROM table_4 
),
table_6 AS (
	SELECT 
		table_2."Location"
		, table_2."EventName"
		, table_2."EventDate"::DATE as "Date"
		, table_2."FullName"
		, table_2."Position"
		, table_2."GridPosition"
		, table_2."Status"
		, table_2."Compound"
		, table_2."TyreLife"
		, table_2."LapTime" AS "BestLapTime"
		, table_5."LapTime" AS "AvgLapTime"
	FROM 
	table_2 JOIN table_5
	ON table_2."Year" = table_5."Year"
	AND table_2."Event" = table_5."Event"
	AND table_2."Abbreviation" = table_5."Driver"
), 
table_graph_1 AS (
	SELECT 
		"Date"
		, COALESCE("Location", 'No data') AS "Location"
		, COALESCE("EventName", 'No data') AS "Event Name"
		, COALESCE("FullName", 'No data') AS "FullName"
		, "Position"::int8
		, "GridPosition"::int8 AS "Grid Position"
		, COALESCE("Status", 'No data') AS "Status"
		, COALESCE("BestLapTime", 'No data') AS "Best Lap Time"
		, COALESCE("Compound", 'No data') AS "Compound"
		, COALESCE("TyreLife"::VARCHAR(50), 'No data') AS "TyreLife"
		, COALESCE("AvgLapTime", 'No data') AS "Avg Lap Time"
	FROM table_6
	WHERE "FullName" IS NOT NULL
)

SELECT * FROM table_graph_1;
