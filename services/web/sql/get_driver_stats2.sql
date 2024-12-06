WITH victors AS(SELECT 
"FullName"
, Count(CASE WHEN "Position" = 1 THEN 1 ELSE null END) AS "Wins"
FROM
"Race_Results"
GROUP BY "FullName"
), joined AS(
SELECT
   v."FullName"
   , v."Wins" + c."Wins_2023" AS "Wins"
   , "Champ" AS "Championships"
FROM
victors v FULL OUTER JOIN "Champs" c
ON v."FullName" = c."FullName"
),
p AS (SELECT 
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
), joined2 AS (
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
, driver_pos AS
(SELECT 
CASE
	WHEN "Position" < 10 THEN '# ' || "Position"::varchar(4)
	ELSE '#' || "Position"::varchar(4)
END "Position"
, "Position" AS "Position_num"
, "FullName"
, "Points"
, "Photo"
, "Country"
, "Team"
FROM
joined2)

SELECT 
	j."FullName"
	, j."Wins"
	, j."Championships"
	, d."Position"
	, pl."Photo"
	, pl."Country"
	, pl."Team"
	, d."Points"
FROM
"Photo_Link" pl JOIN driver_pos d
ON pl."FullName" = d."FullName" 
JOIN joined j 
ON pl."FullName" = j."FullName"
ORDER BY "Position_num" ASC
