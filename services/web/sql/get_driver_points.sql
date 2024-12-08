WITH p AS (SELECT 
	"FullName"
	, SUM("Points") AS "Points"
FROM
	(SELECT
		"FullName"
		, "Points" 
	FROM 
		"Race_Results"
  WHERE "Event" < 21
	UNION ALL 
	SELECT
		"FullName"
		, "Points"
	FROM 
		"Sprint_Results"
  WHERE "Event" < 21
  )
GROUP BY "FullName"
ORDER BY "Points" DESC
), joined AS (
SELECT 
    ROW_NUMBER() OVER (ORDER BY "Points" DESC) AS "Position"
	, p."FullName"
	, p."Points"
	, l."Photo"
	, l."Country"
	, l."Team"
FROM 
p JOIN "Photo_Link" l
ON p."FullName" = l."FullName"
ORDER BY "Position")

SELECT 
CASE
WHEN "Position" < 10 THEN '<div style="font-size: 30px !important; font-weight: bold !important;"># ' || "Position"::varchar(4) || '</div>'
ELSE '<div style="font-size: 30px !important; font-weight: bold !important;">#' || "Position"::varchar(4) || '</div>'
END "Position"
, '<img src="' || "Photo" || '" style="height: 100px; width:100px;"/>' AS "Photo"
, "FullName" AS "Full Name"
, "Points"
, "Country"
, "Team"
FROM
joined
