WITH p AS (SELECT 
	"FullName"
	, SUM("Points") AS "Points"
FROM
	(SELECT
		"FullName"
		, "Points" 
	FROM 
		"Race_Results"
	UNION ALL 
	SELECT
		"FullName"
		, "Points"
	FROM 
		"Sprint_Results")
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
	WHEN "Position" < 10 THEN '# ' || "Position"::varchar(4)
	ELSE '#' || "Position"::varchar(4)
END "Position"
, "FullName"
, "Points"
, "Photo"
, "Country"
, "Team"
FROM
joined
