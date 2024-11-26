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
)
SELECT 
* 
FROM 
joined
