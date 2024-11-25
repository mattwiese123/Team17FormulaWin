SELECT e."EventName",
e."Location",
e."EventDate",
avg(w."AirTemp") as airtemp,
avg(w."Humidity") as humidity,
avg(w."Pressure") as pressure,
max(w."Rainfall") as rainfall,
avg(w."TrackTemp") as tracktemp,
avg(w."WindSpeed") as windspeed
FROM public."Events" e
join public."Race_Weather" w
on e."RoundNumber" = w."Event"
where e."RoundNumber" = {RoundNumber}
group by 1,2,3