WITH p AS (SELECT 
	"TeamName"
	, SUM("Points") AS "Points"
FROM
	(SELECT
		"TeamName"
		, "Points" 
	FROM 
		"Race_Results"
	UNION ALL 
	SELECT
		"TeamName"
		, "Points"
	FROM 
		"Sprint_Results")
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
	WHEN "Position" < 10 THEN '# ' || "Position"::varchar(4)
	ELSE '#' || "Position"::varchar(4)
END "Position"
, '<img src="' || "Logo" || '" style="height: 100px; width:175px;"/>' AS "Logo"
, "TeamName" AS "Team Name"
, "Points"
, "Country"
FROM
joined
