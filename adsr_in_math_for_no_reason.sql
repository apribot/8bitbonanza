--ADSR envelope

select 
	repeat(' ',(((0.5 * ((0.5 * ( t^1.5 + 40 - abs(t^1.5 - 40))) + (100-t) - abs((0.5 * ( t^1.5 + 40 - abs(t^1.5 - 40))) - (100-t))   )) + abs(0.5 * ((0.5 * ( t^1.5 + 40 - abs(t^1.5 - 40))) + (100-t) - abs((0.5 * ( t^1.5 + 40 - abs(t^1.5 - 40))) - (100-t))   )))/2)::int)
	||'|'  
from generate_series(0.0, 200, 1) q(t); 



-- 808 bass
with wav as (
	select (((((((sin((t/10.0) * (pi() * 2)))) * (1.0/((t*.05) +1)) )) + 1.0 ) /2.0) * 50.0)::int as pt   
	from generate_series(0, 1000) q(t) 
), hax as (
	select 
		pt, 
		lag(pt,1) over () as last 
	from wav
) 
select 
	repeat(' ', pt) 
	|| case when pt < last then '/' when pt = last then '|' else '\' end 
from hax;

