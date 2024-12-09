WITH p AS (SELECT 
	"TeamName"
	, SUM("Points") AS "Points"
FROM
	(SELECT
		"TeamName"
		, "Points" 
	FROM 
		"Race_Results"
  WHERE "Event" < 21
	UNION ALL 
	SELECT
		"TeamName"
		, "Points"
	FROM 
		"Sprint_Results"
  WHERE "Event" < 21)
GROUP BY "TeamName"
ORDER BY "Points" DESC
), joined AS (
SELECT 
    ROW_NUMBER() OVER (ORDER BY "Points" DESC) AS "Position"
	, p."TeamName"
	, p."Points"
	, l."Logo"
	, l."Country"
FROM 
p JOIN "Logo_Link" l
ON p."TeamName" = l."TeamName"
ORDER BY "Position")

SELECT 
CASE
WHEN "Position" < 10 THEN '<div style="font-size: 30px !important; font-weight: bold !important;"># ' || "Position"::varchar(4) || '</div>'
ELSE '<div style="font-size: 30px !important; font-weight: bold !important;">#' || "Position"::varchar(4) || '</div>'
END "Position"
, '<img src="' || "Logo" || '" style="height: 100px; width:175px;"/>' AS "Logo"
, "TeamName" AS "Team Name"
, "Points"
, "Country"
FROM
joined
