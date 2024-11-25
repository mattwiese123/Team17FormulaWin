select l."Event",
l."LapNumber",
l."Position",
r."FullName",
l."Compound",
l."TyreLife",
TO_CHAR(l."LapTime", 'HH24:MI:SS.') || LPAD(SPLIT_PART(TO_CHAR(l."LapTime", 'HH24:MI:SS.MS'), '.', 2), 3, '0') AS LapTime
from public."Race_Laps" l
join (select "Abbreviation", "FullName", count(*) from public."Race_Results" group by 1,2) r
on l."Driver" = r."Abbreviation"
where l."Event" = {RoundNumber}